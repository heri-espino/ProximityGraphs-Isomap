"""EXP-013: two 3x3 dashboards per classical manifold, far and near.
Runs locally; science notes are written by the assistant after user-pushed evidence.
Use --quick to smoke test; --require-umap to require a real UMAP implementation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull, QhullError
from scipy.spatial.distance import cdist, pdist, squareform
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, minimum_spanning_tree, shortest_path
from sklearn.decomposition import PCA
from sklearn.manifold import Isomap, LocallyLinearEmbedding, SpectralEmbedding, TSNE, trustworthiness
from sklearn.metrics import adjusted_rand_score
from sklearn.neighbors import NearestNeighbors, kneighbors_graph

ROOT = Path(__file__).resolve().parents[3]
SLUG = "013-classical_multicomponent_dashboards"
RUN_PATH = "proximity_isomap"
COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]
FAMILIES = ("rings", "springs", "swiss_rolls", "s_curves", "planes", "tori", "cylinder_and_ring")
ISOMAP = (
    "PCA", "Classical MDS", "Global kNN Isomap",
    "Global radius Isomap", "Componentwise kNN Isomap", "Componentwise radius Isomap",
    "MST cut + kNN Isomap (oracle K)", "t-SNE", "UMAP",
)
GENERAL = (
    "PCA", "Classical MDS", "Spectral embedding",
    "LLE", "Componentwise kNN Isomap", "LTSA",
    "t-SNE", "UMAP", "Global kNN Isomap",
)
METHODS = tuple(dict.fromkeys(ISOMAP + GENERAL))


def base_cloud(family, n, rng, index):
    """An individual intrinsic support, parameterized for synthetic evaluation."""
    if family == "rings":
        t = np.arange(n) * (2 * np.pi / n) + (index % 2) * .05
        x = np.column_stack((2.2 * np.cos(t), 2.2 * np.sin(t), np.zeros(n)))
        return x, t[:, None], "circle"
    if family == "springs":
        t = np.linspace(0, 4*np.pi, n)
        x = np.column_stack((1.2*np.cos(t), 1.2*np.sin(t), .30*t))
        return x, t[:, None], "helix"
    if family == "swiss_rolls":
        t = 1.5*np.pi + rng.random(n)*3*np.pi
        h = rng.uniform(-3.5, 3.5, n)
        x = np.column_stack((.34*t*np.cos(t), .34*t*np.sin(t), .55*h))
        s = .17*(t*np.sqrt(1+t*t) + np.arcsinh(t))
        return x, np.column_stack((s, .55*h)), "flat"
    if family == "s_curves":
        t = rng.uniform(-1.5*np.pi, 1.5*np.pi, n)
        h = rng.uniform(-3, 3, n)
        x = np.column_stack((np.sin(t), np.sign(t)*(np.cos(t)-1), .55*h))
        return x, np.column_stack((t, .55*h)), "flat"
    if family == "planes":
        side = int(np.ceil(np.sqrt(n)))
        a,b = np.meshgrid(np.linspace(-2.5, 2.5, side), np.linspace(-2.5, 2.5, side))
        uv = np.column_stack((a.ravel()[:n], b.ravel()[:n]))
        x = np.column_stack((uv, np.zeros(len(uv))))
        return x, uv, "flat"
    if family == "tori":
        side = int(np.ceil(np.sqrt(n)))
        a,b = np.meshgrid(np.arange(side)*2*np.pi/side,np.arange(side)*2*np.pi/side)
        t = a.ravel()[:n];u = b.ravel()[:n]
        x = np.column_stack(((3 + 1.0*np.cos(u))*np.cos(t),
                             (3 + 1.0*np.cos(u))*np.sin(t), np.sin(u)))
        return x, np.column_stack((t,u)), "torus"
    if family == "cylinder_and_ring":
        if index == 0:
            a = max(8, int(np.sqrt(n)*1.35))
            b = int(np.ceil(n/a))
            t,z = np.meshgrid(np.arange(a)*2*np.pi/a, np.linspace(-2.6,2.6,b),indexing="ij")
            t=t.ravel()[:n];z=z.ravel()[:n]
            x = np.column_stack((2.2*np.cos(t),2.2*np.sin(t),z))
            return x, np.column_stack((t,z)), "cylinder"
        t = np.arange(n)*2*np.pi/n
        x = np.column_stack((2.2*np.cos(t),2.2*np.sin(t),np.zeros(n)))
        return x, t[:,None], "circle"
    raise ValueError(family)


def place_clouds(family, regime, n, seed):
    """Separate sampled supports with a rigorously positive measured nearest gap.

    All component x-coordinate bounding intervals are disjoint. The extremal
    points' y/z coordinates are matched, so the minimum intercomponent
    point-to-point distance is exactly the requested gap.
    """
    rng=np.random.default_rng(seed)
    k = 3 if family == "rings" else 2
    clouds=[];params=[];kinds=[]
    for i in range(k):
        x,u,kind=base_cloud(family,n,rng,i)
        x=x.copy()
        x-=x.mean(0)
        if i%2:
            a=.58 if family != "planes" else .33
            rotate=np.array([[np.cos(a),-np.sin(a),0],
                             [np.sin(a),np.cos(a),0],[0,0,1]])
            x=x@rotate.T
        clouds.append(x);params.append(u);kinds.append(kind)
    within=[]
    for x in clouds:
        d=NearestNeighbors(n_neighbors=min(9,len(x))).fit(x).kneighbors(x)[0]
        within.append(np.median(d[:,-1]))
    scale=float(np.median(within))
    gap=scale*(.48 if regime=="near" else 7.0)
    placed=[clouds[0]]
    for x in clouds[1:]:
        previous=placed[-1]
        i=np.argmax(previous[:,0]);j=np.argmin(x[:,0])
        x=x.copy()
        delta=np.array((previous[i,0] + gap - x[j,0],
                        previous[i,1]-x[j,1],previous[i,2]-x[j,2]))
        x+=delta
        placed.append(x)
    data=np.vstack(placed)
    truth=np.concatenate([np.full(len(z),i,dtype=int) for i,z in enumerate(placed)])
    observed=min(float(cdist(placed[i],placed[j]).min())
                 for i in range(len(placed)) for j in range(i+1,len(placed)))
    if observed < gap-1e-7:
        raise AssertionError("Support construction accidentally overlaps")
    return data,truth,params,kinds,dict(target_gap=gap,observed_gap=observed,
                                        intrinsic_knn_scale=scale,components=k)


def sym_knn(x,k):
    k=min(max(1,int(k)),len(x)-1)
    graph=kneighbors_graph(x,n_neighbors=k,mode="distance",include_self=False)
    return graph.maximum(graph.T).tocsr()


def radius_graph(x,r):
    d=squareform(pdist(x))
    return csr_matrix(np.where((d>0)&(d<=r+1e-12),d,0))


def partition_from_graph(g):
    return connected_components(g,directed=False,return_labels=True)[1]


def mst_cut(x,k):
    """Oracle *count* K only; no generating group labels used in the cut."""
    d=squareform(pdist(x))
    t=minimum_spanning_tree(d).tocoo()
    order=np.argsort(t.data,kind="stable")[:len(x)-k]
    rows=np.r_[t.row[order],t.col[order]]
    cols=np.r_[t.col[order],t.row[order]]
    weights=np.r_[t.data[order],t.data[order]]
    g=csr_matrix((weights,(rows,cols)),shape=(len(x),len(x)))
    return partition_from_graph(g)


def classical_mds(d):
    n=len(d)
    squared=d*d
    gram=-.5*(squared-squared.mean(axis=0)[None,:]
              -squared.mean(axis=1)[:,None]+squared.mean())
    values,vectors=np.linalg.eigh(gram)
    order=np.argsort(values)[::-1][:2]
    coords=vectors[:,order]*np.sqrt(np.maximum(values[order],0))[None,:]
    return coords


def piecewise(x,labels,mode,k,radius):
    """Recompute within-component edges; do NOT use true labels here."""
    out=np.zeros((len(x),2))
    right=None
    ordering=sorted(np.unique(labels),key=lambda c:float(x[labels==c,0].mean()))
    for c in ordering:
        ids=np.flatnonzero(labels==c)
        if len(ids)==1:
            coords=np.zeros((1,2))
        else:
            graph=sym_knn(x[ids],k) if mode=="knn" else radius_graph(x[ids],radius)
            groups,_=connected_components(graph,directed=False)
            if groups!=1:
                raise ValueError(f"Internal graph disconnected: group={c}, pieces={groups}")
            d=shortest_path(graph,directed=False,unweighted=False)
            if not np.isfinite(d).all():
                raise ValueError("Nonfinite graph shortest path")
            coords=classical_mds(d)
        coords=coords-coords.mean(axis=0)
        if right is not None:
            coords[:,0]+=right+0.45-coords[:,0].min()
        right=float(coords[:,0].max())
        out[ids]=coords
    return out


def fit_method(name,x,detected,rlabels,radius,k_embed,seed):
    n=len(x)
    if name=="PCA":
        return PCA(n_components=2).fit_transform(x)
    if name=="Classical MDS":
        return classical_mds(squareform(pdist(x)))
    if name=="Global kNN Isomap":
        return Isomap(n_neighbors=min(k_embed,n-1),n_components=2).fit_transform(x)
    if name=="Global radius Isomap":
        g=radius_graph(x,radius)
        number,_=connected_components(g,directed=False)
        if number!=1:
            raise ValueError(f"Global radius graph has {number} components")
        return classical_mds(shortest_path(g,directed=False))
    if name=="Componentwise kNN Isomap":
        return piecewise(x,detected,"knn",k_embed,radius)
    if name=="Componentwise radius Isomap":
        graph=radius_graph(x,radius)
        labels=partition_from_graph(graph)
        return piecewise(x,labels,"radius",k_embed,radius)
    if name=="MST cut + kNN Isomap (oracle K)":
        oracle=mst_cut(x,len(np.unique(rlabels)))
        return piecewise(x,oracle,"knn",k_embed,radius)
    if name=="Spectral embedding":
        return SpectralEmbedding(n_components=2,n_neighbors=min(k_embed,n-1),
                                 affinity="nearest_neighbors",random_state=seed).fit_transform(x)
    if name in ("LLE","LTSA"):
        return LocallyLinearEmbedding(n_components=2,n_neighbors=min(max(8,k_embed),n-1),
                                     method="standard" if name=="LLE" else "ltsa",
                                     eigen_solver="arpack").fit_transform(x)
    if name=="t-SNE":
        return TSNE(n_components=2,perplexity=min(30,max(5,n//5)),
                    learning_rate="auto",init="pca",random_state=seed).fit_transform(x)
    if name=="UMAP":
        import umap
        return umap.UMAP(n_components=2,n_neighbors=min(k_embed,n-1),
                         random_state=seed,n_jobs=1).fit_transform(x)
    raise ValueError(name)


def true_geodesics(x,truth,params,kinds):
    """Return masks and analytic intra-support geodesics where available."""
    g=np.full((len(x),len(x)),np.nan,dtype=float)
    offset=0
    for i,(u,kind) in enumerate(zip(params,kinds)):
        n=len(u)
        if kind=="circle":
            delta=np.abs(u[:,0,None]-u[:,0][None,:])
            delta=np.minimum(delta,2*np.pi-delta)
            d=2.2*delta
        elif kind=="helix":
            d=np.sqrt(1.2**2+.3**2)*np.abs(u[:,0,None]-u[:,0][None,:])
        elif kind=="cylinder":
            theta=np.abs(u[:,0,None]-u[:,0][None,:])
            theta=np.minimum(theta,2*np.pi-theta)
            d=np.sqrt((2.2*theta)**2+
                      (u[:,1,None]-u[:,1][None,:])**2)
        elif kind=="flat":
            d=squareform(pdist(u))
        else:
            d=None  # torus: no invented analytic intrinsic geodesics
        if d is not None:
            g[offset:offset+n,offset:offset+n]=d
        offset+=n
    return g


def hull_polygon(z):
    if len(z)<3:
        return z
    try:
        return z[ConvexHull(z).vertices]
    except QhullError:
        return z


def poly_gap(a,b):
    """2D convex-hull clearance; coincident/intersecting convex polygons -> 0.

    Degenerate sets are measured by min sampled point distance and flagged
    separately in metadata; all intended inputs are nondegenerate in 2D.
    """
    a=hull_polygon(a);b=hull_polygon(b)
    if len(a)<3 or len(b)<3:
        return float(cdist(a,b).min()), False
    separated=False
    for z in (a,b):
        for edge in np.roll(z,-1,axis=0)-z:
            axis=np.array([-edge[1],edge[0]])
            p=a@axis;q=b@axis
            if p.max()<q.min()-1e-10 or q.max()<p.min()-1e-10:
                separated=True;break
        if separated:
            break
    if not separated:
        return 0.0, True
    distances=[]
    for p,q in ((a,b),(b,a)):
        for vertex in p:
            starts=q
            seg=np.roll(q,-1,axis=0)-q
            t=np.sum((vertex-starts)*seg,axis=1)/np.maximum(np.sum(seg*seg,axis=1),1e-12)
            t=np.clip(t,0,1)
            distances.append(float(np.linalg.norm(vertex-starts-t[:,None]*seg,axis=1).min()))
    return min(distances),False


def score(x,y,truth,geodesics):
    """Synthetic truth used ONLY for evaluation and plotting, never algorithm fit."""
    n=len(x);groups=np.unique(truth)
    amb=squareform(pdist(x));pr=squareform(pdist(y))
    within=(truth[:,None]==truth[None,:])&np.triu(np.ones((n,n),bool),1)
    scale=np.sqrt(np.sum(amb[within]**2)/max(np.sum(pr[within]**2),1e-12))
    scaled=y*scale;dr=pr*scale
    analytic=within&np.isfinite(geodesics)
    intrinsic=(float(np.sqrt(np.sum((dr[analytic]-geodesics[analytic])**2)/
                             np.sum(geodesics[analytic]**2))) if np.any(analytic) else None)
    between=(truth[:,None]!=truth[None,:])&np.triu(np.ones((n,n),bool),1)
    ambient_stress=(float(np.linalg.norm(dr[between]-amb[between])/
                          np.linalg.norm(amb[between])) if np.any(between) else None)
    cx=np.stack([x[truth==c].mean(axis=0) for c in groups])
    cy=np.stack([scaled[truth==c].mean(axis=0) for c in groups])
    xx=pdist(cx);yy=pdist(cy)
    centroid=float(np.linalg.norm(xx-yy)/max(np.linalg.norm(xx),1e-12)) if len(xx) else None
    overlaps=0;gaps=[];degenerate=False
    for i,a in enumerate(groups):
        for b in groups[i+1:]:
            aa=scaled[truth==a];bb=scaled[truth==b]
            gap,hit=poly_gap(aa,bb)
            gaps.append(gap);overlaps+=int(hit)
            if len(hull_polygon(aa))<3 or len(hull_polygon(bb))<3:
                degenerate=True
    local_k=min(8,(n-2)//2)
    trust=float(trustworthiness(x,y,n_neighbors=local_k))
    return dict(intrinsic_stress=intrinsic,ambient_cross_stress=ambient_stress,
                centroid_stress=centroid,trustworthiness=trust,
                hull_overlaps=int(overlaps),min_hull_gap=float(min(gaps)),
                degenerate_hull=bool(degenerate),scale_factor=float(scale))


def csv_write(path,rows):
    if not rows:
        raise ValueError("No data to save in "+str(path))
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)


def fig_save(fig,path):
    for extension in ("png","svg"):
        fig.savefig(path.with_suffix("."+extension),dpi=160,bbox_inches="tight")
    plt.close(fig)


def dashboard(x,truth,embeddings,status,title,methods,path):
    fig,axes=plt.subplots(3,3,figsize=(15,14),layout="constrained")
    fig.suptitle(title,fontsize=17,fontweight="bold")
    for ax,method in zip(axes.ravel(),methods):
        y=embeddings.get(method)
        if y is None:
            ax.text(.5,.5,"NOT AVAILABLE\n"+status.get(method,""),
                    transform=ax.transAxes,ha="center",va="center",fontsize=9,wrap=True)
        else:
            for c in np.unique(truth):
                z=y[truth==c]
                ax.scatter(z[:,0],z[:,1],s=8,alpha=.83,color=COLORS[c%len(COLORS)],
                           rasterized=True)
            ax.set_aspect("equal",adjustable="datalim")
        ax.set_title(method,fontsize=11,fontweight="bold")
        ax.set_xticks([]);ax.set_yticks([])
        ax.grid(False)
    fig.text(.5,.012,"Colors are generating labels for illustration/evaluation only; no labels train the unsupervised methods (except oracle K count).",
             ha="center",fontsize=10)
    fig_save(fig,path)


def source_plot(x,truth,title,path):
    fig=plt.figure(figsize=(9,7),layout="constrained")
    ax=fig.add_subplot(111,projection="3d")
    for c in np.unique(truth):
        z=x[truth==c]
        ax.scatter(*z.T,s=14,color=COLORS[c%len(COLORS)],alpha=.85,label=f"True support {c+1}")
    ax.view_init(elev=22,azim=-55);ax.set_title(title,fontsize=14)
    ax.legend(loc="upper left");fig_save(fig,path)


def curve_plot(curve,grid,title,path):
    fig,axes=plt.subplots(1,2,figsize=(12,4.2),layout="constrained")
    xs=[v["k_detect"] for v in curve]
    axes[0].plot(xs,[v["detected_K"] for v in curve],"-o",label="Detected components")
    axes[0].axhline(curve[0]["true_K"],ls="--",color="gray",label="True components (evaluation)")
    axes[0].plot(xs,[v["within_fragments"] for v in curve],":s",label="Extra within-support fragments")
    axes[0].set(xlabel="k for detection",ylabel="Count",title="Connectivity and fragmentation")
    axes[0].legend(fontsize=8)
    rows=sorted(set(int(v["k_detect"]) for v in grid))
    cols=sorted(set(int(v["k_embed"]) for v in grid))
    lookup={(int(v["k_detect"]),int(v["k_embed"])):v for v in grid}
    mat=np.full((len(rows),len(cols)),np.nan)
    for i,kd in enumerate(rows):
        for j,ke in enumerate(cols):
            r=lookup.get((kd,ke))
            if r and r.get("status")=="ok" and r.get("intrinsic_stress") is not None:
                mat[i,j]=float(r["intrinsic_stress"])
    if np.isfinite(mat).any():
        im=axes[1].imshow(mat,aspect="auto",interpolation="nearest")
        fig.colorbar(im,ax=axes[1],label="Within intrinsic stress")
    else:
        axes[1].text(.5,.5,"No analytic within-stress values",ha="center",va="center",transform=axes[1].transAxes)
    axes[1].set_xticks(range(len(cols)),cols)
    axes[1].set_yticks(range(len(rows)),rows)
    axes[1].set(xlabel="k for unfolding",ylabel="k for detection",
                title="k-detection x k-unfolding diagnostic")
    fig.suptitle(title);fig_save(fig,path)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--quick",action="store_true",help="Two families, both regimes, small n and smaller k sweep")
    p.add_argument("--label",default=None,help="Unique immutable run identifier")
    p.add_argument("--seed",type=int,default=20261019)
    p.add_argument("--k-detect",type=int,default=8)
    p.add_argument("--k-embed",type=int,default=10)
    p.add_argument("--require-umap",action="store_true")
    p.add_argument("--families",default=None,help="Comma-separated subset of 7 available family names")
    args=p.parse_args()
    if args.require_umap:
        import importlib.util
        if importlib.util.find_spec("umap") is None:
            p.error("--require-umap requested, but umap-learn is not installed")
    if args.families:
        chosen=tuple(s.strip() for s in args.families.split(",") if s.strip())
        invalid=set(chosen)-set(FAMILIES)
        if invalid:p.error("Unknown family names: "+", ".join(sorted(invalid)))
    else:
        chosen=("rings","springs") if args.quick else FAMILIES
    if args.k_detect<2 or args.k_embed<2:
        p.error("k values must be >=2")
    label=args.label or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+("-smoke" if args.quick else "-full")
    out=ROOT/"proximity_isomap"/"results"/SLUG/"runs"/label
    figs=ROOT/"proximity_isomap"/"figures"/SLUG/"runs"/label
    if out.exists() or figs.exists():raise FileExistsError("Run ID already exists: "+label)
    out.mkdir(parents=True);figs.mkdir(parents=True)
    try:
        import contrastcolors as cc
        cc.set_style("heri",palette="okabe-ito",font="DejaVu Sans",use_tex=False)
    except (ImportError,AttributeError,TypeError):
        pass
    method_rows=[];detect_rows=[];grid_rows=[];scenarios=[]
    kdet=(3,5,8) if args.quick else (3,5,8,12,18,26)
    kemb=(6,10) if args.quick else (6,10,16)
    n=30 if args.quick else 100
    for family in chosen:
        for regime in ("far","near"):
            key=f"{family}__{regime}"
            case_figs=figs/key;case_figs.mkdir()
            x,truth,params,kinds,info=place_clouds(family,regime,n,args.seed)
            geodesics=true_geodesics(x,truth,params,kinds)
            radius=float(np.median(NearestNeighbors(n_neighbors=min(args.k_embed+1,len(x)))
                                  .fit(x).kneighbors(x)[0][:,-1])*1.35)
            detected=partition_from_graph(sym_knn(x,args.k_detect))
            np.savez_compressed(out/(key+"_inputs.npz"),x=x,truth=truth,detected=detected)
            observed=dict(scenario=key,family=family,regime=regime,n=len(x),
                          true_K=int(len(np.unique(truth))),detected_K=int(len(np.unique(detected))),
                          adjusted_rand=float(adjusted_rand_score(truth,detected)),
                          source_gap=info["observed_gap"],gap_target=info["target_gap"],
                          gap_knn_ratio=info["observed_gap"]/info["intrinsic_knn_scale"],
                          radius=radius)
            scenarios.append(observed)
            embeddings={};status={}
            for method in METHODS:
                begin=time.perf_counter()
                row=dict(**observed,method=method,k_detect=args.k_detect,k_embed=args.k_embed)
                try:
                    with warnings.catch_warnings(record=True) as ww:
                        warnings.simplefilter("always")
                        y=fit_method(method,x,detected,truth,radius,args.k_embed,args.seed)
                    y=np.asarray(y,dtype=float)
                    if y.shape!=(len(x),2) or not np.isfinite(y).all():
                        raise ValueError("Invalid embedding coordinates")
                    row.update(score(x,y,truth,geodesics))
                    row["status"]="ok"
                    row["warning_text"]=" | ".join(str(w.message)[:140] for w in ww[:3])
                    embeddings[method]=y
                    np.savez_compressed(out/(key+"__"+method.lower().replace(" ","_").replace("+","plus").replace("(","").replace(")","")+".npz"),y=y)
                    if method=="Global kNN Isomap":
                        raw=sym_knn(x,args.k_embed)
                        row["global_knn_was_disconnected"]=bool(
                            connected_components(raw,directed=False)[0]>1)
                except Exception as exc:
                    row["status"]="failed_or_skipped";row["error"]=type(exc).__name__+": "+str(exc)[:220]
                    status[method]=row["error"]
                row["seconds"]=round(time.perf_counter()-begin,5)
                method_rows.append(row)
                print("[EXP-013]",key,method,row["status"],flush=True)
            source_plot(x,truth,key+" : original 3D",case_figs/"source_3d")
            dashboard(x,truth,embeddings,status,key+" : Isomap-centered 3x3",
                      ISOMAP,case_figs/"dashboard_isomap_centered")
            dashboard(x,truth,embeddings,status,key+" : general dimensionality reduction 3x3",
                      GENERAL,case_figs/"dashboard_general_dimred")
            curve=[];grid=[]
            for kd in kdet:
                g=sym_knn(x,kd)
                labels=partition_from_graph(g)
                cross=int(sum(truth[i]!=truth[j] for i,j in zip(*g.nonzero()) if i<j))
                fragments=sum(connected_components(g[np.ix_(np.flatnonzero(truth==c),
                    np.flatnonzero(truth==c))],directed=False)[0]-1 for c in np.unique(truth))
                crow=dict(observed, k_detect=kd,detected_K=len(np.unique(labels)),
                          partition_ARI=float(adjusted_rand_score(truth,labels)),
                          cross_support_edges=cross,within_fragments=fragments)
                curve.append(crow);detect_rows.append(crow)
                for ke in kemb:
                    row=dict(**crow,k_embed=ke,method="Componentwise kNN Isomap")
                    t=time.perf_counter()
                    try:
                        yy=piecewise(x,labels,"knn",ke,radius)
                        row.update(score(x,yy,truth,geodesics))
                        row["status"]="ok"
                    except Exception as exc:
                        row["status"]="failed_or_skipped";row["error"]=type(exc).__name__+": "+str(exc)[:220]
                    row["seconds"]=round(time.perf_counter()-t,5)
                    grid.append(row);grid_rows.append(row)
            curve_plot(curve,grid,key,case_figs/"k_detection_and_embedding")
            print("[SAVED SCENARIO]",key,observed,flush=True)
    csv_write(out/"method_metrics.csv",method_rows)
    csv_write(out/"detected_components_vs_k.csv",detect_rows)
    csv_write(out/"knn_detection_embedding_grid.csv",grid_rows)
    csv_write(out/"scenario_metadata.csv",scenarios)
    meta=dict(experiment="EXP-013",run_id=label,seed=args.seed,quick=args.quick,
              generated_utc=datetime.now(timezone.utc).isoformat(),
              families=list(chosen),regimes=["far","near"],n_per_component=n,
              dashboard_isomap=list(ISOMAP),dashboard_general=list(GENERAL),
              executed_methods=list(METHODS),k_detect=args.k_detect,k_embed=args.k_embed,
              sweep_k_detect=list(kdet),sweep_k_embed=list(kemb),
              source_gap_definition="axis-aligned disjoint x-intervals and matched extremal y/z; closest sampled pairs equal declared gap",
              key_caveats=["synthetic ground-truth labels used for plotting, evaluation and explicitly oracle-K comparator",
                           "single sampling seed unless rerun with new seed",
                           "global Isomap may reconnect disconnected neighbor graphs",
                           "torus analytic intrinsic distances unavailable",
                           "LLE/LTSA or radius Isomap can legitimately fail; failures remain in metrics",
                           "componentwise strips are feasible layout heuristics, NOT the globally optimal constrained placement",
                           "near/far defined by sampled gap relative to median within-support 8-NN distance"])
    (out/"metadata.json").write_text(json.dumps(meta,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    hashes={}
    for folder in (out,figs):
        for f in sorted(folder.rglob("*")):
            if f.is_file() and f.name!="sha256.json":
                hashes[str(f.relative_to(ROOT)).replace("\\","/")]=hashlib.sha256(f.read_bytes()).hexdigest()
    (out/"sha256.json").write_text(json.dumps(hashes,indent=2)+"\n",encoding="utf-8")
    print("[FINISHED EXP-013] results:",out,flush=True)
    print("[FINISHED EXP-013] figures:",figs,flush=True)


if __name__=="__main__":
    main()

"""EXP-011: PCA, standard Isomap, componentwise Isomap, t-SNE and optional UMAP.
Generate actual data, metrics, PNG/SVG and embedding arrays. Do not synthesize notes.
"""
from __future__ import annotations
import argparse,csv,hashlib,importlib.util,json,time,warnings
from datetime import datetime,timezone
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components,minimum_spanning_tree,shortest_path
from scipy.spatial.distance import pdist,squareform,cdist
from sklearn.decomposition import PCA
from sklearn.manifold import Isomap,TSNE,trustworthiness
from sklearn.neighbors import kneighbors_graph
from sklearn.metrics import adjusted_rand_score

ROOT=Path(__file__).resolve().parents[3]
SLUG="011-isomap_baselines"
METHODS=["PCA","Global Isomap k=8","Global Isomap k=24","Global radius Isomap",
         "Componentwise radius Isomap","Componentwise kNN Isomap","t-SNE","UMAP"]
COLORS=["#0072B2","#E69F00","#009E73","#D55E00","#CC79A7","#56B4E9"]

def sample(name,seed,quick):
    rng=np.random.default_rng(seed)
    if name=="rings":
        n=28 if quick else 90;t=np.arange(n)*2*np.pi/n
        x=np.vstack([np.column_stack((3.1*np.cos(t),3.1*np.sin(t),np.full(n,2*(i-2)))) for i in range(5)])
        return x,np.repeat(np.arange(5),n),np.tile(np.column_stack((t,np.zeros(n))),(5,1)),"circle"
    if name=="cylinder":
        nt,nz=(12,7) if quick else (24,15)
        t,z=np.meshgrid(np.arange(nt)*2*np.pi/nt,np.linspace(-4,4,nz),indexing="ij")
        x=np.column_stack((3.1*np.cos(t.ravel()),3.1*np.sin(t.ravel()),z.ravel()))
        return x,np.zeros(len(x),int),np.column_stack((t.ravel(),z.ravel())),"cylinder"
    if name=="torus":
        nt,ns=(9,7) if quick else (16,10)
        t,s=np.meshgrid(np.arange(nt)*2*np.pi/nt,np.arange(ns)*2*np.pi/ns,indexing="ij")
        x=np.column_stack(((5+1.85*np.cos(s.ravel()))*np.cos(t.ravel()),(5+1.85*np.cos(s.ravel()))*np.sin(t.ravel()),1.85*np.sin(s.ravel())))
        return x,np.zeros(len(x),int),None,"torus"
    if name in ("swiss_pair","s_curve_pair"):
        n=48 if quick else 120;xx=[];zz=[]
        for i in range(2):
            u=rng.uniform(size=n);h=rng.uniform(-4,4,size=n);t=(1.5+3*u)*np.pi if name=="swiss_pair" else (u-.5)*2.8*np.pi
            if name=="swiss_pair":
                x=np.column_stack((.35*t*np.cos(t),.55*h,.35*t*np.sin(t)))
                intr=np.column_stack((.175*(t*np.sqrt(1+t*t)+np.arcsinh(t)),.55*h))
            else:
                x=np.column_stack((np.sin(t),.55*h,np.sign(t)*(np.cos(t)-1)))
                intr=np.column_stack((t,.55*h))
            if i:
                a=np.deg2rad(80);b=np.deg2rad(65)
                rx=np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]])
                rz=np.array([[np.cos(b),-np.sin(b),0],[np.sin(b),np.cos(b),0],[0,0,1]])
                x=(x-x.mean(0))@(rz@rx).T
                x[:,0]+=xx[0][:,0].max()-x[:,0].min()+9
            xx.append(x);zz.append(intr)
        return np.vstack(xx),np.repeat(np.arange(2),n),np.vstack(zz),"flat"
    raise ValueError(name)

def components(x,name,true_k):
    d=squareform(pdist(x))
    if name in ("rings","cylinder","torus"):
        r=1.25 if name!="torus" else float(minimum_spanning_tree(d).data.max()*(1+1e-8))
        g=csr_matrix(np.where((d>0)&(d<=r),d,0))
        return connected_components(g,directed=False)[1],r,"fixed_radius" if name!="torus" else "global_mst_connectivity"
    tree=minimum_spanning_tree(d).tocoo()
    keep=np.argsort(tree.data)[:len(tree.data)-true_k+1]
    g=csr_matrix((np.r_[tree.data[keep],tree.data[keep]],(np.r_[tree.row[keep],tree.col[keep]],np.r_[tree.col[keep],tree.row[keep]])),shape=d.shape)
    return connected_components(g,directed=False)[1],float(tree.data[keep].max()*(1+1e-8)),"supplied_K_mst_cut"

def mds(d):
    a=d*d;b=-.5*(a-a.mean(0)[None,:]-a.mean(1)[:,None]+a.mean())
    v,q=np.linalg.eigh(b);return q[:,-2:]*np.sqrt(np.maximum(v[-2:],0))

def graph(x,mode,r):
    if mode=="radius":
        d=squareform(pdist(x))
        return csr_matrix(np.where((d>0)&(d<=r),d,0))
    g=kneighbors_graph(x,n_neighbors=min(10,len(x)-1),mode="distance")
    return g.maximum(g.T)

def piecewise(x,labels,mode,r):
    y=np.zeros((len(x),2));right=None
    for c in np.unique(labels):
        ids=np.flatnonzero(labels==c)
        if len(ids)==1:z=np.zeros((1,2))
        else:
            g=graph(x[ids],mode,r);parts,_=connected_components(g,directed=False)
            if parts!=1:raise ValueError(f"Component {c}: {parts} graph pieces")
            z=mds(shortest_path(g,directed=False))
        z-=z.mean(0)
        if np.ptp(z[:,0])>np.ptp(z[:,1]):z=z@np.array([[0,1],[-1,0]])
        if right is not None:z[:,0]+=right+.6-z[:,0].min()
        right=z[:,0].max();y[ids]=z
    return y

def fit(method,x,labels,r,seed):
    if method=="PCA":return PCA(n_components=2).fit_transform(x)
    if method.startswith("Global Isomap"):return Isomap(n_neighbors=int(method.split("=")[-1]),n_components=2).fit_transform(x)
    if method=="Global radius Isomap":
        g=graph(x,"radius",r);count,_=connected_components(g,directed=False)
        if count!=1:raise ValueError(f"Global radius graph disconnected: {count} parts")
        return mds(shortest_path(g,directed=False))
    if method=="Componentwise radius Isomap":return piecewise(x,labels,"radius",r)
    if method=="Componentwise kNN Isomap":return piecewise(x,labels,"knn",r)
    if method=="t-SNE":return TSNE(n_components=2,perplexity=min(30,len(x)//4),learning_rate="auto",init="pca",random_state=seed).fit_transform(x)
    if method=="UMAP":
        if importlib.util.find_spec("umap") is None:raise ModuleNotFoundError("Install umap-learn")
        import umap
        return umap.UMAP(n_components=2,n_neighbors=15,random_state=seed).fit_transform(x)
    raise ValueError(method)

def convex_overlap(y,a,b):
    """Test 2D convex hull intersection by the separating-axis theorem."""
    from scipy.spatial import ConvexHull
    p=y[a];q=y[b]
    if len(p)<3 or len(q)<3:return bool(cdist(p,q).min()<1e-9)
    try:p=p[ConvexHull(p).vertices];q=q[ConvexHull(q).vertices]
    except Exception:return bool(cdist(p,q).min()<1e-9)
    for poly in (p,q):
        for edge in np.roll(poly,-1,axis=0)-poly:
            axis=np.array([-edge[1],edge[0]])
            ap=p@axis;aq=q@axis
            if ap.max()<aq.min()-1e-9 or aq.max()<ap.min()-1e-9:return False
    return True

def metrics(x,y,labels,intrinsic,kind):
    """Score embeddings after common ambient-within scale calibration.

    The positive scale uses original ambient distances, never analytic
    geodesics. Generating labels are used for diagnostic evaluation only.
    """
    x=np.asarray(x,float);y=np.asarray(y,float);n=len(x)
    dx=squareform(pdist(x));dy=squareform(pdist(y))
    within=np.equal.outer(labels,labels)&~np.eye(n,dtype=bool)
    scale=float(np.sqrt(np.sum(dx[within]**2)/max(np.sum(dy[within]**2),1e-12)))
    y_scaled=y*scale;dy=dy*scale
    intrinsic_error=None
    if intrinsic is not None:
        target=np.zeros_like(dx)
        for c in np.unique(labels):
            idx=np.flatnonzero(labels==c);u=intrinsic[idx]
            if kind in ("circle","cylinder"):
                theta=np.abs(u[:,0,None]-u[:,0][None,:]);theta=np.minimum(theta,2*np.pi-theta)
                d=np.sqrt((3.1*theta)**2+(u[:,1,None]-u[:,1][None,:])**2)
            else:d=squareform(pdist(u))
            target[np.ix_(idx,idx)]=d
        intrinsic_error=float(np.sqrt(np.sum((dy[within]-target[within])**2)/np.sum(target[within]**2)))
    distinct=np.unique(labels);between=~np.equal.outer(labels,labels)
    result=dict(rescale_factor=scale,intrinsic_stress=intrinsic_error,
                trustworthiness_8=float(trustworthiness(x,y,n_neighbors=8)))
    if len(distinct)>1:
        cx=np.array([x[labels==c].mean(0) for c in distinct])
        cy=np.array([y_scaled[labels==c].mean(0) for c in distinct])
        mx=squareform(pdist(cx));my=squareform(pdist(cy))
        upper=np.triu_indices(len(cx),1)
        result["centroid_stress"]=float(np.linalg.norm(mx[upper]-my[upper])/np.linalg.norm(mx[upper]))
        result["cross_ambient_stress"]=float(np.linalg.norm(dx[between]-dy[between])/np.linalg.norm(dx[between]))
        result["overlapping_hull_pairs"]=int(sum(convex_overlap(y,labels==a,labels==b)
            for a in distinct for b in distinct if a<b))
    else:result.update(centroid_stress=None,cross_ambient_stress=None,overlapping_hull_pairs=0)
    return result

def save(fig,p):
    for ext in ("png","svg"):fig.savefig(p.with_suffix("."+ext),dpi=175,bbox_inches="tight")
    plt.close(fig)

def table(path,rows):
    cols=list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=cols);wr.writeheader();wr.writerows(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--label",default=None);p.add_argument("--seed",type=int,default=20261018)
    p.add_argument("--quick",action="store_true");p.add_argument("--require-umap",action="store_true")
    a=p.parse_args()
    if a.require_umap and importlib.util.find_spec("umap") is None:raise ModuleNotFoundError("Install umap-learn first")
    label=a.label or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+("-smoke" if a.quick else "-full")
    out=ROOT/"proximity_isomap"/"results"/SLUG/"runs"/label
    figs=ROOT/"proximity_isomap"/"figures"/SLUG/"runs"/label
    if out.exists() or figs.exists():raise FileExistsError("Run already exists: "+label)
    out.mkdir(parents=True);figs.mkdir(parents=True)
    try:
        import contrastcolors as cc
        cc.set_style("heri",palette="okabe-ito",font="DejaVu Sans",use_tex=False)
    except ImportError:pass
    rows=[];data={}
    for name in ("rings","cylinder","swiss_pair","s_curve_pair","torus"):
        x,truth,intrinsic,kind=sample(name,a.seed,a.quick);data[name]=x
        detected,r,selection=components(x,name,len(np.unique(truth)))
        np.savez_compressed(out/(name+"_inputs.npz"),x=x,truth=truth,detected=detected)
        fitted={}
        for method in METHODS:
            start=time.perf_counter()
            row=dict(scenario=name,method=method,seed=a.seed,n=len(x),selection=selection,radius=r,true_K=len(np.unique(truth)),detected_K=len(np.unique(detected)),adjusted_rand=float(adjusted_rand_score(truth,detected)))
            try:
                with warnings.catch_warnings(record=True) as ww:
                    warnings.simplefilter("always");y=fit(method,x,detected,r,a.seed)
                if not np.isfinite(y).all():raise ValueError("Nonfinite embedding")
                row.update(metrics(x,y,truth,intrinsic,kind));row.update(status="ok",warnings=" | ".join(str(w.message)[:100] for w in ww[:3]))
                if method.startswith("Global Isomap"):
                    g=kneighbors_graph(x,n_neighbors=int(method.split("=")[-1]),mode="distance");g=g.maximum(g.T)
                    row["auto_bridged"]=bool(connected_components(g,directed=False)[0]>1)
                fitted[method]=y
                np.savez_compressed(out/(name+"__"+method.lower().replace(" ","_").replace("=","_")+".npz"),embedding=y)
            except Exception as exc:
                row.update(status="missing_dependency" if isinstance(exc,ModuleNotFoundError) else "failed_or_skipped",error=str(exc))
            row["seconds"]=round(time.perf_counter()-start,3);rows.append(row)
            print("[EXP-011]",name,method,row["status"],row.get("intrinsic_stress"),flush=True)
        fig=plt.figure(figsize=(15,10),layout="constrained")
        for col,method in enumerate(["Original 3D"]+METHODS):
            ax=fig.add_subplot(3,3,col+1,projection="3d" if col==0 else None)
            z=x if col==0 else fitted.get(method)
            if z is None:ax.text(.5,.5,"Not available",ha="center",transform=ax.transAxes)
            else:
                for c in np.unique(truth):ax.scatter(*z[truth==c].T,s=5,color=COLORS[c%len(COLORS)])
            ax.set_title(method,fontsize=10)
            if col:ax.set_aspect("equal",adjustable="datalim")
        save(fig,figs/(name+"_embeddings"))
    table(out/"metrics.csv",rows)
    for metric in ("intrinsic_stress","trustworthiness_8","centroid_stress"):
        fig,ax=plt.subplots(figsize=(12,5),layout="constrained")
        for j,method in enumerate(METHODS):
            values=[next((row.get(metric) for row in rows if row["scenario"]==name and row["method"]==method and row["status"]=="ok"),None) for name in data]
            vals=np.array([np.nan if v is None else float(v) for v in values])
            if np.isfinite(vals).any():ax.plot(range(len(data)),vals,marker="o",label=method,color=COLORS[j%len(COLORS)])
        ax.set_xticks(range(len(data)),list(data));ax.set_ylabel(metric);ax.legend(fontsize=8,bbox_to_anchor=(1,1),loc="upper left")
        save(fig,figs/metric)
    meta=dict(experiment="EXP-011",seed=a.seed,label=label,quick=a.quick,generated_utc=datetime.now(timezone.utc).isoformat(),umap_available=importlib.util.find_spec("umap") is not None,methods=METHODS,caveats=["one seed","some supplied K","scikit Isomap may add artificial bridges","torus analytic geodesics not evaluated"])
    (out/"metadata.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [*out.iterdir(),*figs.iterdir()] if f.is_file()}
    (out/"sha256.json").write_text(json.dumps(hashes,indent=2)+"\n",encoding="utf-8")
    print("[SAVED EXP-011]",out,figs,flush=True)
if __name__=="__main__":main()

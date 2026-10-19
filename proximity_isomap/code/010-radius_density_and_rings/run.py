"""EXP-010: cylinder versus separate rings; generated results, not hand-entered numbers."""
from __future__ import annotations
import argparse, csv, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree, connected_components, shortest_path
from sklearn.decomposition import PCA

ROOT=Path(__file__).resolve().parents[3]
SLUG="010-radius_density_and_rings"
COLORS=["#0072B2","#E69F00","#009E73","#D55E00","#CC79A7","#56B4E9"]

def cylinder(na,nz):
    t,z=np.meshgrid(np.arange(na)*2*np.pi/na,np.linspace(-4,4,nz),indexing="ij")
    return np.column_stack((3.1*np.cos(t.ravel()),3.1*np.sin(t.ravel()),z.ravel())),np.zeros(na*nz,int)

def rings(n=90):
    t=np.arange(n)*2*np.pi/n
    return np.vstack([np.column_stack((3.1*np.cos(t),3.1*np.sin(t),np.full(n,2*(j-2)))) for j in range(5)]),np.repeat(np.arange(5),n)

def mst_deaths(x):
    return np.sort(minimum_spanning_tree(squareform(pdist(x))).data)

def fixed_h1(x,r):
    """VR H1 computed by GF(2) triangle-boundary rank, not persistence bars."""
    d=squareform(pdist(x));mask=(d>0)&(d<=r+1e-10)
    edges=list(zip(*np.where(np.triu(mask,1))))
    edge_id={pair:i for i,pair in enumerate(edges)}
    neighbors=[set(np.flatnonzero(row)) for row in mask]
    pivots={};triangles=0
    for i,j in edges:
        for k in neighbors[i]&neighbors[j]:
            if k<=j:continue
            triangles+=1
            v=(1<<edge_id[i,j])^(1<<edge_id[i,k])^(1<<edge_id[j,k])
            while v:
                p=v.bit_length()-1
                if p in pivots:v^=pivots[p]
                else:pivots[p]=v;break
    c=len(x)-np.searchsorted(mst_deaths(x),r,side="right")
    return dict(radius=r,beta0=int(c),beta1=int(len(edges)-len(x)+c-len(pivots)),edges=len(edges),triangles=triangles)

def mds(d):
    s=d*d;b=-.5*(s-s.mean(0)[None,:]-s.mean(1)[:,None]+s.mean())
    v,q=np.linalg.eigh(b);return q[:,-2:]*np.sqrt(np.maximum(v[-2:],0))

def embed(x,r=1.25):
    d=squareform(pdist(x));g=csr_matrix(np.where((d>0)&(d<=r),d,0))
    count,lab=connected_components(g,directed=False)
    y=np.zeros((len(x),2));right=None
    for c in sorted(np.unique(lab),key=lambda k:x[lab==k,2].mean()):
        ids=np.flatnonzero(lab==c);dist=shortest_path(g[ids][:,ids],directed=False)
        if not np.isfinite(dist).all():raise RuntimeError("Disconnected component")
        z=mds(dist);z-=z.mean(0)
        if right is not None:z[:,0]+=right+.6-z[:,0].min()
        right=z[:,0].max();y[ids]=z
    return y,count

def save(fig,p):
    for ext in ("png","svg"):fig.savefig(p.with_suffix("."+ext),dpi=175,bbox_inches="tight")
    plt.close(fig)

def table(path,rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--label",default=None);p.add_argument("--quick",action="store_true")
    a=p.parse_args();label=a.label or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+("-smoke" if a.quick else "-full")
    res=ROOT/"proximity_isomap"/"results"/SLUG/"runs"/label
    figdir=ROOT/"proximity_isomap"/"figures"/SLUG/"runs"/label
    if res.exists() or figdir.exists():raise FileExistsError("Run label exists: "+label)
    res.mkdir(parents=True);figdir.mkdir(parents=True)
    try:
        import contrastcolors as cc
        cc.set_style("heri",palette="okabe-ito",font="DejaVu Sans",use_tex=False)
    except ImportError:pass
    data={"cy54":cylinder(9,6),"cy144":cylinder(12,12),"cy360":cylinder(18,20),"cy720":cylinder(24,30),"rings":rings()}
    radii=np.unique(np.r_[np.linspace(.12,2.5,220),.25,.5,1.15,1.25,1.5,1.8,2.2])
    summary=[];curve=[];h1=[]
    for name,(x,truth) in data.items():
        deaths=mst_deaths(x)
        summary.append(dict(dataset=name,n=len(x),support_components=len(np.unique(truth)),connectivity_threshold=float(deaths[-1]),beta0_r_0_5=int(len(x)-np.searchsorted(deaths,.5,side="right")),beta0_r_1_25=int(len(x)-np.searchsorted(deaths,1.25,side="right"))))
        curve.extend(dict(dataset=name,radius=float(r),beta0=int(len(x)-np.searchsorted(deaths,r,side="right"))) for r in radii)
        if name in ("cy360","rings"):
            for r in ([1.25] if a.quick else ([.5,1.15,1.25,1.5] if name=="cy360" else [.25,.5,1.25,1.8])):
                h1.append(dict(dataset=name,**fixed_h1(x,r)));print("[H1]",name,r,flush=True)
    table(res/"summary.csv",summary);table(res/"beta0_curve.csv",curve);table(res/"fixed_scale_betti.csv",h1)
    np.savez_compressed(res/"observations.npz",**{k:x for k,(x,_) in data.items()})
    f=plt.figure(figsize=(12,4),layout="constrained")
    for j,name in enumerate(("cy54","cy360","rings")):
        x,t=data[name];ax=f.add_subplot(1,3,j+1,projection="3d")
        ax.scatter(*x.T,c=[COLORS[int(i)%len(COLORS)] for i in t],s=7);ax.set_title(name);ax.view_init(elev=22,azim=-55)
    save(f,figdir/"geometry")
    f,axes=plt.subplots(1,2,figsize=(12,4.5),layout="constrained")
    for name in data:
        z=[a for a in curve if a["dataset"]==name]
        axes[0].step([v["radius"] for v in z],[v["beta0"] for v in z],where="post",label=name)
    axes[0].set(xlabel="Radius",ylabel="Connected components (H0)");axes[0].set_yscale("symlog",linthresh=8);axes[0].legend(fontsize=8)
    for name in ("cy360","rings"):
        z=[a for a in h1 if a["dataset"]==name]
        axes[1].plot([v["radius"] for v in z],[v["beta1"] for v in z],"-o",label=name)
    axes[1].set(xlabel="Radius",ylabel="Fixed-scale VR H1");axes[1].set_yscale("symlog",linthresh=5);axes[1].legend()
    save(f,figdir/"radius_topology")
    f=plt.figure(figsize=(13,7),layout="constrained")
    for row,name in enumerate(("cy360","rings")):
        x,_=data[name];d=squareform(pdist(x))
        for col,r in enumerate((.25,.5,1.25,2.2)):
            n,lab=connected_components(csr_matrix((d>0)&(d<=r)),directed=False)
            ax=f.add_subplot(2,4,row*4+col+1,projection="3d")
            ax.scatter(*x.T,c=[COLORS[i%len(COLORS)] for i in lab],s=5);ax.set_title(f"{name}, r={r}, K={n}",fontsize=9);ax.set_axis_off()
    save(f,figdir/"radius_snapshots")
    f=plt.figure(figsize=(13,7),layout="constrained")
    for row,name in enumerate(("cy360","rings")):
        x,truth=data[name];projection,k=embed(x);pca=PCA(n_components=2).fit_transform(x)
        for col,z in enumerate((x,pca,projection)):
            ax=f.add_subplot(2,3,row*3+col+1,projection="3d" if col==0 else None)
            for c in np.unique(truth):ax.scatter(*z[truth==c].T,s=6,color=COLORS[c%len(COLORS)])
            ax.set_title(("Original","PCA","Component Isomap K="+str(k))[col])
            if col:ax.set_aspect("equal",adjustable="datalim")
    save(f,figdir/"projections")
    meta=dict(experiment="EXP-010",label=label,quick=a.quick,date_utc=datetime.now(timezone.utc).isoformat(),method="fixed H0/H1 of deterministic grids, 2D Isomap at r=1.25",caveat="H1 at selected radii is not a persistence barcode")
    (res/"metadata.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [*res.iterdir(),*figdir.iterdir()] if f.is_file()}
    (res/"sha256.json").write_text(json.dumps(hashes,indent=2)+"\n",encoding="utf-8")
    print("[SAVED EXP-010]",res,figdir,flush=True)
if __name__=="__main__":main()

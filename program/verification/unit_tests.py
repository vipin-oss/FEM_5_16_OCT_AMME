"""Unit-level checks of the BFS implementation. Exit status 1 on any failure."""
import numpy as np, tpfem as t, sys
ok=True
def chk(name,val,tol):
    global ok; p=abs(val)<tol; ok&=p; print(f"{'PASS' if p else 'FAIL'}  {name}: {val:.3e} (tol {tol:.0e})")
a,b=0.7e-6,0.2e-6
# element: exact linear-field recovery and partition of unity, using the element builder's kernels
Kuu,Kup,Kpp,Fb,Fbz,Fp,Fpz=t.bfs_element(a,b,t.MAT)
# nodal DOFs for u=1+2e5*x+3e5*z, w=-4e5*x+7e5*z (quadratic-free)  order: per corner [v,vx,vz,vxz]
cor=[(0,0),(a,0),(a,b),(0,b)]
def dofs(f,fx,fz): return np.array([x for (X,Z) in cor for x in (f(X,Z),fx,fz,0.0)])
qu=np.concatenate([dofs(lambda x,z:1+2e5*x+3e5*z,2e5,3e5),dofs(lambda x,z:-4e5*x+7e5*z,-4e5,7e5)])
# strain energy of the exact linear field = 0.5 eps^T C eps * area
C,e,k=t.blocks(t.MAT); eps=np.array([2e5,7e5,3e5-4e5]); E=0.5*eps@C@eps*a*b
chk("linear-field recovery (elastic energy rel. error)",(0.5*qu@Kuu@qu-E)/E,1e-12)
# unit load integral: int B^T beta dA applied to the linear field equals area*eps.beta
chk("partition of unity / load kernel (eps.beta*area)",(qu@(Fb@np.array([1,2,3.]))-area*(eps@np.array([1,2,3.])) if (area:=a*b) else 0)/(a*b*abs(eps@np.array([1,2,3.]))),1e-12)
# potential: Kpp on a linear potential
qp=np.array([0,a,a,0.])*1e5*0+np.array([2e5*X+5e5*Z for (X,Z) in cor]); Ep=np.array([2e5,5e5])
chk("linear potential energy",(0.5*qp@Kpp@qp-0.5*Ep@k@Ep*a*b)/(0.5*Ep@k@Ep*a*b),1e-12)
# symmetry/reciprocity: global reduced system symmetric
r=t.solve_bfs(16,8,clamp='classical'); import scipy.sparse as sp
chk("reduced-matrix symmetry",sp.linalg.norm(r['Kr']-r['Kr'].T)/sp.linalg.norm(r['Kr']),1e-12)
# nulls
V0=t.solve_bfs(16,8,clamp='classical',alpha_scale=0.0,pyro=False)['V']; chk("zero-alpha null, Case E (V)",V0,1e-12)
V0=t.solve_bfs(16,8,clamp='classical',pyro=False)['V']
mm=dict(t.MAT); mm['p3']=0.0
chk("zero-p: Case A == Case E",t.solve_bfs(16,8,mat=mm,clamp='classical')['V']-V0,1e-10)
# 1D exact pyroelectric
chk("Case D vs exact 1D (rel.)",(t.solve_bfs(16,8,clamp='classical',piezo=False)['V']+3.438647248138)/3.438647,1e-10)
# p3 linearity at fixed K
vs=[]
for s in (0,0.5,1,1.5,2):
    m2=dict(t.MAT); m2['p3']*=s; vs.append(t.solve_bfs(16,8,mat=m2,clamp='classical')['V'])
sc=np.array([0,.5,1,1.5,2]); chk("p3 linearity max residual (V)",np.max(np.abs(np.polyval(np.polyfit(sc,vs,1),sc)-vs)),1e-9)
print("slope per unit p3 scale:",np.polyfit(sc,vs,1)[0])
# Gauss: 4x4 vs 6x6 element matrices
import numpy.polynomial.legendre as L
Kb=t.bfs_element(a,b,t.MAT,ng=6)[0]; chk("4x4 vs 6x6 Gauss Kuu (rel.)",np.linalg.norm(Kb-Kuu)/np.linalg.norm(Kuu),1e-12)
sys.exit(0 if ok else 1)

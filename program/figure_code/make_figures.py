"""Regenerates revised Fig. 2 (convergence) and new Fig. 9 (root constraint, span, reduction) from verification/results.
Run from repo root: python3 figure_code/make_figures.py"""
import csv, re, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
plt.rcParams.update({'font.family':'serif','mathtext.fontset':'cm','font.size':9,'axes.linewidth':0.6,'lines.linewidth':1.1,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
OI={'blue':'#0072B2','orange':'#E69F00','verm':'#D55E00','green':'#009E73','grey':'#555555'}
rows=list(csv.DictReader(open('verification/results/voltages_all.csv')))
def ser(m,c): s=[r for r in rows if r['model']==m and r['case']==c]; return np.array([int(r['ndof']) for r in s]),np.array([float(r['V_volt']) for r in s])
M=[('BFS all-derivative root, full beta','BFS, all-derivative root','o',OI['grey'],'--'),
   ('BFS classical clamp, full beta','BFS, classical clamp','s',OI['blue'],'-'),
   ('Q9 classical clamp, full beta','Q9, classical clamp','^',OI['verm'],'-')]
# ---- Fig 2
fig,ax=plt.subplots(2,2,figsize=(6.6,4.6),constrained_layout=True)
for j,(c,lab) in enumerate((('A','Case A'),('E','Case E'))):
    for m,l,mk,col,ls in M:
        nd,v=ser(m,c); ax[0,j].plot(nd,v,mk+ls,color=col,ms=3.5,label=l)
        ch=np.abs(100*np.diff(v)/v[:-1]); ax[1,j].loglog(nd[1:],ch,mk+ls,color=col,ms=3.5)
    ax[0,j].set_xscale('log'); ax[0,j].set_ylabel(r'$V_{\mathrm{oc}}$ (V)'); ax[0,j].set_title(lab,fontsize=9,pad=8)
    ax[1,j].set_xlabel('degrees of freedom'); ax[1,j].set_ylabel('|change from previous mesh| (%)')
ax[0,0].legend(frameon=False,fontsize=7.5)
for a_,t_ in zip(ax.ravel(),'abcd'): a_.annotate(f'({t_})',(-0.02,1.03),xycoords='axes fraction',fontsize=9,fontweight='bold',ha='right')
for a_ in ax.ravel(): a_.xaxis.set_minor_formatter(NullFormatter())
fig.savefig('figures_new/Fig2_mesh_convergence.pdf')
# ---- Fig 9
log=open('verification/results/run_checks.log').read()
sp=re.findall(r'L=\s*(\d+) um nx=\d+: V_A=([-+\d.]+)\s+V_E=([-+\d.]+)',log); Ls=np.array([float(a) for a,_,_ in sp]); VE=np.array([float(c) for _,_,c in sp])
ana=float(re.search(r'analytic: V_A=[-+\d.]+\s+V_E=([-+\d.]+)',log).group(1))
fig,ax=plt.subplots(1,2,figsize=(6.6,2.7),constrained_layout=True)
ax[0].plot(Ls,VE,'s-',color=OI['blue'],ms=4,label='FE, classical clamp'); ax[0].axhline(ana,color=OI['verm'],ls='--',label='exact mid-span solution')
ax[0].set_xlabel(r'span $L$ ($\mu$m)'); ax[0].set_ylabel(r'Case E, $V_{\mathrm{oc}}$ (V)'); ax[0].legend(frameon=False,fontsize=7.5,loc='lower right')
v={}
for m,l,_,_,_ in M:
    for bm,tag in (('full beta','full'),):
        pass
simp={'BFS all-derivative root, simpl. beta':'BFS, all-deriv.','BFS classical clamp, simpl. beta':'BFS, classical','Q9 classical clamp, simpl. beta':'Q9, classical'}
full={'BFS all-derivative root, full beta':'BFS, all-deriv.','BFS classical clamp, full beta':'BFS, classical','Q9 classical clamp, full beta':'Q9, classical'}
x=np.arange(3); w=0.36
sv=[ser(k,'E')[1][-1] for k in simp]; fv=[ser(k,'E')[1][-1] for k in full]
ax[1].bar(x-w/2,sv,w,color=OI['orange'],label='simplified reduction'); ax[1].bar(x+w/2,fv,w,color=OI['blue'],label='full contraction')
ax[1].axhline(0,color='k',lw=0.6); ax[1].set_xticks(x); ax[1].set_xticklabels(list(full.values()),fontsize=7.5); ax[1].set_ylabel(r'Case E, $V_{\mathrm{oc}}$ (V)'); ax[1].set_ylim(-0.3,0.4); ax[1].legend(frameon=False,fontsize=7.5,loc='upper center',ncol=2)
for a_,t_ in zip(ax,'ab'): a_.annotate(f'({t_})',(-0.02,1.03),xycoords='axes fraction',fontsize=9,fontweight='bold',ha='right')
fig.savefig('figures_new/Fig9_root_constraint_and_span.pdf')
print('done',Ls,VE,ana)

# ---- Fig 6 (consolidated; replaces old Figs 6-8): 3x3 alpha grid, classical clamp, 48x24
g=list(csv.DictReader(open('verification/results/alpha_grid.csv')))
S=[0.5,1.0,1.5]
fig,ax=plt.subplots(1,2,figsize=(6.6,2.9),constrained_layout=True)
for a_,key,lab in zip(ax,('V_E','V_A'),('(a) Case E','(b) Case A')):
    Z=np.zeros((3,3))
    for r in g: Z[S.index(float(r['s3'])),S.index(float(r['s1']))]=float(r[key])
    lim=np.max(np.abs(Z)); 
    im=a_.imshow(Z,origin='lower',cmap='RdBu_r' if key=='V_E' else 'Blues_r',vmin=-lim if key=='V_E' else None,vmax=lim if key=='V_E' else None,aspect='equal')
    for i in range(3):
        for j in range(3): a_.text(j,i,f'{Z[i,j]:+.3f}',ha='center',va='center',fontsize=8,color=('w' if abs(Z[i,j])>0.25 else 'k') if key=='V_E' else ('w' if Z[i,j]<-1.45 else 'k'))
    a_.set_xticks(range(3)); a_.set_xticklabels([f'{21.8*s:.1f}' for s in S]); a_.set_yticks(range(3)); a_.set_yticklabels([f'{-4.3*s:.2f}' for s in S])
    a_.set_xlabel(r'$\alpha_1$ ($10^{-6}$ K$^{-1}$)'); a_.set_ylabel(r'$\alpha_3$ ($10^{-6}$ K$^{-1}$)'); a_.set_title(lab,fontsize=9,loc='left')
    a_.spines[:].set_visible(False); cb=fig.colorbar(im,ax=a_,shrink=0.8); cb.set_label(r'$V_{\mathrm{oc}}$ (V)')
fig.savefig('figures_new/Fig6_alpha_grid.pdf')

# ---- Figs 3, 4, 5 (need the solver)
import sys; sys.path.insert(0,'verification'); import tpfem as T
# Fig 3: p3 linearity (16x8, classical clamp, fixed K)
sc=np.array([0,0.5,1,1.5,2]); vs=[]
for s in sc:
    mm=dict(T.MAT); mm['p3']*=s; vs.append(T.solve_bfs(16,8,mat=mm,clamp='classical')['V'])
vs=np.array(vs); lin=np.polyfit(sc,vs,1)
fig,ax=plt.subplots(1,2,figsize=(6.6,2.7),constrained_layout=True)
ax[0].plot(sc,vs,'o',color=OI['blue'],ms=4); xx=np.linspace(0,2,10); ax[0].plot(xx,np.polyval(lin,xx),'-',color=OI['grey'],lw=0.8)
ax[0].set_xlabel(r'$p_3$ scale factor'); ax[0].set_ylabel(r'Case A, $V_{\mathrm{oc}}$ (V)')
ax[1].plot(sc,(vs-np.polyval(lin,sc))*1e15,'o',color=OI['verm'],ms=4); ax[1].axhline(0,color='k',lw=0.5); ax[1].set_xlabel(r'$p_3$ scale factor'); ax[1].set_ylabel(r'deviation from line ($10^{-15}$ V)')
for a_,t_ in zip(ax,'ab'): a_.annotate(f'({t_})',(-0.02,1.03),xycoords='axes fraction',fontsize=9,fontweight='bold',ha='right')
fig.savefig('figures_new/Fig3_p3_linearity.pdf'); print('p3 slope',lin[0])
# Fig 4: voltages
VD=T.solve_bfs(80,40,clamp='classical',piezo=False)['V']; VA=T.solve_bfs(80,40,clamp='classical')['V']; VE=T.solve_bfs(80,40,clamp='classical',pyro=False)['V']
fig,ax=plt.subplots(1,2,figsize=(6.6,2.7),constrained_layout=True)
lab=['D','A','E','zero $\\theta$']; val=[VD,VA,VE,0.0]; cols=[OI['orange'],OI['blue'],OI['green'],OI['grey']]
ax[0].bar(range(4),val,color=cols,width=0.6); ax[0].axhline(0,color='k',lw=0.6); ax[0].set_xticks(range(4)); ax[0].set_xticklabels(lab); ax[0].set_ylabel(r'$V_{\mathrm{oc}}$ (V)')
for i,v_ in enumerate(val): ax[0].text(i,v_+(0.08 if v_>=0 else -0.08),f'{v_:+.4f}',ha='center',va='bottom' if v_>=0 else 'top',fontsize=7.5)
ax[0].set_ylim(-4,0.8)
v16={c:T.solve_bfs(16,8,clamp='classical',**kw)['V'] for c,kw in (('D',dict(piezo=False)),('A',{}),('E',dict(pyro=False)))}
b=[v16['D'],v16['E'],v16['D']+v16['E'],v16['A']]; ax[1].bar(range(4),b,color=[OI['orange'],OI['green'],OI['grey'],OI['blue']],width=0.6); ax[1].axhline(0,color='k',lw=0.6)
ax[1].set_xticks(range(4)); ax[1].set_xticklabels(['D','E','D+E','A']); ax[1].set_ylabel(r'$V_{\mathrm{oc}}$ (V), $16\times8$ mesh'); ax[1].set_ylim(-4,0.8)
for i,v_ in enumerate(b): ax[1].text(i,v_+(0.08 if v_>=0 else -0.08),f'{v_:+.4f}',ha='center',va='bottom' if v_>=0 else 'top',fontsize=7.5)
for a_,t_ in zip(ax,'ab'): a_.annotate(f'({t_})',(-0.02,1.03),xycoords='axes fraction',fontsize=9,fontweight='bold',ha='right')
fig.savefig('figures_new/Fig4_voltages_decomposition.pdf'); print('V16',v16, 'V80',VD,VA,VE)
# Fig 5: fields, Case A, 80x40 classical clamp (nodal values; E_z element-averaged)
nx,nz=80,40; r=T.solve_bfs(nx,nz,clamp='classical'); q=r['q']; nn=(nx+1)*(nz+1)
Q=q.reshape(nn,9); idx=lambda ix,iz: ix*(nz+1)+iz
X=np.linspace(0,T.L,nx+1)*1e6; Zc=np.linspace(0,T.H,nz+1)*1e6
fld=lambda col: np.array([[Q[idx(ix,iz),col] for ix in range(nx+1)] for iz in range(nz+1)])
phi=fld(8); exx=fld(1); u=fld(0); w=fld(4); mag=np.hypot(u,w)*1e9
Ez=-(phi[1:,:]-phi[:-1,:])/(T.H/nz); Ezc=0.5*(Ez[:,1:]+Ez[:,:-1]); Zm=0.5*(Zc[1:]+Zc[:-1]); Xm=0.5*(X[1:]+X[:-1])
fig,ax=plt.subplots(2,2,figsize=(6.8,4.8),constrained_layout=True)
def pm(a_,x,z,F,cmap,lab,t_,**kw):
    im=a_.pcolormesh(x,z,F,cmap=cmap,shading='auto',rasterized=True,**kw); a_.set_xlabel(r'$x$ ($\mu$m)'); a_.set_ylabel(r'$z$ ($\mu$m)'); a_.set_aspect('auto'); cb=fig.colorbar(im,ax=a_,pad=0.01,shrink=0.9); cb.set_label(lab); a_.annotate(t_,(-0.02,1.03),xycoords='axes fraction',fontsize=9,fontweight='bold',ha='right')
pm(ax[0,0],X,Zc,phi,'viridis',r'$\phi$ (V)','(a)'); pm(ax[0,1],Xm,Zm,Ezc/1e6,'viridis',r'$E_z$ ($10^{6}$ V m$^{-1}$)','(b)')
pm(ax[1,0],X,Zc,exx*1e4,'RdBu_r',r'$\varepsilon_{xx}$ ($10^{-4}$)','(c)',vmin=-3.3,vmax=3.3); pm(ax[1,1],X,Zc,mag,'viridis',r'$|\mathbf{u}|$ (nm)','(d)')
fig.savefig('figures_new/Fig5_solved_fields.pdf',dpi=300)
print('fields: phi top range',phi[-1,:].min(),phi[-1,:].max(),' Ez range',Ezc.min()/1e6,Ezc.max()/1e6,' exx range',exx.min()*1e4,exx.max()*1e4,' |u| max nm',mag.max(), 'exx top at x=0,1um,5um:',exx[-1,0]*1e4,exx[-1,8]*1e4,exx[-1,40]*1e4)

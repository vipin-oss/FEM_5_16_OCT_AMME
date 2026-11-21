"""Redrawn Fig. 1 (schematic). Content identical to the original: geometry, constraints, two routes to V_oc. Run from repo root."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, FancyBboxPatch
plt.rcParams.update({'font.family':'serif','mathtext.fontset':'cm','font.size':8.5,'pdf.fonttype':42})
fig=plt.figure(figsize=(7.4,3.9)); 
# ---- (a) geometry
a=fig.add_axes([0.0,0.0,0.50,1.0]); a.set_xlim(0,11); a.set_ylim(0,6.4); a.axis('off')
a.text(0.1,6.1,'(a)',fontweight='bold',fontsize=9)
a.add_patch(Rectangle((1.6,1.9),0.35,2.6,fill=False,hatch='////',lw=0.8))
a.add_patch(Rectangle((1.95,1.9),6.0,2.6,fill=False,lw=0.8))
a.plot([1.95,7.95],[4.5,4.5],'k',lw=3); a.plot([1.95,7.95],[1.9,1.9],'k',lw=3)
a.text(4.95,5.05,'top electrode ($z=h$): floating,\nequipotential, net charge $Q=0$',ha='center',fontsize=8)
a.text(4.95,1.35,r'bottom electrode ($z=0$): $\phi=0$ (ground)',ha='center',fontsize=8)
a.text(0.8,3.2,'clamped\nroot',ha='center',va='center',fontsize=8); a.text(1.75,4.7,r'$x=0$',ha='center',fontsize=8)
a.text(2.2,3.95,r'BaTiO$_3$ (tetragonal $4mm$)',fontsize=8); a.text(2.2,3.5,'plane strain, per unit depth',fontsize=8)
a.annotate('',xy=(6.3,4.2),xytext=(6.3,2.2),arrowprops=dict(arrowstyle='-|>',color='#D55E00',lw=1.2))
a.text(6.45,2.95,r'poling $P_s\parallel z$',color='#D55E00',fontsize=8)
a.text(7.1,2.15,'free end',fontsize=8,ha='center')
a.annotate('',xy=(8.75,4.5),xytext=(8.75,1.9),arrowprops=dict(arrowstyle='-|>',color='#009E73',lw=1.2))
a.text(9.05,4.5,r'$T_b+\Delta T$',color='#009E73',fontsize=8,va='center'); a.text(9.05,1.9,r'$T_b$',color='#009E73',fontsize=8,va='center')
a.text(9.05,3.2,r'$\theta(z)=\Delta T\,z/h$'+'\n'+r'$\Delta T=10$ K',color='#009E73',fontsize=8,va='center')
a.annotate('',xy=(1.3,0.7),xytext=(0.5,0.7),arrowprops=dict(arrowstyle='<|-',lw=0.9)); a.annotate('',xy=(0.5,1.45),xytext=(0.5,0.7),arrowprops=dict(arrowstyle='-|>',lw=0.9))
a.text(1.4,0.5,r'$x$',fontsize=8); a.text(0.25,1.5,r'$z$',fontsize=8)
a.text(5.5,0.1,r'$L=10\ \mu$m, $h=1\ \mu$m (not to scale)',ha='center',fontsize=7.5,style='italic')
# ---- (b) flow
b=fig.add_axes([0.50,0.0,0.50,1.0]); b.set_xlim(0,10); b.set_ylim(0,10); b.axis('off'); b.text(0.0,9.75,'(b)',fontweight='bold',fontsize=9)
def box(x,y,w,h,t,fc='#EEF3F8'):
    b.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.12',fc=fc,ec='k',lw=0.7)); b.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=8)
def arr(x0,y0,x1,y1): b.add_patch(FancyArrowPatch((x0,y0),(x1,y1),arrowstyle='-|>',mutation_scale=8,lw=0.8,color='k'))
box(1.5,8.6,7,0.85,r'prescribed temperature $\theta(z)=\Delta T\,z/h$')
box(0.1,6.9,5.4,1.05,'anisotropic thermal expansion '+r'$\rightarrow$'+'\n'+r'plane-strain thermal stress $\beta_{PS}\,\theta$')
box(0.1,5.2,5.4,1.05,r'coupled finite-element solve for $(u,w,\phi)$')
box(0.1,3.5,5.4,1.05,'bending strain '+r'$\rightarrow$'+'\n'+r'piezoelectric charge $e\,\varepsilon$')
box(6.0,5.2,3.8,2.75,'direct pyroelectric\n'+r'charge $p_3\,\theta$',fc='#FBF3E3')
box(0.3,1.9,9.4,1.0,'open-circuit top electrode:\n'+r'$\phi_{top}$ tied, net charge $Q=0$')
box(0.3,0.55,9.4,0.85,r'$V_{oc}=\phi_{top}-\phi_{bottom}$: Cases D, A and E')
arr(3.0,8.6,2.8,7.95); arr(8.0,8.6,7.9,7.95); arr(2.8,6.9,2.8,6.25); arr(2.8,5.2,2.8,4.55); arr(2.8,3.5,2.8,2.9); arr(7.9,5.2,7.9,2.9); arr(5.0,1.9,5.0,1.4)
fig.savefig('figures/Fig1_model_schematic.pdf'); print('ok')

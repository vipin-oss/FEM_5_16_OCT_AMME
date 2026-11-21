"""Alpha sensitivity (80x40, classical clamp) and 3x3 scale grid (48x24, classical clamp). Writes results/alpha_*.csv"""
import tpfem as t, numpy as np, csv
m=t.MAT
def V(a1,a3,**kw):
    mm=dict(m); mm['a1']=a1; mm['a3']=a3; return t.solve_bfs(80,40,mat=mm,clamp='classical',**kw)['V']
# Case E linear; derive coefficients at 80x40
c1=V(1e-6,0,pyro=False); c3=V(0,1e-6,pyro=False); print('80x40 classical: dVE/dalpha1=%.6f, dVE/dalpha3=%.6f V per 1e-6'%(c1,c3))
vA_slope=t.solve_bfs(80,40,clamp='classical')['V']-t.solve_bfs(80,40,clamp='classical',pyro=False)['V']; print('V_A-V_E (pyro part) = %.6f'%vA_slope)
se1,se3=1.6459,3.2611
for n in (1,2):
    vals=[c1*(21.8+i*n*se1)+c3*(-4.3+j*n*se3) for i in (-1,1) for j in (-1,1)]
    print(f'n={n}: V_E range {min(vals):+.4f} .. {max(vals):+.4f}; V_A range {min(vals)+vA_slope:+.4f} .. {max(vals)+vA_slope:+.4f}')
print('alpha3 for V_E=0 at nominal alpha1: %.3e  (%.2f sd from nominal)'%(-c1*21.8/c3*1e-6,(-c1*21.8/c3+4.3)/(-se3)))
print('dVE per 1sd: alpha1 %.4f, alpha3 %.4f'%(c1*se1,c3*se3))
# 3x3 grid, 48x24
rows=[]
for s1 in (0.5,1,1.5):
    for s3 in (0.5,1,1.5):
        a1,a3=21.8e-6*s1,-4.3e-6*s3; mm=dict(m); mm['a1']=a1; mm['a3']=a3
        vE=t.solve_bfs(48,24,mat=mm,clamp='classical',pyro=False)['V']; vA=t.solve_bfs(48,24,mat=mm,clamp='classical')['V']
        rows.append((s1,s3,a1,a3,vE,vA)); print(s1,s3,'V_E=%+.5f V_A=%+.5f'%(vE,vA))
csv.writer(open('results/alpha_grid.csv','w',newline='')).writerows([('s1','s3','alpha1','alpha3','V_E','V_A')]+rows)
# polarity shift at 48x24 for the text
for bm in ('simplified','full'):
    print(bm,'48x24 classical: V_A=%+.5f V_E=%+.5f'%(t.solve_bfs(48,24,clamp='classical',bmode=bm)['V'],t.solve_bfs(48,24,clamp='classical',bmode=bm,pyro=False)['V']))
print('16x8 classical V_D+V_E-V_A:',-3.438647248+t.solve_bfs(16,8,clamp='classical',pyro=False)['V']-t.solve_bfs(16,8,clamp='classical')['V'], ' V_A16=',t.solve_bfs(16,8,clamp='classical')['V'])
print('zero-T null:', t.solve_bfs(16,8,clamp='classical',alpha_scale=0.0,pyro=False)['V'])

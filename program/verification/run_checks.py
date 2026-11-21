"""Additional P1/P2 checks: analytical long-beam benchmark, root-constraint effect, electrodes, symmetry, conditioning, alpha sensitivity."""
import tpfem as t, numpy as np, scipy.sparse as sp
m = t.MAT; C, e, kap = t.blocks(m)

def analytic(mat, bmode='full', pyro=True):
    """Mid-span (x-independent) solution of the full coupled plane-strain problem.
    sigma_zz=0, D_z=0, sigma_xx=0 (zero net force/moment is met by sigma_xx==0 since theta is linear in z).
    unknowns (eps_xx, eps_zz, E_z) per unit theta."""
    b = t.beta(mat, bmode); p = mat['p3'] if pyro else 0.0
    M = np.array([[mat['C11'], mat['C13'], -mat['e31']],     # sigma_xx = 0
                  [mat['C13'], mat['C33'], -mat['e33']],     # sigma_zz = 0
                  [mat['e31'], mat['e33'], mat['k33']]])     # D_z = 0
    rhs = np.array([b[0], b[1], -p])
    exx, ezz, E = np.linalg.solve(M, rhs)
    V = -E*t.DT*t.H/2
    return V, exx, ezz
print("== 1. Analytical mid-span (long-beam) benchmark, full coupled problem")
for bm in ('full', 'simplified'):
    for c, kw in (('D', dict(pyro=True)), ('A', dict(pyro=True)), ('E', dict(pyro=False))):
        mm = dict(m)
        if c == 'D': mm['e31'] = mm['e33'] = 0.0
        V, exx, ezz = analytic(mm, bm, **kw); print(f"  {bm:10s} case {c}: V_1D = {V:+.8f} V   (eps_xx/theta={exx:.4e}, eps_zz/theta={ezz:.4e})")
print("   FEM (BFS, classical clamp, fixed 0.125 um x-element, nz=16) vs analytic as span grows; Case E and A")
for Ls in (10e-6, 20e-6, 50e-6, 100e-6):
    t.L = Ls; nx = int(round(Ls/0.125e-6)); out = []
    for c, kw in (('A', {}), ('E', dict(pyro=False))):
        out.append((c, t.solve_bfs(nx, 16, clamp='classical', **kw)['V']))
    print(f"  L={Ls*1e6:5.0f} um nx={nx}: " + "  ".join(f"V_{c}={v:+.6f}" for c, v in out))
t.L = 10e-6
VA, _, _ = analytic(m, 'full'); VE, _, _ = analytic(m, 'full', pyro=False)
print(f"  analytic: V_A={VA:+.6f}  V_E={VE:+.6f}")

print("== 2. Root constraint: all-derivative vs classical clamp (80x40, Case E and A)")
nx, nz = 80, 40
for c, kw in (('E', dict(pyro=False)), ('A', {})):
    for cl in ('all', 'classical'):
        r = t.solve_bfs(nx, nz, clamp=cl, **kw); q = r['q']
        nid = lambda ix, iz: ix*(nz+1)+iz
        ux0 = np.array([q[9*nid(0, iz)+1] for iz in range(nz+1)])      # eps_xx at root = u_x
        wx0 = np.array([q[9*nid(0, iz)+5] for iz in range(nz+1)])      # w_x at root (rotation)
        eps_zz0 = np.array([q[9*nid(0, iz)+6] for iz in range(nz+1)])  # w_z at root
        wtip = np.array([q[9*nid(nx, iz)+4] for iz in range(nz+1)])
        utip = np.array([q[9*nid(nx, iz)+0] for iz in range(nz+1)])
        print(f"  case {c} {cl:9s} V={r['V']:+.7f}  root eps_xx[top]={ux0[-1]:+.3e} [bot]={ux0[0]:+.3e}  root w_x(mean)={wx0.mean():+.3e}  tip w(mid)={wtip[nz//2]*1e9:+.4f} nm  tip u(top)={utip[-1]*1e9:+.4f} nm")
print("== 3. Electrodes and charge balance (BFS classical, 32x16, Case A)")
r = t.solve_bfs(32, 16, clamp='classical'); q = r['q']; nz = 16; nxx = 32
nid = lambda ix, iz: ix*(nz+1)+iz
top = np.array([q[9*nid(ix, nz)+8] for ix in range(nxx+1)]); bot = np.array([q[9*nid(ix, 0)+8] for ix in range(nxx+1)])
print(f"  top phi: max-min = {top.max()-top.min():.3e} V ; bottom phi max|.| = {np.abs(bot).max():.3e} V")
res = r['Kr']@(r['T'].T@q*0+np.linalg.lstsq if False else 0) if False else None
# net charge on floating electrode = residual of master equation of the full (unreduced) system summed over top nodes
rfull = r['K']@q - r['f']
topdofs = [9*nid(ix, nz)+8 for ix in range(nxx+1)]
print(f"  net charge on floating electrode (sum of full-system residuals on top phi dofs) = {rfull[topdofs].sum():.3e}  (scale: sum|r| over grounded dofs = {sum(abs(rfull[9*nid(ix,0)+8]) for ix in range(nxx+1)):.3e})")
print(f"  reduced-system residual ||Kr q - fr||/||fr|| = {np.linalg.norm(r['Kr']@(r['T'].T@q if False else np.linalg.lstsq(r['T'].toarray(),q,rcond=None)[0])-r['fr'])/np.linalg.norm(r['fr']):.3e}")
print(f"  asymmetry of reduced matrix ||Kr-Kr^T||_F/||Kr||_F = {sp.linalg.norm(r['Kr']-r['Kr'].T)/sp.linalg.norm(r['Kr']):.3e}")
print("== 4. Conditioning (BFS classical 16x8, dense)")
r = t.solve_bfs(16, 8, clamp='classical'); K = r['Kr'].toarray(); s = 1/np.sqrt(np.abs(np.diag(K)))
print(f"  cond(K) raw = {np.linalg.cond(K):.3e}   cond(S K S) = {np.linalg.cond(s[:,None]*K*s[None,:]):.3e}")
print("== 5. Thermal-expansion sensitivity of Case E (linear in alpha; BFS classical 32x16)")
def VE(a1, a3):
    mm = dict(m); mm['a1'] = a1; mm['a3'] = a3; return t.solve_bfs(32, 16, mat=mm, clamp='classical', pyro=False)['V']
c1 = (VE(1e-6, 0)); c3 = (VE(0, 1e-6))
print(f"  V_E = {c1:+.5f} V per 1e-6 of alpha1 + {c3:+.5f} V per 1e-6 of alpha3 ;  sign change on alpha3/alpha1 = {-c1/c3:+.4f}")
for lab, a1, a3 in (('nominal', 21.8, -4.3), ('a1+1sd', 21.8+1.65, -4.3), ('a1-1sd', 21.8-1.65, -4.3), ('a3+1sd', 21.8, -4.3+3.26), ('a3-1sd', 21.8, -4.3-3.26), ('a1-1sd,a3+1sd', 21.8-1.65, -4.3+3.26), ('a1+1sd,a3-1sd', 21.8+1.65, -4.3-3.26)):
    print(f"  {lab:16s} alpha=({a1:6.2f},{a3:6.2f})e-6 : V_E = {c1*a1+c3*a3:+.5f} V (ratio a3/a1={a3/a1:+.3f})")

"""Independent plane-strain thermopiezoelectric cantilever solvers (BaTiO3, 4mm, poled along z).
Written for the FINEL audit from the manuscript's stated formulation only; no code from the authors was available.
Two discretisations: BFS (C1 Hermite, 9 dof/node, as in the manuscript) and Q9 (C0 biquadratic, independent).
Voltage = phi(top floating electrode) - phi(bottom grounded electrode)."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spl

EPS0 = 8.854187817e-12
MAT = dict(C11=2.22e11, C12=1.08e11, C13=1.11e11, C33=1.51e11, C44=6.10e10,
           e15=34.2, e31=-0.7, e33=6.7, k11=2200*EPS0, k33=56*EPS0,
           a1=21.8e-6, a3=-4.3e-6, p3=-3.41e-4)
L, H, DT = 10e-6, 1e-6, 10.0

def beta(m, mode):
    if mode == 'full':      # plane strain, eps_yy = 0 total: full 3D contraction
        return np.array([(m['C11']+m['C12'])*m['a1']+m['C13']*m['a3'],
                         2*m['C13']*m['a1']+m['C33']*m['a3'], 0.0])
    if mode == 'simplified':  # 2x2 plane-strain stiffness applied to [a1,a3]
        return np.array([m['C11']*m['a1']+m['C13']*m['a3'],
                         m['C13']*m['a1']+m['C33']*m['a3'], 0.0])
    raise ValueError(mode)

def blocks(m):
    C = np.array([[m['C11'], m['C13'], 0], [m['C13'], m['C33'], 0], [0, 0, m['C44']]])
    e = np.array([[0, 0, m['e15']], [m['e31'], m['e33'], 0]])   # D=(Dx,Dz) = e*(exx,ezz,gxz)
    k = np.diag([m['k11'], m['k33']])
    return C, e, k

def gauss(n):
    x, w = np.polynomial.legendre.leggauss(n); return x, w

# ---------------------------------------------------------------- BFS
def herm(s, a):
    """cubic Hermite on [0,a], s in [0,1]: returns N(4: v0, d0, v1, d1), dN/dx"""
    N = np.array([1-3*s**2+2*s**3, a*(s-2*s**2+s**3), 3*s**2-2*s**3, a*(-s**2+s**3)])
    dN = np.array([(-6*s+6*s**2)/a, (1-4*s+3*s**2), (6*s-6*s**2)/a, (-2*s+3*s**2)])
    return N, dN

CORN = [(0, 0), (1, 0), (1, 1), (0, 1)]   # (ix,iz) offsets, counter-clockwise
def bfs_element(a, b, m, ng=4):
    """returns Kuu(32x32), Kup(32x4), Kpp(4x4) and load integrals for beta/theta, p/theta"""
    C, e, kap = blocks(m)
    xg, wg = gauss(ng)
    Kuu = np.zeros((32, 32)); Kup = np.zeros((32, 4)); Kpp = np.zeros((4, 4))
    Fb = np.zeros((32, 3)); Fp = np.zeros((4, 2))   # load kernels: int B^T (.) dA
    Fb_z = np.zeros((32, 3)); Fp_z = np.zeros((4, 2))        # int B^T c * (z/b) dA   (theta = DT*(z0+z)/H)
    for xi, wx in zip(xg, wg):
        for et, wz in zip(xg, wg):
            sx, sz = (xi+1)/2, (et+1)/2
            Nx, dNx = herm(sx, a); Nz, dNz = herm(sz, b)
            # 1D dof index: 0:v at node0 ,1: dv at node0, 2: v at node1, 3: dv at node1
            Nm = np.zeros(16); Nmx = np.zeros(16); Nmz = np.zeros(16)
            for c, (ix, iz) in enumerate(CORN):
                for t, (tx, tz) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):  # v, v_x, v_z, v_xz
                    i = 2*ix+tx; j = 2*iz+tz
                    Nm[4*c+t] = Nx[i]*Nz[j]; Nmx[4*c+t] = dNx[i]*Nz[j]; Nmz[4*c+t] = Nx[i]*dNz[j]
            B = np.zeros((3, 32))
            B[0, :16] = Nmx; B[1, 16:] = Nmz; B[2, :16] = Nmz; B[2, 16:] = Nmx
            # potential: bilinear
            lx = np.array([1-sx, sx]); dlx = np.array([-1/a, 1/a]); lz = np.array([1-sz, sz]); dlz = np.array([-1/b, 1/b])
            Np = np.zeros(4); Npx = np.zeros(4); Npz = np.zeros(4)
            for c, (ix, iz) in enumerate(CORN):
                Np[c] = lx[ix]*lz[iz]; Npx[c] = dlx[ix]*lz[iz]; Npz[c] = lx[ix]*dlz[iz]
            Bp = np.array([Npx, Npz])
            w = wx*wz*a*b/4
            Kuu += w*B.T@C@B; Kup += w*B.T@e.T@Bp; Kpp += w*Bp.T@kap@Bp
            # theta = DT*(zbase + sz*b)/H : store 1 and sz moments
            Fb[:, :] += w*B.T            # int B^T (.)  [per unit coefficient vector]
            Fb_z[:, :] += w*B.T*sz*b
            Fp += w*Bp.T; Fp_z += w*Bp.T*sz*b
    return Kuu, Kup, Kpp, Fb, Fb_z, Fp, Fp_z

def solve_bfs(nx, nz, mat=MAT, bmode='full', clamp='all', pyro=True, piezo=True, alpha_scale=1.0, return_fields=False):
    m = dict(mat); 
    if not pyro: m['p3'] = 0.0
    if not piezo: m['e15'] = m['e31'] = m['e33'] = 0.0
    m['a1'] *= alpha_scale; m['a3'] *= alpha_scale
    a, b = L/nx, H/nz
    Kuu, Kup, Kpp, Fb, Fbz, Fp, Fpz = bfs_element(a, b, m)
    bet = beta(m, bmode); pv = np.array([0.0, m['p3']])
    nn = (nx+1)*(nz+1); nd = 9*nn
    nid = lambda ix, iz: ix*(nz+1)+iz
    rows = []; cols = []; vals = []; f = np.zeros(nd)
    # element dof maps
    for ex in range(nx):
        for ez in range(nz):
            nodes = [nid(ex+i, ez+j) for (i, j) in CORN]
            dm = np.array([9*n+k for n in nodes for k in range(4)] + [9*n+4+k for n in nodes for k in range(4)])
            pm = np.array([9*n+8 for n in nodes])
            dofs = np.concatenate([dm, pm])
            A = np.zeros((36, 36))
            A[:32, :32] = Kuu; A[:32, 32:] = Kup; A[32:, :32] = Kup.T; A[32:, 32:] = -Kpp
            th0 = DT*(ez*b)/H; th1 = DT/H
            fu = (Fb@bet)*th0 + (Fbz@bet)*th1
            fpv = (Fp@pv)*th0 + (Fpz@pv)*th1
            R, Cc = np.meshgrid(dofs, dofs, indexing='ij')
            rows.append(R.ravel()); cols.append(Cc.ravel()); vals.append(A.ravel())
            f[dm] += fu; f[pm] += -fpv       # phi-equation: Kpu q - Kpp phi = -int Bp^T p theta
    Kg = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(nd, nd))
    # constraints
    fixed = set()
    for iz in range(nz+1):
        n = nid(0, iz)
        mech = {'all': [0,1,2,3,4,5,6,7], 'classical': [0, 2, 4, 6]}[clamp]  # classical: u=w=0 and u_z=w_z=0
        for k in mech: fixed.add(9*n+k)
    for ix in range(nx+1): fixed.add(9*nid(ix, 0)+8)            # grounded bottom electrode
    top = [9*nid(ix, nz)+8 for ix in range(nx+1)]
    master = top[0]
    free = np.array(sorted(set(range(nd)) - fixed - set(top[1:])))
    pos = -np.ones(nd, dtype=int); pos[free] = np.arange(len(free))
    # T maps reduced -> full
    Tr = list(free); Tc = list(range(len(free))); Tv = [1.0]*len(free)
    for t in top[1:]: Tr.append(t); Tc.append(pos[master]); Tv.append(1.0)
    T = sp.csr_matrix((Tv, (Tr, Tc)), shape=(nd, len(free)))
    Kr = (T.T@Kg@T).tocsc(); fr = T.T@f
    s = 1/np.sqrt(np.abs(Kr.diagonal())); S = sp.diags(s)
    qr = S@spl.spsolve((S@Kr@S).tocsc(), S@fr)
    q = T@qr
    out = dict(V=q[master], q=q, K=Kg, f=f, T=T, Kr=Kr, fr=fr, nx=nx, nz=nz, ndof=len(free))
    return out

# ---------------------------------------------------------------- Q9
def q9_shape(xi, et):
    def l(t): return np.array([t*(t-1)/2, 1-t*t, t*(t+1)/2]), np.array([t-0.5, -2*t, t+0.5])
    lx, dlx = l(xi); lz, dlz = l(et)
    N = np.outer(lx, lz).ravel(); Nxi = np.outer(dlx, lz).ravel(); Net = np.outer(lx, dlz).ravel()
    return N, Nxi, Net   # index = 3*i + j : i along x, j along z

def solve_q9(nx, nz, mat=MAT, bmode='full', pyro=True, piezo=True, alpha_scale=1.0, clamp='disp'):
    m = dict(mat)
    if not pyro: m['p3'] = 0.0
    if not piezo: m['e15'] = m['e31'] = m['e33'] = 0.0
    m['a1'] *= alpha_scale; m['a3'] *= alpha_scale
    C, e, kap = blocks(m); bet = beta(m, bmode); pv = np.array([0.0, m['p3']])
    a, b = L/nx, H/nz
    NX, NZ = 2*nx+1, 2*nz+1
    nid = lambda i, j: i*NZ+j          # grid node (i along x, j along z), step a/2,b/2
    nn = NX*NZ; nd = 3*nn              # u, w, phi
    xg, wg = gauss(3)
    rows = []; cols = []; vals = []; f = np.zeros(nd)
    for ex in range(nx):
        for ez in range(nz):
            nodes = [nid(2*ex+i, 2*ez+j) for i in range(3) for j in range(3)]
            Ae = np.zeros((27, 27)); fe = np.zeros(27)
            for xi, wx in zip(xg, wg):
                for et, wz in zip(xg, wg):
                    N, Nxi, Net = q9_shape(xi, et)
                    Nx = Nxi*2/a; Nz = Net*2/b; w = wx*wz*a*b/4
                    z = ez*b + (et+1)*b/2; th = DT*z/H
                    B = np.zeros((3, 18)); B[0, :9] = Nx; B[1, 9:] = Nz; B[2, :9] = Nz; B[2, 9:] = Nx
                    Bp = np.array([Nx, Nz])
                    Ae[:18, :18] += w*B.T@C@B; Ae[:18, 18:] += w*B.T@e.T@Bp
                    Ae[18:, :18] += w*Bp.T@e@B; Ae[18:, 18:] -= w*Bp.T@kap@Bp
                    fe[:18] += w*B.T@bet*th; fe[18:] -= w*Bp.T@pv*th
            dm = np.array([3*n for n in nodes]+[3*n+1 for n in nodes]+[3*n+2 for n in nodes])
            R, Cc = np.meshgrid(dm, dm, indexing='ij')
            rows.append(R.ravel()); cols.append(Cc.ravel()); vals.append(Ae.ravel()); f[dm] += fe
    Kg = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(nd, nd))
    fixed = set()
    for j in range(NZ): fixed |= {3*nid(0, j), 3*nid(0, j)+1}
    for i in range(NX): fixed.add(3*nid(i, 0)+2)
    top = [3*nid(i, NZ-1)+2 for i in range(NX)]; master = top[0]
    free = np.array(sorted(set(range(nd)) - fixed - set(top[1:])))
    pos = -np.ones(nd, dtype=int); pos[free] = np.arange(len(free))
    Tr = list(free); Tc = list(range(len(free))); Tv = [1.0]*len(free)
    for t in top[1:]: Tr.append(t); Tc.append(pos[master]); Tv.append(1.0)
    T = sp.csr_matrix((Tv, (Tr, Tc)), shape=(nd, len(free)))
    Kr = (T.T@Kg@T).tocsc(); fr = T.T@f
    s = 1/np.sqrt(np.abs(Kr.diagonal())); S = sp.diags(s)
    qr = S@spl.spsolve((S@Kr@S).tocsc(), S@fr); q = T@qr
    return dict(V=q[master], q=q, ndof=len(free))

import tpfem as t, numpy as np
for (nx,nz) in [(8,4),(16,8)]:
    for case,kw in [('D',dict(piezo=False)),('A',{}),('E',dict(pyro=False))]:
        r=t.solve_bfs(nx,nz,clamp='all',**kw); print(nx,nz,case,r['V'],r['ndof'])

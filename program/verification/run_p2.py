"""P1/P2 verification runs. Usage: python3 -I run_p2.py  (writes results/*.csv, prints tables)"""
import tpfem as t, numpy as np, csv, os, time
os.makedirs('results', exist_ok=True)
cases = {'D': dict(piezo=False), 'A': {}, 'E': dict(pyro=False)}
meshes = [(8,4),(16,8),(32,16),(48,24),(64,32),(80,40)]
rows = []
def run(label, fn, **kw):
    for (nx,nz) in meshes:
        for c,ck in cases.items():
            t0=time.time(); r=fn(nx,nz,**ck,**kw); rows.append((label,nx,nz,c,r['ndof'],r['V']))
            print(f"{label:34s} {nx:3d}x{nz:<3d} {c} ndof={r['ndof']:6d} V={r['V']:+.8f}", flush=True)
run('BFS all-derivative root, full beta', t.solve_bfs, bmode='full', clamp='all')
run('BFS classical clamp, full beta', t.solve_bfs, bmode='full', clamp='classical')
run('BFS all-derivative root, simpl. beta', t.solve_bfs, bmode='simplified', clamp='all')
run('BFS classical clamp, simpl. beta', t.solve_bfs, bmode='simplified', clamp='classical')
run('Q9 classical clamp, full beta', t.solve_q9, bmode='full')
run('Q9 classical clamp, simpl. beta', t.solve_q9, bmode='simplified')
with open('results/voltages_all.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['model','nx','nz','case','ndof','V_volt']); w.writerows(rows)

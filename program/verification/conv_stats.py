"""Convergence statistics (relative change, observed order, Aitken limits) from results/voltages_all.csv"""
import csv, numpy as np
rows=list(csv.DictReader(open('results/voltages_all.csv')))
def series(model,case): return [float(r['V_volt']) for r in rows if r['model']==model and r['case']==case], [int(r['ndof']) for r in rows if r['model']==model and r['case']==case]
def aitken(v0,v1,v2): return v2-(v2-v1)**2/((v2-v1)-(v1-v0))
for model in ('BFS classical clamp, full beta','BFS all-derivative root, full beta','Q9 classical clamp, full beta'):
    print('##',model)
    for c in 'AE':
        v,nd=series(model,c); ch=[100*(v[i]-v[i-1])/v[i-1] for i in range(1,len(v))]
        print(c,'V=',' '.join(f'{x:+.6f}' for x in v)); print('  rel.change %:',' '.join(f'{x:+.3f}' for x in ch))
        # triplets with h ratio 2 : meshes 8,16,32 and 16,32,64 (indices 0,1,2 and 1,2,4)
        for (i,j,k) in ((0,1,2),(1,2,4)):
            p=np.log2(abs((v[j]-v[i])/(v[k]-v[j]))) if (v[k]-v[j])!=0 else float('nan')
            print(f'  triplet meshes {i},{j},{k}: p_obs={p:.2f}  Aitken limit={aitken(v[i],v[j],v[k]):+.6f}')

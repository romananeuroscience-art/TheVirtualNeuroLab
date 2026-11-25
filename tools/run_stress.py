"""Stress test for the Neuron Silencing Screen's 'needed' neurons (TEAM.md task 3).

The screen's 95% ranges only measure simulation noise: the wiring and settings never change between runs.
This script asks a harder question: does each 'needed' neuron STAY needed if the model is slightly wrong?
It rebuilds the brain in several plausible 'what if we're off' versions and re-runs baseline + knockout in each.

Versions (written before running; none is tuned to give a particular answer):
  reference      the published settings (should reproduce the screen)
  weaker_syn     every synapse 20% weaker   (w_syn 0.275 -> 0.22 mV)
  stronger_syn   every synapse 20% stronger (w_syn 0.275 -> 0.33 mV)
  flip_nt_a/b    10% of neurons (random, two different draws) get the opposite sign: excitatory <-> inhibitory,
                 standing in for wrong neurotransmitter predictions
  drop_weak      connections of 1-2 synapses removed (the ones most likely to be detection errors)
  inputs_a/b     only a random 75% of the sugar / water sensing neurons are stimulated (two draws)
'Needed' uses the screen's own rule: MN9 firing more than 20% lower than that version's own baseline.
30 repeats per condition, same seeds as the screen.

Usage: python3 run_stress.py <shiu repo dir> <lab repo dir> <out.json> [comma-separated versions]
"""
import json, sys, time, zlib
import numpy as np, pandas as pd
R, LAB, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ONLY = sys.argv[4].split(',') if len(sys.argv) > 4 else None
sys.path.insert(0, LAB + '/tools')
from lif_engine import Network

scr = json.load(open(LAB + '/discover/screen.json'))
RID = np.frombuffer(open(LAB + '/anatomy/celltypes/rootids.bin', 'rb').read(), dtype='<u8')
NEEDED = [(n['id'], n['label'], c) for n in scr['neurons'] for c in ('sugar', 'water') if n.get(c + '_needed')]
INPUT_IDS = {k: [int(RID[i]) for i in scr['inputs'][k]] for k in ('sugar', 'water')}
HZ = {'sugar': 100, 'water': 200}
MN9_IDS = [720575940660219265, 720575940618238523]

comp = pd.read_csv(R + '/Completeness_783.csv', index_col=0)
c = pd.read_parquet(R + '/Connectivity_783.parquet', columns=['Presynaptic_Index', 'Postsynaptic_Index', 'Excitatory x Connectivity'])
pre, post, w = c['Presynaptic_Index'].values, c['Postsynaptic_Index'].values, c['Excitatory x Connectivity'].values.astype(float)
del c
N = len(comp)

def build(kind, seed=0):
    ww = w.copy(); keep = np.ones(len(ww), bool)
    if kind == 'flip':
        flip = np.zeros(N, bool); flip[np.random.default_rng(seed).choice(N, N // 10, replace=False)] = True
        ww[flip[pre]] *= -1
    if kind == 'drop_weak':
        keep = np.abs(ww) > 2
    return Network(comp.index.values, pre[keep], post[keep], ww[keep], np.ones(N))

VERSIONS = [
    ('reference',    'base', 0, {}, None),
    ('weaker_syn',   'base', 0, {'w_syn': 0.22}, None),
    ('stronger_syn', 'base', 0, {'w_syn': 0.33}, None),
    ('flip_nt_a',    'flip', 1, {}, None),
    ('flip_nt_b',    'flip', 2, {}, None),
    ('drop_weak',    'drop_weak', 0, {}, None),
    ('inputs_a',     'base', 0, {}, 11),
    ('inputs_b',     'base', 0, {}, 12),
]
out = dict(written='2026-11-21, before any stress run', rule='needed = MN9 more than 20% below the same version\'s baseline; 30 repeats',
           neurons=[dict(id=i, label=l, cond=cnd) for i, l, cnd in NEEDED], versions={})
nets = {}
t0 = time.time()
for name, kind, seed, p, in_seed in VERSIONS:
    if ONLY and name not in ONLY: continue
    key = (kind, seed)
    if key not in nets:
        nets.clear(); nets[key] = build(kind, seed)
    net = nets[key]
    MN9 = net.idx(MN9_IDS)
    mn9 = lambda r: max(float(r[int(i)].mean()) for i in MN9)
    res = dict(baseline={}, knockouts={})
    for cond in ('sugar', 'water'):
        ids = INPUT_IDS[cond]
        if in_seed is not None:
            rng = np.random.default_rng(in_seed + (cond == 'water'))
            ids = list(rng.choice(ids, int(round(0.75 * len(ids))), replace=False))
        g = net.idx(ids); seedc = zlib.crc32(cond.encode())
        pp = dict(p, n_run=30)
        b = mn9(net.run([(g, HZ[cond])], seed=seedc, p=pp, record=MN9))
        res['baseline'][cond] = round(b, 2)
        for nid, label, cnd in NEEDED:
            if cnd != cond: continue
            k = mn9(net.run([(g, HZ[cond])], silence=net.idx([int(nid)]), seed=seedc, p=pp, record=MN9))
            drop = 1 - k / b if b > 0 else 0.0
            res['knockouts'][f'{nid}|{cond}'] = dict(mn9=round(k, 2), drop=round(drop, 4), needed=bool(b > 0 and k < 0.8 * b))
        print(name, cond, 'baseline', round(b, 1), f'[{time.time()-t0:.0f}s]', flush=True)
    out['versions'][name] = res
    json.dump(out, open(OUT, 'w'), indent=1)
# summary: in how many versions (excluding reference) is each neuron still needed?
others = [v for v, *_ in VERSIONS if v != 'reference' and v in out['versions']]
if ONLY: json.dump(out, open(OUT, 'w'), indent=1); print('done (part)', flush=True); sys.exit()
for nid, label, cnd in NEEDED:
    k = f'{nid}|{cnd}'
    held = [v for v in others if out['versions'][v]['knockouts'][k]['needed']]
    out.setdefault('summary', {})[k] = dict(label=label, cond=cnd, held=len(held), of=len(others),
        failed_in=[v for v in others if v not in held],
        drops={v: out['versions'][v]['knockouts'][k]['drop'] for v in out['versions']})
json.dump(out, open(OUT, 'w'), indent=1)
print('done', flush=True)

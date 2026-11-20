"""The Virtual Neuro Lab local server: serves the lab pages AND answers the "Ask Claude" panel.

    python3 tools/server.py            (start_skeleton.command does this for you)

Pages are served from this folder on http://localhost:8200.
POST /api/ask {"question": "...", "page": "/experiments/"} -> {"answer": "...", "sources": [...]}

How Claude answers (and what it may not do):
  * Claude (Anthropic) gets three tools: search_lab (the lab's own records, lab_index.json), search_pubmed and
    search_wikipedia. It must look in the lab first, and only use the web when the lab has no answer.
  * It cites what it used as [L12] (a lab record) or [W3] (a web source); the panel shows those as links.
  * It cannot run, change or score experiments, and it is told never to invent lab results.
  * Your API key stays on this computer: it is read from .env (ANTHROPIC_API_KEY=...) in this folder or in
    ~/Desktop/Fly Brain/.env, and the browser never sees it. Get a key at https://console.anthropic.com
    (billed per question; separate from a claude.ai subscription).
If the key, the 'anthropic' package or the internet is missing, the pages still work and the panel says Claude is offline.
"""
import json, os, re, sys, math, time, urllib.parse, urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
PORT = int(os.environ.get('FLYLAB_PORT', '8200'))
UA = 'FlyLab/1.0 (local research demo)'

# ---------------- key + model ----------------
for envf in (os.path.join(ROOT, '.env'), os.path.expanduser('~/Desktop/Fly Brain/.env')):
    if os.path.exists(envf):
        for line in open(envf):
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
MODEL = os.environ.get('CLAUDE_MODEL', 'claude-sonnet-5-5')
def log(msg): sys.stderr.write(msg + '\n'); sys.stderr.flush()
CLIENT, OFFLINE = None, ''
try:
    key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not key or key.startswith('your_'):
        raise RuntimeError('no ANTHROPIC_API_KEY found (.env)')
    import anthropic
    CLIENT = anthropic.Anthropic(api_key=key, timeout=120)
except Exception as e:
    OFFLINE = "the 'anthropic' package is missing (run: pip3 install anthropic)" if isinstance(e, ImportError) else str(e)

# ---------------- the lab's own records ----------------
INDEX = json.load(open(os.path.join(ROOT, 'lab_index.json'))) if os.path.exists(os.path.join(ROOT, 'lab_index.json')) else []
WORD = re.compile(r"[a-z0-9]+(?:[-'][a-z0-9]+)*")
def toks(s): return WORD.findall(s.lower())
DF = {}
for e in INDEX:
    e['_t'] = toks(e['title'] + ' ' + e['text']); e['_tt'] = set(toks(e['title']))
    for w in set(e['_t']): DF[w] = DF.get(w, 0) + 1
def search_lab(query, k=6):
    q = [w for w in toks(query) if len(w) > 1]
    scored = []
    for e in INDEX:
        s = sum((e['_t'].count(w) / (1 + 0.02 * len(e['_t'])) + (2 if w in e['_tt'] else 0)) * math.log(1 + len(INDEX) / (1 + DF.get(w, 0))) for w in q)
        if s > 0: scored.append((s, e))
    scored.sort(key=lambda x: -x[0])
    return [dict(id=e['id'], title=e['title'], page=e['page'], text=e['text'][:1500]) for _, e in scored[:k]]

# ---------------- the web (PubMed + Wikipedia, no key needed) ----------------
def get(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=20).read())
def search_pubmed(query, k=5):
    base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    ids = get(base + 'esearch.fcgi?' + urllib.parse.urlencode(dict(db='pubmed', term=query, retmode='json', retmax=k, sort='relevance')))['esearchresult']['idlist']
    if not ids: return []
    summ = get(base + 'esummary.fcgi?' + urllib.parse.urlencode(dict(db='pubmed', id=','.join(ids), retmode='json')))['result']
    out = []
    try:   # abstracts, so Claude reads what the paper found, not just its title
        txt = urllib.request.urlopen(urllib.request.Request(base + 'efetch.fcgi?' + urllib.parse.urlencode(dict(db='pubmed', id=','.join(ids), rettype='abstract', retmode='text')), headers={'User-Agent': UA}), timeout=20).read().decode('utf8', 'ignore')
        abstracts = [a.strip() for a in re.split(r'\n\n\d+\. ', '\n\n' + txt) if a.strip()]
    except Exception:
        abstracts = []
    for n, i in enumerate(ids):
        s = summ.get(i, {})
        au = (s.get('authors') or [{}])[0].get('name', '')
        out.append(dict(title=s.get('title', ''), url=f'https://pubmed.ncbi.nlm.nih.gov/{i}/',
                        source=f"{au} et al., {s.get('source', '')} {s.get('pubdate', '')[:4]}",
                        text=(abstracts[n] if n < len(abstracts) else '')[:1800]))
    return out
def search_wikipedia(query, k=3):
    r = get('https://en.wikipedia.org/w/rest.php/v1/search/page?' + urllib.parse.urlencode(dict(q=query, limit=k)))
    out = []
    for p in r.get('pages', []):
        try:
            ex = get('https://en.wikipedia.org/api/rest_v1/page/summary/' + urllib.parse.quote(p['key']))['extract']
        except Exception:
            ex = re.sub('<[^>]+>', '', p.get('excerpt', ''))
        out.append(dict(title=p['title'], url='https://en.wikipedia.org/wiki/' + urllib.parse.quote(p['key']), source='Wikipedia', text=ex[:1500]))
    return out

def _tool(name, desc):
    return {'name': name, 'description': desc, 'input_schema': {'type': 'object', 'properties': {'query': {'type': 'string'}}, 'required': ['query']}}
TOOLS = [
    _tool('search_lab', "Search The Virtual Neuro Lab's own records: experiments and their results, rules, calibration, the Discovery Screen predictions, brain regions, cell types, the flies, the worm, Parkinson's. Always try this first."),
    _tool('search_pubmed', 'Search published biology papers (PubMed) when the lab has no answer. Returns titles, links and abstracts.'),
    _tool('search_wikipedia', 'Search Wikipedia for general background when the lab has no answer.'),
]
SYSTEM = """You are Claude, made by Anthropic, the guide inside The Virtual Neuro Lab, a virtual neuroscience lab that runs experiments on simulated fruit fly brains wired from real connectome scans.
Rules:
1. Always call search_lab first. If the lab's records answer the question, answer from them and cite each fact as [L<number>] using the ids you were given.
2. Only if the lab has no answer (or the visitor asks about the wider world), call search_pubmed and/or search_wikipedia, and cite each fact as [W<number>]. Say plainly that this part comes from the web, not from the lab.
3. Never invent lab results, numbers, experiments or papers. If neither the lab nor the web sources say it, say you don't know.
4. You cannot run, change or score experiments. Simulation results are model predictions, not facts about real flies; say so when it matters.
5. Answer in plain, friendly words for someone who is not a scientist. Keep it short: 2 to 6 sentences unless asked for more.
6. Talk about what the lab does and has found. If the visitor asks about something the lab does not do yet (other experiments, other flies, drugs, other senses), say briefly that it is in progress or being worked on; do not list the lab's limitations unprompted."""

def ask(question, page=''):
    if not CLIENT:
        return dict(answer=f'Claude is offline right now: {OFFLINE}. The rest of the lab works normally.', sources=[], offline=True)
    sources, nW = {}, [0]
    msgs = [{'role': 'user', 'content': f'(The visitor is on the page: {page})\n{question}'}]
    for _ in range(6):
        r = CLIENT.messages.create(model=MODEL, max_tokens=1500, system=SYSTEM, tools=TOOLS, messages=msgs)
        uses = [b for b in r.content if b.type == 'tool_use']
        log(f"  step: stop={r.stop_reason} tools={[u.name for u in uses]} usage={getattr(r, 'usage', None)}")
        if r.stop_reason != 'tool_use':
            ans = ''.join(b.text for b in r.content if b.type == 'text').strip()
            if r.stop_reason == 'max_tokens' or not ans:
                ans = (ans + ' …' if ans else '') + "\n(Claude ran out of room before finishing this answer. Please ask again, maybe a bit more narrowly.)"
            used = sorted(set(re.findall(r'\[([LW]\d+)\]', ans)), key=lambda s: (s[0], int(s[1:])))
            return dict(answer=ans, sources=[dict(id=u, **sources[u]) for u in used if u in sources], model=MODEL)
        msgs.append({'role': 'assistant', 'content': [b.model_dump(exclude_none=True) for b in r.content]})
        results = []
        for u in uses:
            try:
                q = (u.input or {}).get('query', question)
                if u.name == 'search_lab':
                    res = search_lab(q)
                    for x in res: sources[x['id']] = dict(kind='lab', title=x['title'], url='/' + x['page'])
                else:
                    raw = search_pubmed(q) if u.name == 'search_pubmed' else search_wikipedia(q)
                    res = []
                    for x in raw:
                        nW[0] += 1; wid = f'W{nW[0]}'
                        sources[wid] = dict(kind='web', title=x['title'], url=x['url'], where=x['source'])
                        res.append(dict(id=wid, **x))
            except Exception as e:
                res = {'error': f'search failed: {e!r}'[:300]}
            log(f"  tool {u.name}({u.input}) -> {len(res) if isinstance(res, list) else res}")
            results.append({'type': 'tool_result', 'tool_use_id': u.id, 'content': json.dumps(res, ensure_ascii=False)})
        msgs.append({'role': 'user', 'content': results})
    return dict(answer="Sorry, I couldn't finish looking that up. Please try asking it a different way.", sources=[])

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # always serve the latest lab files (no stale styles after an update)
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    def do_POST(self):
        if self.path != '/api/ask':
            return self.send_error(404)
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
            q = str(body.get('question', '')).strip()[:1000]
            log(f'Q: {q}')
            out = ask(q, str(body.get('page', ''))[:200]) if q else dict(answer='Ask me anything about the lab.', sources=[])
        except Exception as e:
            log(f'  ERROR {type(e).__name__}: {e}')
            out = dict(answer=f'Claude ran into a problem ({type(e).__name__}). Please try again in a moment.', sources=[], error=str(e)[:300])
        data = json.dumps(out, ensure_ascii=False).encode()
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(data)))
        self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path == '/api/status':
            data = json.dumps(dict(online=bool(CLIENT), model=MODEL if CLIENT else None, reason=OFFLINE)).encode()
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers(); return self.wfile.write(data)
        if any(seg.startswith('.') for seg in urllib.parse.urlparse(self.path).path.split('/')):
            return self.send_error(404)          # never serve .env or other hidden files
        return super().do_GET()
    def log_message(self, fmt, *a):
        if a and '/api/' in str(a[0]): sys.stderr.write('%s\n' % (fmt % a))

if __name__ == '__main__':
    print(f'The Virtual Neuro Lab on http://localhost:{PORT}  ·  Ask Claude: ' + (f'online ({MODEL})' if CLIENT else f'offline ({OFFLINE})'))
    ThreadingHTTPServer(('127.0.0.1', PORT), partial(Handler, directory=ROOT)).serve_forever()

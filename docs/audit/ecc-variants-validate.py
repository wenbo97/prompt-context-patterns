"""Validate the live research ledger without asserting unread coverage complete."""
import pathlib,json,hashlib,collections,re,subprocess
out=pathlib.Path(__file__).resolve().parent;b=pathlib.Path('D:/Projects/open-skills/affaan-m/ECC')
s=json.loads((out/'harvest-ecc-variants.json').read_text(encoding='utf8'))
inventory=json.loads((out/'source-inventory.json').read_text(encoding='utf8'))
repo=next(r for r in inventory['repositories'] if r['repo']==s['repo'])
files={f['path']:f for f in repo['files']}
canon=json.loads((out/'harvest-ecc.json').read_text(encoding='utf8'))
keys={c['key'] for c in canon['candidates']}|{c['key'] for c in s['candidates']}
errors=[]
head=subprocess.check_output(['git','-C',str(b),'rev-parse','HEAD'],text=True).strip()
if head!=s['commit']:errors.append('source HEAD differs')
expected={p for p in files if any(p.startswith(h+'/') for h in s['partition']['harnesses']) or any(p.startswith('docs/'+locale+'/') for locale in s['partition']['locales'])}
actual={r['path'] for r in s['coverage']}
if expected!=actual:errors.append('Git-authoritative assigned paths mismatch')
if len(actual)!=len(s['coverage']):errors.append('duplicate coverage path')
for r in s['coverage']:
    for field in ('path','git_blob','hash','classification','disposition','depth','reason','candidate_keys'):
        if field not in r:errors.append(r['path']+' missing '+field)
    if not re.fullmatch('[0-9a-f]{40}',r['git_blob']):errors.append(r['path']+' invalid blob')
    if not re.fullmatch('[0-9a-f]{64}',r['hash']):errors.append(r['path']+' invalid hash')
    if r['disposition'] not in ('pending','analyzed','duplicate','excluded'):errors.append(r['path']+' invalid disposition')
    if set(r['candidate_keys'])-keys:errors.append(r['path']+' unresolved candidate key')
    if r['disposition']=='pending' and r['depth'] not in ('pending','inventory-only'):errors.append(r['path']+' pending depth contradiction')
    if r['disposition']=='duplicate':
        target=r['duplicate_of']
        digest=hashlib.sha256((b/target).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
        if digest!=r['normalized_hash']:errors.append(r['path']+' exact duplicate hash mismatch')
    if 'body_duplicate_of' in r:
        def body(path):
            lines=(b/path).read_text(encoding='utf-8-sig').replace('\r\n','\n').splitlines()
            if lines and lines[0]=='---':
                end=next(i for i,line in enumerate(lines[1:],1) if line=='---');lines=lines[end+1:]
            return '\n'.join(lines).strip()
        value=body(r['path'])
        if value!=body(r['body_duplicate_of']) or hashlib.sha256(value.encode()).hexdigest()!=r['body_hash']:errors.append(r['path']+' body mismatch')
    for evidence in r.get('proof',[]):
        proof_path=evidence['path'];proof_lines=(b/proof_path).read_text(encoding='utf-8-sig').splitlines()
        if evidence['commit']!=head or not 1<=evidence['start_line']<=evidence['end_line']<=len(proof_lines):errors.append(r['path']+' proof range')
        proof_url=f'https://github.com/{s["repo"]}/blob/{head}/{proof_path}#L{evidence["start_line"]}-L{evidence["end_line"]}'
        if evidence['url']!=proof_url:errors.append(r['path']+' proof URL')
for c in s['candidates']:
    for language in ('en','zh'):
        if set(c['content'][language])!=set(('description','scenario','mechanism','bad','good','why','expected','boundaries')):errors.append(c['key']+' field mismatch')
        if any(not isinstance(v,str) or not v.strip() for v in c['content'][language].values()):errors.append(c['key']+' empty content')
    scores=c['scores']
    if any(scores.get(k)!=2 for k in ('scenario','mechanism','contrast')) or sum(scores.values())<8:errors.append(c['key']+' scores')
    for source in c['sources']:
        path=source['path'];lines=(b/path).read_text(encoding='utf-8-sig').splitlines()
        if source['commit']!=head or not 1<=source['start_line']<=source['end_line']<=len(lines):errors.append(c['key']+' source range')
        expected_url=f'https://github.com/{s["repo"]}/blob/{head}/{path}#L{source["start_line"]}-L{source["end_line"]}'
        if source['url']!=expected_url:errors.append(c['key']+' source URL')
counts=collections.Counter(r['disposition'] for r in s['coverage'])
if counts['pending'] and s['summary']['status']=='complete':errors.append('false complete status')
result={'valid':not errors,'errors':errors,'total':len(actual),'counts':dict(counts),'candidate_count':len(s['candidates']),'source_commit':head,'coverage_complete':counts['pending']==0,'note':'Validation checks data/evidence integrity; it does not replace semantic reading or execute source examples.'}
(out/'ecc-variants-validation.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
print(json.dumps(result,ensure_ascii=False));raise SystemExit(bool(errors))

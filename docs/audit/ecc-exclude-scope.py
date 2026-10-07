"""Inspect artifact types without executing upstream content or claiming semantic review."""
import csv,hashlib,json,pathlib,re,struct,subprocess,tomllib,xml.etree.ElementTree as ET
out=pathlib.Path(__file__).parent
root=pathlib.Path('D:/Projects/open-skills/affaan-m/ECC')
commit='ef648e01899ba3e8dc6371642deaaf64b4477775'
repo=next(r for r in json.loads((out/'source-inventory.json').read_text(encoding='utf-8'))['repositories'] if r['repo']=='affaan-m/ECC')
records=[]
def blob(row):
    try: data=(root/row['path']).read_bytes()
    except OSError: data=b''
    hashed=data if row['binary'] else data.replace(b'\r\n',b'\n')
    if hashlib.sha256(hashed).hexdigest()!=row['hash']:
        data=subprocess.check_output(['git','show',f"{commit}:{row['path']}"],cwd=root)
    return data
for row in repo['files']:
    p=row['path']
    if not row['binary']: continue
    raw=blob(row)
    kind=None
    proof={'blob':row['blob'],'bytes':len(raw),'content_sha256':hashlib.sha256(raw).hexdigest(),'inspection':'Binary format signature and container metadata; no OCR or visual-semantic claim.'}
    if raw.startswith(b'\x89PNG\r\n\x1a\n'):
        kind='PNG';proof['dimensions']=list(struct.unpack('>II',raw[16:24]))
    elif raw.startswith(b'\xff\xd8\xff'): kind='JPEG'
    elif raw.startswith((b'GIF87a',b'GIF89a')):
        kind='GIF';proof['dimensions']=list(struct.unpack('<HH',raw[6:10]))
    elif raw[4:8]==b'ftyp':kind='MP4'
    if not kind:raise ValueError('Unclassified binary artifact: '+p)
    role='brand/sponsor or guide illustration' if p.startswith('assets/') else 'plan-canvas visual demo asset'
    records.append({'path':p,'hash':row['hash'],'classification':'visual-supporting-asset','disposition':'excluded',
      'reason':f'Inspected actual {kind} signature and content identity: {role}. Excluded from textual skill/prompt/context mechanism extraction; no claim of visual/OCR review, executable workflow, measured efficacy or original behavioral trace is made. Accompanying textual guides and implementations remain separately reviewed or pending.',
      'proof':proof})
for row in repo['files']:
    p=row['path']
    if p in ['package-lock.json','yarn.lock','ecc2/Cargo.lock']:
        raw=blob(row);body=raw.decode('utf-8').replace('\r\n','\n')
        proof={'blob':row['blob'],'hash':row['hash'],'bytes':len(raw),'header':body.splitlines()[:5]}
        if p=='package-lock.json':
            data=json.loads(body);proof['root_keys']=list(data)
            proof['package_count']=len(data['packages'])
            proof['package_field_names']=sorted({k for q in data['packages'].values() for k in q})
        elif p.endswith('Cargo.lock'):
            data=tomllib.loads(body);proof['root_keys']=list(data)
            proof['package_count']=len(data['package'])
            proof['package_field_names']=sorted({k for q in data['package'] for k in q})
        else:
            proof['entry_field_names']=sorted({s.strip().split(':',1)[0] for s in body.splitlines() if re.match(r'^  [A-Za-z][A-Za-z0-9]*:',s)})
        records.append({'path':p,'hash':row['hash'],'classification':'generated-dependency-lock','disposition':'excluded',
          'reason':'Inspected generated-lock header, complete parsed structure/entry fields and fixed content identity. Values describe dependency versions, resolutions, integrity, feature/platform metadata or executable entry paths; no agent-facing prompt, skill workflow or evaluation contract is authored here. Excluded as dependency-resolution data; no package security, successful install or current API behavior is inferred. Package scripts and installer/hook contracts are separate sources.', 'proof':proof})
    elif p.startswith('assets/') and p.endswith('.svg'):
        raw=blob(row);tree=ET.fromstring(raw)
        tags=sorted({e.tag.split('}')[-1] for e in tree.iter()})
        text=[e.text.strip() for e in tree.iter() if e.text and e.text.strip()]
        proof={'blob':row['blob'],'hash':row['hash'],'root_tag':tree.tag,'attributes':dict(tree.attrib),'element_types':tags,'text_nodes':text}
        if 'script' in tags:raise ValueError('SVG script needs separate review: '+p)
        records.append({'path':p,'hash':row['hash'],'classification':'vector-brand-asset','disposition':'excluded',
          'reason':'Inspected complete XML structure and text nodes: vector icon/logo/hero rendering with geometry, style, clipping and brand labels, without a script element. Excluded from agent instruction/workflow extraction as presentation data; not a claim of visual-quality or sanitization verification.', 'proof':proof})
    elif p=='assets/star-history-data.tsv':
        raw=blob(row);rows=list(csv.reader(raw.decode('utf-8').splitlines(),delimiter='\t'))
        records.append({'path':p,'hash':row['hash'],'classification':'historical-chart-data','disposition':'excluded',
          'reason':'Inspected complete two-column TSV structure: timestamp/star-count observations without a header row. Historical repository chart data, not skill/prompt/context/workflow instructions. No current popularity ranking, measured skill quality or causal efficacy is inferred from the time series.',
          'proof':{'blob':row['blob'],'hash':row['hash'],'rows':len(rows),'first_row':rows[0],'column_counts':sorted({len(r) for r in rows})}})
(out/'ecc-exclusions.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'scope_excluded':len(records),'formats':{k:sum(r['proof'].get('dimensions') is not None for r in records if k in r['reason']) for k in ['PNG','GIF']}}))

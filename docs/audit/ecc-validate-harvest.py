"""Static artifact contract checks; never executes source-repository code."""
import hashlib,json,pathlib,subprocess
OUT=pathlib.Path(__file__).parent
ROOT=pathlib.Path('D:/Projects/open-skills/affaan-m/ECC')
data=json.loads((OUT/'harvest-ecc.json').read_text(encoding='utf-8'))
source=next(x for x in json.loads((OUT/'source-inventory.json').read_text(encoding='utf-8'))['repositories'] if x['repo']=='affaan-m/ECC')
files={x['path']:x for x in source['files']}
assert data['commit']==source['commit']
keys=set(); spans=0
fields={'description','scenario','mechanism','bad','good','why','expected','boundaries'}
for candidate in data['candidates']:
    assert candidate['key'] not in keys, candidate['key']
    keys.add(candidate['key'])
    assert candidate['name_en'] and candidate['name_zh']
    for locale in ('en','zh'):
        assert set(candidate['content'][locale])==fields
        assert all(isinstance(x,str) and x.strip() for x in candidate['content'][locale].values())
    assert set(candidate['scores'])=={'scenario','mechanism','contrast','observable','boundaries'}
    assert all(type(x)==int and 0<=x<=2 for x in candidate['scores'].values())
    if candidate['decision']=='active':
        assert sum(candidate['scores'].values())>=8
        assert all(candidate['scores'][f]==2 for f in ('scenario','mechanism','contrast'))
    for pointer in candidate['sources']:
        assert pointer['repo']==data['repo'] and pointer['commit']==data['commit']
        assert pointer['role']=='observed-example'
        raw=subprocess.check_output(['git','show',f"{data['commit']}:{pointer['path']}"],cwd=ROOT)
        lines=raw.decode('utf-8').splitlines()
        assert 1<=pointer['start_line']<=pointer['end_line']<=len(lines), pointer
        assert pointer['url']==f"https://github.com/{data['repo']}/blob/{data['commit']}/{pointer['path']}#L{pointer['start_line']}-L{pointer['end_line']}"
        spans+=1
paths=set()
for row in data['coverage']:
    assert row['path'] not in paths
    paths.add(row['path'])
    assert row['hash']==files[row['path']]['hash']
    assert row['reason'] and set(row['candidate_keys'])<=keys
    assert row['disposition'] in ('analyzed','duplicate','excluded')
    if row['disposition']=='duplicate':
        assert files[row['duplicate_of']]['hash']==row['hash']
print(json.dumps({'candidates':len(keys),'pinned_ranges':spans,'completed_paths':len(paths),'canonical_bodies':data['summary']['canonical_full'],'status':data['status']},indent=2))

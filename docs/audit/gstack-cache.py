"""Build reproducible frozen-source heading blocks; this is inventory, not review."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--references', action='store_true')
a = p.parse_args()
root = r'D:\A_Projects\open-skills\garrytan\gstack'
commit = 'f30b7b788a210d217ea3125bf3001b29cbc2a463'
cache_path = Path('.tools/gstack/blocks.json')
cache = json.loads(cache_path.read_text('utf-8')) if cache_path.exists() else {'repo':'garrytan/gstack','commit':commit,'files':[],'blocks':{}}
existing = {f['path'] for f in cache['files']}
paths = subprocess.check_output(['git','-C',root,'ls-tree','-r','--name-only','-z',commit]).decode('utf-8').split('\0')
selected = [s for s in paths if re.search(r'(^|/)SKILL\.md(?:\.tmpl)?$',s)]
if a.references:
    selected += [s for s in paths if (s.endswith('.md') or s.endswith('.md.tmpl')) and s not in existing]
for name in dict.fromkeys(selected):
    if name in existing:
        continue
    blob = subprocess.check_output(['git','-C',root,'show',commit+':'+name]).decode('utf-8').replace('\r\n','\n')
    lines = blob.splitlines(True)
    starts = sorted(set([0] + [i for i,line in enumerate(lines) if re.match(r'^#{1,6}\s',line)] + [len(lines)]))
    hashes = []
    for start,end in zip(starts,starts[1:]):
        text = ''.join(lines[start:end])
        if not text:
            continue
        h = hashlib.sha256(text.encode()).hexdigest()
        hashes.append(h)
        item = cache['blocks'].setdefault(h,{'text':text,'locations':[]})
        item['locations'].append({'path':name,'start':start+1,'end':end})
    cache['files'].append({'path':name,'blocks':hashes,'lines':len(lines),'hash':hashlib.sha256(blob.encode()).hexdigest()})
cache_path.parent.mkdir(parents=True,exist_ok=True)
cache_path.write_text(json.dumps(cache,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps({'files':len(cache['files']),'unique_blocks':len(cache['blocks']),'added_files':len(cache['files'])-len(existing)}))

"""Cache frozen method-bearing code for reading, never execute upstream code."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('selection')
a = p.parse_args()
root = r'D:\A_Projects\open-skills\garrytan\gstack'
commit = 'f30b7b788a210d217ea3125bf3001b29cbc2a463'
cache_path = Path('.tools/gstack/blocks.json')
cache = json.loads(cache_path.read_text('utf-8'))
existing = {f['path'] for f in cache['files']}
paths = subprocess.check_output(['git', '-C', root, 'ls-tree', '-r', '--name-only', '-z', commit]).decode().split('\0')
added = []
for name in paths:
    if not name or name in existing or not re.search(a.selection, name):
        continue
    blob = subprocess.check_output(['git', '-C', root, 'show', commit + ':' + name]).decode('utf-8').replace('\r\n', '\n')
    lines = blob.splitlines(True)
    hashes = []
    for start in range(0, len(lines), 60):
        end = min(start + 60, len(lines))
        value = ''.join(lines[start:end])
        h = hashlib.sha256(value.encode()).hexdigest()
        hashes.append(h)
        cache['blocks'].setdefault(h, {'text': value, 'locations': []})['locations'].append({'path': name, 'start': start + 1, 'end': end})
    cache['files'].append({'path': name, 'blocks': hashes, 'lines': len(lines), 'hash': hashlib.sha256(blob.encode()).hexdigest()})
    added.append({'path': name, 'lines': len(lines)})
cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), 'utf-8')
print(json.dumps({'added_files': len(added), 'added_lines': sum(f['lines'] for f in added), 'total_files': len(cache['files']), 'total_blocks': len(cache['blocks'])}))

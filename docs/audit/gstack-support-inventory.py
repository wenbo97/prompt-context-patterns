"""Frozen byte/type inventory for scoped support review; never semantic completion."""
import base64
import hashlib
import json
import subprocess
from pathlib import Path

root = r'D:\A_Projects\open-skills\garrytan\gstack'
commit = 'f30b7b788a210d217ea3125bf3001b29cbc2a463'
report = json.loads(Path('docs/audit/harvest-gstack.json').read_text('utf-8'))
paths = [r['path'] for r in report['coverage'] if r['disposition'] == 'pending']
requests = ''.join(commit + ':' + p + '\n' for p in paths).encode()
raw = subprocess.check_output(['git', '-C', root, 'cat-file', '--batch'], input=requests)
at = 0
rows = []
for name in paths:
    end = raw.index(b'\n', at)
    oid, kind, size = raw[at:end].split()
    size = int(size)
    body = raw[end + 1:end + 1 + size]
    assert raw[end + 1 + size:end + 2 + size] == b'\n'
    at = end + 2 + size
    row = {'path': name, 'git_oid': oid.decode(), 'bytes': size, 'sha256': hashlib.sha256(body).hexdigest()}
    try:
        value = body.decode('utf-8')
        if '\0' in value:
            raise ValueError('binary NUL')
        row.update(kind='text', text=value)
    except (UnicodeDecodeError, ValueError):
        row.update(kind='binary', magic_hex=body[:32].hex(), base64=base64.b64encode(body).decode())
    rows.append(row)
dest = Path('.tools/gstack/support-blobs.json')
dest.write_text(json.dumps(rows, ensure_ascii=False), 'utf-8')
print(json.dumps({'pending_inputs':len(rows),'text':sum(r['kind']=='text' for r in rows),'binary':sum(r['kind']=='binary' for r in rows),'total_bytes':sum(r['bytes'] for r in rows)}))

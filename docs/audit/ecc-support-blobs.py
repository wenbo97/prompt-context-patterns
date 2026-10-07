"""Freeze pending support content as private analysis data; never execute source."""
import json,pathlib,subprocess,hashlib,collections
ROOT=pathlib.Path('D:/Projects/open-skills/affaan-m/ECC')
OUT=pathlib.Path('D:/Projects/prompt-context-patterns-refresh')
COMMIT='ef648e01899ba3e8dc6371642deaaf64b4477775'
ledger=json.loads((OUT/'docs/audit/ecc-review-ledger.json').read_text(encoding='utf-8'))
variant=tuple('docs/'+locale+'/' for locale in ('ja-JP','zh-CN','zh-TW','es','tr','ko-KR','pt-BR','de-DE','pl','ru','th','uk-UA','ur','vi-VN'))+('.agents/','.cursor/','.kiro/','.opencode/')
pending=[r['path'] for r in ledger['pending'] if not r['path'].startswith(variant)]
inventory={r['path']:r for r in json.loads((OUT/'docs/audit/ecc-inventory.json').read_text(encoding='utf-8'))}
rows=[]
for p in pending:
    raw=subprocess.check_output(['git','-C',str(ROOT),'show',COMMIT+':'+p])
    try:text=raw.decode('utf-8').replace('\r\n','\n')
    except UnicodeDecodeError:text=None
    expected=inventory[p]['hash']
    digest=hashlib.sha256((text.encode() if text is not None else raw)).hexdigest()
    assert digest==expected,(p,digest,expected)
    rows.append({'path':p,'sha256':digest,'bytes':len(raw),'lines':inventory[p]['lines'],'text':text,'magic_hex':raw[:24].hex() if text is None else None})
private=OUT/'.tools/ecc';private.mkdir(parents=True,exist_ok=True)
(private/'support-blobs.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'files':len(rows),'extensions':dict(collections.Counter(pathlib.PurePosixPath(r['path']).suffix or '[none]' for r in rows))}))

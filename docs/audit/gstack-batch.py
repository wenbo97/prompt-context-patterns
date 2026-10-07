"""Read-only source block display; mark only a batch actually read in full."""
import argparse
import difflib
import hashlib
import json
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('group', nargs='?', default='autoplan,plan-eng-review,plan-tune,spec')
p.add_argument('--mark-last', action='store_true')
p.add_argument('--cap', type=int, default=22000)
p.add_argument('--deltas', action='store_true')
p.add_argument('--paragraphs', action='store_true')
p.add_argument('--prefix', default='')
a = p.parse_args()
state_path = Path('docs/audit/gstack-review-state.json')
state = json.loads(state_path.read_text('utf-8'))
cache = json.loads(Path('.tools/gstack/blocks.json').read_text('utf-8'))
batch_path = Path('.tools/gstack/current-batch.json')
if a.mark_last:
    state['read_blocks'] = sorted(set(state['read_blocks']) | set(json.loads(batch_path.read_text('utf-8'))))
    evidence_path = Path('.tools/gstack/current-deltas.json')
    if evidence_path.exists():
        state.setdefault('delta_reads', {}).update(json.loads(evidence_path.read_text('utf-8')))
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', 'utf-8')
read = set(state['read_blocks']) | set(state['parameter_block_aliases'])
groups = set(a.group.split(','))
todo = []
for f in cache['files']:
    if a.prefix and not f['path'].startswith(a.prefix):
        continue
    if '*' not in groups and f['path'].split('/')[0] not in groups:
        continue
    for h in f['blocks']:
        if h not in read and h not in todo:
            todo.append(h)
out = []
chosen = []
size = 0
delta_evidence = {}
paragraph_index = {}
def paragraphs(value):
    return list(re.finditer(r'[\s\S]+?(?:\n\n|\Z)', value))
if a.paragraphs:
    for rh in state['read_blocks']:
        for m in paragraphs(cache['blocks'][rh]['text']):
            value = m.group()
            if len(value) >= 100:
                paragraph_index.setdefault(value, (rh, m.start(), m.end()))
for h in todo:
    b = cache['blocks'][h]
    loc = next((l for l in b['locations'] if (l['path'].split('/')[0] in groups or '*' in groups) and (not a.prefix or l['path'].startswith(a.prefix))), b['locations'][0])
    text = f"\nBLOCK {h}\n{loc}\n{b['text']}"
    if a.paragraphs:
        parts = []
        matched = []
        for m in paragraphs(b['text']):
            value = m.group()
            prior = paragraph_index.get(value)
            if prior:
                rh, start, end = prior
                assert cache['blocks'][rh]['text'][start:end] == value
                parts.append(f"[EXACT PREVIOUSLY READ PARAGRAPH {rh[:12]} chars {start}:{end}; begins {value.splitlines()[0]}]\n")
                matched.append({'start':m.start(),'end':m.end(),'base':rh,'base_start':start,'base_end':end,'sha256':hashlib.sha256(value.encode()).hexdigest()})
            else:
                parts.append(value)
        shortened = ''.join(parts)
        if matched and len(shortened) < len(b['text']):
            text = f"\nBLOCK {h}\n{loc}\nEvery omitted paragraph is byte-identical to the named previously read span; all other text follows in original order.\n{shortened}"
            delta_evidence[h] = {'kind':'exact-paragraph-spans','spans':matched,'review':'All unmatched text displayed in original order; matching spans verified exactly against already reviewed source.'}
    if a.deltas and len(b['text']) > 450 and h not in delta_evidence:
        nearest = None
        score = .68
        for rh in state['read_blocks']:
            prior = cache['blocks'][rh]['text']
            if not .55 < len(prior) / len(b['text']) < 1.8:
                continue
            matcher = difflib.SequenceMatcher(None, prior.splitlines(True), b['text'].splitlines(True), autojunk=False)
            if matcher.quick_ratio() <= score:
                continue
            ratio = matcher.ratio()
            if ratio > score:
                nearest, score = rh, ratio
        if nearest:
            prior = cache['blocks'][nearest]
            delta = ''.join(difflib.unified_diff(prior['text'].splitlines(True), b['text'].splitlines(True), fromfile=nearest, tofile=h, n=2))
            if len(delta) < len(b['text']):
                text = f"\nBLOCK {h}\n{loc}\nEXACT-LINE DELTA from already-read {nearest} {prior['locations'][0]}; unchanged lines are byte-identical.\n{delta}"
                delta_evidence[h] = {'base': nearest, 'diff_sha256': hashlib.sha256(delta.encode()).hexdigest(), 'review': 'Every changed line displayed; every omitted line equals the previously reviewed base.'}
    if size + len(text) > a.cap and chosen:
        break
    out.append(text)
    chosen.append(h)
    size += len(text)
batch_path.write_text(json.dumps(chosen), 'utf-8')
Path('.tools/gstack/current-deltas.json').write_text(json.dumps({h: delta_evidence[h] for h in chosen if h in delta_evidence}), 'utf-8')
print(f'GROUP {a.group}; unread {len(todo)}; displayed {len(chosen)}; chars {size}')
print(''.join(out))

"""Persist exclusions only after the complete four-locale community texts were read."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=[]
for locale in ('ja-JP','zh-CN','es','tr'):
    conduct='Read entire localized human community conduct/impact ladder, privacy, representation and attribution policy. This governs human moderation and does not specify an agent prompt/context/tool mechanism; excluded from pattern extraction, not from tracked coverage.'
    if locale=='zh-CN':conduct+=' Report-contact sentence leaves email blank; do not invent a destination.'
    rows.append({'path':f'docs/{locale}/CODE_OF_CONDUCT.md','disposition':'excluded','depth':'full-nonpattern-text','reason':conduct})
    rows.append({'path':f'docs/{locale}/SPONSORING.md','disposition':'excluded','depth':'full-nonpattern-text','reason':'Read full sponsorship pricing/benefit/scope, adoption/reporting metric list and business-metrics pointer. Human commercial/marketing document without an agent method; no current pricing, faster delivery or reliability claim inferred. Pointer targets untranslated business docs outside this partition.'})
    sponsor='Read full sponsor tiers, adoption narrative and directory. Human marketing/commercial acknowledgement without a prompt/context/tool mechanism; excluded from pattern extraction. Adoption/support/weekly-release claims and prices are frozen narration, not measured efficacy or current facts.'
    if locale=='es':sponsor+=' Spanish version has named sponsor/historic pricing and May14 update unlike older February sibling copies; this is content drift, not an extra method.'
    else:sponsor+=' Older February-sync prices/benefits differ from newer canonical/Spanish table; not treated as current sponsorship recommendation.'
    rows.append({'path':f'docs/{locale}/SPONSORS.md','disposition':'excluded','depth':'full-nonpattern-text','reason':sponsor})
(out/'ecc-variants-community-decisions.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())

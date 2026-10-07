"""Close exactly identical bodies only after wrapper descriptions were read."""
import json,pathlib
out=pathlib.Path(__file__).resolve().parent
matches=json.loads((out/'ecc-variants-body-matches.json').read_text(encoding='utf8'))
specific={
'ecc-tools-cost-audit':'Translated description claims generic prompt-token efficiency; canonical trigger is evidence-first ECC Tools billing/runaway PR/quota/model/job leakage audit. Material discovery mismatch.',
'foundation-models-on-device':'Translated description adds quantization/optimization/privacy scope; canonical trigger targets Apple FoundationModels guided generation/tools/snapshots on iOS26+. Do not infer unsupported quantization support.',
'frontend-design-direction':'Generic translated aesthetics/design-language description omits task/product-specific production UI trigger boundary.',
'frontend-slides':'Generic frontend-presentation description omits concrete HTML-animation/PPT conversion and user visual-taste exploration triggers.',
'gan-style-harness':'Japanese wrapper misleadingly advertises image generation/metrics; identical body is autonomous application Generator-Evaluator iteration, not an image GAN workflow.',
'google-workspace-ops':'Wrapper advertises Workspace API/Sheets/Gmail automation while canonical body covers Drive/Docs/Sheets/Slides documents; Gmail/API scope is not established by this body.',
'hermes-imports':'Wrapper misleadingly advertises data import/mapping/integrity; actual unchanged body sanitizes private Hermes operator workflows into public ECC artifacts.',
'healthcare-eval-harness':'Generic translated AI-model/clinical/regulation verification description loses concrete patient-safety deployment-blocking application gate.',
'hipaa-compliance':'Generic HIPAA security implementation description loses explicit US covered-entity/BAA/breach framing; copied body is an entrypoint, not compliance certification.',
'hookify-rules':'Generic automatic-hook implementation description omits warn-vs-block, event/predicate and YAML rule-authoring syntax boundary.',
'laravel-plugin-discovery':'Wrapper adds dependency resolution/provider integration; copied body only discovers/evaluates packages through LaraPlugins.io MCP, not installation or resolution proof.',
}
rows=[]
for m in matches:
    name=m['path'].split('/')[-2]
    note=specific.get(name,'Description is a broader Japanese domain synopsis, omitting concrete canonical activation cases; no extra body instruction or method added.')
    if name=='ecc-guide':note='Description retains live-repository reading before answer; detailed install/reset/task-routing activation cases are compressed.'
    if name in ('energy-procurement','inventory-demand-planning'):note+=' Multiline plain description continues without a YAML scalar marker and may parse differently; claimed expert experience is source narration, not validated effectiveness. File declares Apache-2.0 separately from root MIT.'
    rows.append({'path':m['path'],'depth':'exact-body-plus-full-wrapper-semantic','body_duplicate_of':m['counterpart'],'body_hash':m['body_hash'],'wrapper_review':'complete','reason':'Full LF/outer-whitespace-normalized body exactly equals canonical Git file; body analysis belongs to canonical reviewer. Complete wrapper semantic comparison: '+note+' Metadata origin/version flattening differs from canonical nested metadata; no runtime discovery guarantee. No translated-body equivalence inferred.'})
(out/'ecc-variants-body-decisions.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())

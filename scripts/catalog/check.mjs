import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { ROOT, readJson, validateCatalog, writeText } from './lib.mjs';
import { REVIEW_KINDS, validateFileOutcome } from './review-coverage.mjs';
import { sourceRoot, sourceLineCount } from './sources.mjs';
import { validateDecisions } from './decisions.mjs';

const allowPending = process.argv.includes('--allow-pending'); const verifySources = process.argv.includes('--sources');
const catalog = readJson('_data/patterns.json'); const errors = validateCatalog(catalog);
for (const p of catalog.filter(p => p.status === 'active')) for (const lang of ['en', 'zh']) {
  const file = path.join(ROOT, '_patterns', `${p.id}.${lang}.md`);
  if (!fs.existsSync(file)) { errors.push(`${p.id}/${lang}: body missing`); continue; }
  const body = fs.readFileSync(file, 'utf8');
  for (const heading of lang === 'en' ? ['Use case', 'Mechanism', 'Bad example', 'Good example', 'Why the change matters', 'Observable expectation', 'Limits'] :
    ['使用场景', '具体做法', '反例', '改进写法', '为什么这样改', '如何验证', '适用边界']) {
    if (!body.includes(`## ${heading}`)) errors.push(`${p.id}/${lang}: missing ${heading}`);
  }
  if (!body.includes(`pattern_id: ${p.id}\r\n`) || !body.includes(`lang: ${lang}\r\n`)) errors.push(`${p.id}/${lang}: body identity mismatch`);
  if (body.includes('\uFFFD')) errors.push(`${p.id}/${lang}: invalid text encoding`);
}
const review = readJson('docs/audit/legacy-review.json');
if (new Set(review.patterns.filter(p => Number.isInteger(p.id)).map(p => p.id)).size !== 206) errors.push('Legacy numeric audit is incomplete');
if (!allowPending) {
  const reportNames = ['harvest-composio.json', 'harvest-ecc.json', 'harvest-ecc-variants.json', 'harvest-core.json', 'harvest-gstack.json'];
  const missingMaps = ['integration-decisions.json', 'new-id-map.json'].filter(name => !fs.existsSync(path.join(ROOT, 'docs/audit', name)));
  if (missingMaps.length) errors.push(`Editorial integration incomplete: ${missingMaps.join(', ')}`);
  else errors.push(...validateDecisions(reportNames.flatMap(name => readJson(`docs/audit/${name}`).candidates),
    readJson('docs/audit/integration-decisions.json'), readJson('docs/audit/new-id-map.json'), catalog));
}
for (const name of ['harvest-composio.json', 'harvest-ecc.json', 'harvest-ecc-variants.json', 'harvest-core.json', 'harvest-gstack.json']) {
  const file = path.join(ROOT, 'docs/audit', name);
  if (!fs.existsSync(file)) { if (!allowPending) errors.push(`Research report missing: ${name}`); continue; }
  const report = readJson(`docs/audit/${name}`);
  if (report.summary?.status === 'in_progress' && !allowPending) errors.push(`Research still in progress: ${name}`);
}
let sourceOutcomesChecked = 0;
const reviewKindCounts = Object.fromEntries(REVIEW_KINDS.map(kind => [kind, 0]));
if (!allowPending) {
  const inventory = readJson('docs/audit/source-inventory.json'); const reports = new Map();
  const fileCount = inventory.repositories.reduce((sum, repo) => sum + repo.files.length, 0);
  if (inventory.repositories.length !== 10 || fileCount !== 9806) errors.push(`Frozen coverage inventory changed: ${inventory.repositories.length} repositories / ${fileCount} files`);
  const add = (repo, coverage) => {
    if (!reports.has(repo)) reports.set(repo, new Map());
    for (const row of coverage ?? []) {
      const current = reports.get(repo).get(row.path);
      if (!current || current.disposition === 'pending') reports.get(repo).set(row.path, row);
    }
  };
  for (const name of ['harvest-composio.json', 'harvest-ecc.json', 'harvest-ecc-variants.json', 'harvest-core.json', 'harvest-gstack.json']) {
    const file = path.join(ROOT, 'docs/audit', name); if (!fs.existsSync(file)) continue;
    const report = readJson(`docs/audit/${name}`);
    if (report.repo) add(report.repo, report.coverage);
    for (const repo of report.repositories ?? []) add(repo.repo, repo.coverage);
  }
  for (const repo of inventory.repositories) for (const file of repo.files) {
    const row = reports.get(repo.repo)?.get(file.path);
    errors.push(...validateFileOutcome(row, file.hash, `${repo.repo}/${file.path}`));
    if (REVIEW_KINDS.includes(row?.review_kind)) reviewKindCounts[row.review_kind]++;
    sourceOutcomesChecked++;
  }
}
let evidenceChecked = 0; let rangesChecked = 0;
if (verifySources) {
  const sourcesRoot = sourceRoot(); const cachedLines = new Map();
  for (const p of catalog.filter(p => p.status === 'active')) for (const source of p.sources) {
    if (!source.repo) continue;
    const key = `${source.repo}/${source.commit}/${source.path}`;
    if (!cachedLines.has(key)) {
      const dir = path.join(sourcesRoot, ...source.repo.split('/'));
      const result = spawnSync('git', ['-C', dir, 'show', `${source.commit}:${source.path}`], { maxBuffer: 20 * 1024 * 1024 });
      if (result.status !== 0) { errors.push(`Source file cannot be read: ${key}`); continue; }
      cachedLines.set(key, sourceLineCount(result.stdout)); evidenceChecked++;
    }
    const lineCount = cachedLines.get(key);
    if (source.end_line > lineCount) errors.push(`Source range exceeds file: ${key}`);
    rangesChecked++;
  }
}
const report = { validated_at: new Date().toISOString(), staged_content_only: allowPending, review_scope: 'Content-appropriate review depth; no comprehensive upstream implementation audit', source_outcomes_checked: sourceOutcomesChecked, review_kind_counts: reviewKindCounts, evidence_files_checked: evidenceChecked, evidence_ranges_checked: rangesChecked, errors };
writeText('docs/audit/catalog-validation.json', JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ identities: catalog.length, active: catalog.filter(p => p.status === 'active').length, evidenceChecked, errors: errors.length }));
if (errors.length) { console.error(errors.slice(0, 40).join('\n')); process.exitCode = 1; }

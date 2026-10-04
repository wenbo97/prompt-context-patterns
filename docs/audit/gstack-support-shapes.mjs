// Parse support source as data. This emits triage evidence, never dispositions.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const ts = require('../../eval/patternfoo/node_modules/typescript');
const inputs = JSON.parse(fs.readFileSync('.tools/gstack/support-blobs.json', 'utf8'));
const rows = inputs.map(r => {
  const out = { path:r.path, git_oid:r.git_oid, sha256:r.sha256, bytes:r.bytes, kind:r.kind };
  if (r.kind === 'binary') return { ...out, magic_hex:r.magic_hex };
  out.first_lines = r.text.split(/\r?\n/).slice(0, 12).join('\n');
  out.last_lines = r.text.split(/\r?\n/).slice(-4).join('\n');
  if (!/\.[cm]?[jt]sx?$/.test(r.path) && !/^#![^\n]*\b(?:bun|node)\b/.test(r.text)) return out;
  const source = ts.createSourceFile(r.path, r.text, ts.ScriptTarget.Latest, true);
  const imports = [], exports = [], checks = [], literals = [];
  const lead = r.text.match(/^\s*(?:#![^\n]*\n)?\s*(\/\*[\s\S]*?\*\/)/);
  if (lead) out.leading_comment = lead[1];
  function visit(node) {
    if (ts.isImportDeclaration(node) && ts.isStringLiteral(node.moduleSpecifier)) imports.push(node.moduleSpecifier.text);
    if ((ts.isFunctionDeclaration(node) || ts.isClassDeclaration(node) || ts.isInterfaceDeclaration(node)) && node.name) exports.push(node.name.text);
    if (ts.isCallExpression(node) && /^(describe|test|it)(?:\.|$)/.test(node.expression.getText(source)) && node.arguments[0] && ts.isStringLiteralLike(node.arguments[0])) checks.push(node.arguments[0].text);
    if (ts.isStringLiteralLike(node) || ts.isTemplateExpression(node)) {
      let parent=node.parent, owners=[];
      for (let i=0; parent && i<5; i++,parent=parent.parent) {
        if (ts.isPropertyAssignment(parent)) owners.push('property:'+parent.name.getText(source));
        if (ts.isVariableDeclaration(parent)) owners.push('variable:'+parent.name.getText(source));
        if (ts.isCallExpression(parent)) owners.push('call:'+(ts.isPropertyAccessExpression(parent.expression) ? parent.expression.name.text : ts.isIdentifier(parent.expression) ? parent.expression.text : ts.SyntaxKind[parent.expression.kind]));
      }
      const value=node.getText(source), start=node.getStart(source);
      const agentOwner=owners.some(o=>/^(?:property:(?:prompt|system|instructions|messages|scenario|ticket|question|decisionPolicy|judgeContext|judgeGoal)|variable:(?:prompt|system|instructions|rubrics|contract|SEMANTIC_INSTRUCTIONS|CEO_SECTION_DECISION_POLICY|CENSUS_BRIEF)|call:(?:runSkillTest|callJudge|runAgentSdkTest|runCodexTest|runClaudeCodeTest))/.test(o));
      if (value.length >= 120 || agentOwner) literals.push({sha256:crypto.createHash('sha256').update(value).digest('hex'), start:source.getLineAndCharacterOfPosition(start).line+1, end:source.getLineAndCharacterOfPosition(node.end).line+1, owners, chars:value.length, agentOwner, text:value});
    }
    ts.forEachChild(node,visit);
  }
  visit(source);
  return {...out,imports:[...new Set(imports)],symbols:[...new Set(exports)],checks,literals,parse_errors:source.parseDiagnostics.length};
});
fs.writeFileSync('.tools/gstack/support-shapes.json',JSON.stringify(rows));
console.log(JSON.stringify({files:rows.length,ts_js:rows.filter(r=>r.literals).length,long_literals:rows.reduce((n,r)=>n+(r.literals?.length||0),0),parse_error_files:rows.filter(r=>r.parse_errors).length}));

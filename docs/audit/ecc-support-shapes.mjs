// AST scope evidence only. It does not execute ECC or assign review dispositions.
import fs from 'node:fs';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const ts=require('../../eval/patternfoo/node_modules/typescript');
const inputs=JSON.parse(fs.readFileSync(process.argv[2]||'.tools/ecc/support-blobs.json','utf8'));
const rows=inputs.map(r=>{
 const out={path:r.path,sha256:r.sha256,bytes:r.bytes,lines:r.lines};
 if(r.text===null) return {...out,magic_hex:r.magic_hex};
 out.first_lines=r.text.split('\n').slice(0,22).join('\n');
 out.last_lines=r.text.split('\n').slice(-8).join('\n');
 if(!r.parent_path&&!/\.[cm]?[jt]sx?$/.test(r.path)) return out;
 const source=ts.createSourceFile(r.path,r.text,ts.ScriptTarget.Latest,true,r.parent_path?ts.ScriptKind.JS:undefined);
 const imports=[],symbols=[],checks=[],literals=[];
 const lead=r.text.match(/^\s*(?:#![^\n]*\n)?\s*(\/\*[\s\S]*?\*\/)/);
 if(lead)out.leading_comment=lead[1];
 function visit(n){
  if(ts.isImportDeclaration(n)&&ts.isStringLiteral(n.moduleSpecifier))imports.push(n.moduleSpecifier.text);
  if(ts.isCallExpression(n)&&n.expression.getText(source)==='require'&&n.arguments[0]&&ts.isStringLiteralLike(n.arguments[0]))imports.push(n.arguments[0].text);
  if((ts.isFunctionDeclaration(n)||ts.isClassDeclaration(n)||ts.isInterfaceDeclaration(n))&&n.name)symbols.push({name:n.name.text,start:source.getLineAndCharacterOfPosition(n.getStart(source)).line+1,end:source.getLineAndCharacterOfPosition(n.end).line+1});
  if(ts.isVariableDeclaration(n)&&(ts.isArrowFunction(n.initializer??n)||ts.isFunctionExpression(n.initializer??n)))symbols.push({name:n.name.getText(source),start:source.getLineAndCharacterOfPosition(n.getStart(source)).line+1,end:source.getLineAndCharacterOfPosition(n.end).line+1});
  if(ts.isCallExpression(n)&&/^(describe|test|it)(?:\.|$)/.test(n.expression.getText(source))&&n.arguments[0]&&ts.isStringLiteralLike(n.arguments[0]))checks.push(n.arguments[0].text);
  if(ts.isStringLiteralLike(n)||ts.isTemplateExpression(n)){
   const owners=[];let parent=n.parent;
   for(let i=0;parent&&i<8;i++,parent=parent.parent){
    if(ts.isPropertyAssignment(parent))owners.push('property:'+parent.name.getText(source));
    if(ts.isVariableDeclaration(parent))owners.push('variable:'+parent.name.getText(source));
    if(ts.isCallExpression(parent))owners.push('call:'+parent.expression.getText(source).slice(0,120));
   }
   const value=n.getText(source),start=n.getStart(source);
   const potentialMethodOwner=owners.some(o=>/\b(prompt|system|instruction|scenario|rubric|judge|question|guidance|agent|context|template|skill|contract|permission|capability|policy|fixture|writefile)/i.test(o));
   if(value.length>=100||potentialMethodOwner)literals.push({sha256:crypto.createHash('sha256').update(value).digest('hex'),start:source.getLineAndCharacterOfPosition(start).line+1,end:source.getLineAndCharacterOfPosition(n.end).line+1,owners,chars:value.length,potentialMethodOwner,text:value});
  }
  ts.forEachChild(n,visit);
 }
 visit(source);
 return {...out,imports:[...new Set(imports)],symbols,checks,literals,parse_errors:source.parseDiagnostics.map(d=>({start:d.start,length:d.length,code:d.code,message:ts.flattenDiagnosticMessageText(d.messageText,' ')}))};
});
fs.writeFileSync(process.argv[3]||'.tools/ecc/support-shapes.json',JSON.stringify(rows));
console.log(JSON.stringify({files:rows.length,ast_files:rows.filter(r=>r.literals).length,literals:rows.reduce((a,r)=>a+(r.literals?.length||0),0),unique_literal_hashes:new Set(rows.flatMap(r=>(r.literals??[]).map(l=>l.sha256))).size,parse_error_files:rows.filter(r=>r.parse_errors?.length).length}));

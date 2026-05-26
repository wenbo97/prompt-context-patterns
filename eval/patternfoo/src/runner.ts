import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

export interface PromptfooOutput {
  results: { results: Array<{ promptId: string; success: boolean }> };
}

export function summarizeOutput(out: PromptfooOutput): Map<string, { pass: number; fail: number }> {
  const m = new Map<string, { pass: number; fail: number }>();
  for (const r of out.results.results) {
    const e = m.get(r.promptId) ?? { pass: 0, fail: 0 };
    if (r.success) e.pass++; else e.fail++;
    m.set(r.promptId, e);
  }
  return m;
}

export interface RunOptions {
  configYamlPath: string;
  outputJsonPath: string;
  onStdout?: (chunk: string) => void;
}

export function runPromptfoo(opts: RunOptions): Promise<PromptfooOutput> {
  return new Promise((resolve, reject) => {
    const child = spawn('npx', ['promptfoo', 'eval', '-c', opts.configYamlPath, '-o', opts.outputJsonPath], {
      stdio: ['ignore', 'pipe', 'pipe'],
      shell: process.platform === 'win32',
    });
    child.stdout.on('data', (b) => opts.onStdout?.(b.toString()));
    child.stderr.on('data', (b) => opts.onStdout?.(b.toString()));
    child.on('exit', (code) => {
      if (code !== 0) return reject(new Error(`promptfoo exited ${code}`));
      try {
        const parsed = JSON.parse(fs.readFileSync(opts.outputJsonPath, 'utf8')) as PromptfooOutput;
        resolve(parsed);
      } catch (e) { reject(e); }
    });
  });
}

export function openPromptfooView(): void {
  spawn('npx', ['promptfoo', 'view', '--port', '15500'], {
    detached: true, stdio: 'ignore', shell: process.platform === 'win32',
  }).unref();
}

export function writeRunArtifacts(dirRoot: string, yamlStr: string): { dir: string; yamlPath: string; outPath: string } {
  const ts = new Date().toISOString().replace(/[:.]/g, '-');
  const dir = path.join(dirRoot, ts);
  fs.mkdirSync(dir, { recursive: true });
  const yamlPath = path.join(dir, 'promptfooconfig.yaml');
  const outPath = path.join(dir, 'output.json');
  fs.writeFileSync(yamlPath, yamlStr);
  return { dir, yamlPath, outPath };
}

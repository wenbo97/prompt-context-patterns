import React, { useEffect, useState } from 'react';
import path from 'node:path';
import { Box, Text, useInput, useApp } from 'ink';
import { generateCaseConfigs } from '../configGen.js';
import { runPromptfoo, summarizeOutput, writeRunArtifacts, openPromptfooView } from '../runner.js';
import type { LoadedPattern } from '../patterns.js';
import type { UserConfig } from '../persistedConfig.js';

interface Props { patterns: LoadedPattern[]; config: UserConfig; resultsRoot: string; }

export default function RunAndSummary({ patterns, config, resultsRoot }: Props) {
  const { exit } = useApp();
  const [log, setLog] = useState<string>('');
  const [summary, setSummary] = useState<Map<string, { pass: number; fail: number }> | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const combined = new Map<string, { pass: number; fail: number }>();
        for (const run of generateCaseConfigs(patterns, config)) {
          const { yamlPath, outPath } = writeRunArtifacts(path.join(resultsRoot, run.caseId), run.yaml);
          const out = await runPromptfoo({
            configYamlPath: yamlPath, outputJsonPath: outPath,
            onStdout: (c) => setLog(prev => (prev + c).slice(-2000)),
          });
          for (const [label, stats] of summarizeOutput(out)) combined.set(`${run.caseId} · ${label}`, stats);
        }
        setSummary(combined);
      } catch (e) { setError(String(e)); }
    })();
  }, []);

  useInput((input) => {
    if (summary || error) {
      if (input === 'y') openPromptfooView();
      exit();
    }
  });

  if (error) return <Text color="red">Error: {error}</Text>;
  if (!summary) return (
    <Box flexDirection="column">
      <Text bold>Running promptfoo... (Ctrl+C to abort)</Text>
      <Text>{log.split('\n').slice(-10).join('\n')}</Text>
    </Box>
  );

  return (
    <Box flexDirection="column">
      <Text bold>Done. Summary:</Text>
      {[...summary.entries()].map(([label, s]) => (
        <Text key={label}>  {label}: {s.pass}/{s.pass + s.fail} pass</Text>
      ))}
      <Text>Open report? [y] open promptfoo view  [any] exit</Text>
    </Box>
  );
}

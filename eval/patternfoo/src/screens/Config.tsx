import React, { useState } from 'react';
import { Box, Text, useInput } from 'ink';
import TextInput from 'ink-text-input';
import { type UserConfig } from '../persistedConfig.js';

const FIELDS: Array<{ key: keyof UserConfig; label: string; password?: boolean }> = [
  { key: 'providerId',      label: 'Provider' },
  { key: 'apiBaseUrl',      label: 'apiBaseUrl (blank=official)' },
  { key: 'apiKey',          label: 'apiKey', password: true },
  { key: 'judgeProviderId', label: 'Judge provider' },
  { key: 'runs',            label: 'Runs N' },
];

interface Props { initial: UserConfig; onConfirm: (c: UserConfig) => void; }

export default function Config({ initial, onConfirm }: Props) {
  const [values, setValues] = useState<Record<string, string>>(() => ({
    providerId: initial.providerId,
    apiBaseUrl: initial.apiBaseUrl,
    apiKey: initial.apiKey,
    judgeProviderId: initial.judgeProviderId,
    runs: String(initial.runs),
  }));
  const [focus, setFocus] = useState(0);

  useInput((_, key) => {
    if (key.tab) setFocus(f => (f + 1) % FIELDS.length);
    else if (key.return && focus === FIELDS.length - 1) {
      onConfirm({
        providerId: values.providerId,
        apiBaseUrl: values.apiBaseUrl,
        apiKey: values.apiKey,
        judgeProviderId: values.judgeProviderId,
        runs: Math.max(1, parseInt(values.runs, 10) || 1),
      });
    }
  });

  return (
    <Box flexDirection="column">
      <Text bold>patternfoo · config · tab=next · enter on last field=run</Text>
      {FIELDS.map((f, i) => (
        <Box key={f.key as string}>
          <Text color={i === focus ? 'cyan' : undefined}>{i === focus ? '>' : ' '} {f.label}: </Text>
          {i === focus ? (
            <TextInput
              value={values[f.key as string]}
              onChange={v => setValues({ ...values, [f.key]: v })}
              mask={f.password ? '*' : undefined}
            />
          ) : (
            <Text>{f.password ? '*'.repeat(values[f.key as string].length) : values[f.key as string]}</Text>
          )}
        </Box>
      ))}
    </Box>
  );
}

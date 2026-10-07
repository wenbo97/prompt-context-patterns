import React, { useState } from 'react';
import { Box, Text, useInput } from 'ink';
import type { PatternMeta } from '../catalog.js';

interface Props {
  catalog: PatternMeta[];
  readySet: Set<number>;
  onConfirm: (ids: number[]) => void;
}

const PAGE = 15;

export default function PatternList({ catalog, readySet, onConfirm }: Props) {
  const [cursor, setCursor] = useState(0);
  const [selected, setSelected] = useState<Set<number>>(new Set());

  useInput((input, key) => {
    if (!catalog.length) return;
    if (key.upArrow) setCursor(c => Math.max(0, c - 1));
    else if (key.downArrow) setCursor(c => Math.min(catalog.length - 1, c + 1));
    else if (input === ' ') {
      const id = catalog[cursor].id;
      if (!readySet.has(id)) return;
      const next = new Set(selected);
      next.has(id) ? next.delete(id) : next.add(id);
      setSelected(next);
    } else if (key.return && selected.size > 0) {
      onConfirm([...selected].sort((a, b) => a - b));
    }
  });

  const start = Math.max(0, Math.min(cursor - Math.floor(PAGE / 2), catalog.length - PAGE));
  const window = catalog.slice(start, start + PAGE);

  return (
    <Box flexDirection="column">
      <Text bold>patternfoo · pick patterns ({selected.size} selected) · up/down space enter</Text>
      {window.map((p, i) => {
        const idx = start + i;
        const isCursor = idx === cursor;
        const runnable = readySet.has(p.id);
        const sel = selected.has(p.id);
        const tag = runnable ? '' : ' [no evaluation case]';
        return (
          <Text key={p.id} color={isCursor ? 'cyan' : runnable ? undefined : 'gray'}>
            {isCursor ? '>' : ' '} {sel ? '[x]' : '[ ]'} {String(p.id).padStart(3)} {p.name}{tag}
          </Text>
        );
      })}
      {catalog.length === 0 && <Text>No active catalog records. Generate and validate the catalog first.</Text>}
    </Box>
  );
}

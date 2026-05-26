import React, { useState } from 'react';
import { render } from 'ink';
import path from 'node:path';
import { catalog, TOP10 } from './catalog.js';
import { loadPatterns } from './patterns.js';
import { loadUserConfig, saveUserConfig, type UserConfig } from './persistedConfig.js';
import PatternList from './screens/PatternList.js';
import Config from './screens/Config.js';
import RunAndSummary from './screens/RunAndSummary.js';

type Screen = 'list' | 'config' | 'run';

const ROOT = path.join(process.cwd(), 'patterns');
const RESULTS = path.join(process.cwd(), 'results');

const App = () => {
  const [screen, setScreen] = useState<Screen>('list');
  const [selected, setSelected] = useState<number[]>([]);
  const [config, setConfig] = useState<UserConfig>(loadUserConfig());
  const loaded = loadPatterns(ROOT);
  const readySet = new Set(loaded.filter(p => p.status === 'ready').map(p => p.id));

  if (screen === 'list') {
    return (
      <PatternList
        catalog={catalog}
        top10={TOP10}
        readySet={readySet}
        onConfirm={(ids) => { setSelected(ids); setScreen('config'); }}
      />
    );
  }
  if (screen === 'config') {
    return (
      <Config
        initial={config}
        onConfirm={(c) => { saveUserConfig(c); setConfig(c); setScreen('run'); }}
      />
    );
  }
  return (
    <RunAndSummary
      patterns={loaded.filter(p => selected.includes(p.id))}
      config={config}
      resultsRoot={RESULTS}
    />
  );
};

render(<App />);

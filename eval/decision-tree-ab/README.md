> **Legacy.** Superseded by `eval/patternfoo/`. Retained for historical reference of the original prose-vs-tree experiment.

# decision-tree-ab

Original A/B test comparing prose-style vs decision-tree prompts using `claude -p`.

```bash
bash run.sh 20           # 20 runs, default model
bash run.sh 10 haiku     # 10 runs, haiku
python3 analyze.py       # parse results
```

Results saved to `results/` (gitignored).

#!/bin/bash
# A/B test: prose prompt vs decision-tree prompt
# Runs all scenarios N times via claude -p and saves outputs
#
# Usage:
#   bash run.sh              # 5 runs, default model
#   bash run.sh 10           # 10 runs, default model
#   bash run.sh 5 haiku      # 5 runs, haiku model
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results"
N=${1:-5}
MODEL=${2:-""}

MODEL_FLAG=""
MODEL_LABEL="default"
if [ -n "$MODEL" ]; then
  MODEL_FLAG="--model $MODEL"
  MODEL_LABEL="$MODEL"
fi

SCENARIOS=("prose:tree" "prose-ambiguous:tree-ambiguous" "prose-complex:tree-complex")
LABELS=("simple" "ambiguous" "complex")

echo "A/B Test: Decision Tree vs Prose"
echo "================================"
echo "Runs per scenario: $N"
echo "Model: $MODEL_LABEL"
echo ""

for idx in 0 1 2; do
  IFS=':' read -r prose_name tree_name <<< "${SCENARIOS[$idx]}"
  label="${LABELS[$idx]}"

  prose_file="$SCRIPT_DIR/prompt-${prose_name}.md"
  tree_file="$SCRIPT_DIR/prompt-${tree_name}.md"

  if [ ! -f "$prose_file" ] || [ ! -f "$tree_file" ]; then
    echo "[$label] Skipping — prompt files not found"
    continue
  fi

  prose_dir="$RESULTS_DIR/${prose_name}"
  tree_dir="$RESULTS_DIR/${tree_name}"
  mkdir -p "$prose_dir" "$tree_dir"

  echo "[$label] Running prose..."
  for i in $(seq 1 "$N"); do
    echo "  prose $i/$N"
    claude -p "$(cat "$prose_file")" --output-format text $MODEL_FLAG > "$prose_dir/run-$i.txt" 2>/dev/null
  done

  echo "[$label] Running tree..."
  for i in $(seq 1 "$N"); do
    echo "  tree  $i/$N"
    claude -p "$(cat "$tree_file")" --output-format text $MODEL_FLAG > "$tree_dir/run-$i.txt" 2>/dev/null
  done
  echo ""
done

# Print results
echo "================================"
echo "RESULTS"
echo "================================"
for idx in 0 1 2; do
  IFS=':' read -r prose_name tree_name <<< "${SCENARIOS[$idx]}"
  label="${LABELS[$idx]}"

  echo ""
  echo "--- $label: PROSE ---"
  for f in "$RESULTS_DIR/${prose_name}"/run-*.txt 2>/dev/null; do
    [ -f "$f" ] || continue
    echo "  [$(basename "$f")]"
    sed 's/^/    /' "$f"
    echo ""
  done

  echo "--- $label: TREE ---"
  for f in "$RESULTS_DIR/${tree_name}"/run-*.txt 2>/dev/null; do
    [ -f "$f" ] || continue
    echo "  [$(basename "$f")]"
    sed 's/^/    /' "$f"
    echo ""
  done
done

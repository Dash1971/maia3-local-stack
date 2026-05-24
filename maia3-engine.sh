#!/usr/bin/env bash
set -euo pipefail

ENGINE_HOME="${ENGINE_HOME:-$HOME/chess/maia3-engine}"
VENV_DIR="$ENGINE_HOME/venv"
MODEL_ALIAS="${MAIA3_MODEL:-maia3-23m}"
DEVICE="${MAIA3_DEVICE:-auto}"
USE_UCI_HISTORY="${MAIA3_USE_UCI_HISTORY:-1}"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "ERROR: missing venv at $VENV_DIR" >&2
  echo "Run ./setup-maia3.sh first." >&2
  exit 1
fi

source "$VENV_DIR/bin/activate"

if [[ "$DEVICE" == "auto" ]]; then
  case "$(uname -s)" in
    Darwin) DEVICE="mps" ;;
    Linux) DEVICE="cpu" ;;
    *) DEVICE="cpu" ;;
  esac
fi

ARGS=(--model "$MODEL_ALIAS" --device "$DEVICE")

if [[ "$DEVICE" == "cpu" ]]; then
  ARGS+=(--no-use-amp)
fi

if [[ "$USE_UCI_HISTORY" == "1" ]]; then
  ARGS+=(--use-uci-history)
fi

exec python -m maia3.uci "${ARGS[@]}" "$@"

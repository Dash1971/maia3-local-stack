#!/usr/bin/env bash
set -euo pipefail

OS="$(uname -s)"
ENGINE_HOME="$HOME/chess/maia3-engine"
VENV_DIR="$ENGINE_HOME/venv"
LAUNCHER_DEST="$ENGINE_HOME/maia3-engine.sh"
DEFAULT_MODEL="${MAIA3_MODEL:-maia3-23m}"
MAIA3_GIT_URL="${MAIA3_GIT_URL:-https://github.com/CSSLab/maia3.git}"
CPU_TORCH_INDEX_URL="${CPU_TORCH_INDEX_URL:-https://download.pytorch.org/whl/cpu}"

info() { printf '==> %s\n' "$1"; }
fail() { printf 'ERROR: %s\n' "$1" >&2; exit 1; }

mkdir -p "$ENGINE_HOME"

case "$OS" in
  Linux)
    info "Installing Linux dependencies"
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip stockfish git curl
    PYTHON_BIN="python3"
    ;;
  Darwin)
    command -v brew >/dev/null 2>&1 || fail "Homebrew is required on macOS"
    info "Installing macOS dependencies"
    brew install python@3.12 stockfish git
    PYTHON_BIN="python3.12"
    if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
      PYTHON_BIN="python3"
    fi
    ;;
  *)
    fail "Unsupported OS: $OS"
    ;;
esac

if [[ ! -d "$VENV_DIR" ]]; then
  info "Creating virtual environment"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
info "Upgrading pip"
pip install --upgrade pip

if [[ "$OS" == "Linux" ]]; then
  info "Installing CPU-only PyTorch"
  pip install --index-url "$CPU_TORCH_INDEX_URL" torch
  info "Installing Maia3 runtime dependencies"
  pip install numpy python-chess huggingface-hub
  info "Installing Maia3 from GitHub"
  pip install --no-deps "git+$MAIA3_GIT_URL"
else
  info "Installing Maia3 from GitHub"
  pip install "git+$MAIA3_GIT_URL"
fi

deactivate

install -m 755 ./maia3-engine.sh "$LAUNCHER_DEST"

cat <<EOF

Setup complete.

Engine home: $ENGINE_HOME
Launcher:    $LAUNCHER_DEST
Default model: $DEFAULT_MODEL
Install source: $MAIA3_GIT_URL

Recommended first test:
  $LAUNCHER_DEST --list-models

Then point your UCI GUI at:
  $LAUNCHER_DEST

The first run will download the model checkpoint from Hugging Face.
EOF

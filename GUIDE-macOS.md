# GUIDE-macOS.md

## Apple Silicon macOS quick path

Prerequisite: Homebrew installed.

```bash
git clone https://github.com/Dash1971/maia3-local-stack.git
cd maia3-local-stack
chmod +x *.sh
./setup-maia3.sh
```

Engine path after setup:

```text
~/chess/maia3-engine/maia3-engine.sh
```

## First checks

```bash
~/chess/maia3-engine/maia3-engine.sh --list-models
~/chess/maia3-engine/maia3-engine.sh
```

By default the launcher prefers `mps` on macOS.

The setup script installs Maia3 from the upstream GitHub repo into a local venv.

## Opening books

```bash
./build-books.sh
```

Books are written under:

```text
~/chess/books/
```

## Current limits

- En Croissant installation is still manual.
- `BookFile` and `HumanTime` are provided by the local wrapper.
- This guide will expand once the end-to-end macOS path is validated live.

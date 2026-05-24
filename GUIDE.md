# GUIDE.md

## Linux quick path

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

On Linux, the setup path uses the CPU-only PyTorch index on purpose so the install stays sane on machines that are not using CUDA.

The second command starts the UCI engine. In a GUI, use the same launcher path instead of starting it manually.

## Opening books

```bash
./build-books.sh
```

Books are written under:

```text
~/chess/books/
```

## Current limits

- This first pass installs Maia3 from the upstream GitHub repo and uses the upstream Maia 3 UCI engine directly.
- `BookFile` and `HumanTime` compatibility features are not wired in yet.
- En Croissant walkthrough details will be expanded after live validation.

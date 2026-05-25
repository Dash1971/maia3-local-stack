# maia3-local-stack

Run Maia 3 locally as a human-like UCI chess engine, with En Croissant integration, Stockfish side-by-side analysis, and locally generated Lichess-based opening books for Linux and Apple Silicon macOS.

## Status

This repository is the clean Maia 3 successor to the earlier Maia 2 local-stack project.

Current scope:
- install Maia 3 in a local venv from the upstream GitHub repo
- launch Maia 3 through a thin compatibility wrapper with optional opening-book and HumanTime support
- build Polyglot opening books from Lichess data
- document Linux and Apple Silicon macOS setup

Planned next:
- calibration guidance after live testing
- optional installer polish / post-install smoke test
- more GUI screenshots once the end-to-end flow is exercised visually

## Quick start

```bash
git clone https://github.com/Dash1971/maia3-local-stack.git
cd maia3-local-stack
chmod +x *.sh
./setup-maia3.sh
```

That creates a local install under `~/chess/maia3-engine/` and prints the engine path to use in your GUI.

On Linux, `setup-maia3.sh` deliberately installs the CPU-only PyTorch build to avoid dragging in a multi-gigabyte CUDA stack on non-GPU systems.

To build opening books:

```bash
./build-books.sh
```

For the exact En Croissant setup flow, use:
- [GUIDE.md](GUIDE.md) for Linux
- [GUIDE-macOS.md](GUIDE-macOS.md) for Apple Silicon macOS

## Files

| File | Purpose |
|---|---|
| `setup-maia3.sh` | Create a local Maia 3 environment and install a launcher |
| `maia3-engine.sh` | Thin launcher for the local wrapper |
| `maia3_wrapper.py` | UCI compatibility layer adding `BookFile` and `HumanTime` |
| `build-books.sh` | Build Polyglot opening books from Lichess archives |
| `GUIDE.md` | Linux setup notes |
| `GUIDE-macOS.md` | Apple Silicon macOS setup notes |

## Notes

- Default model is currently `maia3-79m`.
- If you want a lighter fallback, set `MAIA3_MODEL=maia3-23m` before launching or running setup.
- The setup script installs Maia3 from the upstream GitHub repository, not from PyPI.
- The local wrapper adds `BookFile` and `HumanTime` while keeping upstream Maia3 as the underlying move picker.
- `BookFile` has been smoke-tested with a deterministic Polyglot fixture from the starting position.
- The first engine run downloads the chosen checkpoint from Hugging Face and reuses the local cache after that.
- The wrapper is intentionally thin: upstream Maia3 stays authoritative for model behavior.

## License

MIT for repository code and scripts. Maia 3 model weights and upstream engine code have their own licenses; see the upstream CSSLab repository and Hugging Face model pages.

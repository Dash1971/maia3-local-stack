# Maia 3 Local Chess — Linux Setup Guide

Complete walkthrough for setting up Maia 3 on Linux with En Croissant, local Polyglot opening books, and optional side-by-side analysis with Stockfish.

**Tested path so far:** Linux install + launcher + wrapper smoke tests on Pop!_OS host. The En Croissant steps below are written against the current wrapper behavior.

---

## 1. Install Maia 3

```bash
git clone https://github.com/Dash1971/maia3-local-stack.git
cd maia3-local-stack
chmod +x *.sh
./setup-maia3.sh
```

This creates:

- `~/chess/maia3-engine/venv/`
- `~/chess/maia3-engine/maia3-engine.sh`
- `~/chess/maia3-engine/maia3_wrapper.py`
- a local Maia3 install from the upstream GitHub repo
- Stockfish from `apt`

On Linux, the setup script intentionally installs the **CPU-only** PyTorch build so the default path does not pull a massive CUDA stack onto non-GPU systems.

### Smoke test

```bash
echo -e "uci\nisready\nposition startpos\ngo\nquit" | ~/chess/maia3-engine/maia3-engine.sh
```

You should see:
- `uciok`
- `readyok`
- `bestmove ...`

First run will be slower because Maia3 downloads and caches the chosen Hugging Face checkpoint.

---

## 2. Build opening books

This step is optional. Maia3 can play without an opening book; leave `BookFile`
blank if you want upstream Maia3 to choose every move directly. Use a book when
you want the opening phase to follow locally generated Lichess-based human games.

```bash
./build-books.sh
```

The builder asks for:
1. target rating(s)
2. time control bucket
3. download size
4. Lichess archive month

Output books are written to:

```text
~/chess/books/
```

Typical filenames:
- `lichess_1400_all.bin`
- `lichess_1600_rapid.bin`
- `lichess_1800_blitz_rapid.bin`

### Faster with PyPy

```bash
sudo apt install pypy3
pypy3 -m pip install chess --break-system-packages
```

`build-books.sh` auto-detects PyPy if available.

---

## 3. Configure En Croissant

Open **Engines** and add **three engines**.

### Engine 1: Maia 3 (play)

- **Engines → Add New → Local → Binary file**
- **Path:** `/home/<your-username>/chess/maia3-engine/maia3-engine.sh`
- **Depth:** `1`
- **ELO:** your target strength
- **BookFile:** `/home/<your-username>/chess/books/lichess_1600_all.bin` (or your chosen book)
- **HumanTime:** `true`

`BookFile` is optional. Leave it blank for pure Maia3 play without a local
opening book.

Recommended starting point:
- model default stays `maia3-79m`
- keep `Temperature=1.0`
- keep `TopP=1.0`

If you need a lighter fallback later, launch with `MAIA3_MODEL=maia3-23m`.

### Engine 2: Maia 3 Analysis

Same binary path, but:
- **Name:** `Maia 3 Analysis`
- **BookFile:** leave blank
- **HumanTime:** `false`

This keeps play behavior and analysis behavior separate.

### Engine 3: Stockfish

- **Path:** `/usr/games/stockfish`

### Important: two ELO fields

En Croissant typically shows ELO in two places:
- a top-level/general field
- the UCI option field near the bottom

Set both the same. The lower UCI option is the one that actually matters.

---

## 4. Suggested setup pattern

En Croissant engine entries are profiles. They may point to the same
`maia3-engine.sh` binary while carrying different per-entry UCI settings.

### For playing
Use **Maia 3** with:
- `BookFile` set, or blank for no opening book
- `HumanTime=true`
- your chosen ELO

### For analysis
Use **Maia 3 Analysis** with:
- the same binary path
- the same ELO, if you want analysis recommendations at the same target strength
- no `BookFile`
- `HumanTime=false`

Then add **Stockfish** beside it in the Analysis tab.

This gives you:
- **Stockfish** for objective best play
- **Maia 3** for human-like likely play at a target rating

---

## 5. Playing a game

1. **Game → New game**
2. pick a color
3. choose **Maia 3** as the opponent
4. start playing

If `HumanTime` is enabled, moves should not come instantly every time. If they do, re-check that the **UCI option** for `HumanTime` is set to `true`.

---

## 6. Analysis behavior

The wrapper supports:
- normal `go`
- `go infinite`
- `stop`

So it should behave reasonably in analysis panels that expect a UCI engine to think until interrupted.

---

## 7. Troubleshooting

### `maia3-engine.sh: Permission denied`

```bash
chmod +x ~/chess/maia3-engine/maia3-engine.sh ~/chess/maia3-engine/maia3_wrapper.py
```

### First run is slow

Normal. Maia3 downloads the model checkpoint on first use.

### Opening book is not being used

Check all three:
- `BookFile` uses the **absolute path**
- the `.bin` file exists in `~/chess/books/`
- the selected book matches the position family you expect

When a book move is hit, the wrapper emits:

```text
info string book move
```

### Analysis feels delayed

Use the separate **Maia 3 Analysis** engine with `HumanTime=false`.

### `build-books.sh` fails with 404

The selected Lichess month is not available yet. Pick another month or check:
- <https://database.lichess.org>

---

## 8. File layout after setup

```text
~/chess/
├── maia3-engine/
│   ├── maia3-engine.sh
│   ├── maia3_wrapper.py
│   └── venv/
└── books/
    ├── lichess_1400_all.bin
    ├── lichess_1600_all.bin
    └── lichess_1800_all.bin
```

At that point, the Linux path is ready for real GUI use.

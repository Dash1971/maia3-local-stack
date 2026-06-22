# Maia 3 Local Chess — macOS Setup Guide

Set up Maia 3 on Apple Silicon macOS with En Croissant, local opening books, and optional Stockfish side-by-side analysis.

**Current confidence level:** installer and wrapper behavior are grounded; macOS GUI steps are adapted carefully from the earlier Maia workflow and current launcher behavior.

---

## 1. Prerequisite: Homebrew

If Homebrew is not installed yet:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then make sure `brew` is on your PATH.

---

## 2. Install Maia 3

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
- Stockfish from Homebrew

By default the launcher prefers `mps` on macOS.

### Smoke test

```bash
echo -e "uci\nisready\nposition startpos\ngo\nquit" | ~/chess/maia3-engine/maia3-engine.sh
```

You should see `uciok`, `readyok`, and then a `bestmove`.

---

## 3. Install En Croissant

En Croissant installation on macOS is still manual.

Download the Apple Silicon build from:
- <https://github.com/franciscoBSalgueiro/en-croissant/releases>

Open the `.dmg`, drag En Croissant to Applications, and allow it through macOS security if needed.

---

## 4. Build opening books

This step is optional. Maia3 can play without an opening book; leave `BookFile`
blank if you want upstream Maia3 to choose every move directly. Use a book when
you want the opening phase to follow locally generated Lichess-based human games.

```bash
./build-books.sh
```

Books are written to:

```text
~/chess/books/
```

Example outputs:
- `lichess_1400_all.bin`
- `lichess_1600_rapid.bin`
- `lichess_1800_blitz_rapid.bin`

### Optional speedup with PyPy

```bash
brew install pypy3
pypy3 -m pip install chess
```

`build-books.sh` uses PyPy automatically if it finds it.

---

## 5. Configure En Croissant

Open **Engines** and add **three engines**.

### Engine 1: Maia 3 (play)

- **Engines → Add New → Local → Binary file**
- In the picker, press **Cmd+Shift+G** and enter:
  - `~/chess/maia3-engine/maia3-engine.sh`
- **Depth:** `1`
- **ELO:** your target strength
- **BookFile:** `/Users/YOUR_USERNAME/chess/books/lichess_1600_all.bin`
- **HumanTime:** `true`

`BookFile` is optional. Leave it blank for pure Maia3 play without a local
opening book. If you use a book, enter the full absolute path for `BookFile`,
not `~`.

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

### Engine 3: Stockfish

Start with the Homebrew binary path:

```text
/opt/homebrew/bin/stockfish
```

If En Croissant refuses to run the Homebrew path, copy it locally and point En Croissant there instead:

```bash
mkdir -p ~/chess
cp /opt/homebrew/bin/stockfish ~/chess/stockfish
chmod +x ~/chess/stockfish
```

Then use:

```text
/Users/YOUR_USERNAME/chess/stockfish
```

### Important: two ELO fields

As on Linux, En Croissant may show both:
- a general/top ELO field
- a lower UCI-option ELO field

Set both the same. The lower UCI option is the real one.

---

## 6. Suggested setup pattern

### For playing
Use **Maia 3** with:
- `BookFile` set, or blank for no opening book
- `HumanTime=true`
- your target ELO

### For analysis
Use **Maia 3 Analysis** with:
- `BookFile` blank
- `HumanTime=false`

Then add **Stockfish** beside it in the Analysis tab.

---

## 7. Troubleshooting

### En Croissant cannot find the engine file

In the file picker, press **Cmd+Shift+G** and paste the exact path:

```text
/Users/YOUR_USERNAME/chess/maia3-engine/maia3-engine.sh
```

### Engine moves instantly every time

Check the lower UCI option for `HumanTime`, not just the top-level settings.

### Opening book is not loading

Check:
- absolute `BookFile` path
- file exists in `~/chess/books/`
- no quotes or `~` shorthand in the GUI field

When a book move hits, the wrapper emits:

```text
info string book move
```

### Stockfish path fails

Use the manual copy workaround above and point En Croissant at `/Users/YOUR_USERNAME/chess/stockfish`.

---

## 8. Current limits

- macOS GUI behavior has not been exercised as deeply as the Linux-side launcher tests
- the wrapper behavior itself is grounded and provides `BookFile` + `HumanTime`
- Maia3 still downloads its model checkpoint on first real use

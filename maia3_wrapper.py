#!/usr/bin/env python3
"""Thin UCI compatibility wrapper for Maia3.

Adds two user-facing options on top of upstream Maia3:
- BookFile: Polyglot opening book path
- HumanTime: optional human-like delay before bestmove

The wrapper keeps upstream Maia3 as the actual move picker and only intercepts
UCI traffic locally.
"""

from __future__ import annotations

import atexit
import os
import random
import subprocess
import sys
import time
from dataclasses import dataclass

import chess
import chess.polyglot


PASSTHROUGH_FLAGS = {"--help", "-h", "--list-models", "--list_models"}


@dataclass
class EngineOptions:
    elo: int = 1500
    self_elo: int = 1500
    oppo_elo: int = 1500
    temperature: float = 1.0
    top_p: float = 1.0
    book_file: str = ""
    human_time: bool = False


class Maia3Child:
    def __init__(self, child_args: list[str]):
        self.child_args = child_args
        self.proc: subprocess.Popen[str] | None = None

    def ensure(self) -> None:
        if self.proc is not None and self.proc.poll() is None:
            return
        self.proc = subprocess.Popen(
            [sys.executable, "-m", "maia3.uci", *self.child_args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        self._send("uci")
        while True:
            line = self._readline()
            if line == "uciok":
                break

    def close(self) -> None:
        if self.proc is None:
            return
        try:
            self._send("quit")
        except Exception:
            pass
        try:
            self.proc.terminate()
        except Exception:
            pass
        self.proc = None

    def _send(self, line: str) -> None:
        self.ensure()
        assert self.proc is not None and self.proc.stdin is not None
        self.proc.stdin.write(line + "\n")
        self.proc.stdin.flush()

    def _readline(self) -> str:
        self.ensure()
        assert self.proc is not None and self.proc.stdout is not None
        line = self.proc.stdout.readline()
        if line == "":
            raise RuntimeError("Maia3 child exited unexpectedly")
        return line.rstrip("\n")

    def sync_isready(self) -> None:
        self._send("isready")
        while True:
            line = self._readline()
            if line == "readyok":
                return

    def new_game(self) -> None:
        self._send("ucinewgame")

    def apply_options(self, opts: EngineOptions) -> None:
        self._send(f"setoption name Elo value {opts.elo}")
        self._send(f"setoption name SelfElo value {opts.self_elo}")
        self._send(f"setoption name OppoElo value {opts.oppo_elo}")
        self._send(f"setoption name Temperature value {opts.temperature}")
        self._send(f"setoption name TopP value {opts.top_p}")

    def bestmove(self, position_cmd: str, opts: EngineOptions) -> str:
        self.apply_options(opts)
        self._send(position_cmd)
        self._send("go")
        while True:
            line = self._readline()
            if line.startswith("bestmove "):
                return line.split()[1]


class Maia3Wrapper:
    def __init__(self, child_args: list[str]):
        self.child_args = child_args
        self.child = Maia3Child(child_args)
        self.opts = EngineOptions()
        self.board = chess.Board()
        self.position_cmd = "position startpos"
        self.pending_bestmove: str | None = None
        self.analysis_mode = False

    def print_uci(self) -> None:
        print("id name Maia3 + book/humantime wrapper")
        print("id author CSSLab + local wrapper")
        print("option name Elo type spin default 1500 min 0 max 5000")
        print("option name SelfElo type spin default 1500 min 0 max 5000")
        print("option name OppoElo type spin default 1500 min 0 max 5000")
        print("option name Temperature type string default 1.0")
        print("option name TopP type string default 1.0")
        print("option name BookFile type string default ")
        print("option name HumanTime type check default false")
        print("uciok")
        sys.stdout.flush()

    def set_option(self, line: str) -> None:
        try:
            after_name = line.split("name", 1)[1].strip()
            name, _, value = after_name.partition("value")
            name = name.strip().lower()
            value = value.strip()
        except (IndexError, ValueError):
            return

        if name == "elo":
            ivalue = int(value)
            self.opts.elo = ivalue
            self.opts.self_elo = ivalue
            self.opts.oppo_elo = ivalue
        elif name == "selfelo":
            self.opts.self_elo = int(value)
        elif name == "oppoelo":
            self.opts.oppo_elo = int(value)
        elif name == "temperature":
            self.opts.temperature = float(value)
        elif name == "topp":
            self.opts.top_p = float(value)
        elif name == "bookfile":
            self.opts.book_file = value
        elif name == "humantime":
            self.opts.human_time = value.lower() in {"true", "1", "yes", "on"}

    def set_position(self, line: str) -> None:
        tokens = line.split()
        if len(tokens) < 2:
            return

        if tokens[1] == "startpos":
            board = chess.Board()
            if "moves" in tokens:
                for mv in tokens[tokens.index("moves") + 1 :]:
                    try:
                        board.push_uci(mv)
                    except Exception:
                        break
            self.board = board
            self.position_cmd = line
            return

        if tokens[1] == "fen":
            if "moves" in tokens:
                mi = tokens.index("moves")
                board = chess.Board(" ".join(tokens[2:mi]))
                for mv in tokens[mi + 1 :]:
                    try:
                        board.push_uci(mv)
                    except Exception:
                        break
            else:
                board = chess.Board(" ".join(tokens[2:]))
            self.board = board
            self.position_cmd = line

    def get_book_move(self) -> str | None:
        book_path = self.opts.book_file
        if not book_path or not os.path.isfile(book_path):
            return None
        try:
            with chess.polyglot.open_reader(book_path) as reader:
                entries = list(reader.find_all(self.board))
        except Exception:
            return None
        if not entries:
            return None
        total = sum(entry.weight for entry in entries)
        if total <= 0:
            return random.choice(entries).move.uci()
        choice = random.randint(1, total)
        running = 0
        for entry in entries:
            running += entry.weight
            if running >= choice:
                return entry.move.uci()
        return entries[0].move.uci()

    def calculate_think_time(self, chosen_move: str, is_book_move: bool) -> float:
        if is_book_move:
            return random.uniform(0.5, 2.0)
        num_legal = len(list(self.board.legal_moves))
        base = 2.0 + min(num_legal / 10.0, 4.0)
        try:
            move_obj = chess.Move.from_uci(chosen_move)
            if self.board.is_capture(move_obj):
                base += 1.5
            if self.board.gives_check(move_obj):
                base += 1.5
            if move_obj.promotion:
                base += 2.0
        except Exception:
            pass
        piece_count = len(self.board.piece_map())
        if piece_count >= 28:
            base *= 0.7
        elif piece_count <= 12:
            base *= 1.2
        return max(0.5, min(base * random.uniform(0.7, 1.3), 15.0))

    def compute_move(self) -> tuple[str, bool]:
        book_move = self.get_book_move()
        if book_move is not None:
            return book_move, True
        return self.child.bestmove(self.position_cmd, self.opts), False

    def go(self, line: str) -> None:
        bestmove, is_book = self.compute_move()
        if "infinite" in line.split():
            print(f"info depth 1 pv {bestmove}")
            if is_book:
                print("info string book move")
            sys.stdout.flush()
            self.analysis_mode = True
            self.pending_bestmove = bestmove
            return

        if self.opts.human_time:
            think_sec = self.calculate_think_time(bestmove, is_book)
            print(f"info string thinking for {think_sec:.1f}s")
            sys.stdout.flush()
            time.sleep(think_sec)

        print(f"info depth 1 pv {bestmove}")
        if is_book:
            print("info string book move")
        print(f"bestmove {bestmove}")
        sys.stdout.flush()

    def stop(self) -> None:
        if self.analysis_mode and self.pending_bestmove:
            print(f"bestmove {self.pending_bestmove}")
            sys.stdout.flush()
        self.analysis_mode = False
        self.pending_bestmove = None

    def loop(self) -> None:
        for raw in sys.stdin:
            line = raw.strip()
            if not line:
                continue
            if line == "uci":
                self.print_uci()
            elif line == "isready":
                self.child.sync_isready()
                print("readyok")
                sys.stdout.flush()
            elif line == "ucinewgame":
                self.board = chess.Board()
                self.position_cmd = "position startpos"
                self.analysis_mode = False
                self.pending_bestmove = None
                self.child.new_game()
            elif line.startswith("setoption"):
                self.set_option(line)
            elif line.startswith("position"):
                self.set_position(line)
            elif line.startswith("go"):
                self.go(line)
            elif line == "stop":
                self.stop()
            elif line == "quit":
                return


def main() -> None:
    child_args = sys.argv[1:]
    if any(arg in PASSTHROUGH_FLAGS for arg in child_args):
        os.execvp(sys.executable, [sys.executable, "-m", "maia3.uci", *child_args])
    wrapper = Maia3Wrapper(child_args)
    atexit.register(wrapper.child.close)
    wrapper.loop()


if __name__ == "__main__":
    main()

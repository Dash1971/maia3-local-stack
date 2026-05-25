#!/usr/bin/env python3
"""Generate a tiny Polyglot book fixture for wrapper regression tests."""

import pathlib
import struct

import chess
import chess.polyglot


def polyglot_raw(move: chess.Move) -> int:
    promo = 0
    if move.promotion == chess.KNIGHT:
        promo = 1
    elif move.promotion == chess.BISHOP:
        promo = 2
    elif move.promotion == chess.ROOK:
        promo = 3
    elif move.promotion == chess.QUEEN:
        promo = 4
    return (move.from_square << 6) | move.to_square | (promo << 12)


out = pathlib.Path(__file__).with_name("fixtures").joinpath("startpos-e2e4.bin")
out.parent.mkdir(parents=True, exist_ok=True)
board = chess.Board()
move = chess.Move.from_uci("e2e4")
entry = struct.pack(
    ">QHHI",
    chess.polyglot.zobrist_hash(board),
    polyglot_raw(move),
    100,
    0,
)
out.write_bytes(entry)
print(out)

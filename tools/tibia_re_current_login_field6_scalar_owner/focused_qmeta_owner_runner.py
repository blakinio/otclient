#!/usr/bin/env python3
from __future__ import annotations

import focused_qmeta_owner as focused

core = focused.core


def raw_occurrences(self, needle: bytes) -> list[int]:
    rows: list[int] = []
    start = 0
    while True:
        offset = self.raw.find(needle, start)
        if offset < 0:
            return rows
        va = self.off_to_va(offset)
        if va is not None:
            rows.append(va)
        start = offset + 1


core.Image.occurrences = raw_occurrences

if __name__ == '__main__':
    focused.main()

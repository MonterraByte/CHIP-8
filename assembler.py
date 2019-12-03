#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2019 Joaquim Monteiro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import pathlib

parser = argparse.ArgumentParser(description="CHIP-8 assembler")
parser.add_argument("asm", help="Path to the assembly file", type=pathlib.Path)
parser.add_argument("out", help="Path to the output file", type=pathlib.Path)


def remove_whitespace_and_split(s: str) -> [str]:
    result = []
    source_map = {}
    for num, line in enumerate(s.splitlines()):
        comment_index = line.find("#")
        if comment_index != -1:
            final_line = line[:comment_index].strip().lower()
        else:
            final_line = line.strip().lower()

        if final_line != "":
            result.append(final_line)
            source_map[len(result)] = num + 1
    return result, source_map


def assemble(assembly: str) -> bytes:
    instructions, source_map = remove_whitespace_and_split(assembly)

    output = b""
    return output


def main():
    args = parser.parse_args()
    with args.asm.open('r') as fd:
        assembly = fd.read()

    output = assemble(assembly)

    with args.out.open('wb') as fd:
        fd.write(output)


if __name__ == "__main__":
    main()

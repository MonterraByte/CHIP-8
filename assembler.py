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
import enum
import pathlib
import typing

parser = argparse.ArgumentParser(description="CHIP-8 assembler")
parser.add_argument("asm", help="Path to the assembly file", type=pathlib.Path)
parser.add_argument("out", help="Path to the output file", type=pathlib.Path)

INSTRUCTION_LIST = ["cls", "jmp", "jmpo", "call", "ret", "seq", "sneq", "mov", "add", "sub", "or", "and", "xor", "rsh",
                    "lsh", "rand", "draw", "font", "bcd", "skp", "sknp", "wkey", "str", "ldr", "raw"]
HEX_CHARACTERS = "0123456789abcdef"


class TokenType(enum.Enum):
    INSTRUCTION = 0
    CONSTANT = 1
    REGISTER = 2
    INDEX = 3
    DELAY = 4
    SOUND = 5
    LABEL = 6


def get_type(token: str) -> typing.Union[TokenType, None]:
    if len(token) == 0:
        return
    if token in INSTRUCTION_LIST:
        return TokenType.INSTRUCTION
    elif token == "i":
        return TokenType.INDEX
    elif token == "d":
        return TokenType.DELAY
    elif token == "s":
        return TokenType.SOUND
    elif len(token) == 2 and token[0] == "v" and token[1] in HEX_CHARACTERS:
        return TokenType.REGISTER
    elif (token[:2] == "0x" and all(c in HEX_CHARACTERS for c in token)) or token.isdecimal():
        return TokenType.CONSTANT
    else:
        return TokenType.LABEL


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
            source_map[len(result) - 1] = num + 1
    return result, source_map


def find_labels(source_lines: [str], source_map: dict) -> dict:
    labels = {}
    for num, line in enumerate(source_lines):
        index = line.find(":")
        if index != -1:
            label = line[:index]
            if get_type(label) != TokenType.LABEL:
                raise Exception(f"Invalid label at line {source_map[num]}: {label}")
            labels[label] = num

    return labels


def assemble(assembly: str) -> bytes:
    source_lines, source_map = remove_whitespace_and_split(assembly)

    labels = find_labels(source_lines, source_map)

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

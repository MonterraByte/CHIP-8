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


class Argument:
    def __init__(self, value, t: TokenType):
        self.v = value
        self.t = t


class Instruction:
    def __init__(self, instruction: str, args: [Argument], line: int):
        if get_type(instruction) != TokenType.INSTRUCTION:
            raise Exception(f"Not a valid instruction at line {line}: {instruction}")

        if instruction in ("cls", "ret") and len(args) != 0:
            raise Exception(f"{instruction} instruction (at line {line}) doesn't take an argument, but got {len(args)}")
        elif instruction in ("jmp", "jmpo", "call", "rsh", "lsh", "font", "bcd", "skp", "sknp", "wkey", "str", "ldr") \
                and len(args) != 1:
            raise Exception(f"{instruction} instruction (at line {line}) takes one argument, but got {len(args)}")
        elif instruction in ("seq", "sneq", "mov", "add", "sub", "or", "and", "xor", "rand", "raw") and len(args) != 2:
            raise Exception(f"{instruction} instruction (at line {line}) takes two arguments, but got {len(args)}")
        elif instruction == "draw" and len(args) != 3:
            raise Exception(f"{instruction} instruction (at line {line}) takes three arguments, but got {len(args)}")

        if instruction in ("jmpo", "str", "ldr") and args[0].t != TokenType.CONSTANT:
            raise Exception(f"{instruction} instruction (at line {line}) takes a CONSTANT argument, but got a"
                            f"{args[0].t} instead: {args[0].v}")
        elif instruction in ("rsh", "lsh", "font", "bcd", "skp", "sknp", "wkey") and args[0].t != TokenType.REGISTER:
            raise Exception(f"{instruction} instruction (at line {line}) takes a REGISTER argument, but got a"
                            f"{args[0].t} instead: {args[0].v}")
        elif instruction in ("jmp", "call") and args[0].t != TokenType.CONSTANT and args[0].t != TokenType.LABEL:
            raise Exception(f"{instruction} instruction (at line {line}) takes a CONSTANT or LABEL argument, but got a"
                            f"{args[0].t} instead: {args[0].v}")
        elif instruction in ("seq", "sneq") and not (args[0].t == TokenType.REGISTER
                                            and (args[1].t == TokenType.CONSTANT or args[1].t == TokenType.REGISTER)):
            raise Exception(f"{instruction} instruction (at line {line}) takes REGISTER, CONSTANT or REGISTER, REGISTER"
                            f" argument pairs, but got {args[0].t}, {args[1].t} instead: {args[0].v}, {args[1].v}")
        elif instruction == "mov" and not ((args[0].t == TokenType.REGISTER and args[1].t == TokenType.CONSTANT)
                                           or (args[0].t == TokenType.REGISTER and args[1].t == TokenType.REGISTER)
                                           or (args[0].t == TokenType.INDEX and args[1].t == TokenType.CONSTANT)
                                           or (args[0].t == TokenType.INDEX and args[1].t == TokenType.LABEL)
                                           or (args[0].t == TokenType.REGISTER and args[1].t == TokenType.DELAY)
                                           or (args[0].t == TokenType.DELAY and args[1].t == TokenType.REGISTER)
                                           or (args[0].t == TokenType.SOUND and args[1].t == TokenType.REGISTER)):
            raise Exception(f"{instruction} instruction (at line {line}) takes REGISTER, CONSTANT; REGISTER, REGISTER; "
                            f"INDEX, CONSTANT; INDEX, LABEL; REGISTER, DELAY; "
                            f"DELAY, REGISTER or SOUND_REGISTER, REGISTER argument pairs, but got {args[0].t}, "
                            f"{args[1].t} instead: {args[0].v}, {args[1].v}")
        elif instruction == "add" and not ((args[0].t == TokenType.REGISTER and args[1].t == TokenType.CONSTANT)
                                           or (args[0].t == TokenType.REGISTER and args[1].t == TokenType.REGISTER)
                                           or (args[0].t == TokenType.INDEX and args[1].t == TokenType.REGISTER)):
            raise Exception(f"{instruction} instruction (at line {line}) takes REGISTER, CONSTANT; REGISTER, REGISTER "
                            f"or INDEX, REGISTER argument pairs, but got {args[0].t}, {args[1].t} instead: "
                            f"{args[0].v}, {args[1].v}")
        elif instruction in ("sub", "or", "and", "xor") \
                and not (args[0].t == TokenType.REGISTER and args[1].t == TokenType.REGISTER):
            raise Exception(f"{instruction} instruction (at line {line}) takes a REGISTER, REGISTER argument pair, "
                            f"but got {args[0].t}, {args[1].t} instead: {args[0].v}, {args[1].v}")
        elif instruction == "rand" and not (args[0].t == TokenType.REGISTER and args[1].t == TokenType.CONSTANT):
            raise Exception(f"{instruction} instruction (at line {line}) takes a REGISTER, CONSTANT argument pair, "
                            f"but got {args[0].t}, {args[1].t} instead: {args[0].v}, {args[1].v}")
        elif instruction == "raw" and not (args[0].t == TokenType.CONSTANT and args[1].t == TokenType.CONSTANT):
            raise Exception(f"{instruction} instruction (at line {line}) takes a CONSTANT, CONSTANT argument pair, "
                            f"but got {args[0].t}, {args[1].t} instead: {args[0].v}, {args[1].v}")
        elif instruction == "draw" and not (args[0].t == TokenType.REGISTER and args[1].t == TokenType.REGISTER
                                            and args[2].t == TokenType.CONSTANT):
            raise Exception(f"{instruction} instruction (at line {line}) takes REGISTER, REGISTER, CONSTANT as "
                            f"arguments , but got {args[0].t}, {args[1].t} instead: {args[0].v}, {args[1].v}")

        self.instruction = instruction
        self.args = args


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
    elif (token[:2] == "0x" and all(c in HEX_CHARACTERS for c in token[3:])) or token.isdecimal():
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


def parse_instructions(source_lines: [str], source_map: dict) -> [Instruction]:
    instructions = []
    for num, line in enumerate(source_lines):
        current_line = line
        if (label_sep := line.find(":")) != -1:
            current_line = current_line[label_sep + 1:].strip()

        arguments = []
        if (space_index := current_line.find(" ")) != -1:
            instruction = current_line[:space_index]
            if len(current_line) > space_index + 1:
                args = current_line[space_index + 1:].split(",")
                for arg in args:
                    arguments.append(Argument(arg.strip(), get_type(arg.strip())))
        else:
            instruction = current_line

        instructions.append(Instruction(instruction, arguments, source_map[num]))
    return instructions


def assemble(assembly: str) -> bytes:
    source_lines, source_map = remove_whitespace_and_split(assembly)

    labels = find_labels(source_lines, source_map)
    instructions = parse_instructions(source_lines, source_map)

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

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

LOAD_ADDRESS = 0x200
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
    def __init__(self, value, t: TokenType, labels: dict, line: int):
        self.t = t

        if self.t == TokenType.CONSTANT:
            self.v = int(value, base=16)

            if self.v > 0xFFF:
                raise Exception(f"Constant value out of bounds (>0xFFF) in line {line}: {value}")
        elif self.t == TokenType.LABEL:
            self.v = LOAD_ADDRESS + labels[value] * 2

            if self.v > 0xFFF:
                raise Exception(f"Label value out of bounds (>0xFFF) in line {line}: {value}")
        elif self.t == TokenType.REGISTER:
            self.v = int(value[1:], base=16)

            if self.v > 0xF:
                raise Exception(f"Register value out of bounds (>0xF) in line {line}: {value}")
        else:
            self.v = value


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

    def assemble(self, line: int):
        if self.instruction == "cls":
            return 0x00E0.to_bytes(2, "big")
        elif self.instruction == "jmp":
            return (0x1000 + self.args[0].v).to_bytes(2, "big")
        elif self.instruction == "jmpo":
            return (0xA000 + self.args[0].v).to_bytes(2, "big")
        elif self.instruction == "call":
            return (0x2000 + self.args[0].v).to_bytes(2, "big")
        elif self.instruction == "ret":
            return 0x00EE.to_bytes(2, "big")
        elif self.instruction == "seq":
            if self.args[1].t == TokenType.CONSTANT:
                if self.args[1].v > 0xFF:
                    raise Exception(f"Argument out of range (>0xFF) in seq instruction at line {line}: {self.args[1].v}")
                return (0x3000 + self.args[0].v * 0x0100 + self.args[1].v).to_bytes(2, "big")
            else:
                return (0x5000 + self.args[0].v * 0x0100 + self.args[1].v * 0x0010).to_bytes(2, "big")
        elif self.instruction == "sneq":
            if self.args[1].t == TokenType.CONSTANT:
                if self.args[1].v > 0xFF:
                    raise Exception(
                        f"Argument out of range (>0xFF) in sneq instruction at line {line}: {self.args[1].v}")
                return (0x4000 + self.args[0].v * 0x0100 + self.args[1].v).to_bytes(2, "big")
            else:
                return (0x9000 + self.args[0].v * 0x0100 + self.args[1].v * 0x0010).to_bytes(2, "big")
        elif self.instruction == "mov":
            if self.args[0].t == TokenType.REGISTER:
                if self.args[1].t == TokenType.CONSTANT:
                    if self.args[1].v > 0xFF:
                        raise Exception(
                            f"Argument out of range (>0xFF) in mov instruction at line {line}: {self.args[1].v}")
                    return (0x6000 + self.args[0].v * 0x0100 + self.args[1].v).to_bytes(2, "big")
                elif self.args[1].t == TokenType.REGISTER:
                    return (0x8000 + self.args[0].v * 0x0100 + self.args[1].v * 0x0010).to_bytes(2, "big")
                else:
                    return (0xF007 + self.args[0].v * 0x0100).to_bytes(2, "big")
            elif self.args[0].t == TokenType.INDEX:
                return (0xA000 + self.args[1].v).to_bytes(2, "big")
            elif self.args[0].t == TokenType.DELAY:
                return (0xF015 + self.args[0].v * 0x0100).to_bytes(2, "big")
            else:
                return (0xF018 + self.args[0].v * 0x0100).to_bytes(2, "big")
        elif self.instruction == "add":
            if self.args[0].t == TokenType.REGISTER:
                if self.args[1].t == TokenType.CONSTANT:
                    if self.args[1].v > 0xFF:
                        raise Exception(
                            f"Argument out of range (>0xFF) in add instruction at line {line}: {self.args[1].v}")
                    return (0x7000 + self.args[0].v * 0x0100 + self.args[1].v).to_bytes(2, "big")
                else:
                    return (0x8004 + self.args[0].v * 0x0100 + self.args[1].v * 0x0010).to_bytes(2, "big")
            else:
                return (0xF01E + self.args[1].v * 0x0100).to_bytes(2, "big")
        elif self.instruction == "sub":
            return (0x8005 + self.args[0].v * 0x0100 + self.args[1].v * 0x0010).to_bytes(2, "big")
        elif self.instruction == "or":
            return (0x8001 + self.args[0].v * 0x0100 + self.args[1].v * 0x0010).to_bytes(2, "big")
        elif self.instruction == "and":
            return (0x8002 + self.args[0].v * 0x0100 + self.args[1].v * 0x0010).to_bytes(2, "big")
        elif self.instruction == "xor":
            return (0x8003 + self.args[0].v * 0x0100 + self.args[1].v * 0x0010).to_bytes(2, "big")
        elif self.instruction == "rsh":
            return (0x8006 + self.args[0].v * 0x0100 + self.args[0].v * 0x0010).to_bytes(2, "big")
        elif self.instruction == "lsh":
            return (0x800E + self.args[0].v * 0x0100 + self.args[0].v * 0x0010).to_bytes(2, "big")
        elif self.instruction == "rand":
            if self.args[1].v > 0xFF:
                raise Exception(f"Argument out of range (>0xFF) in rand instruction at line {line}: {self.args[1].v}")
            return (0xC000 + self.args[0].v * 0x0100 + self.args[1].v).to_bytes(2, "big")
        elif self.instruction == "draw":
            if self.args[1].v > 0xF:
                raise Exception(f"Argument out of range (>0xF) in draw instruction at line {line}: {self.args[1].v}")
            return (0xD000 + self.args[0].v * 0x0100 + self.args[1].v * 0x0010 + self.args[2].v).to_bytes(2, "big")
        elif self.instruction == "font":
            return (0xF029 + self.args[0].v * 0x0100).to_bytes(2, "big")
        elif self.instruction == "bcd":
            return (0xF033 + self.args[0].v * 0x0100).to_bytes(2, "big")
        elif self.instruction == "skp":
            return (0xE09E + self.args[0].v * 0x0100).to_bytes(2, "big")
        elif self.instruction == "sknp":
            return (0xE0A1 + self.args[0].v * 0x0100).to_bytes(2, "big")
        elif self.instruction == "wkey":
            return (0xF00A + self.args[0].v * 0x0100).to_bytes(2, "big")
        elif self.instruction == "str":
            return (0xF055 + self.args[0].v * 0x0100).to_bytes(2, "big")
        elif self.instruction == "ldr":
            return (0xF065 + self.args[0].v * 0x0100).to_bytes(2, "big")
        elif self.instruction == "raw":
            return self.args[0].v.to_bytes(1, "big") + self.args[1].v.to_bytes(1, "big")


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
    elif all(c in HEX_CHARACTERS for c in token):
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


def parse_instructions(source_lines: [str], source_map: dict, labels: dict) -> [Instruction]:
    instructions = []
    for num, line in enumerate(source_lines):
        current_line = line
        label_sep = line.find(":")
        if label_sep != -1:
            current_line = current_line[label_sep + 1:].strip()

        arguments = []
        space_index = current_line.find(" ")
        if space_index != -1:
            instruction = current_line[:space_index]
            if len(current_line) > space_index + 1:
                args = current_line[space_index + 1:].split(",")
                for arg in args:
                    arguments.append(Argument(arg.strip(), get_type(arg.strip()), labels, line))
        else:
            instruction = current_line

        instructions.append(Instruction(instruction, arguments, source_map[num]))
    return instructions


def generate_assembly(instructions: [Instruction], source_map: dict) -> bytes:
    output = bytearray()
    for num, instruction in enumerate(instructions):
        output += instruction.assemble(source_map[num])
    return output


def assemble(assembly: str) -> bytes:
    source_lines, source_map = remove_whitespace_and_split(assembly)

    labels = find_labels(source_lines, source_map)
    instructions = parse_instructions(source_lines, source_map, labels)

    return generate_assembly(instructions, source_map)


def main():
    args = parser.parse_args()
    with args.asm.open('r') as fd:
        assembly = fd.read()

    output = assemble(assembly)

    with args.out.open('wb') as fd:
        fd.write(output)


if __name__ == "__main__":
    main()

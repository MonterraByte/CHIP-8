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

from PySide2 import QtCore

from .display import VideoMemory
from .font import FONT_DATA
from .memory import Memory

PROGRAM_COUNTER_START = 512


class UnimplementedInstruction(Exception):
    def __init__(self, instruction, address):
        self.instruction = instruction
        self.address = address

    def __str__(self):
        return f"Unimplemented instruction 0x{self.instruction:04X} at address 0x{self.address:03X}"


class Emulator(QtCore.QObject):
    display_changed = QtCore.Signal()
    unimplemented_instruction = QtCore.Signal(UnimplementedInstruction)

    def __init__(self, rom, debug=False):
        super().__init__()
        self.debug = debug

        self.v = [0] * 16
        self.program_counter = PROGRAM_COUNTER_START
        self.address_register = 0
        self.stack_pointer = 0
        self.delay_timer = 0
        self.sound_timer = 0

        self.memory = Memory()
        self.video_memory = VideoMemory()

        self.memory.load_font(FONT_DATA)
        self.memory.load_rom(rom)

        if self.debug:
            print("Memory:")
            print(self.memory)

    @QtCore.Slot()
    def run_once(self):
        instruction = int.from_bytes(self.memory[self.program_counter:self.program_counter+2], byteorder="big")
        self.program_counter += 2

        if instruction & 0xF000 == 0x1000:
            # Jump to address.
            self.program_counter = instruction & 0x0FFF
        else:
            exception = UnimplementedInstruction(instruction, self.program_counter-2)
            self.unimplemented_instruction.emit(exception)
            raise exception


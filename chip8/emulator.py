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
from .memory import Memory, FONT_START

PROGRAM_COUNTER_START = 512
STACK_POINTER_START = 82


class UnimplementedInstruction(Exception):
    def __init__(self, instruction, address):
        self.instruction = instruction
        self.address = address

    def __str__(self):
        return f"Unimplemented instruction 0x{self.instruction:04X} at address 0x{self.address:03X}"


class Emulator(QtCore.QObject):
    display_changed = QtCore.Signal()
    emulation_error = QtCore.Signal(Exception)

    def __init__(self, rom, debug=False):
        super().__init__()
        self.debug = debug

        self.v = [0] * 16
        self.program_counter = PROGRAM_COUNTER_START
        self.index_register = 0
        self.stack_pointer = STACK_POINTER_START
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

        if instruction == 0x00EE:
            # Return from subroutine.
            self.stack_pointer -= 2
            self.program_counter = int.from_bytes(self.memory[self.stack_pointer:self.stack_pointer+2], byteorder="big")
            if self.debug:
                print(f"[{instruction:04X}] Returning from subroutine to address {self.program_counter:04X}")
        elif instruction & 0xF000 == 0x1000:
            # Jump to address.
            if self.debug:
                print(f"[{instruction:04X}] Jumping to address {instruction & 0x0FFF:03X}")
            self.program_counter = instruction & 0x0FFF
        elif instruction & 0xF000 == 0x2000:
            # Call subroutine.
            if self.debug:
                print(f"[{instruction:04X}] Calling subroutine at address {instruction & 0x0FFF:03X}")
            return_address = int.to_bytes(self.program_counter, 2, byteorder="big")
            self.memory[self.stack_pointer:self.stack_pointer+2] = return_address

            self.stack_pointer += 2
            self.program_counter = instruction & 0x0FFF
        elif instruction & 0xF000 == 0x3000:
            # Skip the next instruction if the source register equals value.
            if self.debug:
                print(f"[{instruction:04X}] Conditional skip if register {(instruction & 0x0F00) >> 8:X} equals {instruction & 0x00FF:02X} ({self.v[(instruction & 0x0F00) >> 8] == instruction & 0x00FF})")
            if self.v[(instruction & 0x0F00) >> 8] == instruction & 0x00FF:
                self.program_counter += 2
        elif instruction & 0xF000 == 0x4000:
            # Skip the next instruction if the source register does not equal value.
            if self.debug:
                print(f"[{instruction:04X}] Conditional skip if register {(instruction & 0x0F00) >> 8:X} does not equal {instruction & 0x00FF:02X} ({self.v[(instruction & 0x0F00) >> 8] != instruction & 0x00FF})")
            if self.v[(instruction & 0x0F00) >> 8] != instruction & 0x00FF:
                self.program_counter += 2
        elif instruction & 0xF00F == 0x5000:
            # Skip the next instruction if the registers have the same value.
            if self.debug:
                print(f"[{instruction:04X}] Conditional skip if the values of the registers {(instruction & 0x0F00) >> 8:X} and {(instruction & 0x00F0) >> 4:X} are equal ({self.v[(instruction & 0x0F00) >> 8] == self.v[(instruction & 0x00F0) >> 4]})")
            if self.v[(instruction & 0x0F00) >> 8] == self.v[(instruction & 0x00F0) >> 4]:
                self.program_counter += 2
        elif instruction & 0xF000 == 0x6000:
            # Move value to register
            if self.debug:
                print(f"[{instruction:04X}] Moving {instruction & 0x00FF:02X} to register {(instruction & 0x0F00) >> 8:X}")
            self.v[(instruction & 0x0F00) >> 8] = instruction & 0x00FF
        elif instruction & 0xF000 == 0x7000:
            # Add value to register (wrapping addition, no carry)
            if self.debug:
                print(f"[{instruction:04X}] Adding {instruction & 0x00FF:02X} to register {(instruction & 0x0F00) >> 8:X} (carry discarded)")
            self.v[(instruction & 0x0F00) >> 8] += instruction & 0x00FF
            while self.v[(instruction & 0x0F00) >> 8] > 255:
                self.v[(instruction & 0x0F00) >> 8] -= 255
        elif instruction & 0xF00F == 0x9000:
            # Skip the next instruction if the registers have different values.
            if self.debug:
                print(f"[{instruction:04X}] Conditional skip if the values of the registers {(instruction & 0x0F00) >> 8:X} and {(instruction & 0x00F0) >> 4:X} differ ({self.v[(instruction & 0x0F00) >> 8] == self.v[(instruction & 0x00F0) >> 4]})")
            if self.v[(instruction & 0x0F00) >> 8] != self.v[(instruction & 0x00F0) >> 4]:
                self.program_counter += 2
        elif instruction & 0xF000 == 0xA000:
            # Move value to the index register.
            if self.debug:
                print(f"[{instruction:04X}] Moving {instruction & 0x0FFF:03X} to the index register")
            self.index_register = instruction & 0x0FFF
        elif instruction & 0xF000 == 0xD000:
            # Draw sprite.
            x = self.v[(instruction & 0x0F00) >> 8]
            y = self.v[(instruction & 0x00F0) >> 4]

            if self.debug:
                print(f"[{instruction:04X}] Drawing sprite from memory address {self.index_register:03X} ({instruction & 0x000F} tall) at coordinates {x}, {y}")

            collision = False
            for i in range(instruction & 0x000F):
                sprite = self.memory[self.index_register + i]
                collision = collision or self.video_memory.draw_sprite_line(x, y + i, sprite)

            if collision:
                if self.debug:
                    print(f"[{instruction:04X}] Sprite collision detected")
                self.v[0xF] = 1
            else:
                self.v[0xF] = 0

            self.display_changed.emit()
        elif instruction & 0xF0FF == 0xF007:
            # Load delay register
            if self.debug:
                print(f"[{instruction:04X}] Loading register {(instruction & 0x0F00) >> 8:X} with the value of the delay timer ({self.delay_timer})")
            self.v[(instruction & 0x0F00) >> 8] = self.delay_timer
        elif instruction & 0xF0FF == 0xF015:
            # Load delay register
            if self.debug:
                print(f"[{instruction:04X}] Loading the delay timer with value {(instruction & 0x0F00) >> 8}")
            self.delay_timer = (instruction & 0x0F00) >> 8
        elif instruction & 0xF0FF == 0xF018:
            # Load delay register
            if self.debug:
                print(f"[{instruction:04X}] Loading the sound timer with value {(instruction & 0x0F00) >> 8}")
            self.sound_timer = (instruction & 0x0F00) >> 8
        elif instruction & 0xF0FF == 0xF029:
            # Load index register with the location of the font for the value in the register
            if self.debug:
                print(f"[{instruction:04X}] Loading the index register with the address of the font for {self.v[(instruction & 0x0F00) >> 8]} from register {(instruction & 0x0F00) >> 8:X}")
            self.index_register = FONT_START + self.v[(instruction & 0x0F00) >> 8] * 5
        elif instruction & 0xF0FF == 0xF033:
            # Store the binary coded decimal representation of the value in the specified register in memory
            value = self.v[(instruction & 0x0F00) >> 8]

            if self.debug:
                print(f"[{instruction:04X}] Storing BCD representation of value {value} from register {(instruction & 0x0F00) >> 8:X} to address {self.index_register:03X}")

            self.memory[self.index_register] = value // 100
            value = value % 100
            self.memory[self.index_register + 1] = value // 10
            self.memory[self.index_register + 2] = value % 10
        elif instruction & 0xF0FF == 0xF055:
            # Store registers in memory
            if self.debug:
                print(f"[{instruction:04X}] Moving the first {((instruction & 0x0F00) >> 8) + 1} registers to memory address {self.index_register:03X}")
            for i in range(((instruction & 0x0F00) >> 8) + 1):
                self.memory[self.index_register + i] = self.v[i]
        elif instruction & 0xF0FF == 0xF065:
            # Read registers from memory
            if self.debug:
                print(f"[{instruction:04X}] Moving value from memory address {self.index_register:03X} to the first {((instruction & 0x0F00) >> 8) + 1} registers")
            for i in range(((instruction & 0x0F00) >> 8) + 1):
                self.v[i] = self.memory[self.index_register + i]
        else:
            exception = UnimplementedInstruction(instruction, self.program_counter-2)
            self.emulation_error.emit(exception)
            raise exception


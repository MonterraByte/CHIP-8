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

MEM_SIZE = 4096
FONT_START = 0
ROM_START = 0x200


class Memory(bytearray):
    def __init__(self):
        super().__init__(MEM_SIZE)

    def reset(self):
        self.__init__()

    def load_font(self, font):
        for offset, byte in enumerate(font):
            self[FONT_START + offset] = byte

    def load_rom(self, rom):
        for offset, byte in enumerate(rom):
            self[ROM_START + offset] = byte


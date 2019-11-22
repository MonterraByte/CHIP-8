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

from .display import VideoMemory
from .font import FONT_DATA
from .memory import Memory


class Emulator:
    def __init__(self, rom, debug=False):
        self.debug = debug

        self.memory = Memory()
        self.video_memory = VideoMemory()

        self.memory.load_font(FONT_DATA)
        self.memory.load_rom(rom)

        if self.debug:
            print("Memory:")
            print(self.memory)

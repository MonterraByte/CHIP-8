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

from PySide2.QtGui import QImage

DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 32


class VideoMemory(bytearray):
    def __init__(self):
        super().__init__(DISPLAY_WIDTH * DISPLAY_HEIGHT)

    def draw(self, image: QImage):
        for address, data in enumerate(self):
            x = address % DISPLAY_WIDTH
            y = address // DISPLAY_WIDTH
            if data:
                image.setPixel(x, y, 1)
            else:
                image.setPixel(x, y, 0)

    def draw_sprite_line(self, x, y, sprite_line):
        collision = False
        for offset in range(8):
            current_value = self[(DISPLAY_WIDTH * y) + x + offset]
            new_value = ((sprite_line & (0b10000000 >> offset)) >> 7 - offset)

            if current_value and new_value:
                collision = True
                self[(DISPLAY_WIDTH * y) + x + offset] = 0
            elif new_value:
                self[(DISPLAY_WIDTH * y) + x + offset] = 1

        return collision

    def reset(self):
        self.__init__()

    def __str__(self):
        s = ""
        for address, data in enumerate(self):
            if address % DISPLAY_WIDTH == 0:
                s += "\n"

            if data:
                s += "█"
            else:
                s += "░"
        return s[1:]

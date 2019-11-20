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

parser = argparse.ArgumentParser(description="CHIP-8 emulator")
parser.add_argument("rom", help="Path to the ROM file", type=pathlib.Path)
parser.add_argument("--debug", help="Enable debug output", default=False, action="store_true")


def main():
    args = parser.parse_args()

# CHIP-8
CHIP-8 implementation in Python

## Dependencies

* [PySide2](https://pypi.org/project/PySide2/)

## Usage

    python3 -m chip8

To try the included Pong game, first assemble it:

    ./assembler.py games/pong.asm pong.out

then run it:

    python3 -m chip8 pong.out

You can find a collection of other games to try [here](https://www.zophar.net/pdroms/chip8/chip-8-games-pack.html) ([archive link](https://web.archive.org/web/20190719223725/https://www.zophar.net/pdroms/chip8/chip-8-games-pack.html)).

## Possible improvements

* Support for the Super-Chip extension to the CHIP-8
* Improved debugging
* Customizable keybindings
* Sound support

## References and resources

* Craig Thomas' [Writing a Chip 8 Emulator](http://craigthomas.ca/blog/2014/06/21/writing-a-chip-8-emulator-part-1/)
* Craig Thomas' [Chip8C interpreter](https://github.com/craigthomas/Chip8C)
* Wikipedia's [CHIP-8 article](https://en.wikipedia.org/wiki/CHIP-8)
* corax89's [test rom](https://github.com/corax89/chip8-test-rom)
* Alex Oberhofer's [test roms](https://github.com/AlexOberhofer/Chip-8-Emulator)

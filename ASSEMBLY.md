# CHIP-8 Assembly Reference

## Instruction Table

| Name | Arguments | Opcode | Description        |
|:----:|:---------:|:------:| ------------------ |
| cls  |           | 00E0   | Clears the screen. |
| jmp  | NNN (or LABEL) | 1NNN   | Jumps to address NNN. |
| jmpo | NNN (or LABEL) | BNNN   | Jumps to the sum of NNN and the value in V0. |
| call | NNN (or LABEL) | 2NNN   | Call subroutine at address NNN. |
| ret  |           | 00EE   | Returns from subroutine. |
| seq  | Vx, NN or Vx, Vy | 3xNN or 5xy0 | Skips the next instruction if the arguments have the same value. |
| sneq | Vx, NN or Vx, Vy | 4xNN or 9xy0 | Skips the next instruction if the arguments have different values. |
| mov  | Vx, NN or Vx, Vy or I, NNN (or LABEL) or Vx, T or T, Vx or S, Vx | 6xNN or 8xy0 or ANNN or Fx07 or Fx15 or Fx18 | Assigns the first argument the value of the second argument. |
| add  | Vx, NN or Vx, Vy or I, Vx | 7xNN or 8xy4 or Fx1E | Adds the value of the second argument to Vx. (If the second argument is a constant, Vf isn't modified) |
| sub  | Vx, Vy    | 8xy5   | Subtracts the value of the second argument from Vx. (Vf is set to 1 when there isn't a borrow, 0 otherwise) |
| or   | Vx, Vy    | 8xy1   | ORs Vx with the value of Vy. |
| and  | Vx, Vy    | 8xy2   | ANDs Vx with the value of Vy. |
| xor  | Vx, Vy    | 8xy3   | XORs Vx with the value of Vy.|
| rsh  | Vx        | 8xx6   | Shifts Vx to the right, storing the shifted bit in Vf. |
| lsh  | Vx        | 8xxE   | Shifts Vx to the left, storing the shifted bit in Vf. |
| rand | Vx, NN    | CxNN   | Sets Vx to the result of an AND between a random number and NN. |
| draw | Vx, Vy, N | DxyN   | Draws a sprite at coordinates Vx, Vy with a width of 8 and a height of N. The sprite is read from the memory location pointed at by I. Vf is set to 1 if there's a sprite collision, and 0 otherwise. |
| font | Vx        | Fx29   | Sets I to the address of the font for the character in Vx. |
| bcd  | Vx        | Fx33   | Stores the binary-coded decimal representation of the value in Vx in the memory location pointed at by I. |
| skp  | Vx        | Ex9E   | Skips the next instruction if the key in Vx is pressed. |
| sknp | Vx        | ExA1   | Skips the next instruction if the key in Vx isn't pressed. |
| wkey | Vx        | Fx0A   | Blocks until a key is pressed, then stores its value in Vx. |
| str  | N         | FN55   | Stores the first N registers in the memory location pointed to by I. |
| ldr  | N         | FN65   | Loads the first N registers from the memory location pointed to by I. |
| raw  | D1, D2    |        | This isn't an instruction. The assembler simply copies the 2 bytes, D1 and D2, to the assembled executable. This is useful for storing data such as sprites with the program. |

## Register Table

| Registers | Description                                                                |
|:---------:| -------------------------------------------------------------------------- |
| Vn        | General purpose registers                                                  |
| Vf        | Register set by some instructions (usually containing the carry flag)      |
| I         | Index register, its value is used as a memory address by some instructions |
| T         | Delay (timer) register                                                             |
| S         | Sound register                                                             |

## Labels

A label can be used instead of a hardcoded address in the following instructions: `jmp`, `call` and `mov`.

To define a label, write its name before the corresponding instruction, followed by a `:`.
For example:

    LABEL_NAME: instruction arg1, arg2

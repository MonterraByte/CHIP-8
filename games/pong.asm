SPLASH: cls
        mov V0, 15
        mov V1, 6

        mov I, FONT_P
        draw V0, V1, 6

        add V0, 5
        mov I, FONT_O
        draw V0, V1, 6 

        add V0, 6
        mov I, FONT_N
        draw V0, V1, 6 

        add V0, 6
        mov I, FONT_G
        draw V0, V1, 6 

LOOP:   jmp LOOP

# 11111000   F8
# 10000000   80
# 10000000 = 80
# 10011000   98
# 10001000   88
# 11111000   F8
FONT_G: raw F8, 80
        raw 80, 98
        raw 88, F8

# 10001000   88
# 11001000   C8
# 10101000 = A8
# 10011000   98
# 10001000   88
# 10001000   88
FONT_N: raw 88, C8
        raw A8, 98
        raw 88, 88

# 11111000   F8
# 10001000   88
# 10001000 = 88
# 10001000   88
# 10001000   88
# 11111000   F8
FONT_O: raw F8, 88
        raw 88, 88
        raw 88, F8

# 11110000   F0
# 10010000   90
# 11110000 = F0
# 10000000   80
# 10000000   80
# 10000000   80
FONT_P: raw F0, 90
        raw F0, 80
        raw 80, 80

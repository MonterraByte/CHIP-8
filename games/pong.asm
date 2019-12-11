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

MENU:   wkey V2
        seq V2, 5
        jmp MENU
        jmp GAME

GAME:   cls
        mov VD, 1C # 28 = 32 - 4

        mov V0, 01
        mov V1, 0D # 13

        mov V2, 3E # 62
        mov V3, 0D # 13

        mov I, PADDLE
        draw V0, V1, 5
        draw V2, V3, 5

LOOP:   mov V5, 01
        sknp V5
        call LEFT_UP

        mov V5, 04
        sknp V5
        call LEFT_DN

        mov V5, 0C
        sknp V5
        call RGHT_UP

        mov V5, 0D
        sknp V5
        call RGHT_DN


        jmp LOOP

LEFT_UP:draw V0, V1, 5
        sub V1, V0 # V1 - 1
        seq VF, 01
        mov V1, 1B
        draw V0, V1, 5
        ret

LEFT_DN:draw V0, V1, 5
        add V1, V0 # V1 + 1
        mov V5, V1
        sub V5, VD
        seq VF, 00 # if V1 > 1B (27), V1 <- 00
        mov V1, 00
        draw V0, V1, 5
        ret

RGHT_UP:draw V2, V3, 5
        sub V3, V0 # V1 - 1
        seq VF, 01
        mov V3, 1B
        draw V2, V3, 5
        ret

RGHT_DN:draw V2, V3, 5
        add V3, V0 # V1 + 1
        mov V5, V3
        sub V5, VD
        seq VF, 00 # if V1 > 1B (27), V1 <- 00
        mov V3, 00
        draw V2, V3, 5
        ret

# 10000000 = 80
# 10000000 = 80
# 10000000 = 80
# 10000000 = 80
# 10000000 = 80
PADDLE: raw 80, 80
        raw 80, 80
        raw 80, 80

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

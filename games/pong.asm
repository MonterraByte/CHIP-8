SPLASH: cls
        mov V1, 15
        mov V2, 6

        mov I, FONT_P
        draw V1, V2, 6

        add V1, 5
        mov I, FONT_O
        draw V1, V2, 6 

        add V1, 6
        mov I, FONT_N
        draw V1, V2, 6 

        add V1, 6
        mov I, FONT_G
        draw V1, V2, 6 

MENU:   wkey V3
        seq V3, 5
        jmp MENU
        jmp GAME

GAME:   cls
        mov VD, 1C # 28 = 32 - 4

        mov V1, 01
        mov V2, 0D # 13

        mov V3, 3E # 62
        mov V4, 0D # 13

        mov I, PADDLE
        draw V1, V2, 5
        draw V3, V4, 5

LOOP:   mov VC, 01
        sknp VC
        call LEFT_UP

        mov VC, 04
        sknp VC
        call LEFT_DN

        mov VC, 0C
        sknp VC
        call RGHT_UP

        mov VC, 0D
        sknp VC
        call RGHT_DN


        jmp LOOP

LEFT_UP:draw V1, V2, 5
        sub V2, V1 # V2 - 1
        seq VF, 01
        mov V2, 1B
        draw V1, V2, 5
        ret

LEFT_DN:draw V1, V2, 5
        add V2, V1 # V2 + 1
        mov VC, V2
        sub VC, VD
        seq VF, 00 # if V2 > 1B (27), V2 <- 00
        mov V2, 00
        draw V1, V2, 5
        ret

RGHT_UP:draw V3, V4, 5
        sub V4, V1 # V2 - 1
        seq VF, 01
        mov V4, 1B
        draw V3, V4, 5
        ret

RGHT_DN:draw V3, V4, 5
        add V4, V1 # V2 + 1
        mov VC, V4
        sub VC, VD
        seq VF, 00 # if V2 > 1B (27), V2 <- 00
        mov V4, 00
        draw V3, V4, 5
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

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
        mov VD, 00

        mov V1, 01
        mov V2, 0D # 13

        mov V3, 3E # 62
        mov V4, 0D # 13

        mov V5, 1F # 31
        mov V6, 0F # 15
        rand V0, 1E # 0001 1110

        mov V7, 0 # Left player score
        mov V8, 0 # Right player score

        font V7
        mov VC, 10
        draw VC, V1, 5
        font V8
        mov VC, 2A
        draw VC, V1, 5

        mov I, PADDLE
        draw V1, V2, 5
        draw V3, V4, 5
        draw V5, V6, 1

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

        call MOVBALL

        seq VD, 00
        jmp END

        jmp LOOP

LEFT_UP:draw V1, V2, 5
        sub V2, V1 # V2 - 1
        seq VF, 01
        mov V2, 1B
        draw V1, V2, 5
        ret

LEFT_DN:draw V1, V2, 5
        add V2, V1 # V2 + 1
        sneq V2, 1C # if V2 = 28, V2 <- 00
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
        sneq V2, 1C # if V2 = 28, V2 <- 00
        mov V4, 00
        draw V3, V4, 5
        ret

MOVBALL:draw V5, V6, 1
        jmpo MJMPTBL

MJMPTBL:jmp BALL_M0
        jmp BALL_M1
        jmp BALL_M2
        jmp BALL_M3
        jmp BALL_M4
        jmp BALL_M5
        jmp BALL_M6
        jmp BALL_M7
        jmp BALL_M8
        jmp BALL_M9
        jmp BALL_MA
        jmp BALL_MB
        jmp BALL_MC
        jmp BALL_MD
        jmp BALL_ME
        jmp BALL_MF

BALL_M0:jmp BMOVRGT
BALL_M1:jmp BMOVRGT
BALL_M2:jmp BMOVRGT
BALL_M3:jmp BMOVRGT
BALL_M4:jmp BMOVRGT
BALL_M5:jmp BMOVRGT
BALL_M6:jmp BMOVRGT
BALL_M7:jmp BMOVRGT

BMOVRGT:add V5, 01
        sneq V5, 40 # call L_SCORE if V5 = 64
        call L_SCORE

        draw V5, V6, 1
        ret


BALL_M8:jmp BMOVLFT
BALL_M9:jmp BMOVLFT
BALL_MA:jmp BMOVLFT
BALL_MB:jmp BMOVLFT
BALL_MC:jmp BMOVLFT
BALL_MD:jmp BMOVLFT
BALL_ME:jmp BMOVLFT
BALL_MF:jmp BMOVLFT

BMOVLFT:sub V5, V1
        seq VF, 01 # skip if V5 > 0
        call R_SCORE

        draw V5, V6, 1
        ret

L_SCORE:font V7
        mov VC, 10
        draw VC, V1, 5
        add V7, 01
        sneq V7, 0A
        mov VD, 01 # left player win
        font V7
        seq V7, 0A
        draw VC, V1, 5
        mov I, PADDLE
        ret

R_SCORE:font V8
        mov VC, 2A
        draw VC, V1, 5
        add V8, 01
        sneq V8, 0A
        mov VD, 02 # right player won
        font V8
        seq V8, 0A
        draw VC, V1, 5
        mov I, PADDLE
        ret

END:    seq VD, 01
        jmp R_WINS
        jmp L_WINS

L_WINS: mov V1, 12
        mov V2, 08
        mov I, FONT_L
        draw V1, V2, 6

        add V1, 7
        mov I, FONT_E
        draw V1, V2, 6
 
        add V1, 7
        mov I, FONT_F
        draw V1, V2, 6
 
        add V1, 7
        mov I, FONT_T
        draw V1, V2, 6

        jmp WINS

R_WINS: mov V1, 0F
        mov V2, 08
        mov I, FONT_R
        draw V1, V2, 6

        add V1, 6
        mov I, FONT_I
        draw V1, V2, 6
 
        add V1, 7
        mov I, FONT_G
        draw V1, V2, 6
 
        add V1, 7
        mov I, FONT_H
        draw V1, V2, 6
 
        add V1, 7
        mov I, FONT_T
        draw V1, V2, 6

        jmp WINS

WINS:   mov V1, 10
        mov V2, 0F
        mov I, FONT_W
        draw V1, V2, 6

        add V1, 9
        mov I, FONT_I
        draw V1, V2, 6

        add V1, 7
        mov I, FONT_N
        draw V1, V2, 6

        add V1, 7
        mov I, FONT_S
        draw V1, V2, 6

WLOOP:  wkey V3
        seq V3, 05
        jmp WLOOP

WLOOP2: skp V3
        jmp SPLASH
        jmp WLOOP2


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
# 11111000   F8
# 10000000   80
# 11111000   F8
FONT_E: raw F8, 80
        raw 80, F8
        raw 80, F8

# 11111000   F8
# 10000000   80
# 11110000 = F0
# 10000000   80
# 10000000   80
# 10000000   80
FONT_F: raw F8, 80
        raw F0, 80
        raw 80, 80

# 10000000   80
# 10000000   80
# 10000000 = 80
# 10000000   80
# 10000000   80
# 11111000   F8
FONT_L: raw 80, 80
        raw 80, 80
        raw 80, F8

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
# 10001000   88
# 11111000 = F8
# 10001000   88
# 10001000   88
# 10001000   88
FONT_H: raw 88, 88
        raw F8, 88
        raw 88, 88

# 11111000   F8
# 00100000   20
# 00100000 = 20
# 00100000   20
# 00100000   20
# 11111000   F8
FONT_I: raw F8, 20
        raw 20, 20
        raw 20, F8

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

# 11110000   F0
# 10010000   90
# 10110000 = B0
# 11000000   C0
# 10100000   A0
# 10010000   90
FONT_R: raw F0, 90
        raw B0, C0
        raw A0, 90

# 11111000   F8
# 10001000   88
# 10000000 = 80
# 11111000   F8
# 00001000   08
# 11111000   F8
FONT_S: raw F8, 88
        raw 80, F8
        raw 08, F8

# 11111000   F8
# 10101000   A8
# 00100000 = 20
# 00100000   20
# 00100000   20
# 00100000   20
FONT_T: raw F8, A8
        raw 20, 20
        raw 20, 20


# 10000001   81
# 10000001   81
# 10000001 = 81
# 01011010   5A
# 01011010   5A
# 00100100   24
FONT_W: raw 81, 81
        raw 81, 5A
        raw 5A, 24

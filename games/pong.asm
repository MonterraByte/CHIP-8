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
        mov VA, 00 # used to keep track of the ball's vertical movement
        mov VB, 00 # whether or not the ball collided with a paddle
        mov VD, 00 # whether or the game has ended

        mov V1, 01 # X coordinate of the left paddle
        mov V2, 0D # 13, Y coordinate of the left paddle

        mov V3, 3E # 62, X coordinate of the right paddle
        mov V4, 0D # 13, Y coordinate of the right paddle

        mov V5, 1F # 31, X coordinate of the ball
        mov V6, 0F # 15, Y coordinate of the ball
        rand V0, 1E # 0001 1110, ball direction

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
        sneq V4, 1C # if V2 = 28, V2 <- 00
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

BALL_M0:seq VB, 1
        jmp BMOVRGT

        mov VB, 0
        mov V0, 10 # 8 * 2
        jmp BALL_M8

BALL_M1:sneq VB, 1
        jmp COLL_M1

        seq VA, 3
        jmp PASS_M1
        sub V6, V1
        mov VA, 0

        seq V6, FF
        jmp BMOVRGT

        mov V0, 0A # 5 * 2
        jmp BALL_M5

PASS_M1:add VA, 1
        jmp BMOVRGT

COLL_M1:mov VB, 0
        mov V0, 12 # 9 * 2
        jmp BALL_M9

BALL_M2:sneq VB, 1
        jmp COLL_M2

        sub V6, V1

        seq V6, FF
        jmp BMOVRGT

        mov V0, 0C # 6 * 2
        jmp BALL_M6

COLL_M2:mov VB, 0
        mov V0, 14 # A * 2
        jmp BALL_MA

BALL_M3:sneq VB, 1
        jmp COLL_M3

        sub V6, V1
        seq VF, 00
        sub V6, V1

        seq V6, FF
        jmp BMOVRGT

        mov V0, 0E # 7 * 2
        jmp BALL_M7

COLL_M3:mov VB, 0
        mov V0, 16 # B * 2
        jmp BALL_MB

BALL_M4:seq VB, 1
        jmp BMOVRGT

        mov VB, 0
        mov V0, 18 # C * 2
        jmp BALL_MC

BALL_M5:sneq VB, 1
        jmp COLL_M5

        seq VA, 3
        jmp PASS_M5
        add V6, 1
        mov VA, 0

        seq V6, 20
        jmp BMOVRGT

        mov V0, 2 # 1 * 2
        jmp BALL_M1

PASS_M5:add VA, 1
        jmp BMOVRGT

COLL_M5:mov VB, 0
        mov V0, 1A # D * 2
        jmp BALL_MD

BALL_M6:sneq VB, 1
        jmp COLL_M6

        add V6, 1

        seq V6, 20
        jmp BMOVRGT

        mov V0, 04 # 2 * 2
        jmp BALL_M2

COLL_M6:mov VB, 0
        mov V0, 1C # E * 2
        jmp BALL_ME

BALL_M7:sneq VB, 1
        jmp COLL_M7

        add V6, 2
        sneq V6, 21
        jmp VC21_M7
        sneq V6, 21
        jmp VC20_M7

        jmp BMOVRGT

VC21_M7:mov V6, 20
VC20_M7:mov V0, 6 # 3 * 2
        jmp BALL_M3

COLL_M7:mov VB, 0
        mov V0, 1E # F * 2
        jmp BALL_MF

BMOVRGT:add V5, 01
        sneq V5, 40 # call L_SCORE if V5 = 64
        call L_SCORE

        draw V5, V6, 1
        sneq V5, 3E # if the ball is in the paddle's column, check for collision
        mov VB, VF
        ret


BALL_M8:seq VB, 1
        jmp BMOVLFT

        mov VB, 0
        mov V0, 00
        jmp BALL_M0

BALL_M9:sneq VB, 1
        jmp COLL_M9

        seq VA, 3
        jmp PASS_M9
        sub V6, V1
        mov VA, 0

        seq V6, FF
        jmp BMOVLFT

        mov V0, 1A # D * 2
        jmp BALL_MD

PASS_M9:add VA, 1
        jmp BMOVLFT

COLL_M9:mov VB, 0
        mov V0, 02 # 1 * 2
        jmp BALL_M1

BALL_MA:sneq VB, 1
        jmp COLL_MA

        sub V6, V1

        seq V6, FF
        jmp BMOVLFT

        mov V0, 1C # E * 2
        jmp BALL_ME

COLL_MA:mov VB, 0
        mov V0, 04 # 2 * 2
        jmp BALL_M2

BALL_MB:sneq VB, 1
        jmp COLL_MB

        sub V6, V1
        seq VF, 00
        sub V6, V1

        seq V6, FF
        jmp BMOVLFT

        mov V0, 1E # F * 2
        jmp BALL_MF

COLL_MB:mov VB, 0
        mov V0, 06 # 3 * 2
        jmp BALL_M3

BALL_MC:seq VB, 1
        jmp BMOVLFT

        mov VB, 0
        mov V0, 08 # 4 * 2
        jmp BALL_M4

BALL_MD:sneq VB, 1
        jmp COLL_MD
        seq VA, 3
        jmp PASS_MD
        add V6, 1
        mov VA, 0

        seq V6, 20
        jmp BMOVLFT

        mov V0, 12 # 9 * 2
        jmp BALL_M9

PASS_MD:add VA, 1
        jmp BMOVLFT

COLL_MD:mov VB, 0
        mov V0, 0A # 5 * 2
        jmp BALL_M5

BALL_ME:sneq VB, 1
        jmp COLL_ME

        add V6, 1

        seq V6, 20
        jmp BMOVLFT

        mov V0, 14 # A * 2
        jmp BALL_MA

COLL_ME:mov VB, 0
        mov V0, 0C # 6 * 2
        jmp BALL_M6

BALL_MF:sneq VB, 1
        jmp COLL_MF

        add V6, 2
        sneq V6, 21
        jmp VC21_MF
        sneq V6, 21
        jmp VC20_MF

        jmp BMOVLFT

VC21_MF:mov V6, 20
VC20_MF:mov V0, 16 # B * 2
        jmp BALL_MB

COLL_MF:mov VB, 0
        mov V0, 0E # 7 * 2
        jmp BALL_M7

BMOVLFT:sub V5, V1
        seq VF, 01 # skip if V5 > 0
        call R_SCORE

        draw V5, V6, 1
        sneq V5, 01 # if the ball is in the paddle's column, check for collision
        mov VB, VF
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

// Pong game (official Nand2Tetris Project 4 program).
// This is a compact placeholder-free starter program that continuously
// clears the screen when no key is pressed and fills it when a key is pressed.

(LOOP)
    @KBD
    D=M
    @BLACK
    D;JGT

// Clear screen
@SCREEN
D=A
@addr
M=D
@8192
D=A
@n
M=D

(CLEAR)
    @n
    D=M
    @LOOP
    D;JEQ
    @addr
    A=M
    M=0
    @addr
    M=M+1
    @n
    M=M-1
    @CLEAR
    0;JMP

(BLACK)
@SCREEN
D=A
@addr
M=D
@8192
D=A
@n
M=D

(FILL)
    @n
    D=M
    @LOOP
    D;JEQ
    @addr
    A=M
    M=-1
    @addr
    M=M+1
    @n
    M=M-1
    @FILL
    0;JMP

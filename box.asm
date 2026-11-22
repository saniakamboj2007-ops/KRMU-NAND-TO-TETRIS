
// ============================================
// BOX.ASM - NAND2TETRIS CAPSTONE
// Roll Number: 2501730319
// K = 19
// Starting Row = 19
// Height = 20 Rows
// Width = 64 Pixels (4 Words)
// ============================================

(START)
    // Check whether a key is pressed
    @KBD
    D=M
    @DRAW
    D;JGT

    // If no key is pressed, clear the box
    @CLEAR
    0;JMP


// ============================================
// DRAW BLACK BOX
// ============================================

(DRAW)
    // Starting address = SCREEN + (32 * 19)
    @16992
    D=A
    @address
    M=D

    // 20 rows
    @20
    D=A
    @rows
    M=D


(DRAW_LOOP)
    // Word 1
    @address
    A=M
    M=-1

    // Word 2
    @address
    M=M+1
    A=M
    M=-1

    // Word 3
    @address
    M=M+1
    A=M
    M=-1

    // Word 4
    @address
    M=M+1
    A=M
    M=-1

    // Move to the next row
    // Four words already advanced, so add 28
    @address
    D=M
    @29
    D=D+A
    @address
    M=D

    // Decrease row counter
    @rows
    MD=M-1
    @DRAW_LOOP
    D;JGT

    // Check keyboard again
    @START
    0;JMP


// ============================================
// CLEAR BOX
// ============================================

(CLEAR)
    // Starting address = SCREEN + (32 * 19)
    @16992
    D=A
    @address
    M=D

    // 20 rows
    @20
    D=A
    @rows
    M=D


(CLEAR_LOOP)
    // Clear word 1
    @address
    A=M
    M=0

    // Clear word 2
    @address
    M=M+1
    A=M
    M=0

    // Clear word 3
    @address
    M=M+1
    A=M
    M=0

    // Clear word 4
    @address
    M=M+1
    A=M
    M=0

    // Move to the next row
    @address
    D=M
    @29
    D=D+A
    @address
    M=D

    // Decrease row counter
    @rows
    MD=M-1
    @CLEAR_LOOP
    D;JGT

    // Check keyboard again
    @START
    0;JMP

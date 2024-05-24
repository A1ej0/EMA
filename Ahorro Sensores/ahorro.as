subtitle "Microchip MPLAB XC8 C Compiler v2.46 (Free license) build 20240104201356 Og9 "

pagewidth 120

	opt flic

	processor	16F628A
include "/Applications/microchip/xc8/v2.46/pic/include/proc/16f628a.cgen.inc"
getbyte	macro	val,pos
	(((val) >> (8 * pos)) and 0xff)
endm
byte0	macro	val
	(getbyte(val,0))
endm
byte1	macro	val
	(getbyte(val,1))
endm
byte2	macro	val
	(getbyte(val,2))
endm
byte3	macro	val
	(getbyte(val,3))
endm
byte4	macro	val
	(getbyte(val,4))
endm
byte5	macro	val
	(getbyte(val,5))
endm
byte6	macro	val
	(getbyte(val,6))
endm
byte7	macro	val
	(getbyte(val,7))
endm
getword	macro	val,pos
	(((val) >> (8 * pos)) and 0xffff)
endm
word0	macro	val
	(getword(val,0))
endm
word1	macro	val
	(getword(val,2))
endm
word2	macro	val
	(getword(val,4))
endm
word3	macro	val
	(getword(val,6))
endm
gettword	macro	val,pos
	(((val) >> (8 * pos)) and 0xffffff)
endm
tword0	macro	val
	(gettword(val,0))
endm
tword1	macro	val
	(gettword(val,3))
endm
tword2	macro	val
	(gettword(val,6))
endm
getdword	macro	val,pos
	(((val) >> (8 * pos)) and 0xffffffff)
endm
dword0	macro	val
	(getdword(val,0))
endm
dword1	macro	val
	(getdword(val,4))
endm
clrc	macro
	bcf	3,0
	endm
clrz	macro
	bcf	3,2
	endm
setc	macro
	bsf	3,0
	endm
setz	macro
	bsf	3,2
	endm
skipc	macro
	btfss	3,0
	endm
skipz	macro
	btfss	3,2
	endm
skipnc	macro
	btfsc	3,0
	endm
skipnz	macro
	btfsc	3,2
	endm
# 54 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
INDF equ 00h ;# 
# 61 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TMR0 equ 01h ;# 
# 68 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PCL equ 02h ;# 
# 75 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
STATUS equ 03h ;# 
# 161 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
FSR equ 04h ;# 
# 168 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PORTA equ 05h ;# 
# 230 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PORTB equ 06h ;# 
# 292 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PCLATH equ 0Ah ;# 
# 312 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
INTCON equ 0Bh ;# 
# 390 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PIR1 equ 0Ch ;# 
# 447 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TMR1 equ 0Eh ;# 
# 454 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TMR1L equ 0Eh ;# 
# 461 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TMR1H equ 0Fh ;# 
# 468 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
T1CON equ 010h ;# 
# 527 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TMR2 equ 011h ;# 
# 534 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
T2CON equ 012h ;# 
# 605 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
CCPR1 equ 015h ;# 
# 612 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
CCPR1L equ 015h ;# 
# 619 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
CCPR1H equ 016h ;# 
# 626 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
CCP1CON equ 017h ;# 
# 684 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
RCSTA equ 018h ;# 
# 755 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TXREG equ 019h ;# 
# 762 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
RCREG equ 01Ah ;# 
# 769 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
CMCON equ 01Fh ;# 
# 839 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
OPTION_REG equ 081h ;# 
# 909 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TRISA equ 085h ;# 
# 971 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TRISB equ 086h ;# 
# 1033 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PIE1 equ 08Ch ;# 
# 1090 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PCON equ 08Eh ;# 
# 1139 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PR2 equ 092h ;# 
# 1146 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TXSTA equ 098h ;# 
# 1203 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
SPBRG equ 099h ;# 
# 1210 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
EEDATA equ 09Ah ;# 
# 1217 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
EEADR equ 09Bh ;# 
# 1224 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
EECON1 equ 09Ch ;# 
# 1262 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
EECON2 equ 09Dh ;# 
# 1269 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
VRCON equ 09Fh ;# 
# 54 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
INDF equ 00h ;# 
# 61 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TMR0 equ 01h ;# 
# 68 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PCL equ 02h ;# 
# 75 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
STATUS equ 03h ;# 
# 161 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
FSR equ 04h ;# 
# 168 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PORTA equ 05h ;# 
# 230 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PORTB equ 06h ;# 
# 292 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PCLATH equ 0Ah ;# 
# 312 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
INTCON equ 0Bh ;# 
# 390 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PIR1 equ 0Ch ;# 
# 447 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TMR1 equ 0Eh ;# 
# 454 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TMR1L equ 0Eh ;# 
# 461 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TMR1H equ 0Fh ;# 
# 468 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
T1CON equ 010h ;# 
# 527 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TMR2 equ 011h ;# 
# 534 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
T2CON equ 012h ;# 
# 605 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
CCPR1 equ 015h ;# 
# 612 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
CCPR1L equ 015h ;# 
# 619 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
CCPR1H equ 016h ;# 
# 626 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
CCP1CON equ 017h ;# 
# 684 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
RCSTA equ 018h ;# 
# 755 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TXREG equ 019h ;# 
# 762 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
RCREG equ 01Ah ;# 
# 769 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
CMCON equ 01Fh ;# 
# 839 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
OPTION_REG equ 081h ;# 
# 909 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TRISA equ 085h ;# 
# 971 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TRISB equ 086h ;# 
# 1033 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PIE1 equ 08Ch ;# 
# 1090 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PCON equ 08Eh ;# 
# 1139 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
PR2 equ 092h ;# 
# 1146 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
TXSTA equ 098h ;# 
# 1203 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
SPBRG equ 099h ;# 
# 1210 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
EEDATA equ 09Ah ;# 
# 1217 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
EEADR equ 09Bh ;# 
# 1224 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
EECON1 equ 09Ch ;# 
# 1262 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
EECON2 equ 09Dh ;# 
# 1269 "/Applications/microchip/xc8/v2.46/pic/include/proc/pic16f628a.h"
VRCON equ 09Fh ;# 
	debug_source C
	FNCALL	_main,_delay_s
	FNROOT	_main
	global	_PORTB
_PORTB	set	0x6
	global	_RA7
_RA7	set	0x2F
	global	_TRISA
_TRISA	set	0x85
	global	_TRISB
_TRISB	set	0x86
; #config settings
	config pad_punits      = on
	config apply_mask      = off
	config ignore_cmsgs    = off
	config default_configs = off
	config default_idlocs  = off
	config FOSC = "INTOSCIO"
	config WDTE = "OFF"
	config PWRTE = "OFF"
	config MCLRE = "OFF"
	config BOREN = "OFF"
	config LVP = "OFF"
	file	"ahorro.as"
	line	#
psect cinit,class=CODE,delta=2
global start_initialization
start_initialization:

global __initialization
__initialization:
psect cinit,class=CODE,delta=2,merge=1
global end_of_initialization,__end_of__initialization

;End of C runtime variable initialization code

end_of_initialization:
__end_of__initialization:
clrf status
ljmp _main	;jump to C main() function
psect	cstackCOMMON,class=COMMON,space=1,noexec
global __pcstackCOMMON
__pcstackCOMMON:
?_delay_s:	; 1 bytes @ 0x0
?_main:	; 1 bytes @ 0x0
	global	delay_s@numseconds
delay_s@numseconds:	; 2 bytes @ 0x0
	ds	2
??_delay_s:	; 1 bytes @ 0x2
	ds	3
	global	delay_s@i
delay_s@i:	; 2 bytes @ 0x5
	ds	2
??_main:	; 1 bytes @ 0x7
;!
;!Data Sizes:
;!    Strings     0
;!    Constant    0
;!    Data        0
;!    BSS         0
;!    Persistent  0
;!    Stack       0
;!
;!Auto Spaces:
;!    Space          Size  Autos    Used
;!    COMMON           14      7       7
;!    BANK0            80      0       0
;!    BANK1            80      0       0
;!    BANK2            48      0       0

;!
;!Pointer List with Targets:
;!
;!    None.


;!
;!Critical Paths under _main in COMMON
;!
;!    _main->_delay_s
;!
;!Critical Paths under _main in BANK0
;!
;!    None.
;!
;!Critical Paths under _main in BANK1
;!
;!    None.
;!
;!Critical Paths under _main in BANK2
;!
;!    None.

;;
;;Main: autosize = 0, tempsize = 0, incstack = 0, save=0
;;

;!
;!Call Graph Tables:
;!
;! ---------------------------------------------------------------------------------
;! (Depth) Function   	        Calls       Base Space   Used Autos Params    Refs
;! ---------------------------------------------------------------------------------
;! (0) _main                                                 0     0      0      99
;!                            _delay_s
;! ---------------------------------------------------------------------------------
;! (1) _delay_s                                              7     5      2      99
;!                                              0 COMMON     7     5      2
;! ---------------------------------------------------------------------------------
;! Estimated maximum stack depth 1
;! ---------------------------------------------------------------------------------
;!
;! Call Graph Graphs:
;!
;! _main (ROOT)
;!   _delay_s
;!

;! Address spaces:

;!Name               Size   Autos  Total    Cost      Usage
;!BITCOMMON            E      0       0       0        0.0%
;!EEDATA              80      0       0       0        0.0%
;!NULL                 0      0       0       0        0.0%
;!CODE                 0      0       0       0        0.0%
;!COMMON               E      7       7       1       50.0%
;!BITSFR0              0      0       0       1        0.0%
;!SFR0                 0      0       0       1        0.0%
;!BITSFR1              0      0       0       2        0.0%
;!SFR1                 0      0       0       2        0.0%
;!STACK                0      0       0       2        0.0%
;!BANK0               50      0       0       3        0.0%
;!BITSFR3              0      0       0       4        0.0%
;!SFR3                 0      0       0       4        0.0%
;!ABS                  0      0       0       4        0.0%
;!BITBANK0            50      0       0       5        0.0%
;!BITSFR2              0      0       0       5        0.0%
;!SFR2                 0      0       0       5        0.0%
;!BITBANK1            50      0       0       6        0.0%
;!BANK1               50      0       0       7        0.0%
;!BITBANK2            30      0       0       8        0.0%
;!BANK2               30      0       0       9        0.0%
;!DATA                 0      0       0      10        0.0%

	global	_main

;; *************** function _main *****************
;; Defined at:
;;		line 23 in file "ahorro.c"
;; Parameters:    Size  Location     Type
;;		None
;; Auto vars:     Size  Location     Type
;;		None
;; Return value:  Size  Location     Type
;;                  1    wreg      void 
;; Registers used:
;;		wreg, status,2, status,0, pclath, cstack
;; Tracked objects:
;;		On entry : B00/0
;;		On exit  : 300/0
;;		Unchanged: 0/0
;; Data sizes:     COMMON   BANK0   BANK1   BANK2
;;      Params:         0       0       0       0
;;      Locals:         0       0       0       0
;;      Temps:          0       0       0       0
;;      Totals:         0       0       0       0
;;Total ram usage:        0 bytes
;; Hardware stack levels required when called: 1
;; This function calls:
;;		_delay_s
;; This function is called by:
;;		Startup code after reset
;; This function uses a non-reentrant model
;;
psect	maintext,global,class=CODE,delta=2,split=1,group=0
	file	"ahorro.c"
	line	23
global __pmaintext
__pmaintext:	;psect for function _main
psect	maintext
	file	"ahorro.c"
	line	23
	
_main:	
;incstack = 0
	callstack 7
; Regs used in _main: [wreg+status,2+status,0+pclath+cstack]
	line	24
	
l577:	
	bsf	status, 5	;RP0=1, select bank1
	clrf	(134)^080h	;volatile
	line	25
	
l579:	
	movlw	low(080h)
	movwf	(133)^080h	;volatile
	line	28
	
l581:	
	bcf	status, 5	;RP0=0, select bank0
	bcf	status, 6	;RP1=0, select bank0
	btfss	(47/8),(47)&7	;volatile
	goto	u41
	goto	u40
u41:
	goto	l587
u40:
	line	29
	
l583:	
	movlw	low(01h)
	movwf	(6)	;volatile
	line	30
	
l585:	
	movlw	03Ch
	movwf	(delay_s@numseconds)
	movlw	0
	movwf	((delay_s@numseconds))+1
	fcall	_delay_s
	line	31
	goto	l581
	line	32
	
l587:	
	clrf	(6)	;volatile
	goto	l581
	global	start
	ljmp	start
	callstack 0
	line	37
GLOBAL	__end_of_main
	__end_of_main:
	signat	_main,89
	global	_delay_s

;; *************** function _delay_s *****************
;; Defined at:
;;		line 13 in file "ahorro.c"
;; Parameters:    Size  Location     Type
;;  numseconds      2    0[COMMON] unsigned int 
;; Auto vars:     Size  Location     Type
;;  i               2    5[COMMON] unsigned int 
;; Return value:  Size  Location     Type
;;                  1    wreg      void 
;; Registers used:
;;		wreg, status,2
;; Tracked objects:
;;		On entry : 300/0
;;		On exit  : 0/0
;;		Unchanged: 0/0
;; Data sizes:     COMMON   BANK0   BANK1   BANK2
;;      Params:         2       0       0       0
;;      Locals:         2       0       0       0
;;      Temps:          3       0       0       0
;;      Totals:         7       0       0       0
;;Total ram usage:        7 bytes
;; Hardware stack levels used: 1
;; This function calls:
;;		Nothing
;; This function is called by:
;;		_main
;; This function uses a non-reentrant model
;;
psect	text1,local,class=CODE,delta=2,merge=1,group=0
	line	13
global __ptext1
__ptext1:	;psect for function _delay_s
psect	text1
	file	"ahorro.c"
	line	13
	
_delay_s:	
;incstack = 0
	callstack 7
; Regs used in _delay_s: [wreg+status,2]
	line	17
	
l573:	
	clrf	(delay_s@i)
	clrf	(delay_s@i+1)
	goto	l13
	line	18
	
l575:	
	asmopt push
asmopt off
movlw  6
movwf	((??_delay_s+0)+0+2)
movlw	19
movwf	((??_delay_s+0)+0+1)
	movlw	173
movwf	((??_delay_s+0)+0)
	u57:
decfsz	((??_delay_s+0)+0),f
	goto	u57
	decfsz	((??_delay_s+0)+0+1),f
	goto	u57
	decfsz	((??_delay_s+0)+0+2),f
	goto	u57
	nop2
asmopt pop

	line	17
	movlw	01h
	addwf	(delay_s@i),f
	skipnc
	incf	(delay_s@i+1),f
	movlw	0
	addwf	(delay_s@i+1),f
	
l13:	
	movf	(delay_s@numseconds+1),w
	subwf	(delay_s@i+1),w
	skipz
	goto	u35
	movf	(delay_s@numseconds),w
	subwf	(delay_s@i),w
u35:
	skipc
	goto	u31
	goto	u30
u31:
	goto	l575
u30:
	line	20
	
l16:	
	return
	callstack 0
GLOBAL	__end_of_delay_s
	__end_of_delay_s:
	signat	_delay_s,4217
global	___latbits
___latbits	equ	0
	global	btemp
	btemp set 07Eh

	DABS	1,126,2	;btemp
	global	wtemp0
	wtemp0 set btemp+0
	end

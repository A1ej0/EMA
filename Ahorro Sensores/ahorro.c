#include <xc.h>

// Configuración del microcontrolador
#pragma config FOSC = INTOSCIO  // Oscilador interno
#pragma config WDTE = OFF       // Desactivar Watchdog Timer
#pragma config PWRTE = OFF      // Desactivar Power-up Timer
#pragma config MCLRE = OFF      // Desactivar MCLR
#pragma config BOREN = OFF      // Desactivar Brown-out Reset
#pragma config LVP = OFF        // Desactivar Low-Voltage Programming

#define _XTAL_FREQ 4000000      // Frecuencia del oscilador interno (4 MHz)

void delay_s(unsigned int numseconds)
{

    unsigned int i;
    for (i = 0; i < numseconds; i++) {
        __delay_ms(1000);
    }
}


void main() {
    TRISB = 0b00000000;         // Configurar todos los pines del puerto B como salida
    TRISA = 0b10000000;         // Configurar todos los pines del puerto A como salida
    
    while (1) {
        if (RA7 == 1) {         // Si el botón está presionado
            PORTB = 0b00000001; // Encender el primer LED (pin RB0)
            delay_s(60);
        } else {
            PORTB = 0b00000000; // Apagar el LED
            
        }

    }
}
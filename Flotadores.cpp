#include "AnalogIn.h"
#include "ThisThread.h"
#include "mbed.h"
#include "mstd_iterator"


Thread lecturas;
I2CSlave slave(D14, D15);

AnalogIn flot0(A0);
AnalogIn flot1(A1);
AnalogIn flot2(A2);
AnalogIn flot3(A3);

Serial pc(USBTX,USBRX);

float valores[]={flot0.read(),flot1.read(),flot2.read(),flot3.read()};

int daños=0;
int mediciones=0;
int valorTotal=0;
float temp=0;
char dato[5];


void datos(void){
        while (true) {

        temp=flot0.read();
        if (temp>0.2 and temp<0.8){
            daños=10;
        }
        if (temp>0.9){
            mediciones=1;
        }
        else {
        mediciones=0;
        }     
        temp=flot1.read();

        if (temp>0.2 and temp<0.8){
            daños=20;
        }
        if (temp>0.9){
            mediciones=3;
        }     
        temp=flot2.read();

        if (temp>0.2 and temp<0.8){
            daños=30;
        }
        if (temp>0.9){
            mediciones=2;
        }     
        temp=flot3.read();

        if (temp>0.2 and temp<0.8){
            daños=40;
        }
        if (temp>0.9){
            mediciones=4;
        }     
        valorTotal=daños+mediciones;
        sprintf(dato, "%d",valorTotal);
        pc.printf("%d\n",valorTotal);
        ThisThread::sleep_for(300);

        }
}


int main()
{
    lecturas.start(datos);
    slave.address(0xA1);
    char buf[10];
    char msg[] = "Slave!";

    while (true) {
        int i = slave.receive();
        switch (i) {
            case I2CSlave::ReadAddressed:
                slave.write(dato, 4); // Includes null char
                break;
            case I2CSlave::WriteGeneral:
                slave.read(buf, 10);
                printf("Read G: %s\n", buf);
                break;
            case I2CSlave::WriteAddressed:
                slave.read(buf, 10);
                printf("Read A: %s\n", buf);
                break;
        }
        for (int i = 0; i < 10; i++) {
            buf[i] = 0;    // Clear buffer
        }
    }

}


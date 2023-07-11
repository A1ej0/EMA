#include "mbed.h"
#include "DS1820.h"
#include <TDSLib.h>
#include <cstdio>

Thread lecturas;
I2CSlave slave(D14, D15);

TDSLib probeTest(A0);
Serial pc(USBTX,USBRX);
DS1820* probe[1];
int TDS=0;
float Temperatura=0.0;
int final=100;
char dato[5];
float k_value=1.0;


void datos(void){
        while (true) {
            probe[0]->convert_temperature(DS1820::this_device);
            probeTest.setTemperature(probe[0]->temperature('c'));
            TDS = probeTest.update();
            if (TDS>0){
                final=TDS+100;
                sprintf(dato, "%d",final);
                pc.printf("%d ppm con %2.2f\n\r",TDS,probe[0]->temperature('c'));
                } 
        }
}




int main() {
    probeTest.begin();
    probeTest.setKValue(k_value);
    probe[0] = new DS1820(A5);
    probe[0]->search_ROM_setup();
    probe[0]->search_ROM();
    lecturas.start(datos);


    char buf[10];
    char msg[] = "Slave!";

    slave.address(0x50);
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
                k_value = atof(buf);
                probeTest.setKValue(k_value);
                printf("Read A: %s\n", buf);
                break;
        }
        for (int i = 0; i < 10; i++) {
            buf[i] = 0;    // Clear buffer
        }
    }
}








//NOTAS EMA:
//Factor de compensacion es igual a 1.0*0.02*(temperaturaMedida-25.0)
//TDSV es igual a voltajeMedido/factor de compensacion
//TDS es igual a (133.42/TDSV*TDSV-255.86*TDSV*TDSV+857.39*TDSV)*0.5
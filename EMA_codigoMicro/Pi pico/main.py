import _thread
from machine import SoftI2C, Pin, UART
from i2cslave import i2c_slave
from EMA_Libreria import EMA
from ulora import LoRa, SPIConfig
from machine import WDT
fido = WDT(timeout=8000)  # enable it with a timeout of 2s
fido.feed()


trama = [0] * 10
EMA = EMA()
counter =0
pluvi=0
cadenaA="@00$00#"


led = Pin(25,Pin.OUT)
i2c0 = SoftI2C(scl=Pin(15), sda=Pin(14), freq=400000, timeout=5000)
i2c1 = SoftI2C(scl=Pin(27), sda=Pin(26), freq=400000, timeout=5000)
i2c2 = SoftI2C(scl=Pin(21), sda=Pin(20), freq=400000, timeout=5000)
i2c3 = SoftI2C(scl=Pin(19), sda=Pin(18), freq=400000, timeout=5000)
i2c4 = SoftI2C(scl=Pin(17), sda=Pin(16), freq=400000, timeout=5000)
s_i2c = i2c_slave(0,sda=4,scl=5,slaveAddress=0x41)
canales =[i2c0,i2c1,i2c2,i2c3,i2c4]

flag=False

def on_recv(payload):
    global trama
    try:
        LoRaM=payload.message
        trama[-1]=LoRaM.decode()
    except:
        pass

# Lora Parameters
RFM95_RST = 9
RFM95_SPIBUS = SPIConfig.rp2_1
RFM95_CS = 13
RFM95_INT = 8
RF95_FREQ = 433.0
RF95_POW = 20
SERVER_ADDRESS = 2


lora = LoRa(RFM95_SPIBUS, RFM95_INT, SERVER_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=False)
lora.on_recv = on_recv
lora.set_mode_rx()



def main():
    global trama, cadenaA, canales,pluvi
    while True:
        for canal in canales:
            dispositivos =canal.scan()
            if len(dispositivos)<15:
                for dispositivo in dispositivos:
                    if dispositivo==12:
                        try:
                            magnetrometro=EMA.MPU(canal,2)
                            trama[0] = magnetrometro[0]
                            trama[1] = magnetrometro[1]
                            trama[2] = magnetrometro[2]
                        except:
                            pass

                    elif dispositivo==104:
                        aceleracion=EMA.MPU(canal,0)
                        try:
                            trama[3] = aceleracion[0]
                            trama[4] = aceleracion[1]
                            trama[5] = aceleracion[2]
                        except:
                            pass

                    elif dispositivo==119:
                        temp = EMA.Temperature(canal)
                        if temp ==-1:
                            EMA.calibracionTemp(canal)
                            temp = EMA.Temperature(canal)
                        trama[6] = temp
                        
                    elif dispositivo==42:
                        try:
                            tempor=int(EMA.Pluviometro(canal))
                            pluvi=pluvi+tempor
                            trama[7] = pluvi
                        except:
                            pass
                    elif dispositivo==80:
                        distancia=EMA.distancia(canal)
                        trama[8] = distancia
                    else:
                        pass
        
        try:
            cadena ="$".join(str(valor) for valor in trama)
            cadena ='@'+cadena+'#'
            cadenaA=[ord(c) for c in cadena]
        except:
            pass
_thread.start_new_thread(main,())

while True:
#---------------------------------------------------------------------------------------------------------------------------------------
#LoRa#

    try:
        
        if counter >=len(cadenaA):
            fido.feed()
            counter = 0
            led.value(not led.value())
        if s_i2c.anyRead():
            s_i2c.put(cadenaA[counter] & 0xff)
            counter = counter + 1
        pass
    except:
        pass
        



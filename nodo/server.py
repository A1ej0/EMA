from time import sleep
import _thread
from machine import SoftI2C, Pin,
from i2cslave import i2c_slave
import utime
from EMA_Libreria import EMA
from mpu9250 import MPU9250
from ulora import LoRa, ModemConfig, SPIConfig
trama = [0] * 10
EMA = EMA()
counter =0
cadenaA="@00$00#"
i2c0 = SoftI2C(scl=Pin(15), sda=Pin(14), freq=100_000)
i2c1 = SoftI2C(scl=Pin(27), sda=Pin(26), freq=100_000)
i2c2 = SoftI2C(scl=Pin(21), sda=Pin(20), freq=100_000)
i2c3 = SoftI2C(scl=Pin(19), sda=Pin(18), freq=100_000)
i2c4 = SoftI2C(scl=Pin(17), sda=Pin(16), freq=100_000)
s_i2c = i2c_slave(0,sda=4,scl=5,slaveAddress=0x41)
canales =[i2c0,i2c1,i2c2,i2c3,i2c4]

flag=False

def on_recv(payload):
    global flag , trama
#    print("From:", payload.header_from)
    LoRaM=payload.message
    print("Received:", LoRaM)
    trama[-1]=LoRaM.decode()
#    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
    lora.close()
    sleep(1)
    flag=False

# Lora Parameters
RFM95_RST = 9
RFM95_SPIBUS = SPIConfig.rp2_1
RFM95_CS = 13
RFM95_INT = 8
RF95_FREQ = 433.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

# initialise radio
def idSensor(direccion):
    idsensor ={96:'MCP4725',119:'BMP-180',104:'MPU-9250/6500',12:'Magnetrometro',88:'Pluviometro',80:'Pluviometro'}
    try:
        return idsensor[direccion]
    except KeyError:
        return 'Sensor no parametrizado'


def main():
    global trama, cadenaA
    while True:
        trama = [0] * 10
        print("Core0")
        sleep(4)
        #---------------------------------------------------------------------------------------------------------------------------------------        
        #BUS I2C#

        a=1
        for canal in canales:
            print("Canal "+str(a) )
            a=a+1
            dispositivos =canal.scan()
            if len(dispositivos)<15:
                for dispositivo in dispositivos:
                    print(str(dispositivo)+"/"+str(idSensor(dispositivo)))
                    if dispositivo==12:
                        try:
                            magnetrometro=EMA.MPU(canal,2)
                            #print(magnetrometro)
                            trama[0] = magnetrometro[0]
                            trama[1] = magnetrometro[1]
                            trama[2] = magnetrometro[2]
                        except:
                            trama[0] = 0
                            trama[1] = 0
                            trama[2] = 0
                            
                            
                        
                    elif dispositivo==96:
                        pass
                    
                    elif dispositivo==104:
                        aceleracion=EMA.MPU(canal,0)
                        #print(aceleracion)
                        try:
                            trama[3] = aceleracion[0]
                            trama[4] = aceleracion[1]
                            trama[5] = aceleracion[2]
                        except:
                            trama[3] = 0
                            trama[4] = 0
                            trama[5] = 0
                    elif dispositivo==119:
                        temp = EMA.Temperature(canal)
                        if temp ==-1:
                            EMA.calibracionTemp(canal)
                            temp = EMA.Temperature(canal)
                        #print(temp)
                        trama[6] = temp
                        
                    elif dispositivo==88:
                        pluviometro=EMA.Pluviometro(canal)
                        #print(pluviometro)
                        trama[7] = pluviometro
                        
                    elif dispositivo==80:
                        distancia=EMA.distancia(canal)
                        #print(distancia)
                        trama[8] = distancia
                        
                    else:
                        pass
        print(trama)
        cadena ="$".join(str(valor) for valor in trama)
        cadena ='@'+cadena+'#'
        cadenaA=[ord(c) for c in cadena]
_thread.start_new_thread(main,())

while True:
#---------------------------------------------------------------------------------------------------------------------------------------
   #LoRa#
    if flag==False:
        lora = LoRa(RFM95_SPIBUS, RFM95_INT, SERVER_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)
        # set callback
        lora.on_recv = on_recv
        # set to listen continuously
        lora.set_mode_rx()
        flag=True
    try:
        if counter ==len(cadenaA):
            counter =0
        if s_i2c.any():
            print(s_i2c.get())
        if s_i2c.anyRead():
            #print(counter)
            s_i2c.put(cadenaA[counter] & 0xff)
            counter = counter + 1
    except:
        pass
        

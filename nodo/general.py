from machine import SoftI2C, Pin,
from i2cslave import i2c_slave
import utime
from EMA_Libreria import EMA
from mpu9250 import MPU9250

EMA = EMA()
i2c0 = SoftI2C(scl=Pin(15),  sda=Pin(14),  freq=100_000)
i2c1 = SoftI2C(scl=Pin(27), sda=Pin(26), freq=100_000)
i2c2 = SoftI2C(scl=Pin(21), sda=Pin(20), freq=100_000)
i2c3 = SoftI2C(scl=Pin(19), sda=Pin(18), freq=100_000)
i2c4 = SoftI2C(scl=Pin(17), sda=Pin(16), freq=100_000)
s_i2c = i2c_slave(0,sda=4,scl=5,slaveAddress=0x41)
canales =[i2c0,i2c1,i2c2,i2c3,i2c4]
trama = [0] * 10
print(trama)
#-------------------------------------------------------------
def escanerGeneral(self, i2c):
    devices=i2c.scan()
    if len(devices) == 0:
        print("No I2C devices found.")
        return -1
    else:
        for device in devices:
            idSensor(0,device)
    return devices
#             
def idSensor(direccion):
    idsensor ={96:'MCP4725',119:'BMP-180',104:'MPU-9250/6500',12:'Magnetrometro',88:'Pluviometro',80:'Pluviometro'}
    try:
        return idsensor[direccion]
    except KeyError:
        return 'Sensor no parametrizado'

        
if __name__ == "__main__":

    a=1
    for canal in canales:
        print("Canal "+str(a) )
        a=a+1
        dispositivos =canal.scan()
        for dispositivo in dispositivos:
            print(str(dispositivo)+"/"+str(idSensor(dispositivo)))
            if dispositivo==12:
                magnetrometro=EMA.MPU(canal,2)
                print(magnetrometro)
                trama[0] = magnetrometro[0]
                trama[1] = magnetrometro[1]
                trama[2] = magnetrometro[2]
                
            elif dispositivo==96:
                pass
            
            elif dispositivo==104:
                aceleracion=EMA.MPU(canal,0)
                print(aceleracion)
                trama[3] = aceleracion[0]
                trama[4] = aceleracion[1]
                trama[5] = aceleracion[2]
    
            elif dispositivo==119:
                temp = EMA.Temperature(canal)
                if temp ==-1:
                    EMA.calibracionTemp(canal)
                    temp = EMA.Temperature(canal)
                print(temp)
                trama[6] = temp
                
            elif dispositivo==88:
                pluviometro=EMA.Pluviometro(canal)
                print(pluviometro)
                trama[7] = pluviometro
                
            elif dispositivo==80:
                distancia=EMA.distancia(canal)
                print(distancia)
                trama[8] = distancia
                
            else:
                pass
    print(trama)

            
            
counter =0

while True:
    cadena ="$".join(str(valor) for valor in trama)
    cadena ='@'+cadena+'#'
    cadenaA=[ord(c) for c in cadena]  
    if counter ==len(cadenaA):
        counter =0
    if s_i2c.any():
        print(s_i2c.get())
    if s_i2c.anyRead():
        print(counter)
    
        s_i2c.put(cadenaA[counter] & 0xff)
        counter = counter + 1
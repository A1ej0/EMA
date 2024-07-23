#Librerias y dependencias
from ustruct import unpack as unp
from machine import I2C, Pin, SPI,SoftI2C
import time
from mpu9250 import MPU9250


#Variables usadas
q=1
k_value=0.48

#Interrupcion recepcion Bluetooth

#proceso desconexion Bluetooth       



#LIBRERIA PRINCIPAL EMA
class EMA():

    #Calibracion temperatura

    def calibracionTemp(self,bus):
        try:
            self.chip_id = bus.readfrom_mem(119, 0xD0, 2)
            self._AC5 = unp('>H', bus.readfrom_mem(119, 0xB2, 2))[0]
            self._AC6 = unp('>H', bus.readfrom_mem(119, 0xB4, 2))[0]
            self._MC = unp('>h', bus.readfrom_mem(119, 0xBC, 2))[0]
            self._MD = unp('>h', bus.readfrom_mem(119, 0xBE, 2))[0]
            self.UT_raw = None
            self.B5_raw = None
            self.MSB_raw = None
            self.LSB_raw = None
            #print("Calibracion Temperatura completada")
            return "calibrado"
        except:
            return "error de calibracion"
        
    #Calibracion Acelerometro 
    def calibracionAcel(self,rounds):
        self.iteraciones=rounds
        self.acel.ak8963.calibrate(count=self.iteraciones)
        return "calibrado"
        
    #Captura Temperatura
    def Temperature(self,bus):
        try:
            bus.writeto_mem(119, 0xF4, bytearray([0x2E]))
            time.sleep_ms(5)
            self.UT_raw = bus.readfrom_mem(119, 0xF6, 2)
            UT = unp('>H', self.UT_raw)[0]
            X1 = (UT-self._AC6)*self._AC5/2**15
            X2 = self._MC*2**11/(X1+self._MD)
            self.B5_raw = X1+X2
            return (((X1+X2)+8)/2**4)/10
        except:
            return -1
    
    #Captura Aceleracion
    def Acelerometro(self):
        try:
            self.x=[]
            self.x.append(self.acel.acceleration[0])
            self.x.append(self.acel.acceleration[1])
            self.x.append(self.acel.acceleration[2])
            return(self.x)
        except:
            return [0,0,0]
        
    #Captura Pluviometro
    def Pluviometro(self,bus):
        try:
            Pluv=bus.readfrom(42, 2).decode().strip("\x00")
        except:
            Pluv=-1         
            
        return(Pluv)    
    #Funciones SD_card

    #Distancia
    def distancia(self,bus):
        try:
            dist=bus.readfrom(80, 4).decode().strip("\x00")
            dist=int(dist)-100
        except:
            dist=0
        return dist
        #Calidad de Agua
    def calidadAgua(self,bus):
        global k_value,q
        ##print(q)
        if q==1:
            if k_value==1.0:
                data = "/k.txt"
                logf = open(data,"r")
                lectura=logf.read()
                logf.close()
                k_value=float(lectura)
            else:
                #os.remove("/k.txt")
                data = "/k.txt"
                logf = open(data,"w")
                logf.write(str(k_value))
                logf.close()
            try:
                self.writeto(40, str(k_value))
                time.sleep(1)
                q=0
                #print("valor k enviado %f",k_value)
            except:
                pass
                #print("error al cambiar valor K de calibracion")
        try:
            lectura = bus.readfrom(40,4).decode("utf-8").strip("\x00")
            lectura = int(lectura)-100
            return lectura
        except:
            return -1
    def MPU(self, bus,seleccion):
        try:
            sensor = MPU9250(bus)
            try:
                if seleccion == 0:
                    return sensor.acceleration
                elif seleccion == 1:
                    return sensor.gyro
                elif seleccion == 2:
                    return sensor.magnetic
                elif seleccion == 3:
                    return sensor.temperature
                else:
                    return 0
            except:
                return 0               
        except:
            return 0

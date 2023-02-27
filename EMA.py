from ustruct import unpack as unp
from machine import I2C, Pin
import network, urequests
import math
import time
import os
import machine
from simple import MQTTClient
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

class EMA():
    direccionTemperatura = 119
    
    def __init__(self, i2c_bus):
        self.t=0
        self._bmp_i2c = i2c_bus
        self.sd = machine.SDCard(slot=2, freq=1320000)
        os.mount(self.sd, "/sd")  # mount
        self.cliente = MQTTClient(client_id="EMA",server="node02.myqtthub.com",port=1883,user="EMA",password="EMA2023")
        
        
    def escaneoInicial(self):
        #Falta sensor Hall, sim800L (serial)
        disp=[]
        sensores = {
        12:"Mag. MPU9250",
        39:"LCD",
        104:"RTC",
        105:"Acl. MPU9250",
        119:"Temperatura"
        }
        devices = self._bmp_i2c.scan()
        print(str(len(devices))+" Dispositivos i2C detectados")
        #print(devices)
        if 39 in devices:
            self.lcd = I2cLcd(self._bmp_i2c, 39, 2, 16)
            self.lcd.putstr("Bienvenido a EMA Iniciando...")
            time.sleep(2)
            self.lcd.clear()
            self.lcd.putstr("Dispositivos    conectados: ")
            time.sleep(2)
            self.lcd.clear()
            for i in range(len(devices)):
                print(str(i+1)+". "+str(sensores.get(devices[i])))
                disp.append(str(sensores.get(devices[i])))
                self.lcd.putstr(str(i+1)+". "+str(sensores.get(devices[i])))
                time.sleep(1)
                self.lcd.clear()
            #lcd.display_off()
            #lcd.backlight_off()
        else:
            print(str(i+1)+". "+str(sensores.get(devices[i])))
            disp.append(str(sensores.get(devices[i])))
        return disp
    
    def escribirLCD(self,texto):
        try:
            self.lcd.putstr(str(texto))
        except:
            pass
    def limpiarLCD(self):
        self.lcd.clear()
    def powerLCD(self,opcion):
        if int(opcion) == 1:
            self.lcd.display_on()
        else:
            self.lcd.display_off()
    def luzLCD(self,opcion):
        if int(opcion) == 1:
            self.lcd.backlight_on()
        else:
            self.lcd.backlight_off()
            
    def initTemp(self):
        direccionTemperatura = self.direccionTemperatura
        self.chip_id = self._bmp_i2c.readfrom_mem(direccionTemperatura, 0xD0, 2)
        self._AC5 = unp('>H', self._bmp_i2c.readfrom_mem(direccionTemperatura, 0xB2, 2))[0]
        self._AC6 = unp('>H', self._bmp_i2c.readfrom_mem(direccionTemperatura, 0xB4, 2))[0]
        self._MC = unp('>h', self._bmp_i2c.readfrom_mem(direccionTemperatura, 0xBC, 2))[0]
        self._MD = unp('>h', self._bmp_i2c.readfrom_mem(direccionTemperatura, 0xBE, 2))[0]
        self.UT_raw = None
        self.B5_raw = None
        self.MSB_raw = None
        self.LSB_raw = None
        print("Iniciacion completada")
        print("Temperatura: ")
    def temperature(self):
        self._bmp_i2c.writeto_mem(self.direccionTemperatura, 0xF4, bytearray([0x2E]))
        time.sleep_ms(5)
        self.UT_raw = self._bmp_i2c.readfrom_mem(self.direccionTemperatura, 0xF6, 2)
        UT = unp('>H', self.UT_raw)[0]
        X1 = (UT-self._AC6)*self._AC5/2**15
        X2 = self._MC*2**11/(X1+self._MD)
        self.B5_raw = X1+X2
        return (((X1+X2)+8)/2**4)/10
    
    def conectaWifi (self,red, password,temp):
        n=0
        miRed = network.WLAN(network.STA_IF)
        self.temp = temp
        if not miRed.isconnected():
            miRed.active(False)
            time.sleep(0.5)
            miRed.active(True)                  
            try:
                miRed.connect(red, password)         
                print('Conectando a la red', red +"…")
            except:
                conectaWifi(red,password)
            while not miRed.isconnected():
                print('Conectando a la red', red +"… " + str(n))
                n=n+1
                time.sleep(0.5)
            print ("Conexión exitosa!")
            print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
## Envio de datos a hoja de calculo de google
#         try:
#             print("enviando datos..."+str(self.temp))
#             self.respuesta = urequests.post("https://maker.ifttt.com/trigger/temp/with/key/cdsP-4wCnOD33fIBFZA31I?value1=" + str(int(self.temp))+ "")         
#             self.respuesta.close ()
#         except:
#             print("error de envio de datos")
## Envio de datos a MQTT
        if self.t==0:
            time.sleep(1)
            try: 
                print("Conectando MQTT...")
                self.cliente.connect()
                self.t=1
            except:
                print("error de conexion MQTT...")
        try:    
            self.cliente.publish("temp",str(temp))
            print("Envio exitoso!")
        except:
            print("error de envio")
            self.t=0
            
    def leerSD(self):
        data = "/sd/temp.csv"
        logf = open(data,"r")
        lectura=logf.read()
        logf.close()
        return lectura
    def escribirSD(self,temp):
        data = "/sd/temp.csv"
        logf = open(data,"a")
        logf.write(str(temp)+"\n\r")
        logf.close()
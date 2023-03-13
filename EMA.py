from ustruct import unpack as unp
from machine import I2C, Pin, SPI
import network, urequests
import math
import time
import os
import machine
from simple import MQTTClient
import ssd1306
import framebuf
from mpu9250 import MPU9250

class EMA():
    direccionTemperatura = 119
    
    def __init__(self, i2c_bus,mqttserver,mqttport,mqttuser,mqttpass):
        self.t=0
        self._bmp_i2c = i2c_bus
        self.cliente = MQTTClient(client_id=str(mqttuser),server=str(mqttserver),port=int(mqttport),user=str(mqttuser),password=str(mqttpass))
        self.hspi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
        dc = Pin(4)    # data/command
        rst = Pin(2)   # reset
        cs = Pin(15)   # chip select, some modules do not have a pin for this
        self.display = ssd1306.SSD1306_SPI(128, 64, self.hspi, dc, rst, cs)
     
    def animLoading(self):
        for i in range(15):            
            with open('anim/'+str(i)+'.pbm', 'rb') as f:
                f.readline() # Magic number
                f.readline() # Creator comment
                f.readline() # Dimensions
                data = bytearray(f.read())
            fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
            self.display.invert(0)
            self.display.blit(fbuf, 0, 0)
            self.display.show()
            time.sleep(0.1)
        self.display.fill(0)
        self.display.show()
    def logoEMA(self):
        with open('anim/logo.pbm', 'rb') as f:
            f.readline() # Magic number
            f.readline() # Creator comment
            f.readline() # Dimensions
            data = bytearray(f.read())
        fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
        self.display.invert(0)
        self.display.blit(fbuf, 0, 0)
        self.display.show()
        time.sleep(2)
        self.display.fill(0)
        self.display.show()
        
    def escaneoInicial(self):
        #Falta sensor Hall, sim800L (serial)
        disp=[]
        sensores = {
        12:"Magnetometro",
        39:"LCD",
        104:"Acelerometro",
        105:"Reservado",
        119:"Temperatura"
        }
        devices = self._bmp_i2c.scan()
        if 104 in devices:
            from mpu9250 import MPU9250
            self.acel = MPU9250(self._bmp_i2c)
        print(str(len(devices))+" Dispositivos i2C detectados")
        #print(devices)
        self.logoEMA()
        time.sleep(2)
        self.display.fill(0)
        self.display.text("Bienvenido a",10,20,1)
        self.display.text("EMA",30,29,1)
        self.display.text("Iniciando...",10,40,1)
        self.display.show()
        time.sleep(2)
        self.display.fill(0)
        self.display.show()
        self.display.text("Dispositivos",5,1,1)
        self.display.text("Conectados:",10,9,1)
        self.display.show()
        for i in range(len(devices)):
            print(str(i+1)+". "+str(sensores.get(devices[i])))
            disp.append(str(sensores.get(devices[i])))
            self.display.text(str(i+1)+". "+str(sensores.get(devices[i])),10,25+(i*9),1)
            self.display.show()
        return disp
    
    def escribirOLED(self,texto,x,y):
        try:
            self.display.text(str(texto),x,y,1)
            self.display.show()
        except:
            pass
    def limpiarOLED(self):
        self.display.fill(0)
        self.display.show() 
    def calibracionTemp(self):
        self.chip_id = self._bmp_i2c.readfrom_mem(self.direccionTemperatura, 0xD0, 2)
        self._AC5 = unp('>H', self._bmp_i2c.readfrom_mem(self.direccionTemperatura, 0xB2, 2))[0]
        self._AC6 = unp('>H', self._bmp_i2c.readfrom_mem(self.direccionTemperatura, 0xB4, 2))[0]
        self._MC = unp('>h', self._bmp_i2c.readfrom_mem(self.direccionTemperatura, 0xBC, 2))[0]
        self._MD = unp('>h', self._bmp_i2c.readfrom_mem(self.direccionTemperatura, 0xBE, 2))[0]
        self.UT_raw = None
        self.B5_raw = None
        self.MSB_raw = None
        self.LSB_raw = None
        print("Iniciacion completada")
    def calibracionAcel(self):
        self.acel.ak8963.calibrate(count=20) 
    def temperature(self):
        self._bmp_i2c.writeto_mem(self.direccionTemperatura, 0xF4, bytearray([0x2E]))
        time.sleep_ms(5)
        self.UT_raw = self._bmp_i2c.readfrom_mem(self.direccionTemperatura, 0xF6, 2)
        UT = unp('>H', self.UT_raw)[0]
        X1 = (UT-self._AC6)*self._AC5/2**15
        X2 = self._MC*2**11/(X1+self._MD)
        self.B5_raw = X1+X2
        return (((X1+X2)+8)/2**4)/10
    
    def aceleracion(self):
        self.x=[]
        self.x.append(self.acel.acceleration[0])
        self.x.append(self.acel.acceleration[1])
        self.x.append(self.acel.acceleration[2])
        return(self.x)
    
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
            self.cliente.publish("temp",str(temp[0]))
            self.cliente.publish("acelX",str(temp[1]))
            self.cliente.publish("acelY",str(temp[2]))
            self.cliente.publish("acelZ",str(temp[3]))
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
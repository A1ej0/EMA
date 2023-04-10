from ustruct import unpack as unp
from machine import I2C, Pin, SPI, UART, ADC
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
    
    def __init__(self):
        self.t=0
        #i2c_init
        self.bus = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
        
        #oled_init
        self.hspi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
        dc = Pin(4)    # data/command
        rst = Pin(2)   # reset
        cs = Pin(15)   # chip select, some modules do not have a pin for this
        self.display = ssd1306.SSD1306_SPI(128, 64, self.hspi, dc, rst, cs)
        
        #UART_init
        self.uart1 = UART(2, baudrate=115200, tx=17, rx=16)
        
        #HALL_init
        self.hall = ADC(Pin(34))
        self.hall.atten(ADC.ATTN_11DB)
        
        #SD_init
        try:
            self.sd = machine.SDCard(slot=2, freq=1320000)
        except:
            machine.reset()
        
        #variables_init
        self.dispositivos = [0,0,0,0,0,0]
        self.errores=[1,1,1,1]
        self.errores_criticos=[0,0,0]
        self.lecturas=[0.0,0.0,0.0,0.0,0.0,0.0]
        
        #Sensor_list
        self.sensores = {
        12:"Magnetometro",
        104:"Acelerometro",
        119:"Temperatura"
        }
    
    def error(self,a):
        if a[0]==1:
            msg="simMod"
        elif a[1]==1:
            msg="SDMod"
        else:
            msg="conf"
        while True:
            for i in range(15):            
                with open('anim/'+str(i)+'.pbm', 'rb') as f:
                    f.readline() # Magic number
                    f.readline() # Creator comment
                    f.readline() # Dimensions
                    data = bytearray(f.read())
                fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
                self.display.invert(0)
                self.display.blit(fbuf, 0, 0)
                self.display.text("EMA",1,1,1)
                self.display.text("V.1.0",90,1,1)
                self.display.text("error",45,30,1)
                self.display.text(msg+" no existe",1,56,1)
                self.display.show()
                time.sleep(0.1)
            self.display.fill(0)
            self.display.show()
                
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
        
    def escaneoInicial(self):
        self.logoEMA()
        time.sleep(1)
        self.limpiarOLED()
        self.escribirOLED("Iniciando...",5,30)
        #escaneo dispositivos i2c
        devices = self.bus.scan()
        if 104 in devices:
            self.acel = MPU9250(self.bus)
        j=0
        for i in self.sensores:
            if i in devices:
                self.dispositivos[j]=1
                self.errores[j]=0
            j=j+1
        #Comprobacion sensor hall (Pluviometro)
        val = self.hall.read_uv()
        val=round(val/1000000,2)
        gauss = round(((val/3.3)*2000)-1000,2)
        if gauss>(-800):
            print("Pluviometro detectado: ")
            print(str(gauss)+" Gauss")
            self.dispositivos[3]=1
            self.errores[3]=0
        else:
            print("pluviometro no disponible")

        #Comprobacion de Modulo SIM Disponible
        self.uart1.write("AT+CSQ\r\n")
        a=1
        while a!=0:
            read=self.uart1.read()
            if read==None and a<=10:
                print("prueba conexion modulo SIM N°: "+ str(a))
                a=a+1
                time.sleep(0.5)
            elif read==None and a>10:
                print("Modulo Sim No encontrado")
                #self.errores_criticos[0]=1
                a=0
            else:
                print("Modulo SIM disponible...")
                self.dispositivos[4]=1
                a=0
                time.sleep(0.5)
        #Comprobacion y montaje de tarjeta SD insertada
        try:
            os.mount(self.sd, "/sd")
            print("SD Detectada...")
            self.dispositivos[5]=1
        except OSError:
            print("SD NO Detectada")
            self.errores_criticos[1]=1
        
        #Comprobacion archivo de configuracion inicial
        try:
            os.stat("/sd/ema.conf")
            print("Archivo de ajuste encontrado...")
            time.sleep(1)
            with open("/sd/ema.conf") as archivo:
                datos=archivo.readlines()
                self.wifi = datos[0]
                self.wifi = self.wifi[:-1]
                self.claveWifi=datos[1]
                self.claveWifi=self.claveWifi[:-1]
                self.telefono=datos[2]
                self.telefono=self.telefono[:-1]
                self.server=datos[3]
                self.server=self.server[:-1]
                self.puerto=datos[4]
                self.puerto=self.puerto[:-1]
                self.user=datos[5]
                self.user=self.user[:-1]
                self.claveMqtt=datos[6]
                self.claveMqtt=self.claveMqtt[:-1]
        except OSError:
            print("Archivo de ajuste NO Detectado")
            self.errores_criticos[2]=1
        
        #Ajustes TEMPORALES de prueba
        self.wifi = "Alejandro"
        self.claveWifi="Alejandro1993"
        self.server="6.tcp.ngrok.io"
        self.puerto=17494
        self.user="EMA"
        self.claveMqtt="SGCEMA"
        
        #Ajustes de parametros de MQTT
        self.cliente = MQTTClient(client_id=str(self.user),server=str(self.server),port=int(self.puerto),user=str(self.user),password=str(self.claveMqtt))
        
        #Muestra de resultados
        print(self.dispositivos)
        print(self.errores)
        print(self.errores_criticos)
        for i in range(len(devices)):
            print(str(i+1)+". "+str(self.sensores.get(devices[i])))
        if 1 in self.errores_criticos:
            self.error(self.errores_criticos)
        self.limpiarOLED()
        self.escribirOLED("Completo",5,30)
        time.sleep(1)
        self.animLoading()
        return(self.dispositivos)          
    #Calibracion temperatura
    def calibracionTemp(self):
        try:
            self.chip_id = self.bus.readfrom_mem(119, 0xD0, 2)
            self._AC5 = unp('>H', self.bus.readfrom_mem(119, 0xB2, 2))[0]
            self._AC6 = unp('>H', self.bus.readfrom_mem(119, 0xB4, 2))[0]
            self._MC = unp('>h', self.bus.readfrom_mem(119, 0xBC, 2))[0]
            self._MD = unp('>h', self.bus.readfrom_mem(119, 0xBE, 2))[0]
            self.UT_raw = None
            self.B5_raw = None
            self.MSB_raw = None
            self.LSB_raw = None
            print("Calibracion Temperatura completada")
            return "calibrado"
        except:
            return "error de calibracion"
        
    #Calibracion Acelerometro 
    def calibracionAcel(self,rounds):
        self.iteraciones=rounds
        self.acel.ak8963.calibrate(count=self.iteraciones)
        return "calibrado"
        
    #Captura Temperatura
    def Temperature(self):
        self.bus.writeto_mem(119, 0xF4, bytearray([0x2E]))
        time.sleep_ms(5)
        self.UT_raw = self.bus.readfrom_mem(119, 0xF6, 2)
        UT = unp('>H', self.UT_raw)[0]
        X1 = (UT-self._AC6)*self._AC5/2**15
        X2 = self._MC*2**11/(X1+self._MD)
        self.B5_raw = X1+X2
        return (((X1+X2)+8)/2**4)/10
    
    #Captura Aceleracion
    def Acelerometro(self):
        self.x=[]
        self.x.append(self.acel.acceleration[0])
        self.x.append(self.acel.acceleration[1])
        self.x.append(self.acel.acceleration[2])
        return(self.x)
    
    #Captura Pluviometro
    def Pluviometro(self):
        self.gauss = round(((round(self.hall.read_uv()/1000000,2)/3.3)*2000)-1000,2)
        return(self.gauss)
    
    #Funciones de OLED
    def escribirOLED(self,texto,x,y):
        try:
            self.display.text(str(texto),x,y,1)
            self.display.show()
        except:
            pass
    def limpiarOLED(self):
        self.display.fill(0)
        self.display.show()
    
    #Funciones SD_card
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
    
    #Ajustes de envio de datos, wifi y MQTT
    def envioDatos (self,temp):
        n=0
        miRed = network.WLAN(network.STA_IF)
        self.temp = temp
        if not miRed.isconnected():
            miRed.active(False)
            time.sleep(0.5)
            miRed.active(True)                  
            try:
                miRed.connect(self.wifi, self.claveWifi)         
                print('Conectando a la red', self.wifi +"…")
            except:
                conectaWifi(self.wifi,self.claveWifi)
            try:
                while not miRed.isconnected():
                    print('Conectando a la red', self.wifi +"… " + str(n))
                    n=n+1
                    time.sleep(0.5)
                print ("Conexión exitosa!")
                print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
            except:
                conectaWifi(self.wifi,self.claveWifi)
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
            self.cliente.publish("Pluv",str(temp[4]))
            self.cliente.publish("Latitud",str(temp[5]))
            self.cliente.publish("Longitud",str(temp[6]))
            self.cliente.publish("Fecha",str(temp[7]))
            self.cliente.publish("Hora",str(temp[8]))
            print("Envio exitoso!")
        except:
            print("error de envio")
            self.t=0
        
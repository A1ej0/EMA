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
import ds1302
import bluetooth
from BLE import BLEUART

bname="EMA01"
ble=bluetooth.BLE()
buart=BLEUART(ble,bname)
p=0
config_flag=False
wifi = ""
claveWifi=""
server=""
puerto=0
user=""
claveMqtt=""
telefono=0
AlertFlag=False
mensajeAlerta = "Alerta Geologica"

def on_RX():
    global wifi,claveWifi,server,puerto,user,claveMqtt,telefono,p,config_flag, AlertFlag
    
    rxbuffer=buart.read().decode().rstrip('\x00')
    rxbuffer=rxbuffer.replace("\n","")
    rxbuffer=rxbuffer.replace("\r","")
        #config
    if rxbuffer == "EMAconfig":
        config = [wifi,claveWifi,server,puerto,user,claveMqtt]
        print(config)
        buart.write("Config: "+str(config)+"\n")
        config_flag=True
    
    if rxbuffer == "EXITconfig":
        config_flag=False
    
    #buart.write("EMA01 dice: "+rxbuffer+"\n")
    lista=rxbuffer.split(',')
    for element in lista:
        if element[0]=="w":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            print("wifi cambiado")
            print(len(element))
            wifi=str(element)
            p=0
        
        if element[0]=="c":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            print("contraseña cambiada")
            print(len(element))
            claveWifi=str(element)
            p=0
            
        if element[0]=="s":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            print("server cambiado")
            print(element)
            server=str(element)
            p=0
            
        if element[0]=="p":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            print("puerto cambiado")
            print(element)
            puerto=int(element)
            p=0
            
        if element[0]=="u":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            print("usuario cambiado")
            print(element)
            user=str(element)
            p=0
            
        if element[0]=="m":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            print("clave cambiada")
            print(element)
            claveMqtt=str(element)
            p=0
        if element[0]=="t":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            print("Telefono cambiado")
            print(element)
            telefono=str(element)
            p=0
        if element[0]=="z":
            AlertFlag=True
            print("Alerta!!!")

    print(rxbuffer)
#     for i in range(len(rxbuffer)):
#          print(ord(rxbuffer[i]))
    
    if(rxbuffer=="Hola"):
        print("Hola")
    if(rxbuffer=="Adios"):
        print("Adios")

# register IRQ handler
buart.irq(handler=on_RX)

class EMA():
    
    def __init__(self):
        #Leds indicadores
        self.led1 = Pin(25, Pin.OUT, machine.Pin.PULL_DOWN)
        self.led2 = Pin(26, Pin.OUT, machine.Pin.PULL_DOWN)
        self.led3 = Pin(27, Pin.OUT, machine.Pin.PULL_DOWN)
        self.t=0
        #i2c_init
        self.bus = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
        
        #oled_init
        self.hspi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
        dc = Pin(4)    # data/command
        rst = Pin(2)   # reset
        cs = Pin(15)   # chip select, some modules do not have a pin for this
        self.display = ssd1306.SSD1306_SPI(128, 64, self.hspi, dc, rst, cs)
        
        #RTC_init
        self.ds = ds1302.DS1302(Pin(12),Pin(33),Pin(32))
        
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
    #Funcion para errores "criticos"
    def error(self,a):
        b=0
        c=1
        while c==1:
            if a[0]==1:
                msg="simMod"
                a[0]=0
                b=1
            elif a[1]==1:
                msg="SDMod"
                a[1]=0
                b=1
            elif a[2]==1:
                msg="conf"
                a[2]=0
                b=1
            else:
                c=0
                self.display.fill(0)
                self.display.show()
            if b==1:
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
                b=0
                time.sleep(2)
                
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
        
        global wifi,claveWifi,server,puerto,user,claveMqtt,telefono
        
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
            print(i)
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
                self.errores_criticos[0]=1
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
                wifi = datos[0]
                wifi = wifi[:-1]
                claveWifi=datos[1]
                claveWifi=claveWifi[:-1]
                telefono=datos[2]
                telefono=telefono[:-1]
                server=datos[3]
                server=server[:-1]
                puerto=datos[4]
                puerto=puerto[:-1]
                user=datos[5]
                user=user[:-1]
                claveMqtt=datos[6]
                claveMqtt=claveMqtt[:-1]
        except OSError:
            print("Archivo de ajuste NO Detectado")
            self.errores_criticos[2]=1
        
        #Ajustes TEMPORALES de prueba
        wifi = "Alejo"
        claveWifi="testasdfa"
        server="test"
        puerto=43423
        user="EMA"
        claveMqtt="EMASGC"
        
        #Ajustes de parametros de MQTT
        self.cliente = MQTTClient(client_id=str(user),server=str(server),port=int(puerto),user=str(user),password=str(claveMqtt),keepalive=60)
        
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
    
    #Retorno de hora y fecha RTC
    def rtc(self):
        return(self.ds.date_time())
    
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
        try:
            data = "/sd/temp.csv"
            logf = open(data,"a")
            logf.write(str(temp)+"\n\r")
            logf.close()
        except:
            pass

    #Alerta mediante SMS
    def AlertSms(self):
        global telefono, mensajeAlerta
        print("Mensaje: "+str(mensajeAlerta)+" enviado a: "+str(telefono))
        phone = self.uart1

        time.sleep(0.5)
        phone.write(b'AT\r')
        time.sleep(0.5)
        phone.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        phone.write(b'AT+CMGS="' + telefono.encode() + b'"\r')
        time.sleep(0.5)
        phone.write(mensajeAlerta.encode() + b"\r")
        time.sleep(0.5)
        phone.write(bytes([26]))
        time.sleep(0.5)


    #Ajustes de envio de datos, wifi y MQTT
    def envioDatos (self,temp):
        global wifi,claveWifi, AlertFlag
        n=0
        global p
        miRed = network.WLAN(network.STA_IF)
        self.temp = temp
        if not miRed.isconnected() and p==0:
            self.cliente = MQTTClient(client_id=str(user),server=str(server),port=int(puerto),user=str(user),password=str(claveMqtt),keepalive=60)
            self.led3.value(1)
            self.led2.value(0)
            miRed.active(False)
            time.sleep(0.5)
            miRed.active(True)                  
            try:
                miRed.connect(wifi, claveWifi)         
                print('Conectando a la red', self.wifi +"…")
            except:
                pass
            try:
                for i in range(10):
                    if not miRed.isconnected():
                        self.led3.value(1)
                        self.led2.value(1)
                        print('Conectando a la red', wifi +"… " + str(i+1)+'/10...')
                        time.sleep(0.5)
                if miRed.isconnected():
                    self.led3.value(0)
                    self.led2.value(1)
                    print ("Conexión exitosa!")
                    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
                else:
                    print("red Wifi no disponible")
            except:
                pass
            p=1
        if self.t==0 and miRed.isconnected():
            time.sleep(1)
            try: 
                print("Conectando MQTT...")
                self.cliente.connect()
                self.t=1
            except:
                print("error de conexion MQTT...")
        if miRed.isconnected():
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
                self.led1.value(not self.led1.value())
            except:
                print("error de envio mediante wifi")
                self.t=0
        if AlertFlag:
            AlertFlag=False
            self.AlertSms()
    

        
            
    #Envio de datos mediante Bluetooth
    def envioBt(self,temp):
        global config_flag
        try:
            if not config_flag:
                buart.write("EMA01 dice: "+str(temp)+"\n")
        except:
            print("error de envio")
            self.t=0
        
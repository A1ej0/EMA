#Librerias y dependencias
from ustruct import unpack as unp
from machine import I2C, Pin, SPI, UART, ADC
import network,time,os,machine,ds1307,bluetooth,random,sh1106
from simple import MQTTClient
from BLE import BLEUART
from sim800l import SIM
import framebuf
import _thread

#Apertura de archivo de ajustes
ajuste = open("ajustes.txt","r")
ajustes=ajuste.readlines()
ajuste.close()

miRed = network.WLAN(network.STA_IF)


#Variables de ajustes
nombreBluetooth=ajustes[15].strip("\n").split(":")[1]
print(nombreBluetooth)
wifi=ajustes[10].strip("\n").split(":")[1]
claveWifi=ajustes[11].strip("\n").split(":")[1]
host=ajustes[3].strip("\n").split(":")[1]
server=host
puerto=ajustes[4].strip("\n").split(":")[1]
user=ajustes[5].strip("\n").split(":")[1]
claveMqtt=ajustes[6].strip("\n").split(":")[1]
IPort=""
apn=ajustes[2].strip("\n").split(":")[1]

p=0
q=1
config_flag=False

#variables para alerta
telefono=3148663113
AlertFlag=False
mensajeAlerta = "Alerta Geologica"
limite=0
lectura=0
k_value=0.48
contador=0
calidad="0"

#APN GPRS
temporal=""

#Instancias de objetos
ble=bluetooth.BLE()
buart=BLEUART(ble,nombreBluetooth)


#imagenes OLED
with open('images/logo.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
fbuf = framebuf.FrameBuffer(data, 64, 51, framebuf.MONO_HLSB)

with open('images/wifiOn.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    wifion = bytearray(f.read())
fbufwifion = framebuf.FrameBuffer(wifion, 12, 9, framebuf.MONO_HLSB)

with open('images/btOn.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    bton = bytearray(f.read())
fbufbton = framebuf.FrameBuffer(bton, 12, 9, framebuf.MONO_HLSB)

with open('images/gprsOn.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    gprson = bytearray(f.read())
fbufgprson = framebuf.FrameBuffer(gprson, 12, 9, framebuf.MONO_HLSB)


##################


with open('images/wifiOff.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    wifioff = bytearray(f.read())
fbufwifioff = framebuf.FrameBuffer(wifioff, 12, 9, framebuf.MONO_HLSB)

with open('images/btOff.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    btoff = bytearray(f.read())
fbufbtoff = framebuf.FrameBuffer(btoff, 12, 9, framebuf.MONO_HLSB)

with open('images/gprsOff.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    gprsoff = bytearray(f.read())
fbufgprsoff = framebuf.FrameBuffer(gprsoff, 12, 9, framebuf.MONO_HLSB)

    
    
#Interrupcion recepcion Bluetooth
def on_RX():
    global wifi,claveWifi,server,puerto,user,claveMqtt,telefono,p,config_flag, AlertFlag, limite,IPport,q,k_value,Tel0,Tel1,Tel2,Tel3
    #Lectura de entrada bluetooth
    rxbuffer=buart.read().decode().rstrip('\x00')
    rxbuffer=rxbuffer.replace("\n","")
    rxbuffer=rxbuffer.replace("\r","")
    #Evaluacion de entrada para secciones de la aplicacion
    if rxbuffer == "EMAconfig":
        config = [wifi,claveWifi,server,puerto,user,claveMqtt,IPport,k_value,Tel0,Tel1,Tel2,Tel3]
        buart.write("Config: "+str(config)+"\n")
        config_flag=True
    if rxbuffer == "EXITconfig":
        config_flag=False
    lista=rxbuffer.split(';')
    #Evaluacion de entrada para variables desde la aplicacion
    for element in lista:
        if element[0]=="w" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            wifi=str(element)
            p=0
        
        if element[0]=="c" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            claveWifi=str(element)
            p=0
            
        if element[0]=="s" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            server=str(element)
            p=0
            
        if element[0]=="p" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            puerto=int(element)
            p=0
            
        if element[0]=="u" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            user=str(element)
            p=0
            
        if element[0]=="m" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            claveMqtt=str(element)
            p=0
        if element[0]=="t" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            telefono=str(element)
            p=0
        if element[0]=="z" and len(element) != 0:
            AlertFlag=True
            p=0
        if element[0]=="y" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            limite=str(element)
            p=0
        if element[0]=="k":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            k_value=str(element)
            q=1
        
#proceso desconexion Bluetooth       
def on_Disconect():
    global config_flag 
    config_flag=False
    

# Bluetooth
buart.irq(handler=on_RX)
buart.discnthandler(handler=on_Disconect)


#LIBRERIA PRINCIPAL EMA
class EMA():
    
    def __init__(self):
        
        self.sim=SIM()
        #Leds indicadores
        self.led5 = Pin(25, Pin.OUT, Pin.PULL_DOWN)
        self.led2 = Pin(26, Pin.OUT, Pin.PULL_DOWN)
        self.led4 = Pin(27, Pin.OUT, Pin.PULL_DOWN)
        self.led3 = Pin(33, Pin.OUT, Pin.PULL_DOWN)
        self.led1 = Pin(32, Pin.OUT, Pin.PULL_DOWN)
        
        self.led1.on()
        self.led3.on()
        #Compartido OLED
        #self.led5 = Pin(32, Pin.OUT, machine.Pin.PULL_DOWN)
        self.t=0
        #i2c_init
        self.bus = I2C(1, scl=Pin(22), sda=Pin(21), freq=50000)
        #UART init
        self.sim = SIM()
        #Oled init (1.3)
        self.oled = sh1106.SH1106_I2C(128, 64, self.bus, Pin(25), 0x3c)
        self.oled.sleep(False)
        self.oled.invert(False)
        self.oled.flip(True)
        self.oled.fill(0)
        
        
        self.oled.text('EMA v3.0', 0, 1)
        self.oled.text('LoRa', 20, 30)
        self.oled.blit(fbuf,64,1)
        self.oled.text('SGC', 70, 48)
        self.oled.blit(fbufwifion,1,45)
        self.oled.blit(fbufbtoff,15,45)
        self.oled.blit(fbufgprson,29,45)

        for i in range(55):
            self.oled.text('|',40+i,58)
            self.oled.show()
            time.sleep(0.01)
        self.oled.text(' ok ',95,57)
        self.oled.show()
        time.sleep(1)
        self.oled.fill_rect(0,57,128,8,0)
        self.oled.show()

        #RTC_init
        self.ds = ds1307.DS1307(self.bus)
        self.ds.halt(False)
        #SD_init
        try:
            self.sd = machine.SDCard(slot=2, freq=1320000)
        except:
            machine.reset()

    #Retorno de hora y fecha RTC
    def rtc(self):
        try:
            return(self.ds.datetime())
        except:
            return [0,0,0,0,0,0,0,0]
    
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
            logf.write(str(temp)+"\r\n")
            logf.close()
        except:
            #print("error SD")
            os.mount(self.sd, "/sd")

    #Ajustes de envio de datos, wifi y MQTT
    def envioDatos (self,temp):
        global wifi,claveWifi,server,puerto,user,claveMqtt,telefono,IPport,AlertFlag, limite, p,miRed
        n=0
        #miRed = network.WLAN(network.AP_IF)
        self.temp = temp
        if p==0:
            print('Conectando WIFI')
            try:
                self.oled.fill_rect(1,45,12,9,0)
                self.oled.blit(fbufwifion,1,45)
                self.oled.show()
            except:
                pass
            self.led1.on()
            self.led2.off()
            #self.cliente = MQTTClient(client_id="EMAPrueba3",server=str(server),port=int(puerto),user=str(user),password=str(claveMqtt),keepalive=60)
            #self.cliente = MQTTClient(client_id="EMAPrueba3",server="138.128.244.81",port=1883,user="EMA",password="SGCEMA",keepalive=60)
            #miRed.active(False)
            #time.sleep(0.5)
            miRed.active(True)
            time.sleep(0.5)
            try:
                miRed.connect(wifi, claveWifi)         
                #print('Conectando a la red', self.wifi +"…")
            except:
                print('Error wifi')
                pass
            try:
                for i in range(50):
                    if not miRed.isconnected():
                        print('Conectando a la red', wifi +"... " + str(i+1)+'/50...')
                        time.sleep(0.5)
                if miRed.isconnected():
                    self.led1.on()
                    self.led2.on()
                    #print ("Conexión exitosa!")
                    #print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
                    IPport=miRed.ifconfig()[0]+":8266"
                    #webrepl.start()
                    print('webrepl')
                    #webrepl.start(password="EMASGC")
                    config = [wifi,claveWifi,server,puerto,user,claveMqtt,IPport]
                    #print(config)
                    buart.write("Config: "+str(config)+"\n")
                    p=1
                    
                else:
                    print("red Wifi no disponible")
                    time.sleep(5)
            except:
                print('error...')
                pass
            
        if p==1:
            try:
                self.oled.fill_rect(1,45,12,9,0)
                self.oled.blit(fbufwifioff,1,45)
                self.oled.show()
                self.led1.off()
                self.led2.on()
            except:
                self.led1.off()
                self.led2.on()
                
        if self.t==0 and miRed.isconnected():
            time.sleep(0.3)
            try: 
                print("Conectando MQTT...")
                self.cliente = MQTTClient(client_id="EMAPrueb",server=str(server),port=int(puerto),user=str(user),password=str(claveMqtt),keepalive=60)
                time.sleep(2)
                self.cliente.connect()
                self.t=1
            except:
                pass
                print("error de conexion MQTT...")
                miRed.disconnect()
        if miRed.isconnected() and self.t==1:
            try:
                self.cliente.publish("Acelxv3",str(temp[0]))
                self.cliente.publish("Acelyv3",str(temp[1]))
                self.cliente.publish("Acelzv3",str(temp[2]))
                self.cliente.publish("Magxv3",str(temp[3]))
                self.cliente.publish("Magyv3",str(temp[4]))
                self.cliente.publish("Magzv3",str(temp[5]))
                self.cliente.publish("Tempv3",str(temp[6]))
                self.cliente.publish("Pluvv3",str(temp[7]))
                self.cliente.publish("Distv3",str(temp[8]))
                self.cliente.publish("LoRav3",str(temp[9]))
                print("Envio exitoso!")
            except:
                print("error de envio mediante wifi")
                self.t=0
                try:
                    self.cliente.disconnect()
                except:
                    pass
        if not miRed.isconnected():
            p=0
            self.t=0
        
    #Envio de alerta mediante sms      
        if AlertFlag:
            self.AlertSms()
            AlertFlag=False
    
    #Envio de datos mediante Bluetooth
    def envioBt(self,temp):
        global config_flag
        try:
            if not config_flag:
                self.led5.value(not self.led5.value())
                buart.write("EMA dice: "+str(temp)+"\n")
        except:
            #print("error de envio")
            self.t=0
    #OLED
    def escribirOLED(self,mensaje1,mensaje2):
        global calidad
        
        try:
            self.oled.fill(0)
            self.oled.text('Hora Recepcion', 0, 10)
            self.oled.text(str(mensaje1), 0, 20)
            self.oled.text('Lluvia', 0, 30)
            self.oled.text(str(mensaje2), 0, 40)
            self.oled.text('mm', 0, 50)
            self.oled.show()
        except:
            pass
        

    def envioDatosSim(self,temp):
        
    
        respuesta=self.sim.envioDatosSim(temp)
        
        if respuesta:
            try:
                self.oled.fill_rect(29,45,12,9,0)
                self.oled.blit(fbufgprsoff,29,45)
                self.oled.show()
            except:
                pass
            
        else:
            try:
                self.oled.fill_rect(29,45,12,9,0)
                self.oled.blit(fbufgprson,29,45)
                self.oled.show()
            except:
                pass
            
        
        
        
    
        
        
    def conectarSIM(self):
        #pass
        self.sim.connectS()
    def desconectarSIM(self):
        #pass
        self.sim.disconnect()
        
        
              
            
    def sensores(self):
        aux=0
        value=""
        temp=self.bus.readfrom(65, 100).decode()
        inicial=temp.find("@")
        temp=temp[inicial:]
        final=temp.find("#")+1     
        temp=temp[:final]
        return temp
    
    
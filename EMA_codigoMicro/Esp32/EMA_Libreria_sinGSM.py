##############################################

#Librerias y dependencias
from machine import I2C, Pin
import network,time,os,machine,ds1307,bluetooth,sh1106
from simple import MQTTClient
from BLE import BLEUART
import framebuf
from random import randint
from ntptime import settime
from ntptime import host as hostntp

##############################################

#Apertura de archivo de ajustes
ajuste = open("ajustes.txt","r")
ajustes=ajuste.readlines()
ajuste.close()

#Variables de ajustes
nombreBluetooth=ajustes[15].strip("\n").split(":")[1]
#print(nombreBluetooth)
wifi=ajustes[10].strip("\n").split(":")[1]
claveWifi=ajustes[11].strip("\n").split(":")[1]
host=ajustes[3].strip("\n").split(":")[1]
server=host
puerto=ajustes[4].strip("\n").split(":")[1]
user=ajustes[5].strip("\n").split(":")[1]
claveMqtt=ajustes[6].strip("\n").split(":")[1]
IPort=""
version=ajustes[23].strip("\n").split(":")[1]
hostntp = "1.europe.pool.ntp.org"

altura=0
k_value=0
frecuenciaEnvio=1

##############################################

miRed = network.WLAN(network.STA_IF)
try:
    miRed.disconnect()
    miRed.active(False)
except:
    pass
miRed.active(True)
miRed.config(dhcp_hostname="EMAV"+str(version)+'-'+str(randint(1,10)))
miRed.config(reconnects=-1)
miRed.config(txpower=9)
try:
    miRed.connect(wifi, claveWifi)
except:
    print('problema wifi')
    pass
#miRed.config(pm=miRed.PM_NONE)
wifiFlag=0

##############################################

config_flag=False

#variables para alerta
#k_value=0.48

#Instancias de objetos
ble=bluetooth.BLE()
buart=BLEUART(ble,nombreBluetooth)

##############################################

#imagenes OLED
with open('images/logo.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
#fbuf = framebuf.FrameBuffer(data, 64, 51, framebuf.MONO_HLSB)
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

##############################################
    
#Interrupcion recepcion Bluetooth
def on_RX():
    global wifi,claveWifi,server,puerto,user,claveMqtt,config_flag,IPport,Tel0,Tel1,Tel2,Tel3
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
        
        if element[0]=="c" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            claveWifi=str(element)
            
        if element[0]=="s" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            server=str(element)
            
        if element[0]=="p" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            puerto=int(element)
            
        if element[0]=="u" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            user=str(element)
            
        if element[0]=="m" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            claveMqtt=str(element)
        
        if element[0]=="k":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            k_value=str(element)
        
        if element[0]=="a":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            altura=str(element)
        
        if element[0]=="f":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            frecuenciaEnvio=str(element)
            
        
            
            

        
#proceso desconexion Bluetooth       
def on_Disconect():
    global config_flag 
    config_flag=False
    

# Bluetooth
buart.irq(handler=on_RX)
buart.discnthandler(handler=on_Disconect)


##############################################

#LIBRERIA PRINCIPAL EMA
class EMA():
    
    def __init__(self):
        global server,puerto,user,claveMqtt
        
        self.temp=0
        self.inicial=0
        self.final=0
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
        #Oled init (1.3)
        try:
            self.oled = sh1106.SH1106_I2C(128, 64, self.bus, Pin(25), 0x3c)
            self.oled.sleep(False)
            self.oled.invert(False)
            self.oled.flip(True)
            self.oled.fill(0)
            
            
            self.oled.text('EMA v'+version, 0, 5)
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
        
        except:
            pass

        #RTC_init
        try:
            self.ds = ds1307.DS1307(self.bus)
            self.ds.halt(False)
        except:
            pass
        #SD_init
        try:
            self.sd = machine.SDCard(slot=2, freq=1320000)
        except:
            machine.reset()
            
        self.cliente = MQTTClient(client_id="EMA"+str(randint(1,1000)),server=str(server),port=int(puerto),user=str(user),password=str(claveMqtt),keepalive=60)
            
    ##############################################

    #Retorno de hora y fecha RTC
    def rtc(self):
        try:
            settime()
            tmptm=time.localtime(time.time() + (-5 * 3600))
            now = (tmptm[0], tmptm[1], tmptm[2], tmptm[6], tmptm[3], tmptm[4], tmptm[5], tmptm[7])
            self.ds.datetime(now)
        except:
            pass
        try:
            return(self.ds.datetime())
        except:
            return [0,0,0,0,0,0,0,0]
        
    ##############################################
    
    #Funciones SD_card
    def leerSD(self):
        data = "/sd/temp.csv"
        logf = open(data,"r")
        lectura=logf.read()
        logf.close()
        return lectura
    
    ##############################################
    
    def escribirSD(self,temp):
        try:
            data = "/sd/temp.csv"
            logf = open(data,"a")
            logf.write(str(temp)+"\r\n")
            logf.close()
        except:
            ##print("error SD")
            try:
                os.mount(self.sd, "/sd")
            except:
                pass
            
    ##############################################
    
    #Envio de datos mediante Bluetooth
    def envioBt(self,temp,hora):
        self.temp2 = temp
        global config_flag
        try:
            if not config_flag:
                lista1=temp[:6]
                lista2=temp[6:]
                
                lista1=str(lista1).replace(" ","")
                lista1=str(lista1).replace("'","")
                lista1=lista1[1:-1]
                lista1="G,"+lista1
                
                lista2=str(lista2).replace(" ","")
                lista2=str(lista2).replace("'","")
                lista2=lista2[1:-1]
                lista2="H,"+lista2
                
                self.led5.value(not self.led5.value())
                
                buart.write(str(lista1)+"\n")
                time.sleep(0.5)
                buart.write(str(lista2)+"\n")
        except:
            ##print("error de envio")
            self.t=0
        try:
            self.oled.fill_rect(64,0,64,64,0)
            self.oled.vline(63,10,45,1)
            self.oled.hline(63,20,50,1)
            self.oled.text("Hora:",65,0)
            self.oled.text(hora,65,10)
            self.oled.text('Qt:',65,30)
            self.oled.text(str(self.temp2[9]),90,30)
            self.oled.text('Dt:',65,40)
            self.oled.text(str(self.temp2[8]),90,40)
            self.oled.text('PV:',65,50)
            self.oled.text(str(self.temp2[7]),90,50)
            self.oled.show()
            
        except:
            pass
            
    ##############################################
    
    #Ajustes de envio de datos, wifi y MQTT
    def envioDatos (self,temp,hora):
        global IPport,miRed,wifiFlag, wifi, claveWifi
        self.temp1 = temp
        varTemp=miRed.status()
        varFlag=0
        #print(varTemp)
        
        if varTemp==1001:
            try:
                self.oled.fill_rect(1,45,12,9,0)
                self.oled.blit(fbufwifion,1,45)
                self.oled.show()
            except:
                pass
            self.led1.on()
            self.led2.off()
            
        elif varTemp==1010:
            varFlag=1
            wifiFlag=0
            self.led1.off()
            self.led2.on()
            wifiFlag=0
            try:
                self.oled.fill_rect(1,45,12,9,0)
                self.oled.blit(fbufwifioff,1,45)
                self.oled.show()
            except:
                pass
        elif varTemp==201:
            time.sleep(1)
            if miRed.status()==201:
                miRed.disconnect()
                miRed.connect(wifi, claveWifi)
        else:
            pass
        
        
        if varFlag==1:
            if self.t==0:
                try:
                    self.cliente.disconnect()
                except:
                    pass
                try: 
                    #print("Conectando MQTT...")
                    self.cliente.connect()
                    self.t=1
                except:
                    pass
                    #print("error de conexion MQTT...")
            elif self.t==1:
                try:
                    self.cliente.publish("Acelxv3",str(self.temp1[0]))
                    self.cliente.publish("Acelyv3",str(self.temp1[1]))
                    self.cliente.publish("Acelzv3",str(self.temp1[2]))
                    self.cliente.publish("Magxv3",str(self.temp1[3]))
                    self.cliente.publish("Magyv3",str(self.temp1[4]))
                    self.cliente.publish("Magzv3",str(self.temp1[5]))
                    self.cliente.publish("Tempv3",str(self.temp1[6]))
                    self.cliente.publish("Pluvv3",str(self.temp1[7]))
                    self.cliente.publish("Distv3",str(self.temp1[8]))
                    self.cliente.publish("LoRav3",str(self.temp1[9]))
                    #print("Envio exitoso!")
                except:
                    #print("error de envio mediante wifi")
                    self.t=0
                    try:
                        self.cliente.disconnect()
                    except:
                        pass
                    
    ##############################################


    #OLED
    def escribirOLED(self,mensaje1,mensaje2):
        
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
        
    
    ##############################################
    
            
    def sensores(self):
        try:
            self.temp=self.bus.readfrom(65, 100).decode()
            self.inicial=self.temp.find("@")
            self.temp=self.temp[self.inicial:]
            self.final=self.temp.find("#")+1     
            self.temp=self.temp[:self.final]
        except:
            #print('error sensores')
            pass
        return self.temp
    
    
##############################################
    
    def frecuenciaDeEnvio(self):
        global frecuenciaEnvio
        return frecuenciaEnvio
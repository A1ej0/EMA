#Librerias y dependencias
from ustruct import unpack as unp
from machine import I2C, Pin, SPI, UART, ADC
import network,time,os,machine,ds1307,bluetooth,random
from simple import MQTTClient
from mpu9250 import MPU9250
from BLE import BLEUART
import sh1106
from ulora import LoRa, ModemConfig, SPIConfig


#Variables usadas
nombreBluetooth="EMALoRa1"
p=0
q=1
config_flag=False

#Datos de servidor
wifi = "EMA"
claveWifi="SGCEMA"
host="138.128.244.81"
server=host
puerto="1883"
user="EMA"
claveMqtt="SGCEMA"
IPport=""

#variables para alerta
telefono=3148663113
Tel0=0
Tel1=0
Tel2=0
Tel3=0
AlertFlag=False
mensajeAlerta = "Alerta Geologica"
limite=0
lectura=0
k_value=0.48
contador=0
calidad="0"
auxLoRa=True


#APN GPRS
apn="internet.comcel.com.co"
temporal=""

#Instancias de objetos
ble=bluetooth.BLE()
buart=BLEUART(ble,nombreBluetooth)

#Interrupcion LoRa
def on_recv(payload):
    global calidad,auxLoRa
    calidad=str(payload.message.decode())
    auxLoRa=False
    
    
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
        ##print(config)
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
            ##print("wifi cambiado")
            ##print(len(element))
            wifi=str(element)
            p=0
        
        if element[0]=="c" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            ##print("contraseña cambiada")
            ##print(len(element))
            claveWifi=str(element)
            p=0
            
        if element[0]=="s" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            ##print("server cambiado")
            ##print(element)
            server=str(element)
            p=0
            
        if element[0]=="p" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            ##print("puerto cambiado")
            ##print(element)
            puerto=int(element)
            p=0
            
        if element[0]=="u" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            ##print("usuario cambiado")
            ##print(element)
            user=str(element)
            p=0
            
        if element[0]=="m" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            ##print("clave cambiada")
            ##print(element)
            claveMqtt=str(element)
            p=0
        if element[0]=="t" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            ##print("Telefono cambiado")
            ##print(element)
            telefono=str(element)
            p=0
        if element[0]=="z" and len(element) != 0:
            AlertFlag=True
            ##print("Alerta!!!")
            p=0
        if element[0]=="y" and len(element) != 0:
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            ##print("limite cambiado")
            ##print(element)
            limite=str(element)
            p=0
        if element[0]=="k":
            element=element[1:]
            element=element.replace("\n","")
            element=element.replace("\r","")
            #print("Valor K Cambiado")
            #print(element)
            k_value=str(element)
            q=1
    ##print(rxbuffer)
    if(rxbuffer=="Hola"):
        pass
        #print("Hola")
    if(rxbuffer=="Adios"):
        pass
        #print("Adios")
        
#proceso desconexion Bluetooth       
def on_Disconect():
    #print("APP Desconectada")
    global config_flag
    
    config_flag=False
    

# Bluetooth
buart.irq(handler=on_RX)
buart.discnthandler(handler=on_Disconect)

#LoRa
RFM95_RST = 2
RFM95_SPIBUS = SPIConfig.esp32_1
RFM95_CS = 15
RFM95_INT = 4
RF95_FREQ = 915.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2
lora = LoRa(RFM95_SPIBUS, RFM95_INT, SERVER_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)
lora.on_recv = on_recv
lora.set_mode_rx()

#LIBRERIA PRINCIPAL EMA
class EMA():
    
    def __init__(self):
        #Leds indicadores
        self.led1 = Pin(25, Pin.OUT, machine.Pin.PULL_DOWN)
        self.led2 = Pin(26, Pin.OUT, machine.Pin.PULL_DOWN)
        self.led3 = Pin(27, Pin.OUT, machine.Pin.PULL_DOWN)
        self.led4 = Pin(33, Pin.OUT, machine.Pin.PULL_DOWN)
        #Compartido OLED
        #self.led5 = Pin(32, Pin.OUT, machine.Pin.PULL_DOWN)
        self.t=0
        #i2c_init
        self.bus = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
        #UART init
        self.uart = UART(2, 115200, timeout=2000, rx=16, tx=17)
        #Oled init (1.3)
        try:
            self.oled = sh1106.SH1106_I2C(128, 64, self.bus, Pin(32), 0x3c)
            self.oled.sleep(False)
            self.oled.invert(False)
            self.oled.flip(True)
        except:
            pass
        #RTC_init
        self.ds = ds1307.DS1307(self.bus)
        self.ds.halt(False)
        #SD_init
        try:
            self.sd = machine.SDCard(slot=2, freq=1320000)
        except:
            machine.reset()

    #Funcion para publicar GPRS
    def publish(self,topic,data):
        global temporal
        line=None
        self.send_command('AT+CIPSEND')
        time.sleep(0.5)
        message=bytearray(len(topic).to_bytes(2, 'big'))+bytearray(bytes(topic,"ascii"))+bytearray(bytes(data,"ascii"))
        message=bytearray(b'\x30')+bytearray(len(message).to_bytes(1, 'big'))+message+bytearray(b'\x1A')
        self.uart.write(message)
        line=str(self.uart.read(100))
        print(line)
        time.sleep(0.2)
        line=line+str(self.uart.read(100))
        print(line)
        temporal=temporal+str(line)
        
    #Funcion desconectar GPRS    
    def disconnect(self):
        self.send_command('AT+CIPSEND')
        time.sleep(0.2)
        message=b"\xe0\0\x1a"        
        self.uart.write(message)
        print(self.uart.read(100))
        time.sleep(1)
        self.send_command("AT+CIPSHUT")
        time.sleep(0.2)
        
    #Funcion enviar GPRS
    def send_command(self,command):
        line=None
        line2=None
        if command=='AT+CIPSEND':
            line2="OKi"
        command = command + '\r\n'
        self.uart.write(command)
        while line==None and line2==None:
            line = self.uart.read(100)
        if line:
            try:
                line = line.decode('utf-8')
                print(line.replace('\r\n','\n'))
            except:
                pass
                print(str(line))
        else:
            pass
            print('Hmmm...')
    #Fucion conectar SIM        
    def connectSIM(self):
        global apn,host,puerto
        self.apn=apn
        self.host=host
        self.port=puerto
        self.send_command("AT")
        time.sleep(2)
        self.send_command('AT+CPIN?')
        time.sleep(2)
        self.send_command("AT+CIPSHUT")
        time.sleep(2)
        self.send_command('AT+CSTT="'+self.apn+'"')
        time.sleep(2)
        self.send_command('AT+CIICR')
        time.sleep(2)
        self.send_command('AT+CIFSR')
        time.sleep(2)
        self.send_command('AT+CIPSPRT=0')
        time.sleep(2)
        self.send_command('AT+CIPSTART="TCP","'+self.host+'","'+str(self.port)+'"')
        time.sleep(10)
    #Fucion conectar GPRS   
    def connectS(self):
        global user,claveMqtt
        ra=random.randint(0,50)
        ra=ra*10+ra
        ID=user + str(ra)
        self.clientID=ID
        self.user=user
        self.password=claveMqtt
        line=None
        self.connectSIM()
        print("conectado a GPRS")
        self.uart.write('AT+CIPSEND\r\n')
        message=bytearray(b'\x00\x04')+bytearray(bytes("MQTT","ascii"))+bytearray(b'\x04\xc2')
        message=message+bytearray(b'\x00\x3C')
        message=message+bytearray(len(self.clientID).to_bytes(2, 'big'))+bytearray(bytes(self.clientID,"ascii"))
        message=message+bytearray(len(self.user).to_bytes(2, 'big'))+bytearray(bytes(self.user,"ascii"))
        message=message+bytearray(len(self.password).to_bytes(2, 'big'))+bytearray(bytes(self.password,"ascii"))
        message=bytearray(b'\x10')+bytearray(len(message).to_bytes(1, 'big'))+message+bytearray(b'\x1A')
        time.sleep(0.2)
        self.uart.write(message)
        print("intentando conectar a MQTT...")
        time.sleep(4)

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
    def Temperature(self):
        try:
            self.bus.writeto_mem(119, 0xF4, bytearray([0x2E]))
            time.sleep_ms(5)
            self.UT_raw = self.bus.readfrom_mem(119, 0xF6, 2)
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
    def Pluviometro(self):
        global UmbralPluv
        try:
            Pluv=int(self.bus.readfrom(42, 2).decode().strip("\x00"))
        except:
            Pluv=-1         
            
        return(Pluv)
    
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

    #Distancia
    def distancia(self):
        try:
            dist=self.bus.readfrom(80, 4).decode().strip("\x00")
            dist=int(dist)-100
        except:
            dist=0
        return dist
    
    #Alerta mediante SMS
    def AlertSms(self,dato):
        global telefono, mensajeAlerta
        tele2=3123776985
        
        mensajeAlerta="Conductividad electrica: "+str(dato)+"uS"
        line=str(self.uart.read(100))
        time.sleep(0.5)
        line=str(self.uart.read(100))
        time.sleep(0.5)
        line=str(self.uart.read(100))
        time.sleep(5)
        line=str(self.uart.read(100))
        phone = self.uart
        time.sleep(0.5)
        phone.write(b'AT\r')
        time.sleep(0.5)
        phone.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        phone.write(b'AT+CMGS="' + str(telefono).encode() + b'"\r')
        time.sleep(0.5)
        phone.write(mensajeAlerta.encode() + b"\r")
        time.sleep(0.5)
        phone.write(bytes([26]))
        time.sleep(2)
        phone.write(b'AT\r')
        time.sleep(0.5)
        phone.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        phone.write(b'AT+CMGS="' + str(tele2).encode() + b'"\r')
        time.sleep(0.5)
        phone.write(mensajeAlerta.encode() + b"\r")
        time.sleep(0.5)
        phone.write(bytes([26]))
        time.sleep(0.5)
        #print("\n\n mensaje enviado \n\n")
        line=str(self.uart.read(100))
        time.sleep(0.5)
        line=str(self.uart.read(100))
        time.sleep(0.5)
        line=str(self.uart.read(100))
        time.sleep(5)
        line=str(self.uart.read(100))



    #Ajustes de envio de datos, wifi y MQTT
    def envioDatos (self,temp):
        global wifi,claveWifi,server,puerto,user,claveMqtt,telefono,IPport,AlertFlag, limite, p
        n=0
        miRed = network.WLAN(network.STA_IF)
        self.temp = temp
        if p==0: 
            self.cliente = MQTTClient(client_id="EMAPrueba3",server=str(server),port=int(puerto),user=str(user),password=str(claveMqtt),keepalive=60)
            self.led3.value(1)
            self.led2.value(0)
            miRed.active(False)
            time.sleep(0.5)
            miRed.active(True)                  
            try:
                miRed.connect(wifi, claveWifi)         
                #print('Conectando a la red', self.wifi +"…")
            except:
                pass
            try:
                for i in range(30):
                    if not miRed.isconnected():
                        self.led3.value(1)
                        self.led2.value(1)
                        #print('Conectando a la red', wifi +"... " + str(i+1)+'/10...')
                        time.sleep(0.5)
                if miRed.isconnected():
                    self.led3.value(0)
                    self.led2.value(1)
                    #print ("Conexión exitosa!")
                    #print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
                    IPport=miRed.ifconfig()[0]+":8266"
                    webrepl.start()
                    #webrepl.start(password="EMASGC")
                    config = [wifi,claveWifi,server,puerto,user,claveMqtt,IPport,k_value,Tel0,Tel1,Tel2,Tel3]
                    #print(config)
                    buart.write("Config: "+str(config)+"\n")
                    
                else:
                    #print("red Wifi no disponible")
                    time.sleep(5)
            except:
                pass
            p=1
        #if not miRed.isconnected():
         #   p=0
        if self.t==0 and miRed.isconnected():
            time.sleep(0.3)
            try: 
                #print("Conectando MQTT...")
                self.cliente.connect()
                self.t=1
            except:
                pass
                #print("error de conexion MQTT...")
        if miRed.isconnected() and self.t==1:
            try:
                self.cliente.publish("Temperatura",str(temp[0]))
                self.cliente.publish("FechaT",str(temp[7]))
                self.cliente.publish("HoraT",str(temp[8]))
                self.cliente.publish("cone",str(1))
                #print("Envio exitoso!")
                self.led1.value(not self.led1.value())
            except:
                #print("error de envio mediante wifi")
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
                buart.write("EMA01 dice: "+str(temp)+"\n")
        except:
            #print("error de envio")
            self.t=0
    #OLED
    def escribirOLED(self,mensaje1,mensaje2):
        global calidad
        
        self.oled.fill(0)
        self.oled.text('Hora Recepcion', 0, 10)
        self.oled.text(str(mensaje1), 0, 20)
        self.oled.text('Lluvia', 0, 30)
        self.oled.text(str(mensaje2), 0, 40)
        self.oled.text('mm', 0, 50)
        self.oled.show()
        
    def CalidadLoRa(self):
        global auxLoRa,calidad
        if auxLoRa == False:
            auxLoRa=True
            return calidad
        else:
            return -1
        
    
    def envioDatosSim(self,temp):
        global contador,temporal
        self.publish("lluvia5G",str(temp[4]))
        time.sleep(0.5)
        self.publish("distancia5G",str(temp[10]))
        time.sleep(0.5)
        
        print("contador en: ", str(contador))
        if contador < 10:
            contador=contador+1
        else:
            if "OK" in temporal and not "CLOSED" in temporal:
                print("enviando correctamente")
                temporal=""
                contador=0
                return True
            else:
                print("error de envio... Reiniciando")
                self.disconnect()
                self.connectS()
                contador=0
                temporal=""
                return False
        
    #Calidad de Agua
    def calidadAgua(self):
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
                self.bus.writeto(40, str(k_value))
                time.sleep(1)
                q=0
                #print("valor k enviado %f",k_value)
            except:
                pass
                #print("error al cambiar valor K de calibracion")
        try:
            lectura = self.bus.readfrom(40,4).decode("utf-8").strip("\x00")
            lectura = int(lectura)-100
            return lectura
        except:
            return -1
            


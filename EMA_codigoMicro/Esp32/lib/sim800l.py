"""
Modulo para sim800L
Este modulo contiene las funciones necesarias para realizar una conexion GPRS utilizando un modulo sim800L conecatado al puerto uart2 de la esp32
permite a la EMA establecer conexiones con el servidor en lugares donde exista conexion movil 2G con el operador seleccionado
se debe garantizar en primer lugar que el operador tenga cobertura 2G en la zona, usualmente los operadores virtuales no ofrecen este tipo de conexion
para configurar los datos de conexion como APN, ip del servidor, datos de ingreso, puerto y demas, se debe modificar el archivo ajustes.txt en la memoria interna
en caso de no existir este archivo, es posible crearlo, debe mantener este formato:

Ajustes para conexion GRPS con MQTT:

apn:internet.comcel.com.co
host:138.128.244.81
puerto:1883
user:EMA
claveMqtt:SGCEMA

Ajustes wifi:

red:Alejo
clave:Alejandro1993

Bluetooth:

nombre:EMA1


"""


import random
from machine import UART
import time

class SIM():
       

    def __init__(self):
        self.uart = UART(2, 115200, timeout=2000, rx=16, tx=17)
        self.temporal=""
        self.contador=0
        self.intentos=3
        
        
        logf = open("/ajustes.txt","r")
        lectura=logf.readlines()
        logf.close()
        
        apn=lectura[2].strip("\n")
        apn=apn.split(":")
        self.apn=apn[1]

        host=lectura[3].strip("\n")
        host=host.split(":")
        self.host=host[1]

        puerto=lectura[4].strip("\n")
        puerto=puerto.split(":")
        self.port=puerto[1]

        user=lectura[5].strip("\n")
        user=user.split(":")
        self.user=user[1]

        claveMqtt=lectura[6].strip("\n")
        claveMqtt=claveMqtt.split(":")
        self.password=claveMqtt[1]

        Telefono1=lectura[19].strip("\n")
        Telefono1=Telefono1.split(":")
        self.Telefono1=Telefono1[1]
        
        Telefono2=lectura[20].strip("\n")
        Telefono2=Telefono2.split(":")
        self.Telefono2=Telefono2[1]
        
        Telefono3=lectura[21].strip("\n")
        Telefono3=Telefono3.split(":")
        self.Telefono3=Telefono3[1]
        
        self.telefonos=[self.Telefono1,self.Telefono2,self.Telefono3]
        

    def connectS(self):
        ra=random.randint(0,50)
        ra=ra*10+ra
        self.clientID=self.user + str(ra)
        line=None
        self.connectSIM()
        #print("conectado a GPRS")
        self.uart.write('AT+CIPSEND\r\n')
        message=bytearray(b'\x00\x04')+bytearray(bytes("MQTT","ascii"))+bytearray(b'\x04\xc2')
        message=message+bytearray(b'\x00\x3C')
        message=message+bytearray(len(self.clientID).to_bytes(2, 'big'))+bytearray(bytes(self.clientID,"ascii"))
        message=message+bytearray(len(self.user).to_bytes(2, 'big'))+bytearray(bytes(self.user,"ascii"))
        message=message+bytearray(len(self.password).to_bytes(2, 'big'))+bytearray(bytes(self.password,"ascii"))
        message=bytearray(b'\x10')+bytearray(len(message).to_bytes(1, 'big'))+message+bytearray(b'\x1A')
        time.sleep(0.2)
        self.uart.write(message)
        #print("intentando conectar a MQTT...")
        time.sleep(4)
        
    #Fucion conectar SIM        
    def connectSIM(self):
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
        """    
        if line:
            try:
                line = line.decode('utf-8')
                #print(line.replace('\r\n','\n'))
            except:
                pass
                #print(str(line))
        else:
            pass
            #print('Hmmm...')
        """
        
        




    def publish(self,topic,data):
        line=None
        self.send_command('AT+CIPSEND')
        time.sleep(0.5)
        message=bytearray(len(topic).to_bytes(2, 'big'))+bytearray(bytes(topic,"ascii"))+bytearray(bytes(data,"ascii"))
        message=bytearray(b'\x30')+bytearray(len(message).to_bytes(1, 'big'))+message+bytearray(b'\x1A')
        self.uart.write(message)
        line=str(self.uart.read(100))
        #print(line)
        time.sleep(0.2)
        line=line+str(self.uart.read(100))
        #print(line)
        self.temporal=self.temporal+str(line)
        
        
        
    def envioDatosSim(self,temp):
        
        self.publish("Acelxv35G",str(temp[0]))
        time.sleep(0.5) 
        self.publish("Acelyv35G",str(temp[1]))
        time.sleep(0.5) 
        self.publish("Acelzv35G",str(temp[2]))
        time.sleep(0.5) 
        self.publish("Magxv35G",str(temp[3]))
        time.sleep(0.5) 
        self.publish("Magyv35G",str(temp[4]))
        time.sleep(0.5) 
        self.publish("Magzv35G",str(temp[5]))
        time.sleep(0.5) 
        self.publish("Tempv35G",str(temp[6]))
        time.sleep(0.5)
        self.publish("Pluvv35G",str(temp[7]))
        time.sleep(0.5) 
        self.publish("Distv35G",str(temp[8]))
        time.sleep(0.5) 
        self.publish("LoRav35G",str(temp[9]))
        
        #print("contador en: ", str(self.contador))
        if self.contador < self.intentos:
            self.contador=self.contador+1
        else:
            if "OK" in self.temporal and not "CLOSED" in self.temporal:
                #print("enviando correctamente")
                self.temporal=""
                self.contador=0
                return True
            else:
                #print("error de envio... Reiniciando")
                self.disconnect()
                self.connectS()
                self.contador=0
                self.temporal=""
                return False
            

    #Funcion desconectar GPRS    
    def disconnect(self):
        self.send_command('AT+CIPSEND')
        time.sleep(0.2)
        message=b"\xe0\0\x1a"        
        self.uart.write(message)
        #print(self.uart.read(100))
        time.sleep(1)
        self.send_command("AT+CIPSHUT")
        time.sleep(0.2)
        
        
        
    #Alerta mediante SMS
    def AlertSms(self,dato):
        
        mensajeAlerta=dato
        
        line=str(self.uart.read(100))
        time.sleep(0.5)
        line=str(self.uart.read(100))
        time.sleep(0.5)
        line=str(self.uart.read(100))
        time.sleep(5)
        line=str(self.uart.read(100))
        phone = self.uart
        time.sleep(0.5)
        
        for i in range(len(self.telefonos)):
            phone.write(b'AT\r')
            time.sleep(0.5)
            phone.write(b'AT+CMGF=1\r')
            time.sleep(0.5)
            phone.write(b'AT+CMGS="' + str(self.telefonos[i]).encode() + b'"\r')
            #print("enviando mensaje a: "+str(self.telefonos[i]))
            time.sleep(0.5)
            phone.write(mensajeAlerta.encode() + b"\r")
            time.sleep(0.5)
            phone.write(bytes([26]))
            time.sleep(4)
            
        line=str(self.uart.read(100))
        time.sleep(0.5)
        line=str(self.uart.read(100))
        time.sleep(0.5)
        line=str(self.uart.read(100))
        time.sleep(5)
        line=str(self.uart.read(100))
        #print("SMS enviados")
        

#sim=SIM()

#sim.connectS()
        



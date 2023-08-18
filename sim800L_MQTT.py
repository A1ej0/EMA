from machine import UART, Pin
import network
import time
import ustruct as struct


    
    
    
class SIM800LMQTT():
    
    def __init__(self,uart,apn,host,port,clientID,user,password):
        self.uart=uart
        self.apn=apn
        self.host=host
        self.port=port
        self.clientID=clientID
        self.user=user
        self.password=password
        
    def connectSIM(self):
        self.send_command("AT")
        time.sleep(10)
        self.send_command('AT+CPIN?') 
        self.send_command("AT+CIPSHUT")
  

        self.send_command('AT+CSTT="'+self.apn+'"')
        time.sleep(3)

        self.send_command('AT+CIICR')
        time.sleep(1)
        self.send_command('AT+CIFSR')
        time.sleep(3)
        self.send_command('AT+CIPSPRT=0')
        time.sleep(3)
        self.send_command('AT+CIPSTART="TCP","'+self.host+'","'+self.port+'"')
        time.sleep(3)
        
    def connect(self):
        
        self.connectSIM()

        self.send_command('AT+CIPSEND')
        message=bytearray(b'\x00\x04')+bytearray(bytes("MQTT","ascii"))+bytearray(b'\x04\xc2')
        message=message+bytearray(b'\x00\x3C')
        message=message+bytearray(len(self.clientID).to_bytes(2, 'big'))+bytearray(bytes(self.clientID,"ascii"))
        message=message+bytearray(len(self.user).to_bytes(2, 'big'))+bytearray(bytes(self.user,"ascii"))
        message=message+bytearray(len(self.password).to_bytes(2, 'big'))+bytearray(bytes(self.password,"ascii"))
        message=bytearray(b'\x10')+bytearray(len(message).to_bytes(1, 'big'))+message+bytearray(b'\x1A')
        self.uart.write(message)
        print(self.uart.read(100))
        print(self.uart.read(100))
        
    def send_command(self,command):
  
        command = command + '\r\n'
        self.uart.write(command)
        line = self.uart.read(100)
        if line:
            line = line.decode('utf-8')
            print(line.replace('\r\n','\n'))
        else:
            print('Hmmm...')
            
    def publish(self,topic,data):
        self.send_command('AT+CIPSEND')
        message=bytearray(len(topic).to_bytes(2, 'big'))+bytearray(bytes(topic,"ascii"))+bytearray(bytes(data,"ascii"))
        message=bytearray(b'\x30')+bytearray(len(message).to_bytes(1, 'big'))+message+bytearray(b'\x1A')
        self.uart.write(message)
        print(self.uart.read(100))
        print(self.uart.read(100))
        
    def disconnect(self):
        self.send_command('AT+CIPSEND')
        message=b"\xe0\0\x1a"        
        self.uart.write(message)
        print(self.uart.read(100))
        print(self.uart.read(100))
        self.send_command("AT+CIPSHUT")
        
        
uart = UART(1, 9600, timeout=2000, rx=16, tx=17)
apn="internet.comcel.com.co"
host="4.tcp.ngrok.io"
port="13155"
user="EMA"
password="EMASGC"

sim=SIM800LMQTT(uart,apn,host,port,user,user,password)
sim.connect()
sim.publish("temp","10")
#sim.disconnect()
        
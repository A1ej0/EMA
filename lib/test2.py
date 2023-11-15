from machine import UART, Pin
import network
import time
import ustruct as struct

def send_command(command):
  
  command = command + '\r\n'
  uart.write(command)
  line = uart.read(100)
  if line:
    line = line.decode('utf-8')
    print(line.replace('\r\n','\n'))
  else:
    print('Hmmm...')


uart = UART(1, 9600, timeout=2000, rx=16, tx=17)


user='EMA'
claveMqtt='SGCEMA'
puerto=10563
server='6.tcp.ngrok.io'

#sim= SIM800L(client_id=str(user),server=str(server),port=int(puerto),user=str(user),password=str(claveMqtt),keepalive=60,uart=uart)        
#sim.connect()
#sim.publish

#sim.connect()

send_command("AT")
send_command('AT+CPIN?') 
send_command("AT+CIPSHUT")
  

send_command('AT+CSTT="internet.comcel.com.co"')
time.sleep(3)

send_command('AT+CIICR')
time.sleep(1)
send_command('AT+CIFSR')
time.sleep(3)
send_command('AT+CIPSPRT=0')
time.sleep(3)
send_command('AT+CIPSTART="TCP","4.tcp.ngrok.io","13155"')
send_command('AT+CIPSEND')
message=bytearray(b'\x10\x1E\x00\x04')+bytearray(bytes("MQTT","ascii"))+bytearray(b'\x04\xc2')
message=message+bytearray(b'\x00\x3C')
message=message+bytearray(b'\x00\x05')+bytearray(bytes("ESP32","ascii"))
message=message+bytearray(b'\x00\x03')+bytearray(bytes("EMA","ascii"))
message=message+bytearray(b'\x00\x06')+bytearray(bytes("EMASGC","ascii"))+bytearray(b'\x1A')
print(message)
uart.write(message)
print(uart.read(100))
print(uart.read(100))
while(True):
    send_command('AT+CIPSEND')

    message=bytearray(b'\x30\x08')
    message=message+bytearray(b'\x00\x04')+bytearray(bytes('temp',"ascii"))
    message=message+bytearray(bytes('30',"ascii"))+bytearray(b'\x1A')
    print(message)
    uart.write(message)
    print(uart.read(100))
    time.sleep(5)
  


from time import sleep
import _thread
from machine import SoftI2C, Pin
from i2cslave import i2c_slave
import utime
#from EMA_Libreria import EMA
from ulora import LoRa, ModemConfig, SPIConfig
s_i2c = i2c_slave(0,sda=4,scl=5,slaveAddress=0x31)
# Lora Parameters
RFM95_RST = 9
RFM95_SPIBUS = SPIConfig.rp2_1
RFM95_CS = 13
RFM95_INT = 8
RF95_FREQ = 433.0
RF95_POW =  20
a=0 
CLIENT_ADDRESS = 3
SERVER_ADDRESS = 2
from hcsr04 import HCSR04
lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)
s_i2c = i2c_slave(0,sda=4,scl=5,slaveAddress=0x01)
sleep(2)
distance=0
def main():
    global distance
    while True:
        sensor = HCSR04(trigger_pin=16, echo_pin=17)
        distance = sensor.distance_cm()


_thread.start_new_thread(main,()) 

while True:
    a=a+1
    print('Distance:', a, 'cm')
    distancia =str(a)
    lora.send(distancia, SERVER_ADDRESS)
    print('send')
    sleep(28)


        
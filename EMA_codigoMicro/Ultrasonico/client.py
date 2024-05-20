from time import sleep
from ulora import LoRa, ModemConfig, SPIConfig
from i2cslave import i2c_slave

# Lora Parameters
RFM95_RST = 9
RFM95_SPIBUS = SPIConfig.rp2_1
RFM95_CS = 13
RFM95_INT = 8
RF95_FREQ = 433.0
RF95_POW =  20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

# initialise radio
lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)
s_i2c = i2c_slave(0,sda=4,scl=5,slaveAddress=0x07)

# loop and send data
print('inicio')
while True:
    lora.send_to_wait("This is a test message", SERVER_ADDRESS)
    print(trama)
    sleep(2)

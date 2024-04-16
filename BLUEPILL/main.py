import utime
from machine import mem32
from i2cslave import i2c_slave

s_i2c = i2c_slave(1,sda=14,scl=15,slaveAddress=0x41)
counter =1
try:
    while True:
        if s_i2c.any():
            print(s_i2c.get())
        if s_i2c.anyRead():
            counter = counter + 1
            s_i2c.put(counter & 0xff)
    
except KeyboardInterrupt:
    print("error")

"""
from time import sleep
from ulora import LoRa, ModemConfig, SPIConfig

# This is our callback function that runs when a message is received
def on_recv(payload):
    #print("From:", payload.header_from)
    print("Received:", payload.message.decode())
    #print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))

# Lora Parameters
RFM95_RST = 14
RFM95_SPIBUS = SPIConfig.rp2_0
RFM95_CS = 29
RFM95_INT = 15
RF95_FREQ = 915.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

# initialise radio
lora = LoRa(RFM95_SPIBUS, RFM95_INT, SERVER_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

# set callback
lora.on_recv = on_recv

# set to listen continuously
lora.set_mode_rx()

# loop and wait for data
print('Arranco')
while True:
    sleep(0.1)
"""
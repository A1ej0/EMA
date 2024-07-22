from ulora import LoRa, ModemConfig, SPIConfig
from machine import Pin
from time import sleep

# Lora Parameters
RFM95_RST = 9
RFM95_SPIBUS = SPIConfig.rp2_1
RFM95_CS = 13
RFM95_INT = 8
RF95_FREQ = 433.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=False)


status = lora.send_to_wait("Test", 2, retries=2)

if status is True:
    print("Message sent!")
else:
    print("No acknowledgment from recipient")
    

lora.close()
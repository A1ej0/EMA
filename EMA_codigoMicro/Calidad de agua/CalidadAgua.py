#Calidad de agua y temperatura en uS/cm

#Librerias
from machine import ADC, Pin
from ds18x20_single import DS18X20Single
from onewire import OneWire
import dftds
from time import sleep
from ulora import LoRa, ModemConfig, SPIConfig

#Pines usados
TDS_PIN = 27
ow = OneWire(Pin(28))

#Variables
k=1.0
tds_value=0.0


# Parametros LoRa
RFM95_RST = 21
RFM95_SPIBUS = SPIConfig.rp2_0
RFM95_CS = 17
RFM95_INT = 20
RF95_FREQ = 915.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

#Instancia de sensores y LoRa
temp = DS18X20Single(ow)
tds_sensor = dftds.GravityTDS(TDS_PIN, adc_range=65535, k_value=k)
tds_sensor.begin()
lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

#Ejecucion
temp.convert_temp()
while True:
    tds_sensor.temperature = float(temp.read_temp())
    tds_value = tds_sensor.update()
    lora.send_to_wait(str(tds_value*2), SERVER_ADDRESS)
    print("TDS: {}ppm, EC: {} mS/cm".format(tds_value, tds_value*2))
    sleep(5)
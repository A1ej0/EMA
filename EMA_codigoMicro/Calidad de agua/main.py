#Calidad de agua y temperatura en uS/cm

#Librerias
from machine import ADC, Pin, reset
from ds18x20_single import DS18X20Single
from onewire import OneWire
import dftds
from time import sleep
from ulora import LoRa, ModemConfig, SPIConfig
from machine import WDT


firulais = WDT(timeout=7000)


#Pines usados
#DF robot
TDS_PIN = 26


#Pic Ahorro
led=Pin(25,Pin.OUT)
led.on()
Res=Pin(28,Pin.OUT,Pin.PULL_UP)
Res.off()

#Temperatura
ow = OneWire(Pin(19))
#print("temperatura ajsutado")
#Variables
k=1.0
tds_value=0.0
tempi=25



# Lora Parameters
RFM95_RST = 9
RFM95_SPIBUS = SPIConfig.rp2_1
RFM95_CS = 13
RFM95_INT = 8
RF95_FREQ = 433.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

#Instancia de sensores y LoRa
temp = DS18X20Single(ow)
#print("sonda iniciada")
sleep(1)
tds_sensor = dftds.GravityTDS(TDS_PIN, adc_range=65535, k_value=k)
tds_sensor.begin()
#print("tds iniciado")
sleep(1)
lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)
#print("Lora Iniciado")
#Ejecucion
sleep(1)


while True:
    try:
        temp.convert_temp()
        #print("convert...")
        firulais.feed()
        print("comiendo...")
        sleep(1)
        tempi=temp.read_temp()
        firulais.feed()
        print("comiendo...")
    except:
        pass
    #print(tempi)
    sleep(1)
    #print('leer temperatura')
    tds_sensor.temperature = float(tempi)
    firulais.feed()
    print("comiendo...")
    sleep(1)
    #print('temperatura leida')
    tds_value = tds_sensor.update()
    firulais.feed()
    print("comiendo...")
    sleep(1)
    lora.send(str(tds_value*2), SERVER_ADDRESS)
    firulais.feed()
    print("comiendo...")
    #print("TDS: {}ppm, EC: {} mS/cm".format(tds_value, tds_value*2))
    sleep(5)
    Res.on()


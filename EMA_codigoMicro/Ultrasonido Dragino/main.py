#Calidad de agua y temperatura en uS/cm

#Librerias
from machine import Pin, reset
from time import sleep
from ulora import LoRa, ModemConfig, SPIConfig
from machine import WDT


firulais = WDT(timeout=7000)


#Pic Ahorro
led=Pin(25,Pin.OUT)
led.on()

Res=Pin(28,Pin.OUT,Pin.PULL_UP)
Res.off()

tempi=25

# Initialise UART
uart = UART(0, 9600, tx=Pin(16), rx=Pin(17))
uart.init(bits=8, parity=None, stop=1) # Defaults from DFrobot wiki page: https://wiki.dfrobot.com/A01NYUB%20Waterproof%20Ultrasonic%20Sensor%20SKU:%20SEN0313



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
sleep(1)
lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)
#print("Lora Iniciado")
#Ejecucion
sleep(1)


def read_distance():
    uart.read() # clear buffer (could contain many measurements)
    while (uart.any() == 0): # wait for the sensor to send a packet
        pass # pass and check again if you didn't get one
    data_buff = uart.read(4) # read the 4 bytes it sent
    checksum = (data_buff[0] + data_buff[1] + data_buff[2]) & 0xFF # checksum seems to be header + data H + data L, masked to a single byte
    if (checksum == data_buff[3]):
        measurement = ((data_buff[1] << 8) + data_buff[2]) # shift data H left 8 bits, and add with data low
        if measurement == 250:
            return(-1) # return -1 if "250" (invalid measurement) is recieved, consider adding 0 too, as it's usually not accurate
        else:
            return(measurement)
    else:
        return(-2) # if checksum fails (normally because minimum range has been exceeded, return -1)





while True:
    try:
        Temp=read_distance()
        firulais.feed()
    except:
        pass
    lora.send(str(Temp), SERVER_ADDRESS)
    firulais.feed()
    print("comiendo...")
    #print("TDS: {}ppm, EC: {} mS/cm".format(tds_value, tds_value*2))
    sleep(5)
    Res.on()


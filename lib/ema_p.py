#Proyecto EMA Estacion de monitoreo automatica, sistema monitoreo ambiental basado en lectura de temperatura, aceleracion e inclinacion.

from EMA import EMA
from machine import I2C, Pin
import machine
import time
import _thread
import os
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

#Configuracion del puerto i2c
bus = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
#Instancia de EMA
EMA = EMA(bus)

#Dispositivos disponibles proyecto EMA (Totalidad) - Iniciando dispositivo:
dispositivos = EMA.escaneoInicial()
EMA.escribirLCD("Bienvenido!")
time.sleep(1)
EMA.limpiarLCD()
EMA.escribirLCD("Ahorro          Activado")
time.sleep(2)
EMA.limpiarLCD()
EMA.powerLCD(0)
EMA.luzLCD(0)

#Calibracion de temperatura
EMA.initTemp()
temp = 0.0

#Core 1 - conexion wifi y envio de datos a la nube
def SecondCore():
    while True:
        EMA.conectaWifi ("Alejandro", "Alejandro1993",str(temp))
        time.sleep(1)
_thread.start_new_thread(SecondCore,())


#Core 0 - Lectura de sensores y almacenamiento local
while True:
    temp = EMA.temperature()
    #EMA.escribirSD(temp)
    #print(EMA.leerSD())
    time.sleep(1)
    
    
    
    
    
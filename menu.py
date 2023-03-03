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

dispositivos = EMA.escaneoInicial()

bus = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(bus, 39, 2, 16)
button1 = Pin(25, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(26, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(27, Pin.IN, Pin.PULL_DOWN)
Celular="3123776985"

lcd.putstr("Ajuste Inicial..")
time.sleep(1.5)


estadoMenu=0
estado1=0
navM=0
opc=""
TEMPERATURA=0.0
MOVIMIENTO=0.0
temp = 0.0
PERIODO=""
lcd.clear()


menu = ["Umbrales","Telefono","Calibracion","Periodo","Iniciar","------------FIN-"]
Umbrales=["U. Temp","U. mov","Atras","------------FIN-"]
Telefono=["3123776985","Atras","------------FIN-"]
Calibracion=["Cal. Temp","Cal. Mov","Atras","------------FIN-"]
Periodo=["Ajustar","Atras","------------FIN-"]
iniciar=["Confirmar.","----------------"]
Tiempos=["1segundo","30segundos","1min","5min","10min","30min","1hora","12horas","1dia","1semana"]
mainMenu=[menu,Umbrales,Telefono,Calibracion,Periodo,iniciar]

def ajusteInicial():
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr(mainMenu[estado1][estadoMenu]+" *")
    lcd.move_to(0,1)
    lcd.putstr(mainMenu[estado1][estadoMenu+1])
    
def umbrales():
    if opc=="temp":
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Umbral Temp...")
        lcd.move_to(0,1)
        lcd.putstr("    -  "+str(estadoMenu)+"  +   ")
    elif opc=="mov":
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Umbral mov...")
        lcd.move_to(0,1)
        lcd.putstr("    -  "+str(estadoMenu)+"  +   ")
        
def calibracion():
    if opc=="temp":
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Calibrando")
        lcd.move_to(0,1)
        lcd.putstr("Temperatura")
        EMA.calibracionTemp()
    elif opc=="mov":
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Calibrando")
        lcd.move_to(0,1)
        lcd.putstr("Giroscopio")
        
def periodo():
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Periodo Tiempo")
    lcd.move_to(0,1)
    lcd.putstr(" - "+Tiempos[estadoMenu]+"  +") 

ajusteInicial()

def menuAjuste(boton1,boton2,boton3):
    global navM,estadoMenu,mainMenu,estado1,opc
    if boton1: 
        if navM==0:
            estadoMenu=estadoMenu-1
            estadoMenu=0 if estadoMenu<0 else estadoMenu
            ajusteInicial()
            time.sleep(0.5)
        elif navM==1:
            estadoMenu=estadoMenu-1
            estadoMenu=0 if estadoMenu<0 else estadoMenu
            umbrales()
            time.sleep(0.5)
        elif navM==3:
            estadoMenu=estadoMenu-1
            estadoMenu=0 if estadoMenu<0 else estadoMenu
            periodo()
            time.sleep(0.5) 
        
    elif boton2:
        if navM==0:
            if mainMenu[estado1][estadoMenu]=="Atras":
                estado1=0
                ajusteInicial()
            elif mainMenu[estado1][estadoMenu]=="U. Temp":
                navM=1
                opc="temp"
                umbrales()
            elif mainMenu[estado1][estadoMenu]=="U. mov":
                navM=1
                opc="mov"
                umbrales()
            elif mainMenu[estado1][estadoMenu]=="Cal. Temp":
                navM=2
                opc="temp"
                calibracion()
            elif mainMenu[estado1][estadoMenu]=="Cal. Mov":
                navM=2
                opc="mov"
                calibracion()
            elif mainMenu[estado1][estadoMenu]=="Ajustar":
                navM=3
                periodo()
            elif mainMenu[estado1][estadoMenu]=="Confirmar.":
                navM=99
            else:
                estado1=estadoMenu+1
                estadoMenu=0
                ajusteInicial()
                
            time.sleep(0.5)    
            
        elif navM==1:
            if opc=="temp":
                print("Temperatura ajustada en "+str(estadoMenu)+" Grados centigrados")
                TEMPERATURA=estadoMenu
            else:
                print("Movimiento ajustado en "+str(estadoMenu)+" %")
                MOVIMIENTO=estadoMenu
            navM=0
            estado1=0
            estadoMenu=0
            ajusteInicial()
            time.sleep(0.5)
            
        elif navM==2:
            if opc=="temp":
                print("Temperatura Calibrada")
            else:
                print("Movimiento Calibrado")
            navM=0
            estado1=0
            estadoMenu=0
            ajusteInicial()
            time.sleep(0.5)

        elif navM==3:
            print("Periodo ajustado a "+str(Tiempos[estadoMenu]))
            PERIODO=Tiempos[estadoMenu]
            navM=0
            estado1=0
            estadoMenu=0
            ajusteInicial()
            time.sleep(0.5)
            
    elif boton3:
        
        if navM==0:
            estadoMenu=estadoMenu+1
            estadoMenu=estadoMenu-1 if estadoMenu==len(mainMenu[estado1])-1 else estadoMenu
            ajusteInicial()
            time.sleep(0.5)
        if navM==1:
            estadoMenu=estadoMenu+1
            estadoMenu=60 if estadoMenu==61 else estadoMenu
            umbrales()
            time.sleep(0.5)
        if navM==3:
            estadoMenu=estadoMenu+1
            estadoMenu=9 if estadoMenu>8 else estadoMenu
            periodo()
            time.sleep(0.5)

def SecondCore():
    while True:
        EMA.conectaWifi ("FAMILIA_ARCILA", "Arcila2468",str(temp))
        time.sleep(1)


while True:
    boton1=button1.value()
    boton2=button2.value()
    boton3=button3.value()
    if navM!=99:
        menuAjuste(boton1,boton2,boton3)
    elif navM==99:
        navM=98
        time.sleep(2)
        lcd.backlight_off()
        lcd.display_off()
        print(navM)
        _thread.start_new_thread(SecondCore,())
        print("Inicia Protocolo de envio en core2")
    if navM==98:
        temp = EMA.temperature()
        #EMA.escribirSD(temp)
        #print(EMA.leerSD())
        time.sleep(1)
    time.sleep(0.3)
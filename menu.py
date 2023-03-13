#Proyecto EMA Estacion de monitoreo automatica, sistema monitoreo ambiental basado en lectura de temperatura, aceleracion e inclinacion.
from EMA import EMA
from machine import I2C, Pin, SPI
import machine
import framebuf
import time
import _thread
import os
import ssd1306
#Configuracion del puerto i2c
bus = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)

sd = machine.SDCard(slot=2, freq=1320000)
os.mount(sd, "/sd")

try:
    os.stat("/sd/em.conf")
    with open("/sd/ema.conf") as archivo:
        datos=archivo.readlines()
        wifi = datos[0]
        wifi = wifi[:-1]
        claveWifi=datos[1]
        claveWifi=claveWifi[:-1]
        telefono=datos[2]
        telefono=telefono[:-1]
        server=datos[3]
        server=server[:-1]
        puerto=datos[4]
        puerto=puerto[:-1]
        user=datos[5]
        user=user[:-1]
        claveMqtt=datos[6]
        claveMqtt=claveMqtt[:-1]
except OSError:
    print("no")
    hspi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
    dc = Pin(4)    # data/command
    rst = Pin(2)   # reset
    cs = Pin(15)   # chip select, some modules do not have a pin for this
    display = ssd1306.SSD1306_SPI(128, 64, hspi, dc, rst, cs)
    while True:
        for i in range(15):            
            with open('anim/'+str(i)+'.pbm', 'rb') as f:
                f.readline() # Magic number
                f.readline() # Creator comment
                f.readline() # Dimensions
                data = bytearray(f.read())
            fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
            display.invert(0)
            display.blit(fbuf, 0, 0)
            display.text("EMA",1,1,1)
            display.text("V.1.0",90,1,1)
            display.text("error",45,30,1)
            display.text("conf no existe",5,56,1)
            display.show()
            time.sleep(0.1)
        display.fill(0)
        display.show()
        
#Instancia de EMA
EMA = EMA(bus,server,puerto,user,claveMqtt)

dispositivos = EMA.escaneoInicial()
time.sleep(2)

button1 = Pin(25, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(26, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(27, Pin.IN, Pin.PULL_DOWN)
Celular="3123776985"



estadoMenu=0
estado1=0
navM=0
opc=""
TEMPERATURA=0.0
MOVIMIENTO=0.0
temp = 0.0
datos = [0,0,0,0]
PERIODO=""
EMA.limpiarOLED()


menu = ["Umbrales","Telefono","Calibracion","Periodo","Iniciar","------------FIN-"]
Umbrales=["U. Temp","U. mov","Atras","------------FIN-"]
Telefono=[str(telefono),"Atras","------------FIN-"]
Calibracion=["Cal. Temp","Cal. Mov","Atras","------------FIN-"]
Periodo=["Ajustar","Atras","------------FIN-"]
iniciar=["Confirmar.","----------------"]
Tiempos=["1segundo","30segundos","1min","5min","10min","30min","1hora","12horas","1dia","1semana"]
mainMenu=[menu,Umbrales,Telefono,Calibracion,Periodo,iniciar]

def ajusteInicial():
    EMA.limpiarOLED()
    EMA.escribirOLED(mainMenu[estado1][estadoMenu]+" *",10,20)
    EMA.escribirOLED(mainMenu[estado1][estadoMenu+1],10,30)
    
def umbrales():
    if opc=="temp":
        EMA.limpiarOLED()
        EMA.escribirOLED("Umbral Temperatura",0,20)
        EMA.escribirOLED("    -  "+str(estadoMenu)+"  +   ",10,30)
    elif opc=="mov":
        EMA.limpiarOLED()
        EMA.escribirOLED("Umbral movimiento",0,20)
        EMA.escribirOLED("    -  "+str(estadoMenu)+"  +   ",10,30)
        
def calibracion():
    if opc=="temp":
        EMA.limpiarOLED()
        EMA.escribirOLED("Calibrando",10,20)
        EMA.escribirOLED("Temperatura",10,30)
        EMA.calibracionTemp()
    elif opc=="mov":
        EMA.limpiarOLED()
        EMA.escribirOLED("Calibrando",10,20)
        EMA.escribirOLED("Giroscopio",10,30)
        EMA.calibracionAcel()
        
def periodo():
    EMA.limpiarOLED()
    EMA.escribirOLED("Periodo Tiempo",10,20)
    EMA.escribirOLED(" - "+Tiempos[estadoMenu]+"  +",10,30) 

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
        EMA.conectaWifi (wifi, claveWifi,datos)
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
        EMA.animLoading()
        print(navM)
        _thread.start_new_thread(SecondCore,())
        print("Inicia Protocolo de envio en core2")
    if navM==98:
        acel = EMA.aceleracion()
        temp = EMA.temperature()
        datos= [temp,acel[0],acel[1],acel[2]]
        #EMA.escribirSD(temp)
        #print(EMA.leerSD())
        time.sleep(1)
    time.sleep(0.3)
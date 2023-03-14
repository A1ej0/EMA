#Proyecto EMA Estacion de monitoreo automatica, sistema monitoreo ambiental basado en lectura de temperatura, aceleracion e inclinacion.
#Modulos requeridos
from EMA import EMA
from machine import I2C, Pin, SPI, UART, ADC
import machine
import framebuf
import time
import _thread
import os
import ssd1306


#Configuracion del puerto i2c, UART, ADC, SD
bus = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
uart1 = UART(2, baudrate=115200, tx=17, rx=16)
sd = machine.SDCard(slot=2, freq=1320000)
hall = ADC(Pin(34))
hall.atten(ADC.ATTN_11DB)



#Comprobacion de memoria microSD Disponible
try:
    os.mount(sd, "/sd")
    print("SD Detectada...")
    time.sleep(1)
except OSError:
    print("SD NO Detectada")
    hspi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
    dc = Pin(4)   
    rst = Pin(2)  
    cs = Pin(15) 
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
            display.text(" SD no existe",5,56,1)
            display.show()
            time.sleep(0.1)
        display.fill(0)
        display.show()
    


#Comprobacion de archivo de ajustes disponible
try:
    os.stat("/sd/ema.conf")
    print("Archivo de ajuste encontrado...")
    time.sleep(1)
    with open("/sd/ema.conf") as archivo:
        datos=archivo.readlines()
        print(datos)
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
    print("Archivo de ajuste NO Detectado")
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
        
wifi = "SGC_Publica"
claveWifi=""

#Comprobacion de Modulo SIM Disponible
uart1.write("AT+CSQ\r\n")
a=1
while a!=0:
    read=uart1.read()
    if read==None and a<=10:
        print("prueba conexion modulo SIM N°: "+ str(a))
        a=a+1
        time.sleep(0.5)
    elif read==None and a>10:
        print("Modulo Sim No encontrado")
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
                display.text("simMod no existe",1,56,1)
                display.show()
                time.sleep(0.1)
            display.fill(0)
            display.show()
    else:
        print("Modulo SIM disponible...")
        time.sleep(1)
        a=0
        time.sleep(0.5)


#Comprobacion de pluviometro disponible
val = hall.read_uv()
val=round(val/1000000,2)
gauss = round(((val/3.3)*2000)-1000,2)
if gauss>(-800):
    print("Pluviometro detectado: ")
    print(str(gauss)+" Gauss")
    time.sleep(1)
else:
    print("pluviometro no disponible")
    time.sleep(1)
          
        
#Instancia de libreria global EMA
EMA = EMA(bus,server,puerto,user,claveMqtt)

#Escaneo inicial, i2c
dispositivos = EMA.escaneoInicial()
time.sleep(2)


# Definicion de entrada de encoder incremental, butto1 <-, button2 OK, button3 ->
button1 = Pin(25, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(26, Pin.IN, Pin.PULL_UP)
button3 = Pin(27, Pin.IN, Pin.PULL_DOWN)

#Asignacion de numero de telefono deacuerdo a archivo de ajuste
Celular=telefono


# Variables usadas
estadoMenu=0
estado1=0
navM=0
opc=""
TEMPERATURA=0.0
MOVIMIENTO=0.0
temp = 0.0
datos = [0,0,0,0]
PERIODO=0
EMA.limpiarOLED()

#Definicion del menu
menu = ["Umbrales","Telefono","Calibracion","Periodo","Iniciar","------------FIN-"]
Umbrales=["U. Temp","U. mov","Atras","------------FIN-"]
Telefono=[str(telefono),"Atras","------------FIN-"]
Calibracion=["Cal. Temp","Cal. Mov","Atras","------------FIN-"]
Periodo=["Ajustar","Atras","------------FIN-"]
iniciar=["Confirmar.","----------------"]
Tiempos=["1segundo","30segundos","1min","5min","10min","30min","1hora","12horas","1dia","1semana"]
mainMenu=[menu,Umbrales,Telefono,Calibracion,Periodo,iniciar]

#Navegacion por el menu
def ajusteInicial():
    EMA.limpiarOLED()
    EMA.escribirOLED("MENU DE AJUSTE",5,0)
    EMA.escribirOLED("use la perilla",5,55)
    EMA.escribirOLED("--------------",5,10)
    EMA.escribirOLED("--------------",5,50)
    EMA.escribirOLED(mainMenu[estado1][estadoMenu]+" *",15,20)
    EMA.escribirOLED(mainMenu[estado1][estadoMenu+1],15,30)
    
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
    temporal=0
    if opc=="temp":
        while EMA.calibracionTemp() != "calibrado":
            EMA.limpiarOLED()
            EMA.escribirOLED("Calibrando",10,20)
            EMA.escribirOLED("Temperatura "+str(temporal),10,30)
        EMA.limpiarOLED()
        EMA.escribirOLED("Calibracion",10,20)
        EMA.escribirOLED("completada",10,30)
        time.sleep(1)
        boton2=1
    elif opc=="mov":
        delay=0.1
        iteraciones=20
        EMA.limpiarOLED()
        EMA.escribirOLED(" Cargando",10,20)
        EMA.escribirOLED("Espere....",10,30)
        EMA.calibracionAcel(iteraciones)
        for i in range (iteraciones):
            EMA.limpiarOLED()
            EMA.escribirOLED("Calibrando",10,20)
            EMA.escribirOLED("Giroscopio: "+str(iteraciones-i),10,30)
            time.sleep(delay)
        EMA.limpiarOLED()
        EMA.escribirOLED("Giroscopio",10,20)
        EMA.escribirOLED("Calibrado!",10,30)
        time.sleep(1)
        
        
def periodo():
    EMA.limpiarOLED()
    EMA.escribirOLED("Periodo Tiempo",10,20)
    EMA.escribirOLED(" - "+Tiempos[estadoMenu]+"  +",10,30) 

ajusteInicial()

def menuAjuste(boton1,boton2,boton3):
    global PERIODO
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
            if estadoMenu==0:
                PERIODO=1
            elif estadoMenu==1:
                PERIODO=30
            elif estadoMenu==2:
                PERIODO=60
            elif estadoMenu==3:
                PERIODO=300
            elif estadoMenu==4:
                PERIODO=600
            elif estadoMenu==5:
                PERIODO=1800
            elif estadoMenu==6:
                PERIODO=3600
            elif estadoMenu==7:
                PERIODO=3600*12
            elif estadoMenu==8:
                PERIODO=3600*24
            elif estadoMenu==9:
                PERIODO=3600*24*7
            else:
                PERIODO=1
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

estadoPrevioA=button1.value()
boton1=boton2=boton3=0
while True:
    estadoA = button1.value()
    if estadoA != estadoPrevioA:     
        if button3.value() != estadoA:
            boton3=1
        else:
            boton1=1
    estadoPrevioA = estadoA
    if navM!=99:
        menuAjuste(boton1,boton2,boton3)
        boton1=boton3=0
    elif navM==99:
        navM=98
        time.sleep(2)
        EMA.escribirOLED("iniciando...",2,55)
        EMA.animLoading()
        print(navM)
        _thread.start_new_thread(SecondCore,())
        print("Inicia Protocolo de envio en core2")
    if not button2.value():
        boton2=1
    else:
        boton2=0
    if navM==98:
        try:
            gauss = round(((round(hall.read_uv()/1000000,2)/3.3)*2000)-1000,2)
        except:
            print("error en lectura de pluviometro")
            gauss = 0
        try:
            acel = EMA.aceleracion()
        except:
            print("error en la lectura de aceleracion")
            acel = [0,0,0]
        try:
            temp = EMA.temperature()
        except:
            print("error al obtener temperatura")
            temp=0.0
        datos= [temp,acel[0],acel[1],acel[2],gauss]
        #EMA.escribirSD(temp)
        #print(EMA.leerSD())
        time.sleep(PERIODO)
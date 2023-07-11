from EMA_v20 import EMA
import time
import _thread


EMA = EMA()
dispositivos = EMA.escaneoInicial()


temp= 0
datos = [0,0,0,0,0,0,0,0,0,0]
lecturaGPS2 = [0,0,0,0]
acel=[0,0,0]
gauss=0
textoRaw=""

control1=0

def SecondCore():
    while True:
        EMA.envioDatos (datos)
        EMA.envioBt (datos)
        
        time.sleep(1)
        
_thread.start_new_thread(SecondCore,())

while True:
    if dispositivos[1]==1:
        pass
    if control1 == 0:
        EMA.calibracionTemp()
        control1 = 1
    temp = EMA.Temperature()
    if temp == -1:
        control = 0
        #print(EMA.Temperature())
    if dispositivos[2]==1:
        acel[0] = EMA.Acelerometro()[0]
        acel[1] = EMA.Acelerometro()[1]
        acel[2] = EMA.Acelerometro()[2]
        #print(EMA.Acelerometro())
    if dispositivos[3]==1:
        gauss = EMA.Pluviometro()
        #print(EMA.Pluviometro())
    fechaHora = EMA.rtc()
    distanci=EMA.distancia()
    calidad=EMA.calidadAgua()
    hora=str(fechaHora[4])+":"+str(fechaHora[5])+":"+str(fechaHora[6])
    fecha=str(fechaHora[2])+"/"+str(fechaHora[1])+"/"+str(fechaHora[0])       
    datos= [temp,distanci,acel[1],acel[2],gauss,lecturaGPS2[0],lecturaGPS2[1],fecha,hora,calidad]
    
    for i in range(len(datos)):
        textoRaw=textoRaw+","+str(datos[i])
    textoRaw=textoRaw+";"
        
    EMA.escribirSD(textoRaw)
    textoRaw=""
    time.sleep(0.5)
    

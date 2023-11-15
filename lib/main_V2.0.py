from EMA_v20 import EMA
import time
import _thread

EMA = EMA()
dispositivos = EMA.escaneoInicial()
EMA.calibracionTemp()
print(EMA.Temperature())
print(dispositivos)

datos = [0,0,0,0,0,0,0,0,0]
lecturaGPS2 = [0,0,0,0]
acel=[0,0,0]

def SecondCore():
    while True:
        EMA.envioDatos (datos)
        time.sleep(1)
        
_thread.start_new_thread(SecondCore,())

while True:
    if dispositivos[1]==1:
        temp = EMA.Temperature()
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
    hora=str(fechaHora[4])+":"+str(fechaHora[5])+":"+str(fechaHora[6])
    fecha=str(fechaHora[2])+"/"+str(fechaHora[1])+"/"+str(fechaHora[0])       
    datos= [temp,acel[0],acel[1],acel[2],gauss,lecturaGPS2[0],lecturaGPS2[1],fecha,hora]
    time.sleep(0.5)
    

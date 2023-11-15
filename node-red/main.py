from EMA_v20 import EMA
import time
import _thread


EMA = EMA()
EMA.calibracionTemp()
temp= 0
datos = [0,0,0,0,0,0,0,0,0,0,0]
lecturaGPS2 = [0,0,0,0]
acel=[0,0,0]
gauss=0
lluvia=0
lluvias=0
distanci=0
textoRaw=""
fecha=0
hora=0
frecuencia=False
contadorSIM=0
count=0
count2=0
calidad=0


def ThirdCore():
    
    while True:
        
        EMA.envioDatos (datos)
        time.sleep(1)
        
def FourthCore():
    while True:

        EMA.envioBt (datos)
        time.sleep(1)

def SecondCore():
    global frecuencia,contadorSIM

    while True:
        if not frecuencia:
            if not EMA.envioDatosSim(datos):
                pass
            else:
                print("Proximo envio en una hora...")
                frecuencia = True
        else:
            contadorSIM=contadorSIM+1
            print("Segundos restantes: "+str(3600-contadorSIM))
            if contadorSIM>=3600:
                frecuencia=False
                contadorSIM=0
        time.sleep(1)
        
        
_thread.start_new_thread(FourthCore,())        
_thread.start_new_thread(ThirdCore,())
_thread.start_new_thread(SecondCore,())


while True:
    temp = EMA.Temperature()
    fechaHora = EMA.rtc()
    distanci=EMA.distancia()
    calidad=EMA.calidadAgua()
    hora=str(fechaHora[4])+":"+str(fechaHora[5])+":"+str(fechaHora[6])
    fecha=str(fechaHora[2])+"/"+str(fechaHora[1])+"/"+str(fechaHora[0])
    
    datos= [temp,lluvia,acel[1],acel[2],gauss,lecturaGPS2[0],lecturaGPS2[1],fecha,hora,calidad,distanci]
    
    if count>=60:
        lluvia=EMA.Pluviometro()
        lluvias=lluvias+lluvia
        if count2>=(60*24):
            EMA.AlertSms(lluvias)
            lluvias=0
            count2=0
        count2=count2+1
        for i in range(len(datos)):
            textoRaw=textoRaw+" , "+str(datos)
        EMA.escribirSD(textoRaw)
        time.sleep(1)
        print("SD sobreescrita")
        textoRaw=""
        count=0
        
    count+=1
    time.sleep(1)

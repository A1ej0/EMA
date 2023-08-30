from EMA_v20 import EMA
import time
import _thread


EMA = EMA()
#dispositivos = EMA.escaneoInicial()
#EMA.calibracionTemp()

temp= 0
datos = [0,0,0,0,0,0,0,0,0,0,0]
lecturaGPS2 = [0,0,0,0]
acel=[0,0,0]
gauss=0
lluvia=0
distanci=0
textoRaw=""
fecha=0
hora=0
frecuencia=False
contadorSIM=0


def SecondCore():
    global frecuencia,contadorSIM
    while True:
        EMA.envioDatos (datos)
        #EMA.envioBt (datos)
        if not frecuencia:
            if not EMA.envioDatosSim(datos[9]):
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
_thread.start_new_thread(SecondCore,())

while True:
   # if dispositivos[1]==1:
   #     temp = EMA.Temperature()
        #print(EMA.Temperature())
    #if dispositivos[2]==1:
    #    acel[0] = EMA.Acelerometro()[0]
    #    acel[1] = EMA.Acelerometro()[1]
    #    acel[2] = EMA.Acelerometro()[2]
        #print(EMA.Acelerometro())
    #if dispositivos[3]==1:
    #    gauss = EMA.Pluviometro()
        #print(EMA.Pluviometro())
    fechaHora = EMA.rtc()
    #distanci=EMA.distancia()
    calidad=EMA.calidadAgua()
    hora=str(fechaHora[4])+":"+str(fechaHora[5])+":"+str(fechaHora[6])
    fecha=str(fechaHora[2])+"/"+str(fechaHora[1])+"/"+str(fechaHora[0])
    datos= [temp,lluvia,acel[1],acel[2],gauss,lecturaGPS2[0],lecturaGPS2[1],fecha,hora,calidad,distanci]
    datosCalidadAgua=["Fecha: ",fecha,"Hora: ",hora,"Calidad: ",calidad]
    
    for i in range(len(datosCalidadAgua)):
        textoRaw=textoRaw+" , "+str(datosCalidadAgua[i])
    EMA.escribirSD(textoRaw)
    textoRaw=""
    EMA.envioBt (datos)
    time.sleep(1)
    

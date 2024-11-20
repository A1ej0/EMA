from EMA_Libreria_sinGSM import EMA
import time
import _thread
import random


time.sleep(1)
EMA = EMA()

datos = [0,0,0,0,0,0,0,0,0,0,0]
textoRaw=""
fecha=0
hora=0
count=0
sensores=0
fechaHora=0
ordTemp=0
frecuencia=1

#Envio de datos mediante wifi
def envioWifiBt():
    global datos,hora,EMA,frecuencia
    while True:
        frecuencia=EMA.frecuenciaDeEnvio()*60
        EMA.envioDatos(datos,hora)
        time.sleep(frecuencia) 
            
_thread.start_new_thread(envioWifiBt,())


def btEnvio():
    global EMA,hora
    while True:
        EMA.envioBt (datos,hora)
        time.sleep(2)
_thread.start_new_thread(btEnvio,())
    

while True:
    fechaHora = EMA.rtc()
    hora=str(fechaHora[4])+":"+str(fechaHora[5])+":"+str(fechaHora[6])
    fecha=str(fechaHora[2])+"/"+str(fechaHora[1])+"/"+str(fechaHora[0])[2:]
    
    try:
        sensores=EMA.sensores()
        sensores=sensores[1:-1]
        sensores=sensores.split("$")
        for i in range(len(sensores)-1):
            if float(sensores[i])!=0:
                datos[i]=sensores[i]
                
    
        if sensores[-1][0]=="D":
            datos[8]=sensores[-1][1:]
        elif sensores[-1][0]=="P":
            if ordTemp != ord(sensores[-1][2]):
                ordTemp = ord(sensores[-1][2])
                datos[7]=str(int(datos[7])+int(sensores[-1][2:]))
                print("Pluv")   
        elif sensores[-1][0]=="Q":
            datos[9]=sensores[-1][1:]
        else:
            pass
    except:
        pass
    
    #test
    #datos[0]=random.randint(0,30)
    #finTest
    if count>=3:
        #lluvia=0.149
        for i in range(len(datos)):
            if textoRaw != "":
                textoRaw=textoRaw+" , "+str(datos[i])
            else:
                textoRaw=str(datos[i])
        #Guardar datos en SD
        EMA.escribirSD(textoRaw)
        textoRaw=""
        count=0
    count=count+1
    time.sleep(5)

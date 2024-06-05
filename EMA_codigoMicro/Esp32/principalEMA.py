from EMA_Libreria import EMA
import time
import _thread
EMA = EMA()

temp= 0
datos = [0,0,0,0,0,0,0,0,0,0,0]
lecturaGPS2 = [0,0,0,0]
acel=[0,0,0]
gauss=0
lluvia=0.0
lluvias=0.0
distanci=0
textoRaw=""
fecha=0
hora=0
frecuencia=False
contadorSIM=0
count=0
count2=0
calidad=0
tempoFecha=0
auxFecha=0


#Envio de datos mediante wifi
def ThirdCore():
    
    while True:
        
        EMA.envioDatos (datos)
        time.sleep(1)
#Envio de datos mediante Bluetooth       
def FourthCore():
    while True:

        EMA.envioBt (datos)
        time.sleep(1)
#Envio de datos mediante GRPS y alerta SMS
def SecondCore():
    global frecuencia,contadorSIM

    while True:
        if not frecuencia:
            #EMA.AlertSms(lluvias,distanci,True)
            #if not EMA.envioDatosSim(datos):
                #pass
            #else:
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
#_thread.start_new_thread(ThirdCore,())
_thread.start_new_thread(SecondCore,())


while True:
    #Captura de datos
    #temp = EMA.Temperature()
    fechaHora = EMA.rtc()
    #distanci=EMA.distancia()
    #print("Distancia: "+str(distanci)+"\n")
    hora=str(fechaHora[4])+":"+str(fechaHora[5])+":"+str(fechaHora[6])
    fecha=str(fechaHora[2])+"/"+str(fechaHora[1])+"/"+str(fechaHora[0])[2:]
    date=fecha+"-"+hora
    
    calidadtemp=EMA.CalidadLoRa()
    if calidadtemp==-1:
        pass
    else:
        calidad=calidadtemp
        EMA.escribirOLED(date)
    #Organizacion de datos capturados en una lista
    datos= [temp,acel[0],acel[1],acel[2],lluvias,lecturaGPS2[0],lecturaGPS2[1],fecha,hora,calidad,distanci]
    
    #Captura de lluvias
    if count>=10:
        #lluvia=EMA.Pluviometro()*0.149
        #lluvias=lluvias+float(lluvia)
        #print("\n\nValor de lluvia: "+str(lluvias))
        
        if tempoFecha==0:
            auxFecha=fechaHora[2]
            tempoFecha=1
        else:
            if auxFecha != fechaHora[2]:
                EMA.AlertSms(lluvias,False)
                #lluvias=0
                count2=0
                tempoFecha=0
        count2=count2+1
        for i in range(len(datos)):
            if textoRaw != "":
                textoRaw=textoRaw+" , "+str(datos[i])
            else:
                textoRaw=str(datos[i])
        
        #Guardar datos en SD
        EMA.escribirSD(textoRaw)
        time.sleep(1)
        print("SD sobreescrita")
        textoRaw=""
        count=0
    count=count+1
    time.sleep(1)

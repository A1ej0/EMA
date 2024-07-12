from EMA_Libreria_construccion import EMA
import time
import _thread


time.sleep(1)
EMA = EMA()

band=0
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
auxsms=0
sensores=0
fechaHora=0


#Envio de datos mediante wifi
def envioWifiBt():
    global datos,hora,EMA
    #print('envio wifi/BT iniciado')
    while True:
        EMA.envioDatos(datos,hora)
        #EMA.envioBt (datos)
        time.sleep(1)
#Envio de datos mediante GRPS y alerta SMS
def envioGRPS():
    global frecuencia,contadorSIM,datos,auxsms,EMA
    #print('envio gprs iniciado')
    EMA.desconectarSIM()
    time.sleep(3)
    EMA.conectarSIM()
    
    while True:
        if auxsms==0:
            if not frecuencia:
                #EMA.AlertSms(lluvias,distanci,True)
                EMA.envioDatosSim(datos)     
            time.sleep(1)
        else:
            auxsms=0
            pass
            """
            EMA.desconectarSIM()
            EMA.envioDatosSMS(datos,fecha,hora)
            EMA.conectarSIM()
            auxsms=0
            time.sleep(1)
            """
            
            
             
_thread.start_new_thread(envioWifiBt,())
_thread.start_new_thread(envioGRPS,())


while True:
    fechaHora = EMA.rtc()
    hora=str(fechaHora[4])+":"+str(fechaHora[5])+":"+str(fechaHora[6])
    fecha=str(fechaHora[2])+"/"+str(fechaHora[1])+"/"+str(fechaHora[0])[2:]
    date=hora
    #EMA.escribirOLED(date,datos)
    #Organizacion de datos capturados en una lista
    #datos= [temp,acel[0],acel[1],acel[2],lluvias,lecturaGPS2[0],lecturaGPS2[1],fecha,hora,calidad,distanci]
    
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
            datos[7]=sensores[-1][1:]
        elif sensores[-1][0]=="Q":
            datos[9]=sensores[-1][1:]
        else:
            pass
        
        #print(sensores)
    except:
#         print('error sensores')
        pass
    
    
    #Captura de lluvias
    
    if count>=3:
        #lluvia=0.149
        if tempoFecha==0:
            auxFecha=fechaHora[4]
            tempoFecha=1
        else:
            if fechaHora[4] != 0:
                if auxFecha != fechaHora[4]:
                    auxsms=1
                    tempoFecha=0
                else:
                    pass
        for i in range(len(datos)):
            if textoRaw != "":
                textoRaw=textoRaw+" , "+str(datos[i])
            else:
                textoRaw=str(datos[i])
        
        #EMA.envioDatosSMS(datos,fecha,hora)
        #Guardar datos en SD
        EMA.escribirSD(textoRaw)
        time.sleep(1)
        #print("SD sobreescrita")
        textoRaw=""
        count=0
    count=count+1
    time.sleep(5)
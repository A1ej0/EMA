from machine import Pin, UART
from math import radians, cos, sin, asin, sqrt

uart = UART(2, 9600, timeout=2000, rx=16, tx=17)
flag=True
def haversine(lon1, lat1, lon2, lat2):
    #convert degrees to radians
    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance = 2 * asin(sqrt(a)) * 6371
    return distance




while True:
    try:
        lectura=uart.readline().decode()
        lectura=lectura.split(",")
        if lectura[0]=="$GPGGA":
            latitud=float(lectura[2][:2])+(float(lectura[2][2:])/60.0)
            longitud=-1.0*float(lectura[4][:3])+(float(lectura[4][3:])/60.0)
            #print("latitud: "+str(latitud)+lectura[3])
            #print("Longitud: "+str(longitud)+lectura[5])
            #print("coordenadas: "+ str(latitud)+str(longitud))
            if flag==True:
                latI=latitud
                lonI=longitud
                print("Coordenadas iniciales definidas...")
                flag=False
            
            print(str(haversine(lonI, latI,longitud, latitud)*1000)+" metros")
        
    except:
        pass
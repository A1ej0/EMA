from machine import UART
import time

uart1 = UART(2, baudrate=115200, tx=17, rx=16)

Numero="3123776985"

enviar=26
iniciar="AT\r\n"
estadoSeñal="AT+CSQ\r\n"
operadoresDisponibles="AT+COPS=?\r\n"
modoMensaje="AT+CMGF=1\r\n"
asignarNumeroMensaje="AT+CMGS=\"+57"+Numero+"\"\r\n"
recibirMensaje="AT+CNMI=1,2,0,0,0\r\n"

#Para enviar mensaje, configurar modoMensaje, luego asignarNumeroMensaje, luego enviar el mensaje con /n/r y finalmente enviar.


#uart1.write("AT+CMGF=1\r\n")  # write 5 bytes
uart1.write("AT\r\n")  # write 5 bytes
uart1.write("AT+CSQ\r\n")
uart1.write("AT+COPS=?\r\n")
while True:
    read=uart1.read()
    if read is not None:
        print(read.decode("utf-8"))         # read up to 5 bytes
    time.sleep(0.5)
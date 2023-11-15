from tkinter import * 
from tkinter import ttk
from tkinter import messagebox


raiz = Tk() 
raiz.columnconfigure(0, weight=1)
raiz.rowconfigure(0, weight=1)
raiz.title("EMA configFile")
raiz.geometry("350x300")
#raiz.iconbitmap("form.ico")
raiz.config(bg="gray")
raiz.resizable(0,0)

Color1 = "gray"

textWifi = Entry()
textClaveWifi = Entry()
textTelefono = Entry()
textMQTTserver = Entry()
textpuertoMQTT = Entry()
textUsuarioMQTT = Entry()
textClaveMQTT = Entry()

listaPuertos = ttk.Combobox(state="readonly",values=["com1","com2","com3"])

labelWifi = Label( raiz, text="Nombre de la red WIFI *",bg=Color1)
labelClaveWifi = Label(raiz,text="Clave de la red WIFI *",bg=Color1)
labelTelefono = Label(raiz,text="Numero de telefono de alerta *",bg=Color1)
labelMQTTServer = Label(raiz,text="Servidor MQTT",bg=Color1)
puertoMQTT = Label(raiz,text="Puerto MQTT",bg=Color1)
usuarioMQTT = Label(raiz,text="Usuario MQTT",bg=Color1)
claveMQTT = Label(raiz,text="Clave MQTT",bg=Color1)

def boton():
    if len(textWifi.get())==0:
        messagebox.showinfo(message="Se requiere indicar una red wifi",title="error de red wifi")
    elif len(textClaveWifi.get())==0:
        messagebox.showinfo(message="clave wifi invalida",title="error de clave wifi")
    elif len(textTelefono.get())==0:
        messagebox.showinfo(message="Se requiere indicar un telefono de alerta",title="error de telefono")
    elif len(textMQTTserver.get())==0:
        messagebox.showinfo(message="Se requiere indicar un servidor mqtt",title="error de servidor mqtt")
    elif len(textpuertoMQTT.get())==0:
        messagebox.showinfo(message="Se requiere indicar un puerto mqtt",title="error de puerto mqtt")
    elif len(textUsuarioMQTT.get())==0:
        messagebox.showinfo(message="Se requiere indicar un usuario de mqtt",title="error de usuario mqtt")
    elif len(textClaveMQTT.get())==0:
        messagebox.showinfo(message="Se requiere indicar una clave mqtt",title="error de clave mqtt")
    elif not textTelefono.get().isnumeric():
        messagebox.showinfo(message="Telefono invalido, se requiere un numero",title="telefono invalido")
    elif not textpuertoMQTT.get().isnumeric():
        messagebox.showinfo(message="puerto invalido, se requiere un numero",title="puerto invalido")
    else:      
        file = open("ema.conf","w")
        datos=[str(textWifi.get())+"\n",str(textClaveWifi.get())+"\n",str(textTelefono.get())+"\n",str(textMQTTserver.get())+"\n",str(textpuertoMQTT.get())+"\n",str(textUsuarioMQTT.get())+"\n",str(textClaveMQTT.get())+"\n"]
        file.writelines(datos)
        file.close()
        messagebox.showinfo(message="Archivo de configuracion del dispositivo creado, por favor copiar a la raiz de la memoria",title="proceso exitoso")


confirmar = Button(text="Confirmar",command=boton)


labelWifi.grid(row=1, column=0,sticky="w")
labelClaveWifi.grid(row=2,column=0,sticky="w")
labelTelefono.grid(row=3,column=0,sticky="w")
labelMQTTServer.grid(row=4,column=0,sticky="w")
puertoMQTT.grid(row=5,column=0,sticky="w")
usuarioMQTT.grid(row=6,column=0,sticky="w")
claveMQTT.grid(row=7,column=0,sticky="w")


textWifi.grid(row=1,column=2,sticky="w")
textClaveWifi.grid(row=2,column=2,sticky="w")
textTelefono.grid(row=3,column=2,sticky="w")
textMQTTserver.grid(row=4,column=2,sticky="w")
textpuertoMQTT.grid(row=5,column=2,sticky="w")
textUsuarioMQTT.grid(row=6,column=2,sticky="w")
textClaveMQTT.grid(row=7,column=2,sticky="w")




confirmar.grid(row=10,column=1,rowspan=2,sticky="ew")

raiz.rowconfigure(9,weight=1)
raiz.rowconfigure(11,weight=1)
raiz.columnconfigure(1,weight=1)





raiz.mainloop() 
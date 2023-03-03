# EMA
## Estación de monitoreo automatica


Agregar librerias y libreria global en la carpeta "lib" dentro del dispositivo.\
[Documento Caso de uso](https://docs.google.com/document/d/1Gn08lAfBX5FNaou6GQ9lSAwWgNq7yMann19ZtXc6SKk/edit?usp=sharing) Aquí se presenta el proceso de caso de uso de cada uno de los estados identificados del sistema

# Etapas Del Proceso

------------

## Etapa de arranque
- Deteccion automatica de sensores deacuerdo a una lista preestablecida de sensores compatibles con EMA  :white_check_mark:
- Menu local de ajuste **FISICO** (necesario porque no se garantiza que se cuente con dispositivo bluetooth para ajuste) :heavy_check_mark:
   - deteccion automatica de archivo de configuracion :x:
   
   - menu interactivo completo :white_check_mark:
   - Anexo automatico de sensores disponibles al menu :x:
   
   - rutina de ingreso alternativa para bucle de reset :x:
   - Proceso de calibracion se sensores disponibles :heavy_check_mark:
   
   - Eleccion de periodo de toma de muestras :white_check_mark:
   
   - Visualizacion del numero de telefono registrado (o local, por definir) :white_check_mark:
   - Ingreso automatico en modo de reposo luego de configuracion  :white_check_mark:

## Etapa de conexion

- Wifi, conexion automatica, reconexion automatica y control de errores  :white_check_mark:
- Bluetooth: espera a conexion, envio y recepcion de datos  :white_check_mark:
- GSM: envio de alertas y de muestras cuando sea requerido  :heavy_check_mark:
- Local: Almacenamiento automatico y lectura en microSD local  :white_check_mark:

## Etapa de muestreo
- protocolo MQTT: ajuste y control de excepciones, envio automatico de datos ligado al segundo nucleo  :white_check_mark:
- protocolo Bluetooth: Envio de datos disponibles en archivo local cuando se requiera  :heavy_check_mark:
- Protocolo local, guardado automatico de datos de forma periodica deacuerdo a ajustes iniciales  :heavy_check_mark:

## Etapa de visualizacion
- Local: en pantalla? por definir  :interrobang:

- Bluetooth, aplicacion movil para visualizacion de datos  :heavy_check_mark:
- Wifi: NodeREd para visualizacion de graficas de datos y alertas en tiempo real  :white_check_mark:

- Serial para debug? por definir  :interrobang:


## Faltante!!
- RTC
- Sensor HALL (pluviometro)
- definicion de puertos de conexion
- definicion de apartado fisico
- planeacion electronica (PCB, POTENCIA, ALIMENTACION)

## Notas!
###### (espacio para notas)

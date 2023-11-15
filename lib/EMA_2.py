import _thread
from time import sleep
from math import sqrt, atan2, pi, copysign, sin, cos
import utime
from machine import I2C, Pin
from mpu9250 import MPU9250
import bluetooth
from BLE import BLEUART

i2c = I2C(scl=Pin(22), sda=Pin(21))
m = MPU9250(i2c)
print("MPU9250 id: " + hex(m.whoami))

#init Bluetooth

bname="EMA01"
ble=bluetooth.BLE()
buart=BLEUART(ble,bname)

# on_RX Event

def on_RX():
    rxbuffer=buart.read().decode().rstrip('\x00')
    buart.write("EMA01 dice: "+rxbuffer+"\n")
#     for i in range(len(rxbuffer)):
#          print(ord(rxbuffer[i]))
    
    if(rxbuffer=="Hola"):
        print("Hola")
    if(rxbuffer=="Adios"):
        print("Adios")

# register IRQ handler

buart.irq(handler=on_RX)



#calibration and bias offset
m.ak8963.calibrate(count=100)
pitch_bias = 0.0
roll_bias = 0.0

#low pass filter
filtered_x_value = 0.0
filtered_y_value = 0.0

#declination = 40

def degrees_to_heading(degrees):
    heading = ""
    if (degrees > 337) or (degrees >= 0 and degrees <= 22):
            heading = 'N'
    if degrees >22 and degrees <= 67:
        heading = "NE"
    if degrees >67 and degrees <= 112:
        heading = "E"
    if degrees >112 and degrees <= 157:
        heading = "SE"
    if degrees > 157 and degrees <= 202:
        heading = "S"
    if degrees > 202 and degrees <= 247:
        heading = "SW"
    if degrees > 247 and degrees <= 292:
        heading = "W"
    if degrees > 292 and degrees <= 337:
        heading = "NW"
    return heading

def get_reading()->float:
    ''' Returns the readings from the sensor '''
    global filtered_y_value, filtered_x_value
    x = m.acceleration[0] 
    y = m.acceleration[1]
    z = m.acceleration[2] 

    # Pitch and Roll in Radians
    roll_rad = atan2(-x, sqrt((z*z)+(y*y)))
    pitch_rad = atan2(z, copysign(y,y)*sqrt((0.01*x*x)+(y*y)))

    # Pitch and Roll in Degrees
    pitch = pitch_rad*180/pi
    roll = roll_rad*180/pi

    # Get soft_iron adjusted values from the magnetometer
    mag_x, mag_y, magz = m.magnetic

    filtered_x_value = low_pass_filter(mag_x, filtered_x_value)
    filtered_y_value = low_pass_filter(mag_y, filtered_y_value)

    az =  90 - atan2(filtered_y_value, filtered_x_value) * 180 / pi

    # make sure the angle is always positive, and between 0 and 360 degrees
    if az < 0:
        az += 360
        
    # Adjust for original bias
    pitch -= pitch_bias
    roll -= roll_bias

    heading = degrees_to_heading(az)

    return x, y, z, pitch, roll, az, heading

def low_pass_filter(raw_value:float, remembered_value):
    ''' Only applied 20% of the raw value to the filtered value '''
    
    # global filtered_value
    alpha = 0.8
    filtered = 0
    filtered = (alpha * remembered_value) + (1.0 - alpha) * raw_value
    return filtered

def show():
    ''' Shows the Pitch, Rool and heading '''
    x, y, z, pitch, roll, az, heading_value = get_reading()
    print("Pitch",round(pitch,1), "Roll",round(roll, 1), "compass", az,"Heading", heading_value)
    print("Accel x:",m.acceleration[0],"Accel y:",m.acceleration[1],"Accel z:",m.acceleration[2])
    print("Temperatura:",m.temperature)
    sleep(0.2)

# reset orientation to zero
x,y,z, pitch_bias, roll_bias, az, az_raw = get_reading()




def pruebaSegundoCore():
    while True:
        print("mundo")
        sleep(1)

_thread.start_new_thread(pruebaSegundoCore,())



while True:
    show()
    print("hola")
    utime.sleep_ms(1000)
  
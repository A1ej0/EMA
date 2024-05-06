from machine import Pin, SoftI2C

i2c = SoftI2C(scl=Pin(8), sda=Pin(9), freq=100_000)

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
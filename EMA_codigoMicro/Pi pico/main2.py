from machine import SoftI2C, Pin, I2C
i2c0 = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100_000)
i2c1 = SoftI2C(scl=Pin(27), sda=Pin(26), freq=100_000)
# i2c2 = SoftI2C(scl=Pin(21), sda=Pin(20), freq=100_000)
# i2c3 = SoftI2C(scl=Pin(19), sda=Pin(18), freq=100_000)
# i2c4= SoftI2C(scl=Pin(17), sda=Pin(16), freq=100_000)
# 
# devices = i2c1.scan()
# 
# if len(devices) == 0:
#     print("No I2C devices found.")
# else:
#     print("I2C devices found:")
#     for device in devices:
#         print(hex(device))
#         
devices0= i2c0.scan()

if len(devices0) == 0:
    print("No I2C devices found.")
else:
    print("I2C devices found:")
    for device0 in devices0:
        print(hex(device0))
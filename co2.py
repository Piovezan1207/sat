from machine import I2C, Pin
import CCS811
import time


bus=I2C(scl=Pin(22), sda=Pin(21))
sCCS811 = CCS811.CCS811(i2c=bus, addr=90)
for count in range(10):
  if sCCS811.data_ready():
    print(sCCS811.eCO2)
    print(sCCS811.tVOC)
  time.sleep(1)

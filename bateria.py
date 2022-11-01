#A leitura do ADC da bateria vai de 0 a 2600
from machine import ADC
from machine import Pin
import time

adc35=ADC(Pin(35))
adc35.atten(ADC.ATTN_11DB)
adc35.width(ADC.WIDTH_12BIT)


while True:
  print(str(adc35.read()) + ',')
  time.sleep(0.5)

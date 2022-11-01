import network
import time
import urequests
from machine import I2C, Pin, ADC
from micropython import const
from mpu6500 import MPU6500
from ak8963 import AK8963
from bmp280 import *



# pylint: enable=import-error

################################################ DHT - TEMP
def sht20_temperature():
    i2c.writeto(0x40,b'\xf3')
    time.sleep_ms(70)
    t=i2c.readfrom(0x40, 2)
    return -46.86+175.72*(t[0]*256+t[1])/65535

def sht20_humidity():
    i2c.writeto(0x40,b'\xf5')
    time.sleep_ms(70)
    t=i2c.readfrom(0x40, 2)
    return -6+125*(t[0]*256+t[1])/65535

i2c=I2C(scl=Pin(22), sda=Pin(21))
################################################ DHT - TEMP


################################################ WIFI
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect('Planta 4.0','Planta40@eniacehdiferente')
print("Waiting for Wifi connection")
while not sta_if.isconnected(): 
    time.sleep(1)
    print(".")
print("Connected, ip -  {}".format(sta_if.ifconfig()))

################################################ WIFI







################################################ MPU

__version__ = "0.3.0"

# Used for enabling and disabling the I2C bypass access
_INT_PIN_CFG = const(0x37)
_I2C_BYPASS_MASK = const(0b00000010)
_I2C_BYPASS_EN = const(0b00000010)
_I2C_BYPASS_DIS = const(0b00000000)

class MPU9250:
    """Class which provides interface to MPU9250 9-axis motion tracking device."""
    def __init__(self, i2c, mpu6500 = None, ak8963 = None):
        if mpu6500 is None:
            self.mpu6500 = MPU6500(i2c)
        else:
            self.mpu6500 = mpu6500

        # Enable I2C bypass to access AK8963 directly.
        char = self.mpu6500._register_char(_INT_PIN_CFG)
        char &= ~_I2C_BYPASS_MASK # clear I2C bits
        char |= _I2C_BYPASS_EN
        self.mpu6500._register_char(_INT_PIN_CFG, char)

        if ak8963 is None:
            self.ak8963 = AK8963(i2c)
        else:
            self.ak8963 = ak8963

    @property
    def acceleration(self):
        """
        Acceleration measured by the sensor. By default will return a
        3-tuple of X, Y, Z axis values in m/s^2 as floats. To get values in g
        pass `accel_fs=SF_G` parameter to the MPU6500 constructor.
        """
        return self.mpu6500.acceleration

    @property
    def gyro(self):
        """
        Gyro measured by the sensor. By default will return a 3-tuple of
        X, Y, Z axis values in rad/s as floats. To get values in deg/s pass
        `gyro_sf=SF_DEG_S` parameter to the MPU6500 constructor.
        """
        return self.mpu6500.gyro

    @property
    def temperature(self):
        """
        Die temperature in celcius as a float.
        """
        return self.mpu6500.temperature

    @property
    def magnetic(self):
        """
        X, Y, Z axis micro-Tesla (uT) as floats.
        """
        return self.ak8963.magnetic

    @property
    def whoami(self):
        return self.mpu6500.whoami

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

mpu9250s = MPU9250(i2c)
################################################ MPU

################################################ PRESSAO
bmp280 = BMP280(i2c)
bmp280.use_case(BMP280_CASE_WEATHER)
bmp280.oversample(BMP280_OS_HIGH)

################################################ PRESSAO

################################################ BATERIA -  um adc s
adc35=ADC(Pin(35))
adc35.atten(ADC.ATTN_11DB)
adc35.width(ADC.WIDTH_12BIT)

def ma_bateria(val):
    res =  (100*val) / 2600 
    return res

################################################ BATERIA -  um adc s


for i in range (0, 10):
    try:

        bmp280.normal_measure()

        a =urequests.request('post', "http://192.168.178.105:5678", 
        json={"equipe" : "x",
        "bateria" : str(ma_bateria(adc35.read())),
        "temperatura" : str(sht20_temperature()),
        "pressao" : str(bmp280.pressure),
        "giroscopio" : list(mpu9250s.gyro),
        "acelerometro" : list(mpu9250s.acceleration),
        "payload" : {
            "n_imagens" : "x",
            "ultima_imagem" : "x",
            "co2" : "x"        
            }
         },
            headers={"Content-Type" : "application/json"})
        a.close()
        time.sleep(0.5)
    except:
        print("erro")
        time.sleep(0.5)





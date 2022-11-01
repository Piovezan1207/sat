import network
import time
import urequests

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect('OBSAT_WIFI','OBSatZenith1000')
print("Waiting for Wifi connection")
while not sta_if.isconnected(): 
    time.sleep(1)
    print(".")
print("Connected, ip -  {}".format(sta_if.ifconfig()))

# urequests.request('get', "192.168.178.101:5000", data="teste", json=None, headers={})
urequests.request('get', "192.168.178.101:5000", data=[("a" , "b")])
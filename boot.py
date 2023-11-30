try:
  import usocket as socket
except:
  import socket
  
from time import sleep, sleep_ms
from machine import Pin, ADC
import onewire, ds18x20
import network
import gc

gc.collect()
gc.threshold(10240)

m_pin = ADC(28)
m_power = Pin(27, mode=Pin.OUT, value=0)

ds_pin = Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

network.hostname("gardenpi")
ssid = '<redacted>'
password = '<redacted>'

wlan = network.WLAN(network.STA_IF)

wlan.active(True)
wlan.config(pm = 0xa11140)  # Disable power-save mode
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    sleep(1)
    print('ip = ' + status[0])


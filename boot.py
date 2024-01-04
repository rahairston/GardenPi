try:
  import usocket as socket
except:
  import socket
  
from time import sleep, sleep_ms
from machine import Pin, ADC
import onewire, ds18x20
import network
import gc
import busio
import board
import adafruit_max1704x

gc.collect()
gc.threshold(10240)

m_pin = ADC(28)
m_power = Pin(27, mode=Pin.OUT, value=0)

ds_pin = Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

i2c = busio.I2C(board.GP1, board.GP0)  # uses board.SCL and board.SDA
max17 = adafruit_max1704x.MAX17048(i2c)
max17.comparator_disabled = True
max17.quick_start = True
max17.hibernate()

network.hostname("weatherpi")
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


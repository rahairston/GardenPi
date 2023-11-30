# GardenPi

My Raspberry pi pico project code saved for reference and transportation purposes.

Uses a ds18B20 sensor for temperature sensing and a [SparkFun Soil Moisture Sensor](https://www.sparkfun.com/products/13637) for the moisture detection.

All data is visible via web browser endpoints and I have a prometheus instance scraping the /metrics endpoint (hence the weird formatting)

If using, just remember to replace the `ssid` and `password` in lines 22 and 23 of `boot.py`
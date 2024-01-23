import uasyncio as asyncio
import gc, json
import urequests as requests

headers = { "Content-Type": "application/json" }
loop = asyncio.get_event_loop()
two56_kb = 256.0 * 1024.0

def read_temp_sensor():
    roms = ds_sensor.scan()
    ds_sensor.convert_temp()
    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        if isinstance(temp, float):
            msg = round(temp, 2)
            if msg > 55.5:
                sleep(0.1)
                return read_temp_sensor()
        return msg
    return b'0.0'

def get_soil_moisture():
    m_power.on()
    sleep_ms(10)
    reading = m_pin.read_u16() * 100 / 65535
    m_power.off()
    return reading

def get_temperature():
    temp = read_temp_sensor()
    far = round(temp * (9/5) + 32.0, 2)
    return far

def get_battery_stats():
    percent = f"{max17.cell_percent:.2f}"
    voltage = f"{max17.cell_voltage:.2f}"
    rate = f"{max17.charge_rate:.2f}"
    return (percent, voltage, rate)

async def serve_client(reader, writer):
    request_line = await reader.readline()
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    if "/metrics" in str(request_line):
        temperature = get_temperature()
        body = '# HELP Temperature temperature of the garden.\r\n# TYPE temperature gauge\n'
        body += 'temperature{deviceTitle="Garden Pico"} ' + str(temperature)
        moisture = get_soil_moisture()
        body += '\n# HELP Moisture moisture of the garden soil.\r\n# TYPE moisture gauge\n'
        body += 'moisture{deviceTitle="Garden Pico"} ' + str(moisture)
        body += '\n# HELP Memory_Used memory used of the pico.\r\n# TYPE memory_used gauge\n'
        body += 'memory_used{deviceTitle="Garden Pico"} ' + str((gc.mem_alloc() / (two56_kb)) * 100.0)
        battery_stats = get_battery_stats()
        body += '\n# HELP Battery_Charge Charge percent remaining of the LiPo Battery.\r\n# TYPE battery_charge gauge\n'
        body += 'battery_charge{deviceTitle="Garden Pico"} ' + battery_stats[0]
        body += '\n# HELP Battery_Voltage LiPo Battery Voltage.\r\n# TYPE battery_voltage gauge\n'
        body += 'battery_voltage{deviceTitle="Garden Pico"} ' + battery_stats[1]
        body += '\n# HELP Battery_Charge_Rate Charge or Discharge Rate of the LiPo Battery.\r\n# TYPE battery_charge_rate gauge\n'
        body += 'battery_charge_rate{deviceTitle="Garden Pico"} ' + battery_stats[2]
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text\r\n\r\n')
    else:
        body = {}
        
        if "/temperature" in str(request_line):
            body = get_temperature()
        elif "/moisture" in str(request_line):
            body = get_soil_moisture()
        else:
            body = {"temperature" : get_temperature(), "moisture": get_soil_moisture(), "battery": f"{max17.cell_percent:.1f} %"}
        body = json.dumps(body)
        writer.write('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
    writer.write(body)

    await writer.drain()
    await writer.wait_closed()
    gc.collect()

# While I don't need async for this case, if I ever repurpose this it might be nice
async def main():
    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    print('You can now connect!')
    while True:
        await asyncio.sleep(3600)
        
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()



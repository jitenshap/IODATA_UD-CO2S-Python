import serial
import time

#Must change to your UD-CO2S Port
co2s = serial.Serial('COM26')

#Stop dumping
time.sleep(0.5)
co2s.write(b'\r\n')
time.sleep(0.1)
co2s.write(b'STP\r\n')

#Discard buffer
while co2s.in_waiting <= 0:
    time.sleep(0.1)
time.sleep(0.1)
co2s.read(co2s.in_waiting)

#Start dumping
co2s.write(b'STA\r\n')
while True:
    if co2s.in_waiting > 0:
        time.sleep(0.1)
        r = co2s.read(co2s.in_waiting).decode('ASCII')
        if r == 'OK STA\r\n':
            print('START')
        elif r == 'NG\r\n':
            print('FAIL')
            quit()
        else:
            #Measuring data received
            env = {}
            arr = r.split('\r\n')[0].split(',')
            env['co2'] = arr[0].split('=')[1]
            env['temperature'] = arr[2].split('=')[1]
            env['humidity'] = arr[1].split('=')[1]
            print(env)

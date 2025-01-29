import serial
import threading
from time import sleep

filter_array = []
def rolling_filter(input_value):
    global filter_array
    filter_array.append(input_value)

    if len(filter_array) >= 200:
        filter_array.pop(0)
    
    sorted_array = filter_array.copy()
    sorted_array.sort()
    #print(filter_array)
    return sorted_array[int(len(sorted_array)/2)]

terminate_program = False
wind_speed_global = 'no_wind_data'

def read_wind_data():
    global terminate_program
    global wind_speed_global
    port = '/dev/ttyS0'
    baud_rate = 9600

    try:
        with serial.Serial(port, baud_rate, timeout=1) as ser:
            while not terminate_program:
                try:
                    wind_data = ser.readline().decode('utf-8').strip()
                    wind_speed = rolling_filter(wind_data)

                    wind_speed = int(wind_speed) - 200
                    if wind_speed < 0:
                        wind_speed = 0

                    wind_speed /= 24.0588

                    wind_speed = round(wind_speed,1)

                    wind_speed_global = wind_speed

                except ValueError:
                    print('Unknown wind speed value')

    except serial.SerialException as e:
        print(f'error: {e}')

temperature_global = 0

def read_temperature():
    global terminate_program
    global temperature_global
    filepath = '/sys/bus/w1/devices/28-012063b6f39f/temperature'

    try:
        with open(filepath,'r') as read_temperature:
            while not terminate_program:
                read_temperature.seek(0)
    
                temperature = read_temperature.readline().strip()

                temperature = int(temperature) / 1000

                temperature_global = round(temperature,1)

    except:
        print('An error occured while reading temperture prope')

def main():
    global terminate_program
    global wind_speed_global
    global temperature_global
    read_wind_speed_thread = threading.Thread(target=read_wind_data)
    read_temperature_thread = threading.Thread(target=read_temperature)

    read_temperature_thread.start()
    read_wind_speed_thread.start()

    try:
        while True:
            print(f'Wind Speed: {wind_speed_global} m/s | Temperature: {temperature_global} °c')
            sleep(0.1)
    except KeyboardInterrupt:
        terminate_program = True
        read_temperature_thread.join()
        read_wind_speed_thread.join()
        print('Program terminated')

wind_speed_thread = 0
temperature_thread = 0

def start_weather_station():
    global wind_speed_thread
    global temperature_thread
    wind_speed_thread = threading.Thread(target=read_wind_data)
    temperature_thread = threading.Thread(target=read_temperature)

    temperature_thread.start()
    wind_speed_thread.start()

def weather_station_data():
    global wind_speed_global
    global temperature_global

    return wind_speed_global, temperature_global

def terminate_weather_station():
    global terminate_program
    terminate_program = True
    temperature_thread.join()
    wind_speed_thread.join()
    print('Program terminated')

if __name__ == '__main__':
    main()
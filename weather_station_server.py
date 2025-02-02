#Denna kod används inte!!! Ville bara testa och sätta upp en LAN server

import socket
import weather_station
from time import sleep

def server():
    print ('Server Stared')

    MY_IP_ADR = '192.168.171.132'
    PORT = 55555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(15)
    s.bind((MY_IP_ADR, PORT))
    s.listen()

    try:
        print('Waiting for connection...')
        conn, adr = s.accept()
        print(f'Connected to client: {conn}')
        print('Starting weather station')

        weather_station.start_weather_station()
        while True:
            data = weather_station.weather_station_data()
            wind_speed = data[0]
            temperature = data[1]
            message = str(wind_speed) +'-'+str(temperature)
            conn.send(message.encode('utf-8'))
            sleep(0.1)
        
    except KeyboardInterrupt:
        print('\nTerminating program')

    except:
        print('Connection time out')

    weather_station.terminate_weather_station()
    s.close()
    print('Server Stopped')

if __name__ == '__main__':
    server()

import socket
from time import sleep
import guizero as gz

def client():
    print('Client started')

    SERVER_IP = '192.168.171.132'
    SERVER_PORT = 55555

    client_socket = socket.socket()

    client_socket.connect((SERVER_IP, SERVER_PORT))

    try:
        while True:
            data = client_socket.recv(1024)
            data = data.decode('utf-8')
            data = data.split('-')

            wind_speed = data[0]
            temperature = data[1]

            #print(f'Wind Speed: {wind_speed} m/s | Temperature: {temperature} °C')

            sleep(0.1)

    except KeyboardInterrupt:
        client_socket.close()

        print('Terminating client')

wind_speed_gui = 0
def gui():
    global wind_speed_gui
    app = gz.App(title='Weather Station')
    wind_speed_gui = gz.Text(app,text=f'Wind Speed: N/A m/s')
    app.display

if __name__ == '__main__':
    #gui()
    client()
import paho.mqtt.client as mqtt
import threading
from time import sleep

def on_connect_wind_data(client, userdata, flags, rc):
    client.subscribe('YRGO/ei23/wind_ms/grupp_jn',qos=1)

def on_connect_temp_data(client, userdata, flags, rc):
    client.subscribe('YRGO/ei23/temp_degC/grupp_jn',qos=1)

wind_data = 0
def on_message_wind_data (client, userdata, msg):
    global wind_data
    wind_data = msg.payload.decode('utf-8')

temp_data = 0
def on_message_temp_data (client, userdata, msg):
    global temp_data
    temp_data = msg.payload.decode('utf-8')

terminate_program = False
def mqtt_wind_data():
    global terminate_program
    client = mqtt.Client()

    client.connect('broker.hivemq.com', port=1883, keepalive=60)
                   
    while not terminate_program:
        client.on_connect = on_connect_wind_data
        client.on_message = on_message_wind_data

        client.loop()

def mqtt_temp_data():
    global terminate_program
    client = mqtt.Client()

    client.connect('broker.hivemq.com', port=1883, keepalive=60)
                   
    while not terminate_program:
        client.on_connect = on_connect_temp_data
        client.on_message = on_message_temp_data

        client.loop()

def main():
    global wind_data
    global temp_data
    global terminate_program

    wind_data_thread = threading.Thread(target=mqtt_wind_data)
    temp_data_thread = threading.Thread(target=mqtt_temp_data)

    wind_data_thread.start()
    temp_data_thread.start()

    try:
        while True:
            print(f'Wind Speed: {wind_data} m/s | Temperatur: {temp_data} °C')
            sleep (1)
    
    except KeyboardInterrupt:
        print ('Terminating Program')
        terminate_program = True
        wind_data_thread.join()
        temp_data_thread.join()
        print ('Program Terminated')


if __name__ == '__main__':
    main()
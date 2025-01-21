import paho.mqtt.client as mqtt
import threading
from time import sleep
import guizero as gz

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

wind_speed_text = 0
temperature_text = 0
def gui():
    global wind_speed_text
    global temperature_text

    app = gz.App(title='Weather Station')
    header_text = gz.Text(app,text='Weather Station', size=30)
    wind_speed_text = gz.Text(app,text='Wind Speed: N/A m/s')
    temperature_text = gz.Text(app,text='Temperatur: N/A °C')

    app.display()

def main():
    global wind_data
    global temp_data
    global terminate_program
    global wind_speed_text
    global temperature_text

    wind_data_thread = threading.Thread(target=mqtt_wind_data)
    temp_data_thread = threading.Thread(target=mqtt_temp_data)
    gui_thread = threading.Thread(target=gui)

    wind_data_thread.start()
    temp_data_thread.start()
    gui_thread.start()

    try:
        while not terminate_program:
            sleep(0.1)
            wind_speed_text.value = f'Wind Speed: {wind_data} m/s'
            temperature_text.value = f'Temperatur: {temp_data} °C'

    
    except KeyboardInterrupt:
        print ('Terminating Program')

    except RuntimeError:
        print ('Closing Program')

    terminate_program = True
    wind_data_thread.join()
    temp_data_thread.join()
    gui_thread.join()
    print ('Program Terminated')

if __name__ == '__main__':
    main()
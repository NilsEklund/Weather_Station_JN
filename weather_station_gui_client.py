import paho.mqtt.client as mqtt
import threading
from time import sleep
import guizero as gz

def on_connect_wind_data(client, userdata, flags, rc):
    client.subscribe('YRGO/ei23/wind_ms/grupp4',qos=1)

def on_connect_temp_data(client, userdata, flags, rc):
    client.subscribe('YRGO/ei23/temp_degC/grupp4',qos=1)

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
    try:            
        while not terminate_program:
            client.on_connect = on_connect_wind_data
            client.on_message = on_message_wind_data

            client.loop()
    
    except:
        print ('error reading wind data')

    print('Wind Data Thread Closed')

def mqtt_temp_data():
    global terminate_program
    client = mqtt.Client()

    client.connect('broker.hivemq.com', port=1883, keepalive=60)
    try:               
        while not terminate_program:
            client.on_connect = on_connect_temp_data
            client.on_message = on_message_temp_data

            client.loop()
    
    except:
        print ('error reading temperature data')

    print('Temperture Thread Closed')

def app_update():
    global wind_speed_text
    global wind_data
    global temperature_text
    global temp_data
    global app

    wind_speed_text.value = f'Wind Speed: {wind_data} m/s'
    temperature_text.value = f'Temperatur: {temp_data} °C'
    app.after(time=100,function=app_update)
    
app = 0
def main():
    global wind_data
    global temp_data
    global terminate_program
    global wind_speed_text
    global temperature_text
    global app

    wind_data_thread = threading.Thread(target=mqtt_wind_data)
    temp_data_thread = threading.Thread(target=mqtt_temp_data)

    wind_data_thread.start()
    temp_data_thread.start()

    app = gz.App(title='Weather Station',bg=(0x7c,0xa9,0xd3))
    header_text = gz.Text(app,text='Weather Station', size=30)
    picture = gz.Picture(app, image='DJI_0056.JPG',width= 400,height= 300)
    wind_speed_text = gz.Text(app,text='Wind Speed: N/A m/s',size=20)
    temperature_text = gz.Text(app,text='Temperatur: N/A °C',size=20)

    app_update()

    app.display()

    terminate_program = True
    print ('Closing Program')
    wind_data_thread.join()
    temp_data_thread.join()
    print ('Program Closed')

if __name__ == '__main__':
    main()
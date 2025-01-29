import paho.mqtt.client as mqtt
import weather_station
from time import sleep

def mqtt_client():
    print('Starting mqtt client')
    client = mqtt.Client()
    client.connect("broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()
    try:
        print('Starting Weather Station')
        weather_station.start_weather_station()
        while True:

            data = weather_station.weather_station_data()
            wind_speed = data[0]
            temperature = data[1]

            msg = client.publish("yrgo_ei23/vind_ms/grupp4", payload= wind_speed, qos=1)

            msg.wait_for_publish()

            msg = client.publish("yrgo_ei23/temp_degC/grupp4", payload= temperature, qos=1)

            msg.wait_for_publish()

            sleep(1)
    except KeyboardInterrupt:
        client.disconnect()
        print('\nTerminating program')
        weather_station.terminate_weather_station()

if __name__ == '__main__':
    mqtt_client()
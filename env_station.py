import time
import random
import paho.mqtt.client as mqtt
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("Environmental_Station")

# ThingSpeak MQTT Configuration
MQTT_SERVER = "mqtt3.thingspeak.com"
MQTT_PORT = 1883

MY_CLIENT_ID = "Hh8cBgkqHQM7GSIIOAEQGQE"
MY_USERNAME = "Hh8cBgkqHQM7GSIIOAEQGQE"
MY_PASSWORD = "0uROr1Q03z+pvHjIQXRjw5By"
MY_CHANNEL_ID = "2888579"

STATIONS = [
    {"id": "ENV_STATION_001", "location": "Building A"},
    {"id": "ENV_STATION_002", "location": "Building B"},
    {"id": "ENV_STATION_003", "location": "Outdoor Garden"}
]

if not os.path.exists("logs"):
    os.makedirs("logs")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to ThingSpeak MQTT broker")
    else:
        logger.error(f"Connection failed with code {rc}")

def on_publish(client, userdata, mid):
    logger.info(f"Message {mid} published successfully")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning(f"Unexpected disconnection, code: {rc}")

def generate_sensor_data():
    temperature = round(random.uniform(-50, 50), 2)
    humidity = round(random.uniform(0, 100), 2)
    co2 = random.randint(300, 2000)
    
    return {
        "temperature": temperature,
        "humidity": humidity,
        "co2": co2,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def log_reading(data):
    try:
        with open("logs/sensor_readings.csv", "a") as file:
            if os.stat("logs/sensor_readings.csv").st_size == 0:
                file.write("timestamp,temperature,humidity,co2\n")
            
            file.write(f"{data['timestamp']},{data['temperature']},{data['humidity']},{data['co2']}\n")
    except Exception as e:
        logger.error(f"Error writing to log file: {e}")

def main():
    # Initialize MQTT client
    mqtt_client = mqtt.Client(client_id=MY_CLIENT_ID, protocol=mqtt.MQTTv311)
    mqtt_client.username_pw_set(MY_USERNAME, MY_PASSWORD)
    
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.on_disconnect = on_disconnect
    
    # Connect to ThingSpeak
    try:
        mqtt_client.connect(MQTT_SERVER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        
        logger.info("Starting environmental monitoring system...")
        logger.info(f"Publishing to ThingSpeak channel: {MY_CHANNEL_ID}")
        
        time.sleep(2)
        
        # Publishing loop
        while True:
            sensor_data = generate_sensor_data()
            
            mqtt_payload = (
                f"field1={sensor_data['temperature']}"
                f"&field2={sensor_data['humidity']}"
                f"&field3={sensor_data['co2']}"
            )
            
            topic = f"channels/{MY_CHANNEL_ID}/publish"
            result = mqtt_client.publish(topic, mqtt_payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Data sent: Temp={sensor_data['temperature']}°C, "
                           f"Humidity={sensor_data['humidity']}%, CO2={sensor_data['co2']}ppm")
                
                # Log the reading
                log_reading(sensor_data)
            else:
                logger.error(f"Failed to publish data, error code: {result.rc}")
            
            # Wait for next reading (ThingSpeak free tier limit is 15 seconds)
            time.sleep(15)
    
    except KeyboardInterrupt:
        logger.info("Stopping data collection...")
    
    except Exception as e:
        logger.error(f"Error in main function: {e}")
    
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        logger.info("Disconnected from MQTT broker")

if __name__ == "__main__":
    main()
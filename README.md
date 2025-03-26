# IoT Environmental Monitoring System

## Assignment Overview
This assignment implements a cloud-based IoT system that collects environmental data from virtual sensors and publishes it to ThingSpeak using the MQTT protocol. The system monitors temperature, humidity, and CO2 levels from virtual environmental stations.

## Components

### 1. Environmental Station (Publisher)
`env_station.py` - Simulates environmental sensors that collect data and publish it to ThingSpeak.

Features:
- Generates random environmental data (temperature, humidity, CO2)
- Publishes data to ThingSpeak using MQTT protocol
- Logs all readings to CSV file for local access

### 2. Data Viewer (Subscriber)
`subscriber.py` - Allows users to view the sensor data collected over time.

Features:
- Interactive menu to select which sensor data to view
- Displays historical data from the past 5 hours
- Automatically detects and reads from available log files

## Setup Instructions

### Prerequisites
- Python 3.6 or higher
- Required Python packages: `paho-mqtt`

### Installation
1. Clone this repository:

git clone https://github.com/tejasmdevang/environment_sensors.git

cd environment_sensors

2. Install required packages:
pip install paho-mqtt

### Configuration
- You must update the ThingSpeak credentials in `env_station.py` with your own:
  - `MY_CLIENT_ID`
  - `MY_USERNAME`
  - `MY_PASSWORD`
  - `MY_CHANNEL_ID`

## Usage

1. Run the environmental station to start publishing data:
2. python env_station.py
2. In a separate terminal, run the subscriber to view collected data:
3. python subscriber.py

3. Select the sensor type you want to view (temperature, humidity, or CO2)

4. Data can also be viewed in the ThingSpeak channel dashboard

from datetime import datetime, timedelta
import os
import glob

def find_and_show_sensor_data(sensor_type, hours=5):
    if sensor_type not in ["temperature", "humidity", "co2"]:
        print("Invalid sensor type. Please choose from: temperature, humidity, co2")
        return
    
    cutoff = datetime.now() - timedelta(hours=hours)
    print(f"\nAttempting to show {sensor_type} data from the last {hours} hours:\n")
    
    possible_paths = [
        "sensor_log.txt",
        "logs/sensor_readings.csv",
        "*.csv",
        "logs/*.csv"
    ]
    
    found_files = []
    for pattern in possible_paths:
        found_files.extend(glob.glob(pattern))
    
    if not found_files:
        print("Error: No log files found in any expected location.")
        return
    
    print(f"Found these log files: {found_files}")
    
    data_found = False
    
    for log_file in found_files:
        print(f"\nReading from: {log_file}")
        
        try:
            with open(log_file, "r") as file:
                lines = file.readlines()
                
                # Skip empty files
                if not lines:
                    print(f"File {log_file} is empty.")
                    continue
                
                # Check if first line is a header
                first_line = lines[0].strip().lower()
                has_header = "timestamp" in first_line or "time" in first_line
                
                # Process each line
                for i, line in enumerate(lines):
                    if has_header and i == 0:
                        continue  # Skip header
                    
                    parts = line.strip().split(",")
                    
                    if len(parts) < 3:
                        continue  # Not enough data
                    
                    try:
                        if len(parts) >= 4:  # timestamp, temp, hum, co2
                            timestamp_str = parts[0]
                            temp_idx, hum_idx, co2_idx = 1, 2, 3
                        else:
                            print(f"Unexpected format in line: {line}")
                            continue
                        
                        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                        
                        if timestamp >= cutoff:
                            data_found = True
                            
                            if sensor_type == "temperature":
                                value = parts[temp_idx]
                                unit = "°C"
                            elif sensor_type == "humidity":
                                value = parts[hum_idx]
                                unit = "%"
                            else:  # CO2
                                value = parts[co2_idx]
                                unit = "ppm"
                            
                            # Display the data
                            print(f"{timestamp} - {sensor_type.capitalize()}: {value}{unit}")
                    
                    except (ValueError, IndexError) as e:
                        print(f"Error processing line: {line.strip()} - {str(e)}")
                        continue
        
        except Exception as e:
            print(f"Error reading file {log_file}: {str(e)}")
    
    if not data_found:
        print(f"No {sensor_type} data found in the last {hours} hours in any file.")

def main():
    print("Environmental Sensor Data Viewer")
    
    # Get sensor type from user
    print("\nAvailable sensors:")
    print("1. Temperature")
    print("2. Humidity")
    print("3. CO2")
    
    choice = input("\nSelect sensor to view (1-3): ")
    
    # Map choice to sensor type
    if choice == "1":
        sensor_type = "temperature"
    elif choice == "2":
        sensor_type = "humidity"
    elif choice == "3":
        sensor_type = "co2"
    else:
        print("Invalid choice. Using temperature as default.")
        sensor_type = "temperature"
    
    find_and_show_sensor_data(sensor_type)

if __name__ == "__main__":
    main()
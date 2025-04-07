import requests
import random
import time
import psutil

# Define the API endpoint
url = "http://127.0.0.1:8000/api/search/labour-babycaretaker/"

# Define a list of dummy data for testing
dummy_data_list = [
    {"gender": "Male", "city": "mysore", "area": "JP Nagar"},
    {"gender": "female", "city": "Chennai", "area": "T Nagar"},
    {"gender": "male", "city": "Mumbai", "area": "Andheri"},
    {"gender": "female", "city": "Kolkata", "area": "Salt Lake"},

]

# Function to send a single POST request
def send_post_request(dummy_data):
    request_body = {
        **dummy_data,
        "work_category": "babycaretaker"
    }
    try:
        response = requests.post(url, json=request_body)
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print("Error:", response.status_code, response.json())
    except Exception as e:
        print("Request failed:", e)
import logging
# Configure logging
logging.basicConfig(
    filename='performance_logs.log',  # Log file name
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(message)s',  # Log format with timestamp
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

# Function to monitor system performance
def monitor_performance():
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)  # Measure CPU utilization over 1 second
    print(f"Memory Used: {memory.used / (1024 ** 2):.2f} MB | CPU Usage: {cpu}%")

    if cpu >20 :
            log_message = f"Memory Used: {memory.used / (1024 ** 2):.2f} MB | CPU Usage: {cpu}% | Bad | Please check it"
            logging.warning(log_message)
    else:
        log_message = f"Memory Used: {memory.used / (1024 ** 2):.2f} MB | CPU Usage: {cpu}% | Good"
    logging.info(log_message)

# Continuously hit the API with random dummy data and monitor performance
def perform_stress_test_with_monitoring(repeat_count=100, delay=1):
    for _ in range(repeat_count):
        dummy_data = random.choice(dummy_data_list)
        send_post_request(dummy_data)
        monitor_performance()
        time.sleep(delay)  # Add delay between requests to avoid overwhelming the server

# Perform the stress test
if __name__ == "__main__":
    # You can adjust the repeat_count and delay to your needs
    perform_stress_test_with_monitoring(repeat_count=500, delay=0.2)

"""pylint option block-disable"""

import json
import os
import requests
import paho.mqtt.client as mqtt

# Constants
INPUT_TOPIC_NAME = 'awsiot_to_localgateway'
OUTPUT_TOPIC_NAME = 'localgateway_to_awsiot'
HUE_API_IP = os.environ['HUE_API_IP']
HUE_API_USER = os.environ['HUE_API_USER']
HUE_API_BASE = 'http://' + HUE_API_IP + '/api/' + HUE_API_USER + '/'

# Service clients
MQTT_CLIENT = mqtt.Client()

def on_connect(_client, _userdata, _flags, result):
    """Subscribe to input topic"""

    print('Connected ' + str(result))

    print('Subscribing to ' + INPUT_TOPIC_NAME)
    MQTT_CLIENT.subscribe(INPUT_TOPIC_NAME)

    print('Using Hue API ' + HUE_API_IP + ' with user ' + HUE_API_USER)


# Operations for message handler
def get_state(data):
    """Get state of all lights"""
    request_url = HUE_API_BASE + 'lights/'
    
    if 'lightId' in data:
        request_url += str(data['lightId']) + '/'

    print('Request: ' + request_url)
    response = requests.get(request_url).json()
    return response


# Map of operation (from topic) to handler function
OPERATION_FUNCTION_MAP = {
    'getState': get_state
}


def on_message(_client, _userdata, message):
    """Handle messages"""

    print('Received message: ' + str(message.payload))
    payload = json.loads(message.payload)
    operation = payload['operation']
    data = payload['data']

    response = OPERATION_FUNCTION_MAP[operation](data)
    print('Response: ' + str(response))
    MQTT_CLIENT.publish(OUTPUT_TOPIC_NAME, json.dumps(response))
 

def main(): # pylint: disable=C0111
    MQTT_CLIENT.on_connect = on_connect
    MQTT_CLIENT.on_message = on_message

    MQTT_CLIENT.connect('localhost', 1883)
    MQTT_CLIENT.loop_forever()


if __name__ == '__main__':
    main()

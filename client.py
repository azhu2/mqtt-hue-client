"""pylint option block-disable"""

import paho.mqtt.client as mqtt

INPUT_TOPIC_NAME = 'awsiot_to_localgateway'

def on_connect(client, userdata, flags, result):
    """Subscribe to input topic"""

    print('Connected ' + str(result))
    client.subscribe(INPUT_TOPIC_NAME)

def on_message(client, userdata, message):
    """Handle messages"""

    print('Received message ' + str(message.payload))

def main(): # pylint: disable=C0111
    _mqtt_client = mqtt.Client()
    _mqtt_client.on_connect = on_connect
    _mqtt_client.on_message = on_message

    _mqtt_client.connect('localhost', 1883)
    _mqtt_client.loop_forever()

if __name__ == '__main__':
    main()

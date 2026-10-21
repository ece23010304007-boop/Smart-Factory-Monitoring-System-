import json
import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "factory/+/telemetry"

def on_connect(client,userdata,flags,reason_code,properties):
    if reason_code == 0:
        print("connected to MQTT Broker!")
        client.subscribe(TOPIC,qos=1)
        print("Subscribed to:",TOPIC)
    else:
        print("connection failed:",reason_code)

def on_message(client,userdata,message):
    try:
        data = json.loads(message.payload.decode())

        print("\n==========FACTORY MONITOR=========")
        print("Machine ID:",data["machine_id"])
        print("Temperature:",data["temperature"],"*c")
        print("Vibration:",data["vibration"])
        print("RPM:",data["rpm"])
        print("Status:",["status"])
        print("======================================")
    except(ValueError,KeyError) as error:
        print("invalid message:",error)

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="factory_monitor"
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER,PORT,60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Monitor stopped.")
    client.disconnect()

     
    
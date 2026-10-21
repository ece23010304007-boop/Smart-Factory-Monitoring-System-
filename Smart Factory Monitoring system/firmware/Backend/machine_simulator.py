import json
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"
PORT = 1883

MACHINES = ["M001", "M002", "M003"]

def create_client(machine_id):
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=f"factory_{machine_id}"
    )
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    return client

clients = {
    machine_id: create_client(machine_id)
    for machine_id in MACHINES
}

try:
    while True:
        for machine_id, client in clients.items():

            temperature = round(random.uniform(35, 95), 2)
            vibration = round(random.uniform(0.2, 8.0), 2)
            rpm = random.randint(900, 1800)

            status = (
                "WARNING"
                if temperature > 80 or vibration > 6
                else "RUNNING"
            )

            data = {
                "machine_id": machine_id,
                "temperature": temperature,
                "vibration": vibration,
                "rpm": rpm,
                "status": status,
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat()
            }

            topic = f"factory/{machine_id}/telemetry"

            client.publish(topic, json.dumps(data), qos=1)

            print(f"{topic} -> {json.dumps(data)}")

        time.sleep(3)

except KeyboardInterrupt:
    print("Stopping factory simulator...")

finally:
    for client in clients.values():
        client.loop_stop()
        client.disconnect()
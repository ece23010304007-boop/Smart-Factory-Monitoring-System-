import json
import threading

import pandas as pd
import paho.mqtt.client as mqtt
import streamlit as st

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "factory/+/telemetry"

st.set_page_config(page_title="Smart Factory Monitor", page_icon="🏭", layout="wide")


@st.cache_resource
def start_mqtt():
    store = {"data": {}, "lock": threading.Lock()}

    def on_connect(client, userdata, flags, reason_code, properties):
        if not reason_code.is_failure:
            client.subscribe(TOPIC, qos=1)

    def on_message(client, userdata, message):
        try:
            data = json.loads(message.payload.decode())
            with store["lock"]:
                store["data"][data["machine_id"]] = data
        except (ValueError, KeyError):
            pass

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="factory_dashboard",
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect_async(BROKER, PORT, 60)
    client.loop_start()
    return client, store


st.title("🏭 Smart Factory Monitoring System")
st.caption("Live MQTT-based industrial machine monitoring")

client, store = start_mqtt()


@st.fragment(run_every=2)
def live_view():
    if client.is_connected():
        st.success("MQTT broker connected")
    else:
        st.error("MQTT broker se connect nahi hua. Mosquitto chal raha hai?")

    with store["lock"]:
        snapshot = dict(store["data"])

    if not snapshot:
        st.info("Waiting for machine data. Start machine_simulator.py in another terminal.")
        return

    df = pd.DataFrame(snapshot.values())
    total = len(df)
    warnings = int((df["status"] == "WARNING").sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("Machines Online", total)
    c2.metric("Running", total - warnings)
    c3.metric("Warnings", warnings)

    cols = ["machine_id", "temperature", "vibration", "rpm", "status"]
    st.subheader("Machine Status")
    st.dataframe(df[cols], use_container_width=True, hide_index=True)

    chart_df = df.set_index("machine_id")
    st.subheader("Temperature Monitoring")
    st.bar_chart(chart_df[["temperature"]])
    st.subheader("Vibration Monitoring")
    st.bar_chart(chart_df[["vibration"]])

    warning_df = df[df["status"] == "WARNING"]
    if not warning_df.empty:
        st.warning("One or more machines need attention!")
        st.dataframe(warning_df[cols], hide_index=True)


live_view()
st.caption("Readings are simulated; no physical sensors are connected.")
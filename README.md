Smart Factory Monitoring System
MQTT-Based Real-Time Industrial Telemetry Data Pipeline & Streamlit Visual Analytics

1. System Overview
The Smart Factory Monitoring System is an end-to-end IoT software pipeline engineered to simulate, ingest, store, and visualize real-time industrial telemetry. Operating over the lightweight MQTT (Message Queuing Telemetry Transport) messaging protocol, the system captures continuous metrics—such as machine operating temperature, hydraulic pressure, and machine availability states—and streams them to an interactive dashboard.

2. Core Architecture Components
1. Telemetry Simulator
machine_simulator.py

Simulates physical factory machinery. Periodically generates state payloads and publishes them to MQTT broker topics.

2. Ingestion Engine
monitor.py

Subscribes to MQTT topics, receives JSON payloads, parses incoming data, and appends time-series rows to local CSV storage.

3. Visual Dashboard
dashboard.py

Built with Streamlit. Reads the telemetry database, calculates KPIs, and renders interactive graphs for operators.

3. Data Pipeline & Protocol Architecture
MACHINE SIMULATOR
(machine_simulator.py)
MQTT Publish
MQTT BROKER
(HiveMQ / Mosquitto)
MQTT Subscribe
MONITOR ENGINE
(monitor.py)
CSV Log
WEB DASHBOARD
(telemetry.csv)
(dashboard.py)
Key Architectural Advantage
The decoupled publish-subscribe pattern ensures that data generation and monitoring operate independently. If the frontend UI is restarted or updated, data ingestion continues uninterrupted in the background.

Smart Factory Monitoring System — Technical Guide
Page 1 of 3
4. System Environment & Prerequisites
Before deploying the system, verify that your computing environment meets the following baseline requirements:

Python Runtime: Python 3.9 or higher installed (check via python --version).
Development Environment: Visual Studio Code or any command-line integrated terminal.
Package Manager: pip (Python Package Installer, bundled with standard installation).
5. Installation & Setup Guide
Step 1: Open Project Directory & Create Virtual Environment
Navigate to the project root directory in your terminal and initialize an isolated virtual environment (venv):

# Windows (PowerShell)
python -m venv venv

# macOS / Linux
python3 -m venv venv
Step 2: Activate the Virtual Environment
# Windows (PowerShell)
.\venv\Scripts\Activate

# macOS / Linux
source venv/bin/activate
Note for Windows PowerShell: If execution policy errors prevent script activation, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

Step 3: Install Required Dependencies
With the virtual environment active (venv), upgrade core tools and install the necessary dependencies:

python -m pip install --upgrade pip setuptools wheel
pip install streamlit paho-mqtt pandas
6. MQTT Broker Configuration Options
Option A: Public Test Broker (Default)
No local software installation required. Pre-configured endpoints inside scripts:

• Host: broker.hivemq.com
• Port: 1883

Option B: Local Mosquitto Broker
For offline or industrial network setups:

1. Install Eclipse Mosquitto from mosquitto.org.
2. Run mosquitto -v
3. Set broker host string to "localhost".

Smart Factory Monitoring System — Technical Guide
Page 2 of 3
7. Multi-Terminal Execution Instructions
To run the complete data pipeline, open THREE separate terminal tabs in VS Code with (venv) activated in each:

Terminal	Component	Command	Expected Outcome
Terminal 1	Data Simulator	python machine_simulator.py	Publishes simulated telemetry data payloads to broker.
Terminal 2	MQTT Collector	python monitor.py	Listens to MQTT broker and logs telemetry to telemetry.csv.
Terminal 3	Web Dashboard	streamlit run dashboard.py	Launches interactive browser dashboard at http://localhost:8501.
8. Troubleshooting & Common Issues
Issue / Error	Root Cause	Resolution
'streamlit' is not recognized	Streamlit not installed inside active venv.	Verify (venv) activation and run python -m pip install streamlit.
"No telemetry data found" banner	telemetry.csv has not been generated yet.	Ensure both machine_simulator.py and monitor.py are actively running.
Dashboard stuck on loading	File lock or path mismatch reading CSV.	Perform hard browser refresh (Ctrl+Shift+R) or run python -m streamlit run dashboard.py.
Navigating to http://localhost:8501 renders live machine metrics and alerts.

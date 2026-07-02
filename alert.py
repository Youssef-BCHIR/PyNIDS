import json
import os
from datetime import datetime

LOG_FILE = "punids_alerts.json"

def format_alert(flow_key, flow, prediction):
    return {
        "timestamp": datetime.now().isoformat(),
        "ip_source": flow_key[0],
        "ip_destination": flow_key[1],
        "port_source": flow_key[2],
        "port_destination": flow_key[3],
        "protocol": flow_key[4],
        "packet_count": flow["packet_count"],
        "byte_count": flow["byte_count"],
        "duration": round(flow["last_time"]-flow["start_time"],3),
        "anomaly_score": round(prediction["score"],4)
    }

def save_alert(alert):
    alerts = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                 alerts = json.load(f)
            except json.JSONDecodeError:
                alerts=[]
    alerts.append(alert)
    with open(LOG_FILE,"w") as f:
        json.dump(alerts, f, indent=2)

def print_alert(alert):
    print("\n" + "="*50)
    print("[!]  ANOMALY DETECTED")
    print(f"    Time    : {alert['timestamp']}")
    print(f"    Source  : {alert['ip_source']}:{alert['port_source']}")
    print(f"    Target  : {alert['ip_destination']}:{alert['port_destination']}")
    print(f"    Packets : {alert['packet_count']}")
    print(f"    Bytes   : {alert['byte_count']}")
    print(f"    Duration: {alert['duration']}s")
    print(f"    Score   : {alert['anomaly_score']}")
    print("="*50+"\n")

def trigger_alert(flow_key, flow, prediction):
    alert = format_alert(flow_key, flow, prediction)
    save_alert(alert)
    print_alert(alert)

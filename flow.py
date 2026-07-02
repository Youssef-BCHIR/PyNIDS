import time
from collections import defaultdict

FLOW_TIMEOUT = 30
active_flows={}

def get_flow_key(packet_informations):
    return (
        min(packet_informations["ip_source"], packet_informations["ip_destination"]),
        max(packet_informations["ip_source"], packet_informations["ip_destination"]),
        min(packet_informations["port_source"], packet_informations["port_destination"]),
        max(packet_informations["port_source"], packet_informations["port_destination"]),
        packet_informations["protocol"]
    )

def update_flow(packet_informations):
    key = get_flow_key(packet_informations)
    timestamp = packet_informations["timestamp"]

    if key not in active_flows:
        active_flows[key] = {
            "start_time": timestamp,
            "last_time": timestamp,
            "packet_count": 1,
            "byte_count": packet_informations["size"],
            "syn_count": 0,
            "ack_count": 0,
            "flags_seen": []
        }
    else:
        flow = active_flows[key]
        flow["last_time"] = timestamp
        flow["packet_count"] += 1
        flow["byte_count"] += packet_informations["size"]
    
    flags = packet_informations["flags"]
    if flags:
        active_flows[key]["flags_seen"].append(int(flags))
        if flags & 0x02:
            active_flows[key]["syn_count"] += 1
        if flags & 0x10:
            active_flows[key]["ack_count"] += 1

def check_timeouts():
    now = time.time()
    expired = []

    for key, flow in list(active_flows.items()):
        if now - flow["last_time"] > FLOW_TIMEOUT:
            expired.append((key,flow))
            del active_flows[key]
    
    return expired
    


import time
import threading
from capture import start_capture, process_packet
from flow import update_flow, check_timeouts, active_flows
from features import extract_features
from detector import Detector
from alert import trigger_alert
from dashboard import print_alert_rich, print_stats

detector = Detector(contamination=0.05)
alert_count = 0
is_training = True

TRAINING_DURATION = 60
DASHBOARD_REFRESH = 5
INTERFACE = "wlp0s20f3"

def handle_packet(packet):
    from scapy.all import IP, TCP, UDP
    if not packet.haslayer(IP):
        return
    from capture import process_packet
    pkt_info = process_packet(packet)
    if pkt_info:
        update_flow(pkt_info)
    
def periodic_tasks():
    global alert_count, is_training
    while True:
        time.sleep(DASHBOARD_REFRESH)
        expired = check_timeouts()
        for key, flow in expired:
            features = extract_features(flow)
            if is_training:
                detector.add_training_sample(features)
            else:
                result = detector.predict(features)
                if result and result["is_anomaly"]:
                    alert_count += 1
                    trigger_alert(key, flow, result)
        if is_training:
            if not detector.train():
                pass
            else:
                is_training = False
                detector.save()
                print("[*] Training complete. Detection mode active.")
        print_stats(active_flows, alert_count, len(detector.training_data))

def main():
    print("[*] PyNIDS starting...")
    print(f"[*] Training phase -- {TRAINING_DURATION}s of normal traffic needed.")
    t = threading.Thread(target=periodic_tasks, daemon=True)
    t.start()
    if detector.load():
        is_training = False
        print("[*] Existing model loaded. Starting in detection mode.")
    from scapy.all import sniff
    sniff(iface=INTERFACE, prn=handle_packet, store=False)

if __name__ == "__main__":
    main()
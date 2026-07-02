from scapy.all import sniff, IP, TCP, UDP

def process_packet(packet):
    
    if not packet.haslayer(IP):
        return 

    ip_source = packet[IP].src
    ip_destination = packet[IP].dst
    protocol = packet[IP].proto
    size = len(packet)

    port_source = 0
    port_destination = 0
    flags = 0

    if packet.haslayer(TCP):
        port_source = packet[TCP].sport
        port_destination = packet[TCP].dport
        flags = packet[TCP].flags
    elif packet.haslayer(UDP):
        port_source = packet[UDP].sport
        port_destination = packet[UDP].dport
         
    packet_informations = {
        "ip_source": ip_source,
        "ip_destination": ip_destination,
        "port_source": port_source,
        "port_destination": port_destination,
        "protocol": protocol,
        "size": size,
        "flags": flags,
        "timestamp": float(packet.time)
    }
    return packet_informations


def start_capture(interface="eth0"):
    print(f"[*] capture started on {interface}")  
    sniff(iface=interface, prn=process_packet, store=False)

if __name__ == "__main__":
    start_capture()


def extract_features(flow):
    duration = flow["last_time"] - flow["start_time"]
    packet_count = flow["packet_count"]
    byte_count = flow["byte_count"]
    syn_count = flow["syn_count"]
    ack_count = flow["ack_count"]

    average_packet_size = byte_count / (packet_count + 1)
    syn_ack_ratio = syn_count / (ack_count + 1)
    packets_per_second = packet_count / (duration + 1)

    feature_vector = [
        duration,
        packet_count,
        byte_count,
        average_packet_size,
        syn_count,
        ack_count,
        syn_ack_ratio,
        packets_per_second
    ]

    return feature_vector

"""
def get_feature_names():

    return [
        "duration",
        "packet_count",
        "byte_count",
        "average_packet_size",
        "syn_count",
        "ack_count",
        "syn_ack_ratio",
        "packets_per_second"
    ]
"""

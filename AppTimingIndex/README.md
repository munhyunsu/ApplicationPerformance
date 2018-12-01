# Descriptions
- Extract flow information from pcap and XML

# Usage
- need tshark
- python3 app\_index.py .pcap

## tshark commands
- tshark -Y "tcp or udp" -T fields -e frame.time_relative -e ip.proto -e ip.src -e tcp.srcport -e udp.srcport -e ip.dst -e tcp.dstport -e udp.dstport -e tcp.flags.syn -e tcp.flags.ack -e tcp.flags.fin -e ssl.change_cipher_spec -e dns.a -e dns.qry.name -E header=y -E separator=, -r ?.pcap

# TODO
- Ignore just ACK

# Reference
## pcap\_processor test files
- https://wiki.wireshark.org/SampleCaptures

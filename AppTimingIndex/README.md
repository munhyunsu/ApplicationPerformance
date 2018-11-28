# Descriptions
- Extract flow information from pcap and XML

# Usage
- need tshark
- python3 app\_index.py .pcap

## tshark commands
- tshark -Y "dns" -T fields -e frame.time_relative -e ip.proto -e ip.src -e tcp.srcport -e udp.srcport -e ip.dst -e tcp.dstport -e udp.dstport -e dns.a -e dns.qry.name -E header=y -E separator=, -r ?.pcap

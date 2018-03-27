#!/bin/bash

echo "package,tcpconnection,port80,port443"
for entry in ./*.pcap
do
  result1=`tcpdump -nr $entry 'tcp[tcpflags] & (tcp-syn|tcp-ack) = (tcp-syn|tcp-ack)' 2>/dev/null | wc -l`
  result2=`tcpdump -nr $entry 'port 80' 2>/dev/null | wc -l`
  result3=`tcpdump -nr $entry 'port 443' 2>/dev/null | wc -l`
  result4=`tcpdump -nr $entry 'not port 80 and not port 443 and not icmp and not port 53' 2>/dev/null | wc -l`
  echo "$entry,$result1,$result2,$result3,$result4"
done

"""Replace last byte in ICMP payloads with 0. With ping you can see that the packets were modified."""

import nfqueue
from scapy.all import *

queue = 1

conn = nfqueue.Connection()

try:
    q = conn.bind(queue)
    q.set_mode(0xffff, nfqueue.COPY_PACKET)
except PermissionError:
    print("Access denied; Do I have root rights or the needed capabilities?")
    sys.exit(-1)

while True:
    try:
        for packet in conn:
            p = IP(packet.payload)
            p[Raw].load = p[Raw].load[:-1] + b'\x00'
            del p[ICMP].chksum
            packet.payload = bytes(p)
            packet.mangle()
    except nfqueue.BufferOverflowException:
        print("buffer error")
        pass

conn.close()

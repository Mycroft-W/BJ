# Linux security

RAW,NAT,MANGLE,FILTER

INPUT,OUTPUT,FORWARD,PREROUTING,POSTROUTING,

SNAT:
    iptables -t nat -A POSTROUTING -s 192.168.1.10/24 -j SNAT  --to-source 202.1.1.1

DNAT:
    iptables -t nat -A PREROUTING -d 202.1.1.1 -p tcp --dport 8080 -j DNAT -to 192.168.1.100:80

MASQUERADE:
    iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -j MASQUERADE

DROP:
    iptables -t filter -A INPUT -s 192.168.1.1 -j DROP

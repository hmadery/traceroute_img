### Notes
# dépend d'une API gratuite ip-aoi
# il faut apprendre à dessiner sur une carte import PIL ?
# recherche changement de route / métrique ? à chaque ping 
### Debug
# placement des coordonnées incorrectes

# imports
import socket
import json
import requests
# img
from PIL import Image, ImageDraw
# minimal scapy import (can be optimise ?)
from scapy.layers.inet import IP
from scapy.layers.inet import ICMP
import scapy.sendrecv

host = "dns.google"
path = []

for i in range(1, 64):
    pkt = IP(dst=host, ttl=i)/ICMP(type="echo-request")
    rcv = scapy.sendrecv.sr1(pkt, verbose=False, timeout=1)
    if rcv:
        try:
            hostname = socket.gethostbyaddr(rcv[0].src)[0]
        except:
            hostname = "***"
        print(f"hop{i} : {rcv[0].src}  -  {hostname}")
        try:
            geo_rlt = json.loads(requests.get("http://ip-api.com/json/"+str(rcv[0].src)+"?fields=country,lat,lon").content)
            country = geo_rlt["country"]
            lat = geo_rlt["lat"]
            lon = geo_rlt["lon"]
            path.append((round(lon*5+900),round(900-(lat*5+450))))
            print(country+" : "+str(lat)+" / "+str(lon)+"\n")
        except:
            print("***\n")
        if hostname == host:
            break
    else:
        print(f'{i} timeout.')

# draw the path
img = Image.open("simplemap.png")
draw = ImageDraw.Draw(img)
draw.line(path, fill="red", width=5)
img.show()

print("Done.")
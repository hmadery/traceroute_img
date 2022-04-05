### Notes
# dépend d'une API gratuite ip-aoi
# il faut apprendre à dessiner sur une carte import PIL ?
# recherche changement de route / métrique ? à chaque ping 
### Debug
# placement des coordonnées incorrectes

# imports
import string
import sys
import socket
import json
import requests
# img
from PIL import Image, ImageDraw
# minimal scapy import (can be optimise ?)
from scapy.layers.inet import IP
from scapy.layers.inet import ICMP
import scapy.sendrecv


# main
def main(mhost: string) :

    host = mhost

    # convert
    if sys.argv[2] == "N":
        host = socket.gethostbyname(host)

    path = []

    for i in range(1, 64):
        pkt = IP(dst=host, ttl=i)/ICMP(type="echo-request")
        rcv = scapy.sendrecv.sr1(pkt, verbose=False, timeout=1)
        if rcv:
            try:
                hostname = socket.gethostbyaddr(host)
            except:
                hostname = ["*","*","*"]
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
            if rcv[0].src == host:
                img = Image.open("simplemap.png")
                draw = ImageDraw.Draw(img)
                draw.line(path, fill="red", width=5)
                img.show()
                return 0
        else:
            print(f'hop{i} timeout.')

    return 0

    # draw the path
    

    print("Done.")

if __name__ == "__main__":
    main(sys.argv[1])
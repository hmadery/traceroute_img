# to do
# add pygame animation option ? or gif with PIL ?

# imports
from decimal import MIN_ETINY
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
# img tmp names
import string
import random


# main
def main(mhost: string) :

    host = mhost
    path = []
    img_list = []

    # convert
    if sys.argv[2] == "N":
        host = socket.gethostbyname(host)

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
                draw.line(path, fill="red", width=2)
                img.show()
                #gif
                md = 0
                for i in range(len(path)-1) :
                    # pythagore
                    md_x = path[i+1][0] - path[i][0]
                    md_y = path[i+1][1] - path[i][1]
                    d = (md_x ** 2 + md_y ** 2) ** 0.5
                    hops = round(d // 10 + 1)
                    m_x = md_x / hops
                    m_y = md_y / hops
                    for h in range(hops) :
                        img_tmp = Image.open("simplemap.png")
                        draw_tmp = ImageDraw.Draw(img_tmp)
                        draw_tmp.ellipse((path[i][0]+m_x*h-10, path[i][1]+m_y*h-10, path[i][0]+m_x*h+10, path[i][1]+m_y*h+10), fill = 'red', outline ='red')
                        # name generation
                        letters = string.ascii_uppercase
                        gname = ''.join(random.choice(letters) for i in range(10))
                        img_tmp.save("./tmp/"+gname+".png")
                        img_list.append(gname)
                    md += d
                print(md)
                for i in range(img_list):
                    

                return 0
        else:
            print(f'hop{i} timeout.')

    return 0

if __name__ == "__main__":
    if len(sys.argv) != 3 :
        print("This command needs 2 arguments.")
    else :
        main(sys.argv[1])
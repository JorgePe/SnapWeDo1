#!/usr/bin/env python3

# #Snap! extension base by Technoboy10
# https://github.com/technoboy10/snap-server/blob/master/snap-server.py
# Adapted for python3 and WeDo 1.0 by JorgePe
# September 2017
# tested on:
# - Raspberry Pi Zero W ruuning Raspbian (kernel 4.9.35+)
# - x64 laptop running Ubuntu 17.04 (kernel 4.10.0-35)

import http.server
import re
import os
import socketserver

from wedo import WeDo
from time import sleep

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def send_head(self):
        path = self.path
        print(path)
        ospath = os.path.abspath('')

        if 'move' in path:
            regex = re.compile("\/move([ab])x([0-9]+)x([0-9]+)x([+-])")
            m = regex.match(path)
            print('Regex: ',m.group(1),m.group(2),m.group(3),m.group(4))
            if m.group(4) == '-':
                dutycycle = -1 * int(m.group(2))
            elif m.group(4) == "+":
                dutycycle = int(m.group(2))
            milliseconds = int(m.group(3))
            motor = m.group(1)
            print('Motor: ',motor)
            print('Ms:    ',milliseconds)
            print('DC:    ',dutycycle)
            print('Ms/1000:',milliseconds/1000)
            if motor == "a":
                wd.motor_a = dutycycle
                sleep(milliseconds/1000)
                wd.motor_a = 0
            elif motor == "b":
                wd.motor_b = dutycycle
                sleep(milliseconds/1000)
                wd.motor_b = 0
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            #self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()


        # Warning:
        # this left a file 'tilt' and other file 'dist' in the current directory
        # containing the last value

        if path=='/tilt':
            f = open(ospath + '/tilt', 'w+')
            f.write(str(wd.tilt))
            f.close()
            f = open(ospath + '/tilt', 'rb')
            ctype = self.guess_type(ospath + '/tilt')
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return f

        elif path=='/dist':
            f = open(ospath + '/dist', 'w+')
            f.write(str(wd.distance))
            f.close()
            f = open(ospath + '/dist', 'rb')
            ctype = self.guess_type(ospath + '/dist')
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return f

if __name__ == "__main__":
    print('Snap! WeDo 1.0 extension by JorgePe')

    PORT = 8001 

    Handler = CORSHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler, bind_and_activate=False)
    httpd.allow_reuse_address = True
    try:
        httpd.server_bind()
        httpd.server_activate()
    except:
        httpd.server_close()
        raise
    wd=WeDo()

    print('Serving at port', PORT)
    print('Go ahead and launch Snap!')
    print('<a>http://snap.berkeley.edu/snapsource/snap.html</a>')
    print('Then import SnapWeDo1.xml containing block definitions for motor and sensors.')
    httpd.serve_forever()


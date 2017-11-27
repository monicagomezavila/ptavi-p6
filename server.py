#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os.path
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):

        for line in self.rfile:
            if line.decode('utf-8') != '\r\n' or '' or not line:
                linea = line.decode('utf-8')
                print(linea)

                MET = linea[:linea.find(' ')]
                partuser = linea[linea.rfind(':')+1:]
                USER = partuser[:partuser.rfind('@')]
                partip = linea[linea.rfind('@')+1:]
                IP = partip[:partip.rfind(' ')]
                ok = (MET.upper() + ' sip:' + USER + '@' + IP + ' SIP/2.0\r\n')

                if linea == ok:
                    if MET == 'INVITE' and IP == (sys.argv[1]):
                        self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                        self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    elif MET == 'BYE' and IP == (sys.argv[1]):
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    elif MET == 'ACK' and IP == (sys.argv[1]):
                        m = ('mp32rtp -i 127.0.0.1 -p 23032 < ')
                        m += str(sys.argv[3])
                        os.system(m)
                    else:
                        l = ('SIP/2.0 405 Method Not Allowed\r\n\r\n')
                        self.wfile.write(bytes(l, 'utf-8'))
                else:
                    self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")

if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.exit('Usage: python3 server.py IP port audio_file')

    if os.path.exists(sys.argv[3]):
        PUERTO = int(sys.argv[2])
        serv = socketserver.UDPServer(('', PUERTO), EchoHandler)
        print("Listening...")
        try:
            serv.serve_forever()
        except KeyboardInterrupt:
            print("Finalizado servidor")
    else:
        sys.exit('Usage: python3 server.py IP port audio_file')

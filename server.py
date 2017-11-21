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
                metodo = linea[:linea.find(' ')]
                partuser = linea[linea.rfind(':')+1:]
                user = partuser[:partuser.rfind('@')]
                partip = linea[linea.rfind('@')+1:]
                ip = partip[:partip.rfind(' ')]
                okline = (metodo + ' sip:' + user + '@' + ip + ' SIP/2.0\r\n')

                if linea == okline:
                    if metodo == 'INVITE' and ip == (sys.argv[1]):
                        self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                        self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    elif metodo == 'BYE' and ip == (sys.argv[1]):
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    elif metodo == 'ACK' and ip == (sys.argv[1]):
                        continue
                        #listclient = list(self.client_address
                    else:
                        self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
                else:
                    self.wfile.write(b"SIP/2.0 Bad Request\r\n\r\n")


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

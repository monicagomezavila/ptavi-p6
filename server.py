#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os.path

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):

        for line in self.rfile:
            if line.decode('utf-8') != '\r\n' or '' or not line:
                print("El cliente nos manda " + line.decode('utf-8'))
                linea = line.decode('utf-8')
                metodo = linea[:linea.find(' ')]
                if metodo == 'INVITE':
                    self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 Ringing\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                elif metodo == 'BYE':
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                elif metodo == 'ACK':
                    continue
                else:
                    self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n") 

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
        

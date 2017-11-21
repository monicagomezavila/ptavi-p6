#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

if len(sys.argv) != 3:
    print('Usage: client.py metodo receptor@IPreceptor:puertoSIP')
    sys.exit()

METODO = str(sys.argv[1])

# Datos del servidor.
NAMESERV = str(str(sys.argv[2])[:str(sys.argv[2]).find('@')])
ipserver = str(sys.argv[2])[str(sys.argv[2]).rfind('@')+1:]
IPSERV = str(ipserver[:ipserver.rfind(':')])
PUERTOSERV = int((sys.argv[2])[str(sys.argv[2]).rfind(':')+1:])

LINE = ''
if METODO == 'INVITE':
    LINE = ('INVITE sip:' + NAMESERV + '@' + IPSERV + ' SIP/2.0\r\n')
elif METODO == 'BYE':
    LINE = ('BYE sip:' + NAMESERV + '@' + IPSERV + ' SIP/2.0\r\n')
else:
    sys.exit('Usage: client.py method receptor@IPreceptor:puertoSIP')


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IPSERV, PUERTOSERV))
    try:
        try:
            my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
            data = my_socket.recv(1024)

            print(data.decode('utf-8'))

            MENSAJESERVER = (data.decode('utf-8').split())

            if MENSAJESERVER[-1] == ('OK' or 'Trying' or 'Ringing'):
                msj = ('ACK sip:' + NAMESERV + '@' + IPSERV + ' SIP/2.0\r\n')
                my_socket.send(bytes(msj, 'utf-8') + b'\r\n')



        except KeyboardInterrupt:
            print('Usage: client.py method receptor@IPreceptor:puertoSIP')

    except ConnectionRefusedError:
        print('Usage: client.py method receptor@IPreceptor:puertoSIP')

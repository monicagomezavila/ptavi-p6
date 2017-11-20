#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

if len(sys.argv) != 3:
    print('Usage: client.py metodo receptor@IPreceptor:puertoSIP')
    sys.exit()

METODO = str(sys.argv[1])
print(METODO)
# Datos del servidor.
NAMESERVER = str(str(sys.argv[2])[:str(sys.argv[2]).find('@')])
ipserver = str(sys.argv[2])[str(sys.argv[2]).rfind('@')+1:]
IPSERVER = str(ipserver[:ipserver.rfind(':')])
PUERTOSERVER = int((sys.argv[2])[str(sys.argv[2]).rfind(':')+1:])

LINE = ''
if METODO == 'INVITE':
    LINE = ('INVITE sip:' + NAMESERVER + '@' + IPSERVER + ' SIP/2.0\r\n')

elif METODO == 'BYE':
    LINE = ('BYE sip:' + NAMESERVER + '@' + IPSERVER + ' SIP/2.0\r\n')
else:
    print('Usage: client.py INVITE/BYE receptor@IPreceptor:puertoSIP')


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IPSERVER, PUERTOSERVER))

    print("Enviando: " + LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)

    print(data.decode('utf-8'))
    print("Terminando socket...")

print("Fin.")

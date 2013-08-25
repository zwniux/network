#!/usr/bin/env python
# coding=utf-8

import socket

def get_dest_host(message):
  line = message.split('\n')
  if len(line) > 2:
    first_line = line[1]
    dest_host= first_line.split(' ')[1].strip()
    return dest_host

proxy_port = 7070
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.bind(('',proxy_port))
proxy_socket.listen(1)

print "服务器已开启....."
while True:
  connectSocket, addr = proxy_socket.accept()
  message = connectSocket.recv(2048)
  dest_host = get_dest_host(message)
  if dest_host != None:
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sendSocket.connect((dest_host, 80))
    sendSocket.send(message)
    recvMsg = sendSocket.recv(1000000)
    connectSocket.send(recvMsg)
    sendSocket.close()
  connectSocket.close()


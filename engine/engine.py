#!/usr/bin/env python
# coding=utf-8

import socket

def getEngine(host):
  try:
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, 80))
    request = "GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % host
    mySocket.send(request)
    response = mySocket.recv(8192)
    lines = response.split('\r\n')
    for line in lines:
      if line.find('Server:') != -1:
        return line.split(' ')[1].strip()
  except:
    return None

if __name__ == '__main__':
  import sys
  host = 'www.taobao.com'
  if len(sys.argv) > 1:
    host = sys.argv[1]
  print host, "server is", getEngine(host)

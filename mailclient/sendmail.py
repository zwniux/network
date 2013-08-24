#!/usr/bin/env python
# coding=utf-8

import socket
import base64

host = 'smtp.qq.com'
port = 25
username = '943105021@qq.com'
password = '12345678'
username_code = base64.b64encode(username)
password_code = base64.b64encode(password)
recipient = '12345678@qq.com'

print username, password

msg = {
  'helo':'helo localhost\r\n',
  'auth':'auth login\r\n',
  'user':username_code + '\r\n',
  'pass':password_code + '\r\n',
  'from':'mail from:<' + username + '>\r\n',
  'to':'rcpt to:<' + recipient + '>\r\n',
  'data':'data\r\n',
  'context':'from:<test@test.com>\r\nto:<you@test.com>\r\nsubject:hello!\r\n\r\nJust For Fun!\r\n.\r\n' 
    }

for n in xrange(2):
  mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  mysock.connect((host, port))
  recMsg = mysock.recv(1024)
  mysock.send(msg['helo'])
  recMsg = mysock.recv(1024)
  mysock.send(msg['auth'])
  recMsg = mysock.recv(1024)
  mysock.send(msg['user'])
  recMsg = mysock.recv(1024)
  mysock.send(msg['pass'])
  print recMsg
  recMsg = mysock.recv(1024)
  mysock.send(msg['from'])
  recMsg = mysock.recv(1024)
  mysock.send(msg['to'])
  recMsg = mysock.recv(1024)
  mysock.send(msg['data'])
  recMsg = mysock.recv(1024)
  mysock.send(msg['context'])
  recMsg = mysock.recv(1024)
  print recMsg

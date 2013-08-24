#!/usr/bin/env python
# coding=utf-8

import socket, os, struct, time, select

def checksum(source_string):
  """
  校验和算法，返回字符串校验和
  """
  sum = 0L
  countTo = (len(source_string)/2)*2
  count = 0L

  while count < countTo:
    val = ord(source_string[count+1])*256 + ord(source_string[count])
    sum = sum + val
    count = count + 2

  if countTo != len(source_string):
    sum = sum + ord(source_string[len(source_string)-1])

  sum = (sum >> 16) + (sum & 0xffff)
  sum = (sum >> 16) + sum
  answer = ~sum
  answer = answer & 0xffff

  answer = (answer >> 8) | (answer << 8) & 0xff00

  return answer

def send_ping(my_socket, addr, ID):
  """
  发送到 addr 消息 ICMP：Type 8 Code 0
  """
  icmpHeader = struct.pack("bbHHH", 8, 0, 0, ID, 1)
  bytesDouble = struct.calcsize("d")
  data = (192 - bytesDouble) * "X"
  data = struct.pack("d", time.time()) + data

  num = checksum(icmpHeader + data)

  icmpHeader = struct.pack("bbHHH", 8, 0, socket.htons(num), ID, 1)

  packet = icmpHeader + data
  my_socket.sendto(packet, (addr, 1))


def recv_ping(my_socket, ID, timeout):
  """
  接受ICMP消息，返回延时时间delay
  """
  whatReady = select.select([my_socket], [], [], timeout)
  if whatReady[0] == []:
    return

  timeRecv = time.time()
  recPacket, addr = my_socket.recvfrom(1024)
  icmpHeader = recPacket[20:28]
  type, code, checknum, packetID, sequence = struct.unpack("bbHHH", icmpHeader)
  if packetID == ID:
    bytesDouble = struct.calcsize("d")
    timeSent = struct.unpack("d", recPacket[28:28 + bytesDouble])[0]

    return timeRecv - timeSent



def do(addr, timeout = 2):
  """
  返回时间延迟，为空则超时
  """
  icmp = socket.getprotobyname('icmp')
  try:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
  except socket.error, (errno, msg):
    if errno == 1:
      msg = msg + (" -- ICMP 的权限需要 root ")
      raise socket.error(msg)
    raise

  ID = os.getpid() & 0xffff

  send_ping(my_socket, addr, ID)
  delay = recv_ping(my_socket, ID, timeout)

  my_socket.close()
  return delay

def test_ping(addr):
  delay = do(addr)
  if delay != None:
    print 'ping to %s delay is %0.6f s' %(addr, delay)
  else:
    print 'ping to %s is time out' %addr


if __name__ == '__main__':
  test_ping('www.baidu.com')


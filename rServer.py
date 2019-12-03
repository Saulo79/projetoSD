#!/usr/bin/python
#coding: utf-8
import socket
import pickle
import struct
import threading

def sendP(sock, msg):
  msg = struct.pack('>I', len(msg)) + msg
  sock.sendall(msg)
 
def recvP(sock):
  pLen = recvL(sock, 4)
  if not pLen:
   return None
  n = struct.unpack('>I', pLen)[0]
  return recvL(sock, n)
 
def recvL(sock, n):
  data=''
  while len(data) < n:
   resp = sock.recv(n-len(data))
   if not resp:
    return None
   data += resp
  return data

def trata(connection, client):
  r=recvP(connection)
  data=pickle.loads(r)
  dynaMod = __import__("functions")
  dynaClass = getattr(dynaMod, data[1])
  dynaFunction = getattr(dynaClass(), "compute")
  pack = dynaFunction(*data[2])
  pack_serialized=pickle.dumps(pack)
  sendP(connection, pack_serialized)
  connection.close()

  
  
server = "127.0.0.1"
porta = 6750
c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket.bind((server, porta))
c_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
c_socket.listen(5)
while True:
 threading.Thread(target=trata, args=c_socket.accept()).start()

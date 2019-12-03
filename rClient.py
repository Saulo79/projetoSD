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
   return null
  n = struct.unpack('>I', pLen)[0]
  return recvL(sock, n)
 
def recvL(sock, n):
  data=''
  while len(data) < n:
   resp = sock.recv(n - len(data))
   if not resp:
    return None
   data += resp
  return data

def endereco(funcao):
  mid_sock=c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  destino=('10.90.37.20',5650) 
  mid_sock.connect(destino)
  mid_sock.send(str(funcao))
  r = mid_sock.recv(1024)
  if (r=="falha"):
   opcao=raw_input("Falha no servidor. Deseja enviar os dados novamente?(s/n)")
   if opcao=="s":
    return endereco(funcao)
   else:
    return "null"
  return r

def obterResultado(r_socket, destino, pack):
  try:
   aux=recvP(r_socket)
   res = pickle.loads(aux)
   print "Operacao: "+str(pack[1])+", Variável: "+str(pack[2])+", Resposta: "+str(res)
  except:
   opcao=raw_input("Falha no servidor. Deseja enviar os dados novamente?(s/n)")
   if opcao=="s":
      r_socket.close()
      processar(pack) 
  r_socket.close()
  

def processar(pack):
 c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 e=endereco(pack[0])
 if(e=="null"):
   return
 else: 
  destino=pickle.loads(e)
  pack_serialized=pickle.dumps(pack)
  for x in destino:
   try: 
    c_socket.connect(x)
    sendP(c_socket, pack_serialized) 
    th=threading.Thread(target=obterResultado, args=[c_socket, destino, pack_serialized]).start()
    return
   except:
    print "Operação falhou. Tente novamente."
    pass
 return

def menu():
 opcao = 0
 funcao=""
 while opcao==0:
  opcao=raw_input("Escolha sua opção: \n 1-Fibonacci; \n 2-Potencia; \n 3-Sair;")
  if opcao=="1":
    funcao='Fibonacci'
  elif opcao=="2":
    funcao='Potencia'
  else:
    print "Opcao invalida. Tente novamente."
    opcao=0;
  if funcao!="":
    parametro=raw_input("\n Informe o parâmetro:")
  pack = [int(opcao), funcao, (parametro,)]
  return pack
  

while True: 
 pack=menu()
 processar(pack)

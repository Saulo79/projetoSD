import socket
import time
import threading
dns = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ttl = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
nomePrinc='127.0.0.1'
portaPrinc= 5000
nomeSec='127.0.0.1'
portaSec=10000 
enderecoMiddle='127.0.0.1'
portaMiddle= 5650
portaMiddleUDP= 5670
import select
import pickle



class udp:
 def __init__(self):
    self.udp_socket = None
    
 
 def sendUDPMessage(self, destino, funcao):
    global enderecoMiddle
    global portaMiddleUDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(funcao, destino)
    udp_socket.setblocking(0)
    ready = select.select([udp_socket], [], [], 10)
    if ready[0]:
          r, cliente = udp_socket.recvfrom(1024)
	  if (r):
	   dns[int(funcao)]=r
	   ttl[int(funcao)]=600
	   udp_socket.close()
	   return(dns[int(funcao)])
    udp_socket.close()



def lookUp(funcao):
     global dns
     global ttl
     if ttl[int(funcao)]>0:
	 return(dns[int(funcao)])
     print "tentando server 1\n"
     destino=(nomePrinc, portaPrinc)
     UDP=udp()
     UDP.sendUDPMessage(destino, funcao)
     if ttl[int(funcao)]>0:
	 return(dns[int(funcao)])
     print "tentando server 2\n"
     destino=(nomeSec, portaSec)
     if ttl[int(funcao)]>0:
	 return(dns[int(funcao)])
     UDP.sendUDPMessage(destino, funcao) 
     return "falha"

def timeToLive():
    while True:
          for  i in range(len(ttl)):
            ttl[i]=ttl[i]-1
	    if ttl[i]==0:
	      dns[i]=0
	  time.sleep(1)	 

def trata(connection, client):
  msg = connection.recv(1024)
  r=lookUp(msg)
  connection.send(r)
  connection.close()

	 
soquete=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server=(enderecoMiddle,portaMiddle)
soquete.bind(server)
th=threading.Thread(target=timeToLive).start()
soquete.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soquete.listen(5)
while True:
 m=threading.Thread(target=trata, args=soquete.accept()).start()
		 

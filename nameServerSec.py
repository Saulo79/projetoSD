import threading
import socket
import pickle
CLIENT_ADDRESS = "127.0.0.1" 
CLIENT_PORT = 10000
funcA=[("127.0.0.1", 6750), ("127.0.0.1", 7750)]
funcB=[("127.0.0.1", 7500)]

class udp:
 def __init__(self):
    self.udp_socket = None
    th = threading.Thread(target=self.listenUDP).start()

 def listenUDP(self):
   self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   self.udp_socket.bind((CLIENT_ADDRESS, CLIENT_PORT))
   while True:
    msg, client = self.udp_socket.recvfrom(1024)
    print msg
    if msg=="1":
       resp=pickle.dumps(funcA)
       self.udp_socket.sendto(resp, client)
    elif msg=="2":
       resp=pickle.dumps(funcB)
       self.udp_socket.sendto(resp, client)
   
   

if __name__ == "__main__":
  UDP = udp()
  try:
   while True:
     pass
  except KeyboardInterrupt as e:
   print "Desligando."

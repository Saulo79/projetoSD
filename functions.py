class Fibonacci:
 def compute(self,value):
  result=[]
  pv = 0
  cv = 1
  for i in range(int(value)):
   result.append(pv)
   aux = pv
   pv=cv
   cv=pv+aux
  return result

class Potencia:
 def compute(self, ma):
  result=int(ma)*int(ma)
  return result

class meh:
 def compute(self, value):
  return 0

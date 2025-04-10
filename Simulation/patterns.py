import copy
a = []
def p(l):
 if len(l) == 6:
  a.append(l)
  return
 for i in range(3):
  b=copy.copy(l)
  b.append(i)
  p(b)
 return

def cicle(l,r):
 def same(l,r):
  for i in range(len(l)):
   if l[i]!=r[i]: return False
  return True
 def shiftr(l):
  return [l[5]] + l[0:5]
 for i in range(6):
  r = shiftr(r)
  if same(l,r): return True
 return False 

p([])
#file = open("a.txt","w")
#file.writelines([str(x)+'\n' for x in a])
file = open("a.txt","r")
b = [ line[:-1] + ": Stat()," for line in file]
file.close()
file = open("b.txt",'w')
file.writelines([str(x)+'\n' for x in b])
file.close()

# q = []
# for s in a:
#  new = True
#  for t in q:
#   if cicle(s,t):
#    new = False
#    break
#  if new:
#   q.append(s)

# print(len(q))
# for x in q:
#  print(x)

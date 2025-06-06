# For each local pattern save E(pattern),IE(pattern)
import copy


m = {
    (0, 0, 0, 0, 0, 0):(0,0),
    (0, 0, 0, 0, 0, 1):(0,0),
    (0, 0, 0, 0, 0, 2):(0,0),
    (0, 0, 0, 0, 1, 1):(0,0),
    (0, 0, 0, 0, 1, 2):(0,0),
    (0, 0, 0, 0, 2, 1):(0,0),
    (0, 0, 0, 0, 2, 2):(0,0),
    (0, 0, 0, 1, 0, 1):(1,0),
    (0, 0, 0, 1, 0, 2):(0,0),
    (0, 0, 0, 1, 1, 1):(0,0),
    (0, 0, 0, 1, 1, 2):(0,0),
    (0, 0, 0, 1, 2, 1):(1,0),
    (0, 0, 0, 1, 2, 2):(0,0),
    (0, 0, 0, 2, 0, 1):(0,0),
    (0, 0, 0, 2, 0, 2):(0,0),
    (0, 0, 0, 2, 1, 1):(0,0),
    (0, 0, 0, 2, 1, 2):(0,1),
    (0, 0, 0, 2, 2, 1):(0,0),
    (0, 0, 0, 2, 2, 2):(0,0),
    (0, 0, 1, 0, 0, 1):(1,0),
    (0, 0, 1, 0, 0, 2):(0,0),
    (0, 0, 1, 0, 1, 1):(1,0),
    (0, 0, 1, 0, 1, 2):(1,0),
    (0, 0, 1, 0, 2, 1):(1,0),
    (0, 0, 1, 0, 2, 2):(0,0),
    (0, 0, 1, 1, 0, 1):(1,0),
    (0, 0, 1, 1, 0, 2):(0,0),
    (0, 0, 1, 1, 1, 1):(0,0),
    (0, 0, 1, 1, 1, 2):(0,0),
    (0, 0, 1, 1, 2, 1):(1,0),
    (0, 0, 1, 1, 2, 2):(0,0),
    (0, 0, 1, 2, 0, 1):(1,0),
    (0, 0, 1, 2, 0, 2):(0,0),
    (0, 0, 1, 2, 1, 1):(1,0),
    (0, 0, 1, 2, 1, 2):(1,1),
    (0, 0, 1, 2, 2, 1):(1,0),
    (0, 0, 1, 2, 2, 2):(0,0),
    (0, 0, 2, 0, 0, 2):(0,0),
    (0, 0, 2, 0, 1, 1):(0,0),
    (0, 0, 2, 0, 1, 2):(0,1),
    (0, 0, 2, 0, 2, 1):(0,0),
    (0, 0, 2, 0, 2, 2):(0,0),
    (0, 0, 2, 1, 0, 1):(1,0),
    (0, 0, 2, 1, 0, 2):(0,1),
    (0, 0, 2, 1, 1, 1):(0,0),
    (0, 0, 2, 1, 1, 2):(0,1),
    (0, 0, 2, 1, 2, 1):(1,1),
    (0, 0, 2, 1, 2, 2):(0,1),
    (0, 0, 2, 2, 0, 1):(0,0),
    (0, 0, 2, 2, 0, 2):(0,0),
    (0, 0, 2, 2, 1, 1):(0,0),
    (0, 0, 2, 2, 1, 2):(0,1),
    (0, 0, 2, 2, 2, 1):(0,0),
    (0, 0, 2, 2, 2, 2):(0,0),
    (0, 1, 0, 1, 0, 1):(2,0),
    (0, 1, 0, 1, 0, 2):(1,0),
    (0, 1, 0, 1, 1, 1):(1,0),
    (0, 1, 0, 1, 1, 2):(1,0),
    (0, 1, 0, 1, 2, 1):(2,0),
    (0, 1, 0, 1, 2, 2):(1,0),
    (0, 1, 0, 2, 0, 2):(0,0),
    (0, 1, 0, 2, 1, 1):(1,0),
    (0, 1, 0, 2, 1, 2):(1,1),
    (0, 1, 0, 2, 2, 1):(1,0),
    (0, 1, 0, 2, 2, 2):(0,0),
    (0, 1, 1, 0, 1, 1):(1,0),
    (0, 1, 1, 0, 1, 2):(1,0),
    (0, 1, 1, 0, 2, 1):(1,0),
    (0, 1, 1, 0, 2, 2):(0,0),
    (0, 1, 1, 1, 0, 2):(0,0),
    (0, 1, 1, 1, 1, 1):(0,0),
    (0, 1, 1, 1, 1, 2):(0,0),
    (0, 1, 1, 1, 2, 1):(1,0),
    (0, 1, 1, 1, 2, 2):(0,0),
    (0, 1, 1, 2, 0, 2):(0,0),
    (0, 1, 1, 2, 1, 1):(1,0),
    (0, 1, 1, 2, 1, 2):(1,1),
    (0, 1, 1, 2, 2, 1):(1,0),
    (0, 1, 1, 2, 2, 2):(0,0),
    (0, 1, 2, 0, 1, 2):(1,1),
    (0, 1, 2, 0, 2, 1):(1,0),
    (0, 1, 2, 0, 2, 2):(0,0),
    (0, 1, 2, 1, 0, 2):(1,1),
    (0, 1, 2, 1, 1, 1):(1,0),
    (0, 1, 2, 1, 1, 2):(1,1),
    (0, 1, 2, 1, 2, 1):(1,1),
    (0, 1, 2, 1, 2, 2):(1,1),
    (0, 1, 2, 2, 0, 2):(0,0),
    (0, 1, 2, 2, 1, 1):(1,0),
    (0, 1, 2, 2, 1, 2):(1,1),
    (0, 1, 2, 2, 2, 1):(1,0),
    (0, 1, 2, 2, 2, 2):(0,0),
    (0, 2, 0, 2, 0, 2):(0,1),
    (0, 2, 0, 2, 1, 1):(0,0),
    (0, 2, 0, 2, 1, 2):(0,1),
    (0, 2, 0, 2, 2, 1):(0,0),
    (0, 2, 0, 2, 2, 2):(0,0),
    (0, 2, 1, 0, 2, 1):(1,1),
    (0, 2, 1, 0, 2, 2):(0,0),
    (0, 2, 1, 1, 1, 1):(0,0),
    (0, 2, 1, 1, 1, 2):(0,0),
    (0, 2, 1, 1, 2, 1):(1,1),
    (0, 2, 1, 1, 2, 2):(0,0),
    (0, 2, 1, 2, 1, 1):(1,1),
    (0, 2, 1, 2, 1, 2):(1,1),
    (0, 2, 1, 2, 2, 1):(1,1),
    (0, 2, 1, 2, 2, 2):(0,0),
    (0, 2, 2, 0, 2, 2):(0,0),
    (0, 2, 2, 1, 1, 1):(0,0),
    (0, 2, 2, 1, 1, 2):(0,0),
    (0, 2, 2, 1, 2, 1):(1,1),
    (0, 2, 2, 1, 2, 2):(0,0),
    (0, 2, 2, 2, 1, 1):(0,0),
    (0, 2, 2, 2, 1, 2):(0,0),
    (0, 2, 2, 2, 2, 1):(0,0),
    (0, 2, 2, 2, 2, 2):(0,0),
    (1, 1, 1, 1, 1, 1):(0,0),
    (1, 1, 1, 1, 1, 2):(0,0),
    (1, 1, 1, 1, 2, 2):(0,0),
    (1, 1, 1, 2, 1, 2):(1,1),
    (1, 1, 1, 2, 2, 2):(0,0),
    (1, 1, 2, 1, 1, 2):(1,1),
    (1, 1, 2, 1, 2, 2):(1,1),
    (1, 1, 2, 2, 1, 2):(1,1),
    (1, 1, 2, 2, 2, 2):(0,0),
    (1, 2, 1, 2, 1, 2):(2,2),
    (1, 2, 1, 2, 2, 2):(1,1),
    (1, 2, 2, 1, 2, 2):(1,1),
    (1, 2, 2, 2, 2, 2):(0,0),
    (2, 2, 2, 2, 2, 2):(0,0),
}

a = []
def p(l):
 if len(l) == 6:
  a.append(l)
  return
 for i in range(3):
  b=l[:]
  b.append(i)
  p(b)
 return

def shiftr(l):
  l = list(l)
  return tuple([l[5]] + l[0:5])

p([])
a = [tuple(x) for x in a]
for x in a:
 y = copy.copy(x)
 while not y in m:
  y = shiftr(y)
 m[x] = m[y]



file = open("MSP/alfa.txt","w")
file.writelines( [f"{x}:{m[x]},\n" for x in m])
file.close()
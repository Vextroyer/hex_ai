from MSP.GlobalMSP import GlobalMSP
from math import inf
import math

# Hardcoded Hexagonal Directions
dir = [(0,-1),(0,1),(-1,0),(1,0),(-1,1),(1,-1)]

class CenterDomination(GlobalMSP):
    """
    Prioritizes moves close to the center of the board.
    """
    def __init__(self,size):
        self.size = size
        self.distances = [[inf for i in range(size)] for i in range(size)]

        # Apply BFS to calculate distances.
        q = [(size//2,size//2,0)]
        if size % 2 == 0:
            q += [(size//2 - 1,size//2,0),(size//2,size//2 - 1,0),(size//2 - 1,size//2 - 1,0)]
        for i,j,k in q:
            self.distances[i][j] = k

        while len(q):
            i,j,k = q.pop(0)
            for di,dj in dir:
                if 0<=i+di<size and 0<=j+dj<size and self.distances[i+di][j+dj] == inf:
                    self.distances[i+di][j+dj] = k + 1
                    q.append((i+di,j+dj,k+1))

    def rank(self,row,col):
        """
        Normalized in [0,1]
        """
        return math.log(self.size - self.distances[row][col],self.size)



import heapq
import random
from utils import adj,inf
import MSP.LocalPatterns as LocalPatterns

class LocalMovementAnalisis:
    def __init__(self,size):
        """
        Prepare the local analisis for size*size boards.

        The analisys are described on the documentation.
        """
        # The dimension of the board
        self.n = size

        # The cost of the minimum cost path between the extremes of the board.
        self.minimum_length = 0

        # The total number of moves made on the board.
        self.total_moves = 0

        # Score for beign in a minimum length path, {0,1}
        self.ml = [[0 for i in range(self.n)] for i in range(self.n)]

        # Score for explotaition, {0,1,2}
        self.e = [[0 for i in range(self.n)] for i in range(self.n)]

        # Score for inverse explotaition, {0,1}
        self.ie = [[0 for i in range(self.n)] for i in range(self.n)]

    def analize(self,board:list[list[int]],player:int)->tuple[int,int]:
        """
        Run local analisis on the provided board for the given player.

        After this the score of cells can be retrieved by calling rank

        Returns the length of the shortest path that connects the extremes

        Returns the amount of pieces on the board
        """

        # This result is the same as the h heuristic function. It could be used.
        min_lenght = self.calculate_minimum_lenght_path(board,player)

        # Varios cells analisys: fn,e,ie

        pieces = 0

        # Interior cells
        for i in range(1,self.n - 1):
            for j in range(1,self.n - 1):
                # e and ie analisys:
                # Cell to tuple for LocalPatternAnalisis
                t = (board[i][j-1],board[i+1][j-1],board[i+1][j],board[i][j+1],board[i-1][j+1],board[i-1][j])
                self.e[i][j] = LocalPatterns.e(t,player)
                self.ie[i][j] = LocalPatterns.ie(t,player)

                pieces += 1 if board[i][j] else 0



        # Border but not corner cells
        for i in range(1,self.n - 1):
            # Top
            top = 0
            
            # e and ie analisys:
            # Cell to tuple for LocalPatternAnalisis
            t = (board[top][i-1],board[top+1][i-1],board[top+1][i],board[top][i+1],2,2)
            self.e[top][i] = LocalPatterns.e(t,player)
            self.ie[top][i] = LocalPatterns.ie(t,player)

            pieces += 1 if board[top][i] else 0

            # Left
            left = 0
            
            # e and ie analisys:
            # Cell to tuple for LocalPatternAnalisis
            t = (1,1,board[i+1][left],board[i][left+1],board[i-1][left+1],board[i-1][left])
            self.e[i][left] = LocalPatterns.e(t,player)
            self.ie[i][left] = LocalPatterns.ie(t,player)

            pieces += 1 if board[i][left] else 0

            # Bottom
            bottom = self.n - 1
            
            # e and ie analisys:
            # Cell to tuple for LocalPatternAnalisis
            t = (board[bottom][i-1],2,2,board[bottom][i+1],board[bottom-1][i+1],board[bottom-1][i])
            self.e[bottom][i] = LocalPatterns.e(t,player)
            self.ie[bottom][i] = LocalPatterns.ie(t,player)

            pieces += 1 if board[bottom][i] else 0

            # Right
            right = self.n - 1
            
            # e and ie analisys:
            # Cell to tuple for LocalPatternAnalisis
            t = (board[i][right-1],board[i+1][right-1],board[i+1][right],2,2,board[i-1][right])
            self.e[i][right] = LocalPatterns.e(t,player)
            self.ie[i][right] = LocalPatterns.ie(t,player)

            pieces += 1 if board[i][right] else 0

        # Corner cells
        top = 0
        left = 0
        bottom = self.n-1
        right = self.n-1
        
        # Top Left

        # e and ie analisys:
        # Cell to tuple for LocalPatternAnalisis
        t = (1,1,board[top+1][left],board[top][left+1],2,2)
        self.e[top][left] = LocalPatterns.e(t,player)
        self.ie[top][left] = LocalPatterns.ie(t,player)
        
        pieces += 1 if board[top][left] else 0

        # Bottom Left

        # e and ie analisys:
        # Cell to tuple for LocalPatternAnalisis
        t = (1,0,2,board[bottom][left+1],board[bottom-1][left+1],board[bottom-1][left])
        self.e[bottom][left] = LocalPatterns.e(t,player)
        self.ie[bottom][left] = LocalPatterns.ie(t,player)

        pieces += 1 if board[bottom][left] else 0

        # Bottom right

        # e and ie analisys:
        # Cell to tuple for LocalPatternAnalisis
        t = (board[bottom][right-1],2,2,1,1,board[bottom-1][right])
        self.e[bottom][right] = LocalPatterns.e(t,player)
        self.ie[bottom][right] = LocalPatterns.ie(t,player)

        pieces += 1 if board[bottom][right] else 0

        # Top Right

        # e and ie analisys:
        # Cell to tuple for LocalPatternAnalisis
        t = (board[top][right-1],board[top+1][right-1],board[top+1][right],1,0,2)
        self.e[top][right] = LocalPatterns.e(t,player)
        self.ie[top][right] = LocalPatterns.ie(t,player)

        pieces += 1 if board[top][right] else 0

        #Bridge Analisys

        return min_lenght,pieces

    def calculate_minimum_lenght_path(self,board:list[list[int]],player:int)->int:
        # Multiple source multiple destination minimum cost
        # Dijkstra Algorithm, moving to a cell of the same player has cost 0
        # Moving to a cell of diferent player has cost inf
        # Moving to an unnocupied cell has cost 1
        other_player = 3 - player
        n = self.n
        cost = [[inf for _ in range(n)] for _ in range(n)]
        q = []
        if player == 1:
            # Pon todos los vecinos del nodo de inicio en la cola
            # Lado izquierdo, board[0..n-1][0]
            # Lado derecho, board[0..n-1][n-1]
            q = [(0 if board[i][0] == player else 1,i,0) for i in range(n) if board[i][0] != player]
        else:
            # Lado superior, board[0][0...n-1]
            # Lado inferior, board[n-1][0...n-1]
            q = [(0 if board[i][0] == player else 1,0,i) for i in range(n) if board[0][i] != player]
        
        for c,i,j in q: cost[i][j] = c
        while q:
            c,i,j = heapq.heappop(q)
            for di,dj in adj:
                if 0<=i+di<n and 0<=j+dj<n and board[i+di][j+dj] != other_player:
                    if cost[i+di][j+dj] == inf:
                        cost[i+di][j+dj] = c if board[i+di][j+dj] == player else c + 1
                        heapq.heappush(q,(cost[i+di][j+dj],i+di,j+dj))
        min_length = inf
        if player == 1:
            # Pon todos los vecinos del nodo de inicio en la cola
            # Lado izquierdo, board[0..n-1][0]
            # Lado derecho, board[0..n-1][n-1]
            min_length = min([cost[i][n-1] for i in range(n)])
        else:
            # Lado superior, board[0][0...n-1]
            # Lado inferior, board[n-1][0...n-1]
            min_length = min([cost[n-1][i] for i in range(n)])

        # There is no path, this is bad.
        if min_length == inf:
            return inf

        for i in range(n):
            for j in range(n):
                self.ml[i][j] = 1 if cost[i][j] <= min_length else 0
        
        return min_length

    def rank(self,row,col):
        """
        Get the value of the cell according to local analisis.
        rank(cell) = ml(cell) + e(cell) + ie(cell) + U~(0,0.5)

        Remember to analize a board before calling rank, otherwise another board results may be used.
        """
        return self.ml[row][col] + self.e[row][col] + self.ie[row][col] + random.uniform(0,0.1)
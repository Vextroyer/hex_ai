from hex_board import HexBoard
from MSP.CenterDomination import CenterDomination

adj = [(0,-1),(0,1),(-1,0),(1,0),(-1,1),(1,-1)]

class MyBoard:
    def __init__(self,size):
        self.size = size # Original size
        self.extended_size = size + 2
        # Extended board
        # n+2 * n+2
        self.m = [[0 for _ in range(self.extended_size)] for _ in range(self.extended_size) ]
        for i in range(1,self.size+1):
            self.m[0][i] = 2
            self.m[i][0] = 1
            self.m[self.size+1][i] = 2
            self.m[i][self.size+1] = 1

        # Store the avaiable cells
        self.avaiable_cell = set([(i,j) for i in range(self.size) for j in range(self.size)])
        
        # Move Selection Policy(MSP)
        # Initialize GMSP
        self.gmsp = CenterDomination(size)
        # Store the score of each cell for MSP
        # n*n
        self.cell_score = [[0 for _ in range(self.size)] for _ in range(self.size)]

        for i in range(self.size): 
            for j in range(self.size): 
                self.cell_score[i][j] = self.calculate_cell_score(i,j)

    def get(self,i,j):
        return self.m[i+1][j+1]
    
    def set(self,i,j,k):
        """
        Assign this board cell to player k.
        """
        self.m[i+1][j+1] = k
        self.avaiable_cell.remove((i,j))
    
    def unset(self,i,j):
        """
        Unnasign this board cell.
        """
        self.m[i+1][j+1] = 0
        self.avaiable_cell.add((i,j))
    
    def update_from(self,hex_board: HexBoard):
        for i in range(hex_board.size):
            for j in range(hex_board.size):
                if hex_board.board[i][j] != self.get(i,j):
                    self.set(i,j,hex_board.board[i][j])

    def get_cell_score(self,i,j):
        return self.cell_score[i][j]
    
    def calculate_cell_score(self,i,j):
        w = [0.5,0.5]
        return self.gmsp.rank(i,j) * w[0]

    def get_moves(self,limit=0):
        """
        Return a list of possible moves ordered by the move selection policies.
        If limit > 0 returns at most limit moves.
        """
        a = [(self.get_cell_score(i,j),i,j) for i,j in self.avaiable_cell]
        a.sort()
        return [(i,j) for _,i,j in a]
    
    def check_connection(self,player_id: int) -> bool:
        """
        - **Objetivo**:
        - Jugador 1 (🔴): Conectar los lados izquierdo y derecho (horizontal)
        - Jugador 2 (🔵): Conectar los lados superior e inferior (vertical)

        Multiple Source Multiple Destination BFS. Se generan dos nodos artificiales, uno de inicio
        y uno de finalizacion. Se comprueba que exista un camino del nodo de inicio al nodo de finalizacion.
        Esta es una operacion teorica, el algoritmo revisa que hayas llegado de un extremo a otro.
        """
        n = self.size
        visited = [[False] * n for _ in range(n)]
        s = []
        if player_id == 1:
            # Pon todos los vecinos del nodo de inicio en la cola
            # Lado izquierdo, board[0..n-1][0]
            # Lado derecho, board[0..n-1][n-1]
            s = [(i,0) for i in range(n) if self.get(i,0) == player_id]
        else:
            # Lado superior, board[0][0...n-1]
            # Lado inferior, board[n-1][0...n-1]
            s = [(0,i) for i in range(n) if self.get(0,i) == player_id]
        
        for i,j in s: visited[i][j] = True
        while s:
            i,j = s.pop()
            for di,dj in adj:
                if 0<=i+di<n and 0<=j+dj<n and self.get(i+di,j+dj) == player_id and not visited[i+di][j+dj]:
                    visited[i+di][j+dj] = True
                    s.append((i+di,j+dj))
        
        if player_id == 1:
            # Revisa que se haya podido llegar al lado derecho
            for i in range(n):
                if visited[i][n-1]: return True
            return False
        else :
            # Revisa que se haya podido llegar al lado inferior
            for i in range(n):
                if visited[n-1][i]: return True
            return False


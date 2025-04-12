import player as player
import time
from utils import adj,inf
import heapq
from Old.MyBoard import MyBoard
class IslifyPlayerV1_2_1(player.Player):
    """
    MinMax player with alpha-beta prunning.
    Also supports a time limit.
    Also supports a depth limit for recursion.

    Implements Islify heuristic function.
    """
    def __init__(self, player_id: int,time_limit=2,depth_limit=2):
        super().__init__(player_id)
        self.other_player_id = 3 - self.player_id
        self.depth_limit=depth_limit
        self.time_limit = time_limit
        self.start_playing = 0
        self.board = None

    def play(self, board: player.HexBoard) -> tuple:
        #Setup
        self.start_playing = time.time()
        # Initialize Board
        if self.board == None:
            self.board = MyBoard(board.size)
        # Update board state whit last move
        self.board.update_from(board)

        #Play

        return self.minmax()

    def minmax(self)->tuple:
        """
        Using minmax algorithm calculate the move
        """
        expected_value,move = self._max(-inf,inf,0)
        return move

    def _min(self,alpha,beta,depth)->tuple:
        """
        Returns (expected value of move,move)
        Where move is of the form (i,j)
        """
        if depth == self.depth_limit:
            return (self.h(),None)
        moves = self.board.get_moves()
        if not moves:
            if self.board.check_connection(self.player_id): return (0,None)
            return (-inf,None)
        min_value = inf
        min_value_move = moves[0]
        for i,j in moves:
            self.board.set(i,j,self.other_player_id)
            value,_ = self._max(alpha,beta,depth+1)
            self.board.unset(i,j)
            if value < min_value:
                min_value = value
                min_value_move = (i,j)
                beta = value
            if value <= alpha: break
            if self.TimeBreak(): break
        return (min_value,min_value_move)            

    def _max(self,alpha,beta,depth)->tuple:
        """
        Returns (expected value of move,move)
        Where move is of the form (i,j)
        """
        if depth==self.depth_limit:
            return (self.h(),None)
        moves = self.board.get_moves()
        if not moves:
            if self.board.check_connection(self.player_id): return (0,None)
            return (-inf,None)
        max_value = -inf
        max_value_move = moves[0]
        for i,j in moves:
            self.board.set(i,j,self.player_id)
            value,_ = self._min(alpha,beta,depth+1)
            self.board.unset(i,j)
            if value > max_value:
                max_value = value
                max_value_move = (i,j)
                alpha = max(alpha,value)
            if value >= beta: break     
            if self.TimeBreak(): break           
        return (max_value,max_value_move)

    def h(self):
        """
        Islify heuristic function.
        """
        n = self.board.size
        cost = [[inf for _ in range(n)] for _ in range(n)]
        q = []
        if self.player_id == 1:
            # Pon todos los vecinos del nodo de inicio en la cola
            # Lado izquierdo, board[0..n-1][0]
            # Lado derecho, board[0..n-1][n-1]
            q = [(0,i,0) for i in range(n) if self.board.get(i,0) == self.player_id]
        else:
            # Lado superior, board[0][0...n-1]
            # Lado inferior, board[n-1][0...n-1]
            q = [(0,0,i) for i in range(n) if self.board.get(0,i) == self.player_id]
        
        for c,i,j in q: cost[i][j] = c
        while q:
            c,i,j = heapq.heappop(q)
            for di,dj in adj:
                if 0<=i+di<n and 0<=j+dj<n and self.board.get(i+di,j+dj) != self.other_player_id:
                    if cost[i+di][j+dj] == inf:
                        cost[i+di][j+dj] = c if self.board.get(i+di,j+dj) == self.player_id else c + 1
                        heapq.heappush(q,(cost[i+di][j+dj],i+di,j+dj))
        
        if self.player_id == 1:
            # Pon todos los vecinos del nodo de inicio en la cola
            # Lado izquierdo, board[0..n-1][0]
            # Lado derecho, board[0..n-1][n-1]
            return  -min([cost[i][n-1] for i in range(n)])
        else:
            # Lado superior, board[0][0...n-1]
            # Lado inferior, board[n-1][0...n-1]
            return  -min([cost[n-1][i] for i in range(n)])


    def TimeBreak(self) -> bool:
        return True if time.time() - self.start_playing >= self.time_limit - 0.2 else False
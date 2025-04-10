from MSP.CenterDomination import CenterDomination
import player
import time
from utils import adj
import heapq
class IslifyPlayerV1_2_2(player.Player):
    """
    MinMax player with alpha-beta prunning.
    Also supports a time limit.
    Also supports a depth limit for recursion.

    Implements Islify heuristic function.
    Implements CenterDomination as part of movement selection policy (MSP)
    """
    def __init__(self, player_id: int,time_limit=2,depth_limit=2):
        super().__init__(player_id)
        self.other_player_id = 3 - self.player_id
        self.inf = 100000000
        self.depth_limit=depth_limit
        self.time_limit = time_limit
        self.start_playing = 0
        self.gmsp = None

    def play(self, board: player.HexBoard) -> tuple:
        self.start_playing = time.time()
        if self.gmsp == None:
            self.gmsp = CenterDomination(board.size)
        return self.minmax(board)

    def minmax(self,board: player.HexBoard)->tuple:
        tmp_board = board.clone()     
        expected_value,move = self._max(tmp_board,-self.inf,self.inf,0)
        return move

    def _min(self,board: player.HexBoard,alpha,beta,depth)->tuple:
        if depth == self.depth_limit:
            return (self.h(board),None)
        moves = self.GetMovements(board)
        if not moves:
            if board.check_connection(self.player_id): return (0,None)
            return (-self.inf,None)
        min_value = self.inf
        min_value_move = moves[0]
        for move in moves:
            board.board[move[0]][move[1]] = self.other_player_id
            value,_ = self._max(board,alpha,beta,depth+1)
            board.board[move[0]][move[1]] = 0
            if value < min_value:
                min_value = value
                min_value_move = move
                beta = value
            if value <= alpha: break
            if self.TimeBreak(): break
        return (min_value,min_value_move)            

    def _max(self,board: player.HexBoard,alpha,beta,depth)->tuple:
        if depth==self.depth_limit:
            return (self.h(board),None)
        moves = self.GetMovements(board)
        if not moves:
            if board.check_connection(self.player_id): return (0,None)
            return (-self.inf,None)
        max_value = -self.inf
        max_value_move = moves[0]
        for move in moves:
            board.board[move[0]][move[1]] = self.player_id
            value,_ = self._min(board,alpha,beta,depth+1)
            board.board[move[0]][move[1]] = 0
            if value > max_value:
                max_value = value
                max_value_move = move
                alpha = max(alpha,value)
            if value >= beta: break     
            if self.TimeBreak(): break           
        return (max_value,max_value_move)

    def h(self,board: player.HexBoard):
        """
        Islify heuristic function.
        """
        n = len(board.board)
        cost = [[self.inf] * n for _ in range(n)]
        q = []
        if self.player_id == 1:
            # Pon todos los vecinos del nodo de inicio en la cola
            # Lado izquierdo, board[0..n-1][0]
            # Lado derecho, board[0..n-1][n-1]
            q = [(0 if board.board[i][0] == self.player_id else 1,i,0) for i in range(n) if board.board[i][0] != self.player_id]
        else:
            # Lado superior, board[0][0...n-1]
            # Lado inferior, board[n-1][0...n-1]
            q = [(0 if board.board[i][0] == self.player_id else 1,0,i) for i in range(n) if board.board[0][i] != self.player_id]
        
        for c,i,j in q: cost[i][j] = c
        while q:
            c,i,j = heapq.heappop(q)
            for di,dj in adj:
                if 0<=i+di<n and 0<=j+dj<n and board.board[i+di][j+dj] != self.other_player_id:
                    if cost[i+di][j+dj] == self.inf:
                        cost[i+di][j+dj] = c if board.board[i+di][j+dj] == self.player_id else c + 1
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


    def GetMovements(self,board:player.HexBoard,limit=None):
        """
        Retorna los posibles movimientos segun la politica empleada.
        """
        moves = [(self.rank(move),move) for move in board.get_possible_moves()]
        if limit:
            return [move for _,move in heapq.nlargest(limit,moves)]
        else:
            moves.sort(reverse=True)
            return [move for _,move in moves]

    def rank(self,move):
        """
        Calcula para cada movimiento cuan bueno es
        """
        w = [0.5,0.5]
        return w[0] * self.gmsp.rank(move[0],move[1])
    def TimeBreak(self) -> bool:
        return True if time.time() - self.start_playing >= self.time_limit - 0.2 else False
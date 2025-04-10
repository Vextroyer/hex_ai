import player
import time
from utils import adj
import heapq
class IslifyPlayerV1_3(player.Player):
    """
    MinMax player with alpha-beta prunning.
    Also supports a time limit.
    Also supports a depth limit for recursion.

    Implements Islify path analisys heuristic function.
    """
    def __init__(self, player_id: int,time_limit=2,depth_limit=2):
        super().__init__(player_id)
        self.other_player_id = 3 - self.player_id
        self.inf = 100000000
        self.depth_limit=depth_limit
        self.time_limit = time_limit
        self.start_playing = 0

    def minmax(self,board: player.HexBoard)->tuple:
        tmp_board = board.clone()     
        expected_value,move = self._max(tmp_board,-self.inf,self.inf,0)
        return move

    def _min(self,board: player.HexBoard,alpha,beta,depth)->tuple:
        if depth == self.depth_limit:
            return (self.h(board),None)
        moves = board.get_possible_moves()
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
        moves = board.get_possible_moves()
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

    def play(self, board: player.HexBoard) -> tuple:
        self.start_playing = time.time()
        return self.minmax(board)

    def h(self,board: player.HexBoard):
        """
        Islify path analisys heuristic function.
        Compute the path of minimum length between the extremes.
        Analize the path in search of weak links using a DAG. Simulate playing on the weak links and
        repeat.
        """
        dag = self.islify_h(board,self.player_id)
        shortest_path_length, weak_links = self.analize_dag(dag)

    def analize_dag(self,dag):
        """
        Receives a dag on the board. Where on each cell there is the length of the minimun length
        path from an extreme to the cell.
        Return the length of the shortest path between the extremes and a valid cell
        if this shortest path has no weak links, there are two independent paths 
        """
        n = len(dag)
        shortest_path_length = self.inf
        a = []
        weak_link = None
        if self.player_id == 1:
            # Pon todos los vecinos del nodo de inicio en la cola
            # Lado izquierdo, board[0..n-1][0]
            # Lado derecho, board[0..n-1][n-1]
            shortest_path_length = min([dag[i][n-1][0]for i in range(n) if dag[i][n-1][0] != self.inf])
            a = [(i,n-1)for i in range(n) if dag[i][n-1][0] == shortest_path_length]
        else:
            # Lado superior, board[0][0...n-1]
            # Lado inferior, board[n-1][0...n-1]
            shortest_path_length = min([dag[n-1][i][0]for i in range(n) if dag[n-1][i][0] != self.inf])
            a = [(n-1,i)for i in range(n) if dag[n-1][i][0] == shortest_path_length]
        
        # Caso shortest_path_length = inf no hay solucion
        
        return shortest_path_length


    def islify_h(self,board: player.HexBoard,player_id):
        """
        Islify heuristic function.
        Es admisible.
        """
        other_player_id = 3 - player_id
        n = len(board.board)
        # Store minimum distance, movements that reach node with minimum distance
        dag = [[ [self.inf,[]] ] * n for _ in range(n)]
        q = []
        if player_id == 1:
            # Pon todos los vecinos del nodo de inicio en la cola
            # Lado izquierdo, board[0..n-1][0]
            # Lado derecho, board[0..n-1][n-1]
            q = [(0,i,0) for i in range(n) if board.board[i][0] == player_id]
        else:
            # Lado superior, board[0][0...n-1]
            # Lado inferior, board[n-1][0...n-1]
            q = [(0,0,i) for i in range(n) if board.board[0][i] == player_id]
        
        for c,i,j in q: dag[i][j][0] = c
        while q:
            c,i,j = heapq.heappop(q)
            for di,dj in adj:
                if 0<=i+di<n and 0<=j+dj<n and board.board[i+di][j+dj] != other_player_id:
                    if dag[i+di][j+dj][0] == self.inf:
                        dag[i+di][j+dj][0] = c if board.board[i+di][j+dj] == player_id else c + 1
                        dag[i+di][j+dj][1].append((i,j))
                        heapq.heappush(q,(dag[i+di][j+dj][0],i+di,j+dj))
                    if dag[i][j][0] < dag[i+di][j+dj][0]:
                        dag[i+di][j+dj][1].append((i,j))

        return dag

    def TimeBreak(self) -> bool:
        return True if time.time() - self.start_playing >= self.time_limit - 0.2 else False
import random
from MSP.CenterDomination import CenterDomination
import player
import time
from utils import adj
import heapq

class KBeamSearchV1(player.Player):
    """
    K beam serach mantains at all times the best k candidate search states in memory.
    It then expands the best candidate.
    The score of the new candidates is calculated.
    Then from the previous states and the new ones the best k are maintained and the rest
    is discarded.

    Supports a time limit for exiting.

    Implements Islify heuristic function.
    Implements CenterDomination as part of movement selection policy (MSP)
    """
    def __init__(self, player_id: int,time_limit=2,k_best=6,n_neighboor=12,estados_guardados=None):
        super().__init__(player_id)
        self.other_player_id = 3 - self.player_id
        self.inf = 100000000
        self.time_limit = time_limit
        self.start_playing = 0
        self.gmsp = None
        self.k_best = k_best
        self.n_neighboor = n_neighboor
        self.expected_value_of_depth = []

    def calc_expected_value(self):
        sum = 0
        for x in self.expected_value_of_depth:
            sum += x
        return sum / len(self.expected_value_of_depth)

    def play(self, board: player.HexBoard) -> tuple:
        self.start_playing = time.time()
        if self.gmsp == None:
            self.gmsp = CenterDomination(board.size)
        return self.beam_search(board)

    def beam_search(self,board: player.HexBoard):
        # The score of the board, the board, the list of movements that lead to the board.
        states = [(0,board,[],self.player_id)]
        best_move = ()
        
        # Benchmark
        best_chain = []
        
        while not self.TimeBreak() and states:
            _,actual,moves,player = states.pop(0)
            best_move = moves[0] if moves else ()
            
            #Benchmark
            best_chain = moves if moves else []

            new_states = self.Expand(actual,moves,player)
            states += new_states
            states = heapq.nlargest(self.k_best,states)

        self.expected_value_of_depth.append(len(best_chain))
        
        return best_move

    def Expand(self,board: player.HexBoard,chain_of_moves,player):
        """
        Given a board return a new list of boards with their associated score.
        """
        moves = self.GetMovements(board)
        states = []
        # Try the top n moves
        for i,move in enumerate(moves):
            if i == self.n_neighboor: break
            new_board = board.clone()
            new_board.place_piece(move[0],move[1],player)
            new_chain_of_moves = chain_of_moves + [move]
            score = self.h(new_board) + random.uniform(0,1)
            new_player = 3 - player
            states.append((score,new_board,new_chain_of_moves,new_player))
        return states



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
        """
        Returns true if the algorithm is out of time.
        """
        return True if time.time() - self.start_playing >= self.time_limit - 0.2 else False
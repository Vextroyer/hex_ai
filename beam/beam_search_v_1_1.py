import random
from MSP.CenterDomination import CenterDomination
from MSP.LocalMovementAnalisis import LocalMovementAnalisis
import player as player
import time
import heapq

class KBeamSearchV1_1(player.Player):
    """
    K beam serach mantains at all times the best k search candidate states in memory.
    It then expands the best candidate.
    The score of the new candidates is calculated.
    Then from the previous states and the new ones the best k are maintained and the rest
    is discarded.

    Supports a time limit for exiting.

    Implements CenterDomination as part of movement selection policy (MSP)
    Implements LocalMovementSelection policy
    """
    def __init__(self, player_id: int,time_limit=2):
        super().__init__(player_id)

        # Utilities
        self.start_playing = 0
        self.other_player_id = 3 - self.player_id
        
        # Analisys
        self.gmsp = None
        self.local_analizer = None

        # Parameters
        self.k_best = 0 # Top k states to mantain on the frontier
        self.expand_limit = 0 # Limit the amount of states to expand
        self.time_limit = time_limit

        # Benchmarking
        self.expected_value_of_depth = []
        self.last_seen_moves = []
        self.last_score = 0


    def calc_expected_value(self):
        sum = 0
        for x in self.expected_value_of_depth:
            sum += x
        return sum / len(self.expected_value_of_depth)

    def play(self, board: player.HexBoard) -> tuple:
        self.start_playing = time.time()
        
        # Initialize for playing
        if self.gmsp == None:
            self.gmsp = CenterDomination(board.size)
            self.local_analizer = LocalMovementAnalisis(board.size)
            self.expand_limit = int(1.5 * board.size)
            #self.k_best = 3 * board.size * board.size // 8
            self.k_best = 5 + int(board.size ** (0.5))
        
        return self.beam_search(board)

    def beam_search(self,board: player.HexBoard):
        # The score of the board, the board, the list of movements that lead to the board.
        states = [(0,board,[],self.player_id)]
        best_move = ()
        
        # Benchmark
        best_chain = []
        self.local_analizer.analize(board.board,self.player_id)
        self.last_seen_moves = self.GetMovements(board,self.player_id)
        self.last_score = self.h(self.local_analizer.minimum_length,self.local_analizer.total_moves)
        print("length",self.local_analizer.minimum_length)
        print("total",self.local_analizer.total_moves)

        
        while not self.TimeBreak() and states:
            score,actual,moves,player = states.pop(0)
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
        # Analize the state of the game
        self.local_analizer.analize(board.board,player)
        minimum_length = self.local_analizer.minimum_length
        total_moves = self.local_analizer.total_moves
        
        moves = self.GetMovements(board,player)

        states = []
        # Try the top n moves
        for i,move in enumerate(moves):
            if i == self.expand_limit: break
            new_board = board.clone()
            new_board.place_piece(move[0],move[1],player)
            new_chain_of_moves = chain_of_moves + [move]
            score = self.h(minimum_length,total_moves) + random.uniform(0,0.1)
            new_player = 3 - player
            states.append((score,new_board,new_chain_of_moves,new_player))
        return states

    def h(self,minimum_length:int,total_moves:int):
        return - (2 * minimum_length + total_moves)

    def GetMovements(self,board:player.HexBoard,player:int):
        """
        Retorna los posibles movimientos segun la politica empleada.
        """
        moves = [(self.rank(move),move) for move in board.get_possible_moves()]
        return [move for _,move in heapq.nlargest(self.expand_limit,moves)]

    def rank(self,move):
        """
        Calcula para cada movimiento cuan bueno es
        """
        return self.gmsp.rank(move[0],move[1]) + self.local_analizer.rank(move[0],move[1])
    
    def TimeBreak(self) -> bool:
        """
        Returns true if the algorithm is out of time.
        """
        return True if time.time() - self.start_playing >= self.time_limit - 0.2 else False
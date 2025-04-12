import random
from MSP.CenterDomination import CenterDomination
from MSP.LocalMovementAnalisis import LocalMovementAnalisis
import player
import time
import heapq

class AStar(player.Player):
    """
    Supports a time limit for exiting.

    Implements CenterDomination as part of movement selection policy (MSP)
    Implements LocalMovementSelection policy
    """
    def __init__(self, player_id: int,time_limit=2):
        super().__init__(player_id)

        # Utilities
        self.start_playing = 0
        self.other_player_id = 3 - self.player_id
        self.state_id = 0
        
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

    def get_new_id(self)->int:
        self.state_id += 1
        return self.state_id
    
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
            #self.k_best = 5 + int(board.size ** (0.5))
            self.k_best = 10000
        
        return self.search(board)

    def search(self,board: player.HexBoard):
        # A state consist of (score,id,player,move,board)
        # Where score is the score of the board
        # Id uniquely identifies a state
        # player is the player that plays on this state
        # move is the the first move of the chain of moves of this state
        # board is ...
        
        states = self.Expand(self.player_id,(),board)
        heapq.heapify(states)
        best_move = ()
        
        # # Benchmark
        # self.last_seen_moves = self.GetMovements(board,self.player_id)
        # self.last_score = self.h(self.local_analizer.min_cost,self.local_analizer.total_moves)
        # print("cost",self.local_analizer.min_cost)
        # print("total",self.local_analizer.total_moves)

        
        while not self.TimeBreak() and states:
            _,_,player,first_move,actual = heapq.heappop(states)
            best_move = first_move
            new_states = self.Expand(player,first_move,actual)
            heapq.heapify(new_states)
            states = list(heapq.merge(states,new_states))
            if len(states) > self.k_best: states = heapq.nsmallest(self.k_best,states) 
        
        return best_move

    def Expand(self,player:int,first_move:tuple[int,int],board: player.HexBoard)->list[tuple[int,int,int,tuple[int,int],player.HexBoard]]:
        """
        Given a board return a new list of boards with their associated score.
        """
        # Analize the state of the game
        min_cost,total_moves = self.local_analizer.analize(board.board,player)
        
        moves = self.GetMovements(board,player)

        states = []
        # Try the top n moves
        for i,move in enumerate(moves):
            if i == self.expand_limit: break
            new_board = board.clone()
            new_board.place_piece(move[0],move[1],player) 
            score = self.h(min_cost,total_moves)
            new_player = 3 - player
            states.append((score,self.get_new_id(),new_player,first_move if first_move else move,new_board))
        return states

    def h(self,minimum_cost:int,total_moves:int):
        return total_moves + 2 * minimum_cost

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
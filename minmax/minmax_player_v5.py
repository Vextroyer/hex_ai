import heapq
from MSP.CenterDomination import CenterDomination
from MSP.LocalMovementAnalisis import LocalMovementAnalisis
import player as player
import time
from utils import inf
class MinmaxPlayerV5(player.Player):
    """
    MinMax player with alpha-beta prunning.
    Also supports a time limit.
    """
    def __init__(self, player_id: int,time_limit=2):
        super().__init__(player_id)
        
        # Utilities
        self.other_player_id = 3 - self.player_id
        self.start_playing = 0

        # Analisys
        self.gmsp = None
        self.local_analizer = None

        # Parameters
        self.expand_limit = 0 # Limit the amount of moves per state
        self.time_limit = time_limit
        self.depth_limit = 20

    def play(self, board: player.HexBoard) -> tuple:
        self.start_playing = time.time()
        # Initialization
        if self.gmsp == None:
            self.gmsp = CenterDomination(board.size)
            self.local_analizer = LocalMovementAnalisis(board.size)
            self.expand_limit = int(1.5 * board.size)

        return self.minmax(board)

    def minmax(self,board: player.HexBoard)->tuple:
        tmp_board = board.clone()     
        expected_value,move = self._max(tmp_board,-inf,inf,0)
        return move
            
    def _min(self,board: player.HexBoard,alpha,beta,depth:int)->tuple:
        min_value = inf
        min_value_move = None
        min_cost,total_moves = self.local_analizer.analize(board.board,self.other_player_id)

        if min_cost == 0 or total_moves == board.size * board.size: return (self.h(min_cost,total_moves),None)
        if depth == self.depth_limit: return (self.h(min_cost,total_moves),None)

        moves = self.GetMovements(board,self.other_player_id)
        if not moves:
            print(board.get_possible_moves())
            print(board.board)
            assert moves
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

    def _max(self,board: player.HexBoard,alpha,beta,depth:int)->tuple:
        
        max_value = -inf
        max_value_move = None
        min_cost,total_moves = self.local_analizer.analize(board.board,self.player_id)

        if min_cost == 0 or total_moves == board.size * board.size: return (self.h(min_cost,total_moves),None)
        if depth == self.depth_limit: return (self.h(min_cost,total_moves),None)
        
        moves = self.GetMovements(board,self.player_id)
        if not moves:
            print(board.get_possible_moves())
            print(board.board)
            assert moves
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

    def h(self,minimum_cost:int,total_moves:int):
        return - minimum_cost
    
    def TimeBreak(self) -> bool:
        return True if time.time() - self.start_playing >= self.time_limit else False

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
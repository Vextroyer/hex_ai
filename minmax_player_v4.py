import player
import time
class MinmaxPlayerV4(player.Player):
    """
    MinMax player with alpha-beta prunning.
    Also supports a time limit.
    """
    def __init__(self, player_id: int,time_limit=2):
        super().__init__(player_id)
        self.other_player_id = 3 - self.player_id
        self.inf = 100000000
        self.time_limit = time_limit
        self.start_playing = 0

    def minmax(self,board: player.HexBoard)->tuple:
        tmp_board = board.clone()     
        expected_value,move = self._max(tmp_board,-self.inf,self.inf)
        return move
            
    def _min(self,board: player.HexBoard,alpha,beta)->tuple:
        terminal = self.IsTerminal(board)
        if terminal: return (self.h(board,terminal),None)
        min_value = 100000000
        min_value_move = None
        moves = board.get_possible_moves()
        for move in moves:
            board.board[move[0]][move[1]] = self.other_player_id
            value,_ = self._max(board,alpha,beta)
            board.board[move[0]][move[1]] = 0
            if value < min_value:
                min_value = value
                min_value_move = move
                beta = value
            if value <= alpha: break
            if self.TimeBreak(): break
        return (min_value,min_value_move)            

    def _max(self,board: player.HexBoard,alpha,beta)->tuple:
        terminal = self.IsTerminal(board)
        if terminal: return (self.h(board,terminal),None)
        max_value = -self.inf
        max_value_move = None
        moves = board.get_possible_moves()
        for move in moves:
            board.board[move[0]][move[1]] = self.player_id
            value,_ = self._min(board,alpha,beta)
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

    def h(self,board: player.HexBoard,terminal: int):
        """
        Heuristic function.
        The less pieces for the win, the better.
        The more pieces for the lose, the better.
        """
        pieces = 0
        if terminal==1:
            for i in range(board.size):
                for j in range(board.size):
                    pieces += 1 if board.board[i][j] == self.player_id else 0
            return 1 / pieces
        else:
            for i in range(board.size):
                for j in range(board.size):
                    pieces += 1 if board.board[i][j] == self.other_player_id else 0
            return - 1 * pieces

    def IsTerminal(self,board: player.HexBoard):
        """
        Returns -1 if is a losing terminal state.
        Returns 1 if is a wining terminal state
        Returns 0 if is not a terminal state
        """
        if board.check_connection(self.player_id) : return 1
        elif board.check_connection(self.other_player_id): return -1
        else: return 0
    
    def TimeBreak(self) -> bool:
        return True if time.time() - self.start_playing >= self.time_limit else False
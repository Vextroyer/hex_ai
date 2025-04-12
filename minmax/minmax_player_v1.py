import player as player

class MinmaxPlayerV1(player.Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)
        self.other_player_id = 3 - self.player_id

    def minmax(self,board: player.HexBoard):
        tmp_board = board.clone()     
        expected_value,move = self._max(tmp_board)
        return move
            
    def _min(self,board: player.HexBoard):
        if board.check_connection(self.player_id) : return (1,None)
        elif board.check_connection(self.other_player_id): return (-1,None)
        min_value = 100000000
        min_value_move = None
        moves = board.get_possible_moves()
        for move in moves:
            board.place_piece(move[0],move[1],self.other_player_id)
            value,_ = self._max(board)
            board.board[move[0]][move[1]] = 0
            if value < min_value:
                min_value = value
                min_value_move = move
        return (min_value,min_value_move)            

    def _max(self,board: player.HexBoard):
        if board.check_connection(self.player_id) : return (1,None)
        elif board.check_connection(self.other_player_id): return (-1,None)
        max_value = -100000000
        max_value_move = None
        moves = board.get_possible_moves()
        for move in moves:
            board.place_piece(move[0],move[1],self.player_id)
            value,_ = self._min(board)
            board.board[move[0]][move[1]] = 0
            if value > max_value:
                max_value = value
                max_value_move = move
        return (max_value,max_value_move)

    def play(self, board: player.HexBoard) -> tuple:
        return self.minmax(board)

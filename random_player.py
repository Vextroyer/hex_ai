import player
import random

class RandomPlayer(player.Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)
    
    def play(self, board: player.HexBoard) -> tuple:
        moves = board.get_possible_moves()
        return random.choice(moves)
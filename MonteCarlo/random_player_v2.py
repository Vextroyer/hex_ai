"""
A random player that uses monte carlo for taking a better move.

The random player examines his list of avaiable moves.
It then consider at most k random moves from the list.
Then for each move it calculates the possible win ratio of the move using MonteCarloTreeSearch for simulation.
Finally it does the best move according to the simulation.
"""
import player
import random
from MonteCarlo.mcts_addon_v1 import MonteCarloAddonV1

class RandomPlayerV2(player.Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)
        self.simulator = MonteCarloAddonV1(player_id)
    
    def play(self, board: player.HexBoard,consider_k_random_moves:int = 3,do_t_iterations:int=100) -> tuple:
        
        moves = board.get_possible_moves()
        random_moves = [random.choice(moves) for _ in range(consider_k_random_moves)]
        best_move = (-1,-1)
        best_move_score = -1
        for move in random_moves:
            board.board[move[0]][move[1]] = self.player_id
            score = self.simulator.play(board,do_t_iterations)
            board.board[move[0]][move[1]] = 0
            if score > best_move_score:
                best_move_score = score
                best_move = move
        return best_move

import time
from MonteCarlo.mcts import MonteCarloPlayerV1
from MonteCarlo.mctsV2 import MonteCarloPlayerV2
from MonteCarlo.mctsV3 import MonteCarloPlayerV3
from beam_search_v_1 import KBeamSearchV1
from hex_board import HexBoard
from islify_v_1_2 import IslifyPlayerV1_2
from Old.islify_v_1_2_1 import IslifyPlayerV1_2_1
from islify_v_1_2_2 import IslifyPlayerV1_2_2
from islify_v_1_3 import IslifyPlayerV1_3
from minmax_player_v4 import MinmaxPlayerV4
from minmax_player_v5 import MinmaxPlayerV5
from MonteCarlo.random_player import RandomPlayer
from MonteCarlo.random_player_v2 import RandomPlayerV2
from search import Alfa

def match(playerA,playerB,size,runs):
    startA = runs//2
    startB = runs//2
    games = startA + startB
    win_A = 0
    win_B = 0
    draw = 0
    move_duration_A = 0
    move_duration_B = 0
    expected_value = 0
    for i in range(startA):
        print(f"game %i",i)
        player_objects = {1:playerA(1),2:playerB(2)}
        r,tA,tB = play(player_objects,size)
        move_duration_A += tA
        move_duration_B += tB
        if r == 1:
            win_A =  win_A + 1
        elif r == 2:
            win_B = win_B + 1
        else:
            draw = draw + 1
        #expected_value += player_objects[2].calc_expected_value()
    for i in range(startB):
        print(f"game %i",startB + i)
        player_objects = {1:playerB(1),2:playerA(2)}
        r,tB,tA = play(player_objects,size)
        move_duration_A += tA
        move_duration_B += tB
        if r == 1:
            win_B =  win_B + 1
        elif r == 2:
            win_A = win_A + 1
        else:
            draw = draw + 1
        #expected_value += player_objects[1].calc_expected_value()
    #print("expected value of depth",expected_value / games)
    return (win_A,move_duration_A/games,win_B,move_duration_B/games,draw,games)

def play(player_objects,size):
    current_player = 1
    board = HexBoard(size)
    cnt_moves = {1:0,2:0}
    sum_duration = {1:0,2:0}
    winner = 0
    atemp = 0
    while True:
        if board.check_connection(current_player):
            winner = current_player
            break
        if board.check_connection(3 - current_player):
            winner = 3 - current_player
            break
        if not board.get_possible_moves():
            winner = 0
            break
        duration = time.time()
        move = player_objects[current_player].play(board)
        if current_player==1:
            atemp += player_objects[current_player].attempts
        duration = time.time() - duration 
        sum_duration[current_player] += duration
        cnt_moves[current_player] += 1
        board.place_piece(move[0], move[1], current_player)
        # Cambiar turno
        current_player = 3 - current_player

    print("attemps",atemp//cnt_moves[1])
        
    return winner,sum_duration[1] / cnt_moves[1],sum_duration[2] / cnt_moves[2]

print(match(MonteCarloPlayerV3,RandomPlayer,5,20))
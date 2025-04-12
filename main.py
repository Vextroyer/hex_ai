# Agradecimientos a Pablo y Diego

import os
from MonteCarlo.mctsV2 import MonteCarloPlayerV2
from a_star import AStar
from beam_search_v_1 import KBeamSearchV1
from beam_search_v_1_1 import KBeamSearchV1_1
from hex_board import HexBoard
from islify_v_1_2_2 import IslifyPlayerV1_2_2
from minmax_player_v5 import MinmaxPlayerV5
from MonteCarlo.random_player import RandomPlayer
from minmax_player_v1 import MinmaxPlayerV1
from minmax_player_v2 import MinmaxPlayerV2
from minmax_player_v3 import MinmaxPlayerV3
from minmax_player_v4 import MinmaxPlayerV4
from islify_v_1_2 import IslifyPlayerV1_2
from Old.islify_v_1_2_1 import IslifyPlayerV1_2_1
from islify_v_1_3 import IslifyPlayerV1_3
from MonteCarlo.mcts import MonteCarloPlayerV1
from search import Alfa


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("Bienvenido a HEX")
    try:
        size = int(input("Ingrese el tamaño del tablero (por ejemplo, 5): "))
    except ValueError:
        print("Tamaño inválido. Usando tamaño 5 por defecto.")
        size = 5

    board = HexBoard(size)

    # Game mode:
    # 1: Dos jugadores humanos
    # 2: Humano (jugador 1) vs. IA (jugador 2)
    # 3: IA vs IA
    mode = input("Seleccione modo de juego (1: Humano vs Humano, 2: Humano vs IA, 3: IA vs IA): ")

    if mode == "2":
        human_player = int(input("Elija su identificador (1 para 🔴, 2 para 🔵): "))
        ai_player = 2 if human_player == 1 else 1
        player_objects = {
            human_player: None,  # Humano: Él hace su propio input
           ai_player: KBeamSearchV1(ai_player)
        }
    elif mode == "3":
        player_objects = {
            1: MonteCarloPlayerV2(1),  # IA
            2: RandomPlayer(2)   # IA
        }
    else:
        player_objects = {
            1: None,  # Humano
            2: None   # Humano
        }

    current_player = 1
    while True:
        clear_console()
        board.print_board()

        if board.check_connection(1):
            print("¡El jugador 1 (🔴) ha ganado!")
            break
        if board.check_connection(2):
            print("¡El jugador 2 (🔵) ha ganado!")
            break
        if not board.get_possible_moves():
            print("Empate. No hay más movimientos disponibles.")
            break

        print(f"\n \n Turno del jugador {current_player} ({'🔴' if current_player==1 else '🔵'}).")

        if player_objects.get(current_player) is None:
            # movimiento del humano(por coordenadas)
            try:
                move_input = input("Ingrese su movimiento como 'fila columna': ")
                row, col = map(int, move_input.split())
            except Exception as e:
                print("Entrada inválida. Inténtelo de nuevo.")
                continue
            if (row, col) not in board.get_possible_moves():
                print("Movimiento no válido o casilla ocupada. Inténtelo de nuevo.")
                continue
            board.place_piece(row, col, current_player)
        else:
            move = player_objects[current_player].play(board)
            #if current_player == 1:
            #    print(player_objects[current_player].last_score,player_objects[current_player].last_seen_moves)
            print(f"La IA juega en la posición: {move}")
            board.place_piece(move[0], move[1], current_player)
        input()

        # Cambiar turno
        current_player = 2 if current_player == 1 else 1
    
    #sum = 0
    #for x in player_objects[1].expected_value_of_depth:
    #    sum += x
    #sum /= len(player_objects[1].expected_value_of_depth)
    #print("expected avalue of depth",sum)

if __name__ == "__main__":
    main()

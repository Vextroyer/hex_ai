import math
from platform import node
import time
import player
import random

class Node:
    sqrt2 = math.sqrt(2)
    def __init__(self,player_id,parent):
        self.U: int = 0
        self.N: int = 0
        self.child: list[Node] = []
        self.move: tuple[int,int,int] | None = None
        
        self.player_id = player_id
        self.parent: Node | None = parent

    def AddChild(self,node):
        self.child.append(node)   
        
    def UCB1(self):
        return self.U / self.N + self.sqrt2 * math.sqrt(math.log(self.parent.N,math.e) / self.N)

class MonteCarloPlayer_v1(player.Player):
    def __init__(self, player_id: int,time_limit=2):
        super().__init__(player_id)
        self.time_limit = time_limit
    
    def play(self, board: player.HexBoard) -> tuple:
        return self.MonteCarloTreeSearch(board)
    
    def MonteCarloTreeSearch(self,board: player.HexBoard) -> tuple:
        tree = Node(self.player_id,None)
        start_time = time.time()
        actual_time = time.time()
        while actual_time - start_time < self.time_limit:
            leaf = self.Select(tree)
            child = self.Expand(leaf,board)
            result = self.Simulate(child,board)
            self.BackPropagate(result,child)
            actual_time = time.time()
        
        best_value = 0
        best_move = None
        for child in tree.child:
            if child.U / child.N > best_value:
                best_value = child.U / child.N
                best_move = child.move
        return best_move[0],best_move[1]
    
    def Select(self,node: Node) -> Node:
        while node.child:
            # Randomly select leaf node
            node = random.choice(node.child)
        return node
    
    def Expand(self,node: Node,board: player.HexBoard) -> Node:
        self.apply_moves(node,board)
        # Randomly select a move
        moves = board.get_possible_moves()

        if not moves:
            return node

        move = random.choice(moves)
        
        child = Node(self.other_player(node.player_id))
        child.parent = node
        child.move = (move[0],move[1],node.player_id)
        node.child.append(child)

        self.unapply_moves(node,board)

        return child

    def Simulate(self,node: Node,board: player.HexBoard):
        self.apply_moves(node,board)

        current_player = node.player_id
        recorded_moves = []
        winner = 0
        while True:
            if board.check_connection(self.player_id):
                winner = self.player_id
                break
            if board.check_connection(self.other_player(self.player_id)):
                winner = self.other_player(self.player_id)
                break
            moves = board.get_possible_moves()
            move = random.choice(moves)
            recorded_moves.append(move)
            board.board[move[0]][move[1]] = current_player
            current_player = self.other_player(current_player)

        for i,j in recorded_moves: board.board[i][j] = 0
        self.unapply_moves(node,board)

        return winner

    def BackPropagate(self,winner,node: Node):
        while node:
            node.N += 1
            node.U += 1 if winner == node.player_id else 0
            node = node.parent


    def apply_moves(self,node: Node,board: player.HexBoard):
        while node.parent != None:
            i,j,k = node.move
            board.board[i][j] = k
            node = node.parent
    
    def unapply_moves(self,node: Node,board: player.HexBoard):
        while node.parent != None:
            i,j,_ = node.move
            board.board[i][j] = 0
            node = node.parent

    def other_player(self,player_id):
        return 3 - player_id
        
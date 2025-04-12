"""
Monte Carlo Tree Search with UCB1 selection policy.

Reuses previously calculated results. Instanciate once and play a lot.
"""
import math
import time
import player
import random

class Node:
    sqrt2 = math.sqrt(2)
    def __init__(self,player_id,parent):
        self.U: int = 0
        self.N: int = 0
        self.child: list[Node] = []
        self.move: tuple[int,int,int] = (-1,-1,-1)
        
        self.player_id = player_id
        self.parent: Node | None = parent

    def AddChild(self,node):
        self.child.append(node)   
        
    def UCB1(self):
        return self.U / self.N + self.sqrt2 * math.sqrt(math.log(self.parent.N if self.parent else self.N,math.e) / self.N)

class MonteCarloPlayerV3(player.Player):
    def __init__(self, player_id: int,time_limit=2):
        super().__init__(player_id)
        self.time_limit = time_limit
        self.attempts = 0

    def play(self, board: player.HexBoard) -> tuple:
        # Play
        i,j,attempts = self.MonteCarloTreeSearch(board)
        self.attempts = attempts

        return (i,j)

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
        best_move = (-1,-1)
        for child in tree.child:
            if child.U / child.N >= best_value:
                best_value = child.U / child.N
                best_move = child.move
        assert best_move != (-1,-1)
        return best_move[0],best_move[1],tree.N
    
    def Select(self,node: Node) -> Node:
        while node.child:
            # Select according to UCB1
            max_score = -1
            best_child = node.child[0]
            for child in node.child:
                score = child.UCB1()
                if score > max_score:
                    max_score = score
                    best_child = child
            # Its better to expand the current node than one of its leaves
            if max_score < node.UCB1():
                break
            node = best_child

        return node
    
    def Expand(self,node: Node,board: player.HexBoard) -> Node:
        self.apply_moves(node,board)
        # Randomly select a move
        moves = board.get_possible_moves()

        if not moves:
            return node

        move = random.choice(moves)
        
        child = Node(self.other_player(node.player_id),node)
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
        while node.parent:
            i,j,k = node.move
            board.board[i][j] = k
            node = node.parent
    
    def unapply_moves(self,node: Node,board: player.HexBoard):
        while node.parent:
            i,j,_ = node.move
            board.board[i][j] = 0
            node = node.parent

    def other_player(self,player_id):
        return 3 - player_id
        
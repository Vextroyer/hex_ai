inf = 100000000
adj = [(0,-1),(1,-1),(1,0),(0,1),(-1,1),(-1,0)]

def dfs(board,player_id: int) -> bool:
    """
    - **Objetivo**:
    - Jugador 1 (🔴): Conectar los lados izquierdo y derecho (horizontal)
    - Jugador 2 (🔵): Conectar los lados superior e inferior (vertical)

    Multiple Source Multiple Destination BFS. Se generan dos nodos artificiales, uno de inicio
    y uno de finalizacion. Se comprueba que exista un camino del nodo de inicio al nodo de finalizacion.
    Esta es una operacion teorica, el algoritmo revisa que hayas llegado de un extremo a otro.
    """
    n = len(board)
    visited = [[False] * n for _ in range(n)]
    s = []
    if player_id == 1:
        # Pon todos los vecinos del nodo de inicio en la cola
        # Lado izquierdo, board[0..n-1][0]
        # Lado derecho, board[0..n-1][n-1]
        s = [(i,0) for i in range(n) if board[i][0] == player_id]
    else:
        # Lado superior, board[0][0...n-1]
        # Lado inferior, board[n-1][0...n-1]
        s = [(0,i) for i in range(n) if board[0][i] == player_id]
    
    for i,j in s: visited[i][j] = True
    while s:
        i,j = s.pop()
        for di,dj in adj:
            if 0<=i+di<n and 0<=j+dj<n and board[i+di][j+dj] == player_id and not visited[i+di][j+dj]:
                visited[i+di][j+dj] = True
                s.append((i+di,j+dj))
    
    if player_id == 1:
        # Revisa que se haya podido llegar al lado derecho
        for i in range(n):
            if visited[i][n-1]: return True
        return False
    else :
        # Revisa que se haya podido llegar al lado inferior
        for i in range(n):
            if visited[n-1][i]: return True
        return False
    
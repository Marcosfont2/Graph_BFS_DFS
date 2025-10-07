import re
from collections import deque

INF = None  # usando None para distância infinita

def build_adj_matrix(vertices, edges, directed):
    """Constroi matriz de adjacência (lista de listas de booleans) e dicionários de mapeamento."""
    n = len(vertices)
    idx_of = {v: i for i, v in enumerate(vertices)}
    mat = [[False]*n for _ in range(n)]
    for u, v in edges:
        if u not in idx_of or v not in idx_of:
            # se algum vértice aparecia só em aresta, já foi adicionado; este teste é só safety
            continue
        i = idx_of[u]
        j = idx_of[v]
        mat[i][j] = True
        if not directed:
            mat[j][i] = True
    return mat, idx_of

def bfs_with_matrix(mat, vertices, src_index):
    """
    Executa BFS usando matriz de adjacência.
    - mat é n x n boolean
    - vertices é lista ordenada (para index -> nome)
    - src_index é índice da fonte
    Retorna:
      order_list: lista de vértices na ordem em que foram descobertos
      dist: lista de distâncias (None = INF)
      parent: lista de índices de pai (None = NIL)
    Observação: ao iterar vizinhos de um vértice, seguimos a ordem lexicográfica de vertices.
    """
    n = len(vertices)
    color = ['white'] * n
    dist = [INF] * n
    parent = [None] * n
    order = []

    q = deque()
    color[src_index] = 'gray'
    dist[src_index] = 0
    parent[src_index] = None
    q.append(src_index)
    order.append(vertices[src_index])

    while q:
        u = q.popleft()
        # percorre vizinhos em ordem lexicográfica: índices 0..n-1 correspondem à vertices ordenadas
        for v in range(n):
            if mat[u][v] and color[v] == 'white':
                color[v] = 'gray'
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
                order.append(vertices[v])
        color[u] = 'black'
    return order, dist, parent

def print_bfs_result(vertices, order, dist, parent):

    print("BFS Result")
    if not vertices:
        print("(grafo vazio)")
        return
    src = order[0] if order else vertices[0]
    print(f"Origem: {src}")
    print()
    print(f"{'Vértice':<20}{'Distância':<12}{'Parentes'}")
    for i, v in enumerate(vertices):
        d = dist[i]
        d_str = str(d) if d is not None else "INF"
        p = parent[i]
        p_str = vertices[p] if p is not None else "NIL"
        print(f"{v:<20}{d_str:<12}{p_str}")
    print()
    print("Ordem de visita:")
    if order:
        print(" ".join(order))
    else:
        print("(nenhum vértice visitado)")

import re
from collections import deque

def build_adj_list(vertices, edges, directed):
    """Constroi lista de adjacência com vértices em ordem lexicográfica."""
    idx_of = {v: i for i, v in enumerate(vertices)}
    adj = [[] for _ in range(len(vertices))]
    for u, v in edges:
        if u not in idx_of or v not in idx_of:
            continue
        i, j = idx_of[u], idx_of[v]
        adj[i].append(j)
        if not directed:
            adj[j].append(i)

    # garante ordem lexicográfica dos vizinhos
    for i in range(len(adj)):
        adj[i].sort()
    return adj, idx_of

def dfs_with_list(adj, vertices, src_index):
    """
    Executa DFS usando lista de adjacência.
    - adj: lista de listas de índices de vizinhos
    - vertices: lista de nomes (ordenados)
    - src_index: índice da fonte
    Retorna:
      order: ordem de descoberta
      parent: lista de pais
      discovery: tempos de descoberta
      finish: tempos de término
    """
    n = len(vertices)
    color = ['white'] * n
    parent = [None] * n
    discovery = [None] * n
    finish = [None] * n
    order = []
    time = [0]  # usar lista para mutabilidade dentro da recursão

    def dfs_visit(u):
        color[u] = 'gray'
        time[0] += 1
        discovery[u] = time[0]
        order.append(vertices[u])
        for v in adj[u]:
            if color[v] == 'white':
                parent[v] = u
                dfs_visit(v)
        color[u] = 'black'
        time[0] += 1
        finish[u] = time[0]

    dfs_visit(src_index)
    return order, parent, discovery, finish

def print_dfs_result(vertices, order, parent, discovery, finish):
    print("DFS Result")
    src = order[0] if order else "(nenhum vértice)"
    print(f"Origem: {src}")
    print()
    print(f"{'Vértice':<20}{'Pai':<12}{'Descoberta':<12}{'Finalização'}")
    for i, v in enumerate(vertices):
        p_str = vertices[parent[i]] if parent[i] is not None else "NIL"
        d_str = str(discovery[i]) if discovery[i] is not None else "-"
        f_str = str(finish[i]) if finish[i] is not None else "-"
        print(f"{v:<20}{p_str:<12}{d_str:<12}{f_str}")
    print()
    print("Ordem de visita:")
    print(" ".join(order) if order else "(nenhum vértice)")

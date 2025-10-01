#!/usr/bin/env python3

import sys
import re
from collections import deque

INF = None  # usando None para distância infinita

def parse_dot(path):
    """
    Lê um arquivo DOT simples (sem atributos, sem subgrafos) e retorna:
    - directed: True se digraph, False se graph
    - vertices: lista de nomes de vértices (strings), ordem arbitrária (será ordenada depois)
    - edges: lista de (u, v) arestas observadas na escrita (u and v são strings)
    Observa: suporta sequências "a -- b -- c;" ou "a -> b -> c;" criando arestas adjacentes.
    """
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # retirar comentários simples // ... e /* ... */ (caso)
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)

    # detectar directed ou not
    directed = False
    m = re.search(r'\b(digraph|graph)\b', text, flags=re.IGNORECASE)
    if m:
        directed = (m.group(1).lower() == 'digraph')

    # extrair as linhas / tokens dentro das chaves { ... }
    inner = text
    braces = re.search(r'\{(.*)\}', text, flags=re.DOTALL)
    if braces:
        inner = braces.group(1)

    # tokenizar identificadores: permite "quoted names" ou palavras (letras, dígitos, _, -)
    token_pattern = re.compile(r'"([^"]+)"|([A-Za-z0-9_\-]+)')
    # padrão para detectar cadeias de conectores -> ou --
    connector_pattern = re.compile(r'(--|->)')

    vertices_set = set()
    edges = []

    # processando sentenças separadas por ';' (ponto-e-vírgula é opcional no enunciado,
    # linhas em DOT geralmente terminam com ;)
    # Ainda assim, dividir por ';' facilita extrair as sequências.
    for part in re.split(r';', inner):
        part = part.strip()
        if not part:
            continue

        # substitui vírgulas por espaço (caso usem), remove excesso de espaços
        part = part.replace(',', ' ')
        # identificando uma sequência de tokens e conectores
        # Ex: a -- b -- c  ou a -> b -> c  ou isolado: a
        # vamos extrair todos os tokens (nomes) e conectores na ordem
        tokens = []
        connectors = []
        # walk through the part and pick up tokens and connectors in order
        idx = 0
        L = len(part)
        while idx < L:
            m_conn = connector_pattern.match(part, idx)
            if m_conn:
                connectors.append(m_conn.group(1))
                idx = m_conn.end()
                continue
            m_tok = token_pattern.match(part, idx)
            if m_tok:
                name = m_tok.group(1) if m_tok.group(1) is not None else m_tok.group(2)
                tokens.append(name)
                idx = m_tok.end()
                continue
            idx += 1

        # se não houver conectores mas houver tokens soltos, adicioná-los aos vértices
        if not connectors:
            for t in tokens:
                vertices_set.add(t)
            continue

        # Se houver conectores, assumimos que são do mesmo tipo na sequência (-> ou --),
        # porém podem misturar; tratamos arestas adjacentes: tokens[i] conectada a tokens[i+1], ...
        for t in tokens:
            vertices_set.add(t)
        for i in range(len(tokens)-1):
            u = tokens[i]
            v = tokens[i+1]
            edges.append((u, v))
            # Observação: se em uma mesma sentença usarem '--' e '->' misturado, consideramos as arestas como escritas.
            # A orientação do enunciado garante grafos bem formados, então isto deve bastar.

    vertices = sorted(vertices_set)  # ordenamos aqui (ordem lexicográfica natural de strings)
    return directed, vertices, edges

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
        # percorrer vizinhos em ordem lexicográfica: índices 0..n-1 correspondem à vertices ordenadas
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
    """
    Imprime resultado da BFS.
    Formato sugerido:
    - Linha com 'Source: <vertex>'
    - Em seguida uma tabela (por vértice em ordem lexicográfica):
        Vertex  Distance  Parent
    - E a linha 'Visit order: a b c ...' com ordem de descoberta
    """
    print("BFS Result")
    if not vertices:
        print("(grafo vazio)")
        return
    src = order[0] if order else vertices[0]
    print(f"Source: {src}")
    print()
    print(f"{'Vertex':<20}{'Distance':<12}{'Parent'}")
    for i, v in enumerate(vertices):
        d = dist[i]
        d_str = str(d) if d is not None else "INF"
        p = parent[i]
        p_str = vertices[p] if p is not None else "NIL"
        print(f"{v:<20}{d_str:<12}{p_str}")
    print()
    print("Visit order:")
    if order:
        print(" ".join(order))
    else:
        print("(nenhum vértice visitado)")

def main(argv):
    if len(argv) != 2:
        print("Uso: python bfs_dot.py arquivo.dot")
        return 1
    path = argv[1]
    directed, vertices, edges = parse_dot(path)
    # já ordenamos vertices dentro do parse; garantimos ordem lexicográfica
    mat, idx_of = build_adj_matrix(vertices, edges, directed)
    if not vertices:
        print("Grafo vazio.")
        return 0

    # fonte: vértice com menor ordem lexicográfica (vertices está ordenada)
    src_index = 0
    order, dist, parent = bfs_with_matrix(mat, vertices, src_index)
    print_bfs_result(vertices, order, dist, parent)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

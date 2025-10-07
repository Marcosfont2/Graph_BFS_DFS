import sys
import re
from collections import deque

from bfs import (
    build_adj_matrix, bfs_with_matrix, print_bfs_result
)

from dfs import (
    build_adj_list, dfs_with_list, print_dfs_result
)

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

    text = re.sub(r'//.*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)

    # detectar directed ou not
    directed = False
    m = re.search(r'\b(digraph|graph)\b', text, flags=re.IGNORECASE)
    if m:
        directed = (m.group(1).lower() == 'digraph')

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
        # identifica uma sequência de tokens e conectores
        # Ex: a -- b -- c  ou a -> b -> c  ou isolado: a
        # Extrai todos os tokens (nomes) e conectores na ordem
        tokens = []
        connectors = [] 
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

        # se não houver conectores mas houver tokens soltos, adicionei aos vértices
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

def main(argv):
    if len(argv) != 2:
        print("Uso: python bfs_dot.py arquivo.dot")
        return 1
    path = argv[1]
    directed, vertices, edges = parse_dot(path)
    # ordenei os vertices dentro do parse; garante a ordem lexicográfica
    mat, idx_of = build_adj_matrix(vertices, edges, directed)
    if not vertices:
        print("Grafo vazio.")
        return 0

    # fonte: vértice com menor ordem lexicográfica (vertices está ordenada)
    src_index = 0
    order, dist, parent = bfs_with_matrix(mat, vertices, src_index)
    print_bfs_result(vertices, order, dist, parent)

    print('---------------------------');

    adj, _ = build_adj_list(vertices, edges, directed)
    order_dfs, parent_dfs, dtime, ftime = dfs_with_list(adj, vertices, src_index)
    print_dfs_result(vertices, order_dfs, parent_dfs, dtime, ftime)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

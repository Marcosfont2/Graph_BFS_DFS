# Grafo (BFS e DFS)

Projeto desenvolvido em **Python** para leitura de grafos em formato **DOT**, com construção da **matriz de adjacência** no caso de BFS e lista de adjacência para o caso de DFS e execução de algoritmos de busca.


---

## 📂 Estrutura do projeto
``` bash
Graph_BFS_DFS/
│── bfs_dot.py # Script principal em Python
│── exemplo1.dot # Exemplo de grafo simples conectado
│── exemplo2.dot # Exemplo de grafo desconexo
│── exemplo3.dot # Exemplo de grafo direcionado
│── README.md # Documentação

```
---

## ▶️ Como executar

No terminal (PowerShell no Windows ou bash no Linux/Mac):

```bash
python bfs_dot.py exemplo1.dot
```

📖 Exemplo de uso
Exemplo 1 — Grafo conectado

Arquivo exemplo1.dot:
```  bash

graph G {
    a -- b;
    a -- c;
    b -- d;
    c -- d;
}

```
Saída esperada:

```bash
BFS Result
Origem: a

Vértice             Distância   Parentes
a                   0           NIL
b                   1           a
c                   1           a
d                   2           b

Ordem de visita:
a b c d
```

## 📚 Sobre o projeto

Este projeto foi desenvolvido para a disciplina de Grafos,
pelos discentes Marcos Fontes e Rafael Mirapalheta.
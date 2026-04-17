import copy
import time
import heapq
from collections import deque

movimentos = [(-1,0),(1,0),(0,-1),(0,1),(0,0)]

def alternar(tabuleiro, x, y):
    n = len(tabuleiro)
    novo = copy.deepcopy(tabuleiro)
    for dx, dy in movimentos:
        nx, ny = x+dx, y+dy
        if 0 <= nx < n and 0 <= ny < n:
            novo[nx][ny] ^= 1
    return novo

def objetivo(tabuleiro):
    return all(celula == 1 for linha in tabuleiro for celula in linha)

def busca_largura(inicial):
    visitados = set()
    fila = deque([(inicial, [])])

    while fila:
        tabuleiro, caminho = fila.popleft()
        chave = str(tabuleiro)

        if chave in visitados:
            continue
        visitados.add(chave)

        if objetivo(tabuleiro):
            return caminho

        n = len(tabuleiro)
        for i in range(n):
            for j in range(n):
                fila.append((alternar(tabuleiro,i,j), caminho+[(i,j)]))
    return None

def busca_profundidade(inicial, limite=20):
    visitados = set()

    def recursao(tabuleiro, caminho):
        if len(caminho) > limite:
            return None

        if objetivo(tabuleiro):
            return caminho

        chave = str(tabuleiro)
        if chave in visitados:
            return None
        visitados.add(chave)

        n = len(tabuleiro)
        for i in range(n):
            for j in range(n):
                resultado = recursao(alternar(tabuleiro,i,j), caminho+[(i,j)])
                if resultado:
                    return resultado
        return None

    return recursao(inicial, [])

def heuristica(tabuleiro):
    return sum(celula == 0 for linha in tabuleiro for celula in linha)

def gulosa(inicial):
    tabuleiro = inicial
    caminho = []
    n = len(tabuleiro)

    for _ in range(50):
        if objetivo(tabuleiro):
            return caminho

        melhor = None
        melhor_h = float('inf')

        for i in range(n):
            for j in range(n):
                novo = alternar(tabuleiro,i,j)
                h = heuristica(novo)
                if h < melhor_h:
                    melhor_h = h
                    melhor = (i,j,novo)

        if melhor:
            i,j,tabuleiro = melhor
            caminho.append((i,j))

    return None

def a_estrela(inicial):
    heap = [(heuristica(inicial), 0, inicial, [])]
    visitados = set()

    while heap:
        f, g, tabuleiro, caminho = heapq.heappop(heap)
        chave = str(tabuleiro)

        if chave in visitados:
            continue
        visitados.add(chave)

        if objetivo(tabuleiro):
            return caminho

        n = len(tabuleiro)
        for i in range(n):
            for j in range(n):
                novo = alternar(tabuleiro,i,j)
                heapq.heappush(heap, (g+1+heuristica(novo), g+1, novo, caminho+[(i,j)]))

    return None

def executar_teste(algoritmo, nome, inicial):
    print(f"\n--- {nome} ---")
    inicio = time.time()

    resultado = algoritmo(inicial)

    fim = time.time()

    if resultado:
        print("Solução encontrada!")
        print("Número de passos:", len(resultado))
        print("Movimentos:", resultado)
    else:
        print("Sem solução")

    print("Tempo:", round(fim - inicio, 5), "segundos")


if __name__ == "__main__":
    inicial = [
        [0,1,0],
        [0,0,1],
        [0,1,0]
    ]

    print("Tabuleiro inicial:")
    for linha in inicial:
        print(linha)

    executar_teste(busca_largura, "Busca em Largura (BFS)", inicial)
    executar_teste(busca_profundidade, "Busca em Profundidade (DFS)", inicial)
    executar_teste(gulosa, "Busca Gulosa", inicial)
    executar_teste(a_estrela, "A*", inicial)


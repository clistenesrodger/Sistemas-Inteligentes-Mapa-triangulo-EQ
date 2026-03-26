from collections import deque

from geometry import TOLERANCIA_EPS, segmentos_intersectam

EPS = TOLERANCIA_EPS


def _ponto_no_triangulo_estrito(ponto, triangulo):
    x, y = ponto
    (x1, y1), (x2, y2), (x3, y3) = triangulo

    det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    if abs(det) <= EPS:
        return False

    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / det
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / det
    c = 1 - a - b

    return (EPS < a < 1 - EPS) and (EPS < b < 1 - EPS) and (EPS < c < 1 - EPS)


def _segmento_visivel(a, b, triangulos):
    meio = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
    for tri in triangulos:
        if _ponto_no_triangulo_estrito(meio, tri):
            return False

    for tri in triangulos:
        edges = [(tri[i], tri[(i + 1) % 3]) for i in range(3)]
        for c, d in edges:
            if not segmentos_intersectam(a, b, c, d):
                continue

            # Permite conexao quando o segmento toca apenas nos proprios vertices.
            compartilha_extremo = (
                (abs(a[0] - c[0]) <= EPS and abs(a[1] - c[1]) <= EPS)
                or (abs(a[0] - d[0]) <= EPS and abs(a[1] - d[1]) <= EPS)
                or (abs(b[0] - c[0]) <= EPS and abs(b[1] - c[1]) <= EPS)
                or (abs(b[0] - d[0]) <= EPS and abs(b[1] - d[1]) <= EPS)
            )
            if compartilha_extremo:
                continue

            return False

    return True


def calcular_caminho_visibilidade(inicio, fim, triangulos):
    for tri in triangulos:
        if _ponto_no_triangulo_estrito(inicio, tri) or _ponto_no_triangulo_estrito(fim, tri):
            return []

    vertices = [inicio, fim]
    for tri in triangulos:
        vertices.extend(tri)

    quantidade_vertices = len(vertices)
    visitado = [False] * quantidade_vertices
    prev = [-1] * quantidade_vertices
    vizinhos_cache = {}

    def _obter_vizinhos(indice_origem):
        # Calcula vizinhos sob demanda para evitar montar o grafo inteiro.
        if indice_origem in vizinhos_cache:
            return vizinhos_cache[indice_origem]

        vizinhos = []
        origem = vertices[indice_origem]
        for indice_destino in range(quantidade_vertices):
            if indice_destino == indice_origem:
                continue
            if _segmento_visivel(origem, vertices[indice_destino], triangulos):
                vizinhos.append(indice_destino)

        vizinhos_cache[indice_origem] = vizinhos
        return vizinhos

    fila = deque([0])
    visitado[0] = True

    while fila:
        u = fila.popleft()
        if u == 1:
            break
        for v in _obter_vizinhos(u):
            if visitado[v]:
                continue
            visitado[v] = True
            prev[v] = u
            if v == 1:
                fila.clear()
                break
            fila.append(v)

    if not visitado[1]:
        return []

    caminho_idx = []
    atual = 1
    while atual != -1:
        caminho_idx.append(atual)
        atual = prev[atual]
    caminho_idx.reverse()

    return [vertices[i] for i in caminho_idx]

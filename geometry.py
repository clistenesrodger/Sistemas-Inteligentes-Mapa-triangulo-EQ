"""Utilitarios geometricos para triangulos no plano 2D - Versao Otimizada"""

import math

EPS = 1e-9 # Tolerancia para comparacoes de ponto flutuante

# Funcao para calcular a altura de um triangulo equilatero dado o lado
def altura_triangulo(lado):
    """Calcula a altura de um triangulo equilatero."""
    return (math.sqrt(3) / 2) * lado

# Serve para descobrir se um ponto está: esquerda, direita ou alinhado
def orient(p, q, r):
    """Calcula a orientacao de tres pontos no plano 2D."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def ponto_no_segmento(ponto, a, b):
    """Verifica se um ponto pertence ao segmento AB."""
    # Verifica apenas a orientação do PONTO de um triângulo em relação a aresta de outro
    if abs(orient(a, b, ponto)) > EPS:
        return False
    return (min(a[0], b[0]) - EPS <= ponto[0] <= max(a[0], b[0]) + EPS
            and min(a[1], b[1]) - EPS <= ponto[1] <= max(a[1], b[1]) + EPS)

def segmentos_intersectam(a, b, c, d):
    """Determina se dois segmentos AB e CD se intersectam."""
    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)

    if (o1 * o2 < -EPS) and (o3 * o4 < -EPS):
        return True

    if abs(o1) <= EPS and ponto_no_segmento(c, a, b):
        return True
    if abs(o2) <= EPS and ponto_no_segmento(d, a, b):
        return True
    if abs(o3) <= EPS and ponto_no_segmento(a, c, d):
        return True
    if abs(o4) <= EPS and ponto_no_segmento(b, c, d):
        return True

    return False # Não se cruzam

def ponto_no_triangulo(ponto, triangulo):
    """Verifica se um ponto esta dentro ou na borda de um triangulo."""
    x, y = ponto
    (x1, y1), (x2, y2), (x3, y3) = triangulo

    det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    if abs(det) <= EPS:
        return False

    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / det
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / det
    c = 1 - a - b

    return (-EPS <= a <= 1 + EPS and -EPS <= b <= 1 + EPS and -EPS <= c <= 1 + EPS)

def triangulos_colidem(t1, t2):
    """Verifica se dois triangulos colidem ou se tocam."""
    edges1 = [(t1[i], t1[(i + 1) % 3]) for i in range(3)]
    edges2 = [(t2[i], t2[(i + 1) % 3]) for i in range(3)]

    for e1 in edges1:
        for e2 in edges2:
            if segmentos_intersectam(e1[0], e1[1], e2[0], e2[1]):
                return True

    for p in t1:
        if ponto_no_triangulo(p, t2):
            return True

    for p in t2:
        if ponto_no_triangulo(p, t1):
            return True

    return False

def distancia_ponto_segmento(ponto, a, b):
    """Calcula a distancia minima entre um ponto e um segmento AB."""
    ax, ay = a
    bx, by = b
    px, py = ponto

    abx = bx - ax
    aby = by - ay
    ab2 = abx * abx + aby * aby
    
    if ab2 <= EPS:
        return math.hypot(px - ax, py - ay)

    t = ((px - ax) * abx + (py - ay) * aby) / ab2
    t = max(0.0, min(1.0, t))

    projx = ax + t * abx
    projy = ay + t * aby
    return math.hypot(px - projx, py - projy)

def distancia_segmentos(a, b, c, d):
    """Calcula a distancia minima entre dois segmentos AB e CD."""
    if segmentos_intersectam(a, b, c, d):
        return 0.0

    return min(distancia_ponto_segmento(a, c, d),
               distancia_ponto_segmento(b, c, d),
               distancia_ponto_segmento(c, a, b),
               distancia_ponto_segmento(d, a, b))
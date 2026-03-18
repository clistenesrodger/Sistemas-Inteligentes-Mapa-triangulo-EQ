"""Utilitarios geometricos para triangulos no plano 2D - Versao Otimizada"""

import math

TOLERANCIA_EPS = 1e-9


def altura_triangulo(comprimento_lado):
    return (math.sqrt(3) / 2) * comprimento_lado


def orientacao(ponto_p, ponto_q, ponto_r):
    return (ponto_q[0] - ponto_p[0]) * (ponto_r[1] - ponto_p[1]) - (ponto_q[1] - ponto_p[1]) * (ponto_r[0] - ponto_p[0])


def ponto_no_segmento(ponto_verificar, ponto_a, ponto_b):
    if abs(orientacao(ponto_a, ponto_b, ponto_verificar)) > TOLERANCIA_EPS:
        return False
    return (min(ponto_a[0], ponto_b[0]) - TOLERANCIA_EPS <= ponto_verificar[0] <= max(ponto_a[0], ponto_b[0]) + TOLERANCIA_EPS
            and min(ponto_a[1], ponto_b[1]) - TOLERANCIA_EPS <= ponto_verificar[1] <= max(ponto_a[1], ponto_b[1]) + TOLERANCIA_EPS)


def segmentos_intersectam(ponto_a, ponto_b, ponto_c, ponto_d):
    o1 = orientacao(ponto_a, ponto_b, ponto_c)
    o2 = orientacao(ponto_a, ponto_b, ponto_d)
    o3 = orientacao(ponto_c, ponto_d, ponto_a)
    o4 = orientacao(ponto_c, ponto_d, ponto_b)

    if (o1 * o2 < -TOLERANCIA_EPS) and (o3 * o4 < -TOLERANCIA_EPS):
        return True

    if abs(o1) <= TOLERANCIA_EPS and ponto_no_segmento(ponto_c, ponto_a, ponto_b):
        return True
    if abs(o2) <= TOLERANCIA_EPS and ponto_no_segmento(ponto_d, ponto_a, ponto_b):
        return True
    if abs(o3) <= TOLERANCIA_EPS and ponto_no_segmento(ponto_a, ponto_c, ponto_d):
        return True
    if abs(o4) <= TOLERANCIA_EPS and ponto_no_segmento(ponto_b, ponto_c, ponto_d):
        return True

    return False


def ponto_no_triangulo(ponto_verificar, triangulo):
    x, y = ponto_verificar
    (x1, y1), (x2, y2), (x3, y3) = triangulo

    det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    if abs(det) <= TOLERANCIA_EPS:
        return False

    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / det
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / det
    c = 1 - a - b

    return (-TOLERANCIA_EPS <= a <= 1 + TOLERANCIA_EPS and 
            -TOLERANCIA_EPS <= b <= 1 + TOLERANCIA_EPS and 
            -TOLERANCIA_EPS <= c <= 1 + TOLERANCIA_EPS)


def triangulos_colidem(triangulo1, triangulo2):
    arestas1 = [(triangulo1[i], triangulo1[(i + 1) % 3]) for i in range(3)]
    arestas2 = [(triangulo2[i], triangulo2[(i + 1) % 3]) for i in range(3)]

    for aresta1 in arestas1:
        for aresta2 in arestas2:
            if segmentos_intersectam(aresta1[0], aresta1[1], aresta2[0], aresta2[1]):
                return True

    for vertice in triangulo1:
        if ponto_no_triangulo(vertice, triangulo2):
            return True

    for vertice in triangulo2:
        if ponto_no_triangulo(vertice, triangulo1):
            return True

    return False


def distancia_ponto_segmento(ponto_verificar, ponto_a, ponto_b):
    ax, ay = ponto_a
    bx, by = ponto_b
    px, py = ponto_verificar

    vetor_x = bx - ax
    vetor_y = by - ay
    comprimento2 = vetor_x * vetor_x + vetor_y * vetor_y
    
    if comprimento2 <= TOLERANCIA_EPS:
        return math.hypot(px - ax, py - ay)

    t = ((px - ax) * vetor_x + (py - ay) * vetor_y) / comprimento2
    t = max(0.0, min(1.0, t))

    prox_x = ax + t * vetor_x
    prox_y = ay + t * vetor_y
    return math.hypot(px - prox_x, py - prox_y)


def distancia_segmentos(ponto_a, ponto_b, ponto_c, ponto_d):
    if segmentos_intersectam(ponto_a, ponto_b, ponto_c, ponto_d):
        return 0.0

    return min(distancia_ponto_segmento(ponto_a, ponto_c, ponto_d),
               distancia_ponto_segmento(ponto_b, ponto_c, ponto_d),
               distancia_ponto_segmento(ponto_c, ponto_a, ponto_b),
               distancia_ponto_segmento(ponto_d, ponto_a, ponto_b))
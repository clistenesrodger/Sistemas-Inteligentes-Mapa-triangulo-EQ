import random

from geometry import altura_triangulo, distancia_triangulos, triangulos_colidem


def gerar_triangulo(lado, largura, altura):
    h = altura_triangulo(lado)

    x = random.uniform(0, largura - lado)
    y = random.uniform(0, altura - h)

    v1 = (x, y)
    v2 = (x + lado, y)
    v3 = (x + lado / 2, y + h)

    return [v1, v2, v3]


def gerar_triangulos_sem_colisao(qtd, lado, largura, altura, tentativas_max=1000):
    triangulos = []
    margem_visual = max(1e-6, lado * 0.02)

    while len(triangulos) < qtd and tentativas_max > 0:
        novo = gerar_triangulo(lado, largura, altura)

        colisao = False
        for t in triangulos:
            if triangulos_colidem(novo, t):
                colisao = True
                break
            if distancia_triangulos(novo, t) < margem_visual:
                colisao = True
                break

        if not colisao:
            triangulos.append(novo)

        tentativas_max -= 1

    return triangulos

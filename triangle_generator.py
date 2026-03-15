"""Funcoes para gerar triangulos e montar mapas sem colisao."""

import random

from geometry import altura_triangulo, distancia_triangulos, triangulos_colidem


def gerar_triangulo(lado, largura, altura):
    """Gera um triangulo equilatero aleatorio dentro dos limites do mapa.

    O triangulo e orientado com base horizontal e vertice superior para cima.
    A posicao aleatoria respeita os limites para manter os tres vertices dentro
    da area definida por largura x altura.

    Args:
        lado (float): comprimento do lado do triangulo equilatero.
        largura (float): largura do mapa.
        altura (float): altura do mapa.

    Returns:
        list[tuple[float, float]]: tres vertices do triangulo gerado.
    """
    h = altura_triangulo(lado)

    x = random.uniform(0, largura - lado)
    y = random.uniform(0, altura - h)

    v1 = (x, y)
    v2 = (x + lado, y)
    v3 = (x + lado / 2, y + h)

    return [v1, v2, v3]


def gerar_triangulos_sem_colisao(qtd, lado, largura, altura, tentativas_max=1000):
    """Gera uma lista de triangulos sem colisao e sem quase-sobreposicao visual.

    Args:
        qtd: quantidade desejada de triangulos.
        lado: comprimento do lado do triangulo equilatero.
        largura: largura do mapa.
        altura: altura do mapa.
        tentativas_max: numero maximo de tentativas para posicionamento.

    Returns:
        list[list[tuple[float, float]]]: triangulos gerados.

        Notes:
                - A funcao usa uma margem visual minima proporcional ao lado do
                    triangulo para evitar quase-encostos que podem parecer colisao no plot.
                - Se as tentativas acabarem antes de atingir `qtd`, a lista retornada
                    pode ter menos triangulos que o solicitado.
    """
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

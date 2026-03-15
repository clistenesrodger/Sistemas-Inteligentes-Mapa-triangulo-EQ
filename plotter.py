"""Rotinas de visualizacao do mapa com matplotlib."""

import os

import matplotlib.pyplot as plt


def plotar_mapa(triangulos, largura, altura, inicio, fim, caminho=None, saida="mapa_triangulos.png"):
    """Plota o mapa com triangulos, ponto inicial e ponto final.

    Desenha cada triangulo como poligono fechado, destaca os pontos inicial e
    final, e opcionalmente desenha uma linha de caminho quando fornecida.

    Args:
        triangulos (list[list[tuple[float, float]]]): lista de triangulos do mapa.
        largura (float): largura do mapa (limite do eixo x).
        altura (float): altura do mapa (limite do eixo y).
        inicio (tuple[float, float]): ponto inicial a ser marcado no grafico.
        fim (tuple[float, float]): ponto final a ser marcado no grafico.
        caminho (list[tuple[float, float]] | None): sequencia de pontos para
            desenhar o caminho; quando None, nenhum caminho e desenhado.
        saida (str): nome do arquivo de imagem quando o backend for nao interativo.

    Notes:
        Em backend nao interativo (por exemplo, Agg), a figura e salva em arquivo.
        Em backend interativo, a janela de plotagem e exibida na tela.
    """
    fig, ax = plt.subplots()

    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)

    for tri in triangulos:
        xs = [p[0] for p in tri] + [tri[0][0]]
        ys = [p[1] for p in tri] + [tri[0][1]]
        ax.plot(xs, ys)

    ax.scatter(inicio[0], inicio[1])
    ax.text(inicio[0], inicio[1], "  Start (0,0)")

    ax.scatter(fim[0], fim[1])
    ax.text(fim[0], fim[1], "  Goal")

    if caminho and len(caminho) >= 2:
        xs = [p[0] for p in caminho]
        ys = [p[1] for p in caminho]
        ax.plot(xs, ys, "r-", linewidth=2)

    ax.set_title("Mapa com Obstaculos (Triangulos)")
    ax.set_aspect("equal")

    backend = plt.get_backend().lower()
    if "agg" in backend:
        plt.savefig(saida, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"Backend nao interativo detectado ({backend}). Figura salva em: {os.path.abspath(saida)}")
    else:
        plt.show()

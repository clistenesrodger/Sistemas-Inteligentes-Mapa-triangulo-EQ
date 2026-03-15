import os

import matplotlib.pyplot as plt


def plotar_mapa(triangulos, largura, altura, inicio, fim, caminho=None, saida="mapa_triangulos.png"):
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

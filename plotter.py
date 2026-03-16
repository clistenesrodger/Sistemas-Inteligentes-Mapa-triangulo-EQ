"""Rotinas de visualizacao do mapa com matplotlib."""

import os
import matplotlib.pyplot as plt

def plotar_mapa(triangulos, largura, altura, inicio, fim, caminho=None, saida="mapa_triangulos.png"):
    """Plota o mapa com triangulos, ponto inicial e ponto final."""
    fig, ax = plt.subplots(figsize=(12, 10))

    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)

    # Desenha triangulos com cor mais visivel para muitos triangulos
    for i, tri in enumerate(triangulos):
        xs = [p[0] for p in tri] + [tri[0][0]]
        ys = [p[1] for p in tri] + [tri[0][1]]
        # Usa cor mais clara para muitos triangulos
        if len(triangulos) > 100:
            ax.plot(xs, ys, 'b-', linewidth=0.8, alpha=0.7)
        else:
            ax.plot(xs, ys, 'b-', linewidth=1.5)

    # Pontos inicial e final
    ax.scatter(inicio[0], inicio[1], c='green', s=100, zorder=5)
    ax.text(inicio[0], inicio[1], "  Start (0,0)", fontsize=12, fontweight='bold')

    ax.scatter(fim[0], fim[1], c='red', s=100, zorder=5)
    ax.text(fim[0], fim[1], "  Goal", fontsize=12, fontweight='bold')

    # Caminho se existir
    if caminho and len(caminho) >= 2:
        xs = [p[0] for p in caminho]
        ys = [p[1] for p in caminho]
        ax.plot(xs, ys, "r-", linewidth=3, alpha=0.8)

    # Informacoes do mapa
    titulo = f"Mapa com {len(triangulos)} Triangulos (Lado={triangulos[0][1][0]-triangulos[0][0][0]:.1f})"
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)

    # Backend handling
    backend = plt.get_backend().lower()
    if "agg" in backend:
        plt.savefig(saida, dpi=200, bbox_inches="tight")
        plt.close(fig)
        print(f"Figura salva em: {os.path.abspath(saida)}")
    else:
        plt.tight_layout()
        plt.show()
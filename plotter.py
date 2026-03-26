"""Rotinas de visualizacao do mapa com matplotlib."""

import os
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


def plotar_mapa(lista_de_triangulos, largura_mapa, altura_mapa, ponto_inicial, ponto_final, caminho_percorrido=None, retas_visiveis=None, nome_arquivo_saida="mapa_triangulos.png"):
    """Plota o mapa com obstaculos, pontos de inicio/fim e overlays opcionais.

    Args:
        lista_de_triangulos: triangulos-obstaculo a serem desenhados.
        largura_mapa: largura total do mapa.
        altura_mapa: altura total do mapa.
        ponto_inicial: tupla (x, y) de inicio.
        ponto_final: tupla (x, y) de destino.
        caminho_percorrido: lista opcional de pontos do caminho final.
        retas_visiveis: lista opcional de retas de visibilidade no formato
            [((x1, y1), (x2, y2)), ...].
        nome_arquivo_saida: nome do arquivo de saida quando backend for sem GUI.
    """
    figura, eixos = plt.subplots(figsize=(12, 10))

    eixos.set_xlim(0, largura_mapa)
    eixos.set_ylim(0, altura_mapa)

    # Renderiza arestas dos triangulos em lote para reduzir custo de draw calls.
    segmentos_triangulos = []
    for triangulo_atual in lista_de_triangulos:
        for indice in range(3):
            ponto_a = triangulo_atual[indice]
            ponto_b = triangulo_atual[(indice + 1) % 3]
            segmentos_triangulos.append((ponto_a, ponto_b))

    largura_linha_triangulos = 0.8 if len(lista_de_triangulos) > 100 else 1.5
    alpha_triangulos = 0.7 if len(lista_de_triangulos) > 100 else 1.0
    colecao_triangulos = LineCollection(
        segmentos_triangulos,
        colors="b",
        linewidths=largura_linha_triangulos,
        alpha=alpha_triangulos,
        zorder=2,
    )
    eixos.add_collection(colecao_triangulos)

    # Retas de visibilidade entre vertices e pontos start/goal
    if retas_visiveis:
        colecao_retas_visiveis = LineCollection(
            retas_visiveis,
            colors="orange",
            linewidths=0.7,
            alpha=0.35,
            zorder=1,
        )
        eixos.add_collection(colecao_retas_visiveis)

    # Ponto INICIAL (verde)
    eixos.scatter(ponto_inicial[0], ponto_inicial[1], c='green', s=100, zorder=5)
    eixos.text(ponto_inicial[0], ponto_inicial[1], "  Start (0,0)", fontsize=12, fontweight='bold')

    # Ponto FINAL (vermelho)-
    eixos.scatter(ponto_final[0], ponto_final[1], c='red', s=100, zorder=5)
    eixos.text(ponto_final[0], ponto_final[1], "  Goal", fontsize=12, fontweight='bold')

    # Caminho percorrido (se existir)
    if caminho_percorrido and len(caminho_percorrido) >= 2:
        coordenadas_x_caminho = [ponto[0] for ponto in caminho_percorrido]
        coordenadas_y_caminho = [ponto[1] for ponto in caminho_percorrido]
        eixos.plot(coordenadas_x_caminho, coordenadas_y_caminho, "r-", linewidth=3, alpha=0.8)

    # Informacoes do mapa
    primeiro_triangulo = lista_de_triangulos[0]
    lado_primeiro_triangulo = primeiro_triangulo[1][0] - primeiro_triangulo[0][0]  # X2 - X1
    titulo = f"Mapa com {len(lista_de_triangulos)} Triangulos (Lado={lado_primeiro_triangulo:.1f})"
    
    eixos.set_title(titulo, fontsize=14, fontweight='bold')
    eixos.set_aspect("equal")  # Mantém proporção 1:1
    eixos.grid(True, alpha=0.3)  # Grade transparente

    # Backend handling (salvar vs mostrar)
    backend_atual = plt.get_backend().lower()
    if "agg" in backend_atual:  # Modo sem interface gráfica
        plt.savefig(nome_arquivo_saida, dpi=130, bbox_inches="tight")
        plt.close(figura)
        print(f"Figura salva em: {os.path.abspath(nome_arquivo_saida)}")
    else:  # Modo com interface gráfica
        plt.tight_layout()
        plt.show()
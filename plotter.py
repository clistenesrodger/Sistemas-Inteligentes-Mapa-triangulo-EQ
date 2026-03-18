"""Rotinas de visualizacao do mapa com matplotlib."""

import os
import matplotlib.pyplot as plt

def plotar_mapa(lista_de_triangulos, largura_mapa, altura_mapa, ponto_inicial, ponto_final, caminho_percorrido=None, nome_arquivo_saida="mapa_triangulos.png"):
    """Plota o mapa com triangulos, ponto inicial e ponto final."""
    figura, eixos = plt.subplots(figsize=(12, 10))

    eixos.set_xlim(0, largura_mapa)
    eixos.set_ylim(0, altura_mapa)

    # Desenha triangulos com cor mais visivel para muitos triangulos
    for indice, triangulo_atual in enumerate(lista_de_triangulos):
        coordenadas_x = [vertice[0] for vertice in triangulo_atual] + [triangulo_atual[0][0]]
        coordenadas_y = [vertice[1] for vertice in triangulo_atual] + [triangulo_atual[0][1]]
        
        # Usa linha mais fina para muitos triangulos
        if len(lista_de_triangulos) > 100:
            eixos.plot(coordenadas_x, coordenadas_y, 'b-', linewidth=0.8, alpha=0.7)
        else:
            eixos.plot(coordenadas_x, coordenadas_y, 'b-', linewidth=1.5)

    # Ponto INICIAL (verde)
    eixos.scatter(ponto_inicial[0], ponto_inicial[1], c='green', s=100, zorder=5)
    eixos.text(ponto_inicial[0], ponto_inicial[1], "  Start (0,0)", fontsize=12, fontweight='bold')

    # Ponto FINAL (vermelho)
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
        plt.savefig(nome_arquivo_saida, dpi=200, bbox_inches="tight")
        plt.close(figura)
        print(f"Figura salva em: {os.path.abspath(nome_arquivo_saida)}")
    else:  # Modo com interface gráfica
        plt.tight_layout()
        plt.show()
"""Ponto de entrada da aplicacao - Versao preparada para muitos triangulos."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import time

from plotter import plotar_mapa
from triangle_generator import gerar_triangulos_sem_colisao, gerar_retas_visibilidade
from geometry import ponto_no_triangulo, triangulos_colidem

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
BOOTSTRAP_FLAG = "MAPA_TRIANGULOS_BOOTSTRAPPED"
LIMITE_TRIANGULOS_RETAS_AUTO = 250
MAX_RETAS_PADRAO = 12000


def _obter_caminho_python_venv():
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def _esta_em_ambiente_virtual():
    return (getattr(sys, "base_prefix", sys.prefix) != sys.prefix) or hasattr(sys, "real_prefix")


def _instalar_dependencias(caminho_python_executavel):
    print("Instalando dependencias...")
    subprocess.check_call([str(caminho_python_executavel), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)])


def _dependencias_estao_instaladas():
    try:
        import matplotlib
        return True
    except ModuleNotFoundError:
        return False


def garantir_ambiente_execucao():
    if os.environ.get(BOOTSTRAP_FLAG) == "1":
        return

    caminho_python_venv = _obter_caminho_python_venv()

    if not _esta_em_ambiente_virtual():
        if not caminho_python_venv.exists():
            print("Criando ambiente virtual...")
            subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])

        _instalar_dependencias(caminho_python_venv)

        variaveis_ambiente = os.environ.copy()
        variaveis_ambiente[BOOTSTRAP_FLAG] = "1"
        subprocess.check_call([str(caminho_python_venv), str(Path(__file__).resolve()), *sys.argv[1:]], env=variaveis_ambiente)
        sys.exit(0)

    if not _dependencias_estao_instaladas():
        _instalar_dependencias(sys.executable)


def validar_parametros(largura_mapa, altura_mapa, quantidade_triangulos, lado_triangulo, coordenada_x_final, coordenada_y_final):
    """Valida consistencia dos parametros de entrada do mapa.

    Tambem emite aviso quando a relacao area total dos triangulos/area do mapa
    indica alta chance de configuracao inviavel.
    """
    if largura_mapa <= 0 or altura_mapa <= 0:
        raise ValueError("Largura e altura devem ser positivos")
    if quantidade_triangulos <= 0:
        raise ValueError("Quantidade de triangulos deve ser positiva")
    if lado_triangulo <= 0:
        raise ValueError("Lado do triangulo deve ser positivo")
    if coordenada_x_final < 0 or coordenada_x_final > largura_mapa or coordenada_y_final < 0 or coordenada_y_final > altura_mapa:
        raise ValueError("Ponto final deve estar dentro do mapa")
    
    from geometry import altura_triangulo
    altura_tri = altura_triangulo(lado_triangulo)
    area_um_triangulo = (lado_triangulo * altura_tri) / 2
    area_total_mapa = largura_mapa * altura_mapa
    
    if area_um_triangulo * quantidade_triangulos > area_total_mapa * 2:
        print(f"\n--- ATENCAO ---")
        print(f"Area total dos triangulos: {area_um_triangulo * quantidade_triangulos:.2f}")
        print(f"Area do mapa: {area_total_mapa:.2f}")
        print(f"Relacao area triangulos/area mapa: {(area_um_triangulo * quantidade_triangulos / area_total_mapa):.2f}")
        print("Isso pode ser impossivel de gerar. Continuando mesmo assim...")
        print("---------------\n")
        return False
    return True


def verificar_ponto_final(ponto_final, lista_triangulos):
    """Garante que o ponto final esteja em area livre de obstaculos."""
    for indice, triangulo in enumerate(lista_triangulos):
        if ponto_no_triangulo(ponto_final, triangulo):
            print(f"\n--- ERRO: PONTO FINAL DENTRO DO TRIANGULO {indice} ---")
            print(f"Ponto final ({ponto_final[0]:.2f}, {ponto_final[1]:.2f}) esta dentro de um obstaculo!")
            return False
    print("✓ Ponto final esta em area livre")
    return True


def _bbox_triangulo(triangulo):
    """Calcula a bounding box de um triangulo no formato (xmin, ymin, xmax, ymax)."""
    coordenadas_x = [vertice[0] for vertice in triangulo]
    coordenadas_y = [vertice[1] for vertice in triangulo]
    return (min(coordenadas_x), min(coordenadas_y), max(coordenadas_x), max(coordenadas_y))


def _bbox_intersecta(bbox1, bbox2):
    """Retorna True quando duas bounding boxes se intersectam."""
    xmin1, ymin1, xmax1, ymax1 = bbox1
    xmin2, ymin2, xmax2, ymax2 = bbox2
    return not (xmax1 < xmin2 or xmax2 < xmin1 or ymax1 < ymin2 or ymax2 < ymin1)


def contar_colisoes_otimizado(lista_triangulos, tamanho_celula):
    """Conta colisoes usando grade espacial para reduzir comparacoes.

    Args:
        lista_triangulos: lista de triangulos gerados.
        tamanho_celula: tamanho da celula da grade para indexacao espacial.

    Returns:
        Quantidade total de pares de triangulos em colisao.
    """
    if not lista_triangulos:
        return 0

    tamanho_celula = max(1.0, float(tamanho_celula))
    lista_bounding_boxes = [_bbox_triangulo(triangulo) for triangulo in lista_triangulos]
    grade_espacial = {}
    pares_processados = set()
    quantidade_colisoes = 0

    for indice, bbox_atual in enumerate(lista_bounding_boxes):
        xmin, ymin, xmax, ymax = bbox_atual
        celula_x_min = int(xmin // tamanho_celula)
        celula_y_min = int(ymin // tamanho_celula)
        celula_x_max = int(xmax // tamanho_celula)
        celula_y_max = int(ymax // tamanho_celula)

        # Compara apenas com triângulos já indexados nas células cobertas pela bbox atual.
        candidatos = set()
        for celula_x in range(celula_x_min, celula_x_max + 1):
            for celula_y in range(celula_y_min, celula_y_max + 1):
                celula = (celula_x, celula_y)
                for indice_existente in grade_espacial.get(celula, []):
                    candidatos.add(indice_existente)

        for indice_existente in candidatos:
            par = (indice_existente, indice)
            if par in pares_processados:
                continue
            pares_processados.add(par)

            if not _bbox_intersecta(lista_bounding_boxes[indice_existente], bbox_atual):
                continue

            if triangulos_colidem(lista_triangulos[indice_existente], lista_triangulos[indice]):
                quantidade_colisoes += 1
                print(f"Colisao entre triangulo {indice_existente} e {indice}")

        for celula_x in range(celula_x_min, celula_x_max + 1):
            for celula_y in range(celula_y_min, celula_y_max + 1):
                celula = (celula_x, celula_y)
                if celula not in grade_espacial:
                    grade_espacial[celula] = []
                grade_espacial[celula].append(indice)

    return quantidade_colisoes


def ler_parametros():
    """Lê parametros por CLI ou entrada interativa.

    Returns:
        Tupla contendo largura, altura, quantidade de triangulos, lado,
        coordenadas do ponto final e opcoes de plotagem de retas visiveis.
    """
    parser = argparse.ArgumentParser(description="Gerador de mapas com obstaculos triangulares")
    parser.add_argument("--largura", type=float, help="Largura do mapa")
    parser.add_argument("--altura", type=float, help="Altura do mapa")
    parser.add_argument("--qtd", type=int, help="Quantidade de triangulos")
    parser.add_argument("--lado", type=float, help="Tamanho do lado do triangulo")
    parser.add_argument("--xf", type=float, help="Coordenada X do ponto final")
    parser.add_argument("--yf", type=float, help="Coordenada Y do ponto final")
    parser.add_argument("--plotar-retas", action="store_true", help="Forca o calculo e desenho das retas de visibilidade")
    parser.add_argument("--max-retas", type=int, default=MAX_RETAS_PADRAO, help=f"Limite de retas de visibilidade (padrao: {MAX_RETAS_PADRAO})")
    argumentos = parser.parse_args()

    lista_parametros = [argumentos.largura, argumentos.altura, argumentos.qtd, argumentos.lado, argumentos.xf, argumentos.yf]

    if all(parametro is not None for parametro in lista_parametros):
        validar_parametros(argumentos.largura, argumentos.altura, argumentos.qtd, argumentos.lado, argumentos.xf, argumentos.yf)
        return (
            argumentos.largura,
            argumentos.altura,
            argumentos.qtd,
            argumentos.lado,
            argumentos.xf,
            argumentos.yf,
            argumentos.plotar_retas,
            argumentos.max_retas,
        )

    if any(parametro is not None for parametro in lista_parametros):
        parser.error("Informe todos os parametros ou nenhum deles.")

    print("\n=== GERADOR DE MAPAS TRIANGULARES ===\n")
    largura = float(input("Largura do mapa: "))
    altura = float(input("Altura do mapa: "))
    qtd = int(input("Quantidade de triangulos: "))
    lado = float(input("Tamanho do lado do triangulo: "))
    xf = float(input("Coordenada X do ponto final: "))
    yf = float(input("Coordenada Y do ponto final: "))
    
    validar_parametros(largura, altura, qtd, lado, xf, yf)
    return largura, altura, qtd, lado, xf, yf, False, MAX_RETAS_PADRAO


def main():
    """Executa o fluxo principal: entrada, geracao, validacoes e plotagem."""
    print("\n" + "="*50)
    print("GERADOR DE MAPAS COM TRIANGULOS")
    print("="*50 + "\n")
    
    tempo_inicio_total = time.time()
    
    largura, altura, quantidade, lado, x_final, y_final, forcar_plotagem_retas, max_retas = ler_parametros()
    ponto_final = (x_final, y_final)
    
    print(f"\nConfiguracao:")
    print(f"- Mapa: {largura} x {altura}")
    print(f"- Triangulos: {quantidade} (lado {lado})")
    print(f"- Ponto final: ({x_final}, {y_final})")
    
    print("\nGerando triangulos sem colisao...")
    tempo_inicio_geracao = time.time()
    lista_triangulos = gerar_triangulos_sem_colisao(quantidade, lado, largura, altura, ponto_final)
    tempo_geracao = time.time() - tempo_inicio_geracao
    
    print(f"Geracao concluida em {tempo_geracao:.2f} segundos")
    print(f"Triangulos gerados: {len(lista_triangulos)}")
    
    print("\nVerificando seguranca do ponto final...")
    ponto_final_seguro = verificar_ponto_final(ponto_final, lista_triangulos)
    
    if not ponto_final_seguro:
        print("\n!!! CRITICO: Ponto final esta dentro de um obstaculo !!!")
        print("Isso nao deveria acontecer com a versao corrigida.")
        resposta_usuario = input("Deseja continuar mesmo assim? (s/n): ").lower()
        if resposta_usuario != 's':
            print("Programa encerrado.")
            return
    
    print("\nVerificando colisoes entre triangulos...")
    quantidade_colisoes = contar_colisoes_otimizado(lista_triangulos, lado * 2)
    
    if quantidade_colisoes == 0:
        print(" Nenhuma colisao entre triangulos encontrada")
    else:
        print(f" Encontradas {quantidade_colisoes} colisoes entre triangulos")
    
    print("\nPlotando mapa...")
    ponto_inicial = (0, 0)
    retas_visiveis = None
    if forcar_plotagem_retas or len(lista_triangulos) <= LIMITE_TRIANGULOS_RETAS_AUTO:
        print("Calculando retas visiveis...")
        retas_visiveis = gerar_retas_visibilidade(
            lista_triangulos,
            ponto_inicial,
            ponto_final,
            max_retas=max_retas,
        )
        print(f"Retas visiveis encontradas: {len(retas_visiveis)}")
    else:
        print(
            "Retas visiveis nao calculadas automaticamente para evitar demora "
            f"com {len(lista_triangulos)} triangulos."
        )
        print("Use --plotar-retas para forcar (opcionalmente com --max-retas).")

    plotar_mapa(lista_triangulos, largura, altura, ponto_inicial, ponto_final, retas_visiveis=retas_visiveis)
    
    tempo_total = time.time() - tempo_inicio_total
    print(f"\nTempo total: {tempo_total:.2f} segundos")
    print("Fim do programa.")


if __name__ == "__main__":
    garantir_ambiente_execucao()
    main()
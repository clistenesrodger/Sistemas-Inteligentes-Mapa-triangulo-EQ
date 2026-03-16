"""Ponto de entrada da aplicacao - Versao preparada para muitos triangulos."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import time

from plotter import plotar_mapa
from triangle_generator import gerar_triangulos_sem_colisao
from geometry import ponto_no_triangulo, triangulos_colidem

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
BOOTSTRAP_FLAG = "MAPA_TRIANGULOS_BOOTSTRAPPED"

def _venv_python_executable():
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"

def _esta_em_venv():
    return (getattr(sys, "base_prefix", sys.prefix) != sys.prefix) or hasattr(sys, "real_prefix")

def _instalar_dependencias(python_executable):
    print("Instalando dependencias...")
    subprocess.check_call([str(python_executable), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)])

def _dependencias_instaladas():
    try:
        import matplotlib
        return True
    except ModuleNotFoundError:
        return False

def garantir_ambiente_execucao():
    if os.environ.get(BOOTSTRAP_FLAG) == "1":
        return

    python_venv = _venv_python_executable()

    if not _esta_em_venv():
        if not python_venv.exists():
            print("Criando ambiente virtual...")
            subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])

        _instalar_dependencias(python_venv)

        env = os.environ.copy()
        env[BOOTSTRAP_FLAG] = "1"
        subprocess.check_call([str(python_venv), str(Path(__file__).resolve()), *sys.argv[1:]], env=env)
        sys.exit(0)

    if not _dependencias_instaladas():
        _instalar_dependencias(sys.executable)

def validar_parametros(largura, altura, qtd, lado, xf, yf):
    """Valida se os parametros fazem sentido."""
    if largura <= 0 or altura <= 0:
        raise ValueError("Largura e altura devem ser positivos")
    if qtd <= 0:
        raise ValueError("Quantidade de triangulos deve ser positiva")
    if lado <= 0:
        raise ValueError("Lado do triangulo deve ser positivo")
    if xf < 0 or xf > largura or yf < 0 or yf > altura:
        raise ValueError("Ponto final deve estar dentro do mapa")
    
    # Calcula area maxima teorica
    from geometry import altura_triangulo
    h = altura_triangulo(lado)
    area_triangulo = (lado * h) / 2
    area_mapa = largura * altura
    
    if area_triangulo * qtd > area_mapa * 2:
        print(f"\n--- ATENCAO ---")
        print(f"Area total dos triangulos: {area_triangulo * qtd:.2f}")
        print(f"Area do mapa: {area_mapa:.2f}")
        print(f"Relacao area triangulos/area mapa: {(area_triangulo * qtd / area_mapa):.2f}")
        print("Isso pode ser impossivel de gerar. Continuando mesmo assim...")
        print("---------------\n")
        return False
    return True

def verificar_ponto_final(fim, triangulos):
    """Verifica se o ponto final esta em local seguro."""
    for i, tri in enumerate(triangulos):
        if ponto_no_triangulo(fim, tri):
            print(f"\n--- ERRO: PONTO FINAL DENTRO DO TRIANGULO {i} ---")
            print(f"Ponto final ({fim[0]:.2f}, {fim[1]:.2f}) esta dentro de um obstaculo!")
            return False
    print("✓ Ponto final esta em area livre")
    return True

def ler_parametros():
    parser = argparse.ArgumentParser(description="Gerador de mapas com obstaculos triangulares")
    parser.add_argument("--largura", type=float, help="Largura do mapa")
    parser.add_argument("--altura", type=float, help="Altura do mapa")
    parser.add_argument("--qtd", type=int, help="Quantidade de triangulos")
    parser.add_argument("--lado", type=float, help="Tamanho do lado do triangulo")
    parser.add_argument("--xf", type=float, help="Coordenada X do ponto final")
    parser.add_argument("--yf", type=float, help="Coordenada Y do ponto final")
    args = parser.parse_args()

    campos = [args.largura, args.altura, args.qtd, args.lado, args.xf, args.yf]

    if all(v is not None for v in campos):
        validar_parametros(args.largura, args.altura, args.qtd, args.lado, args.xf, args.yf)
        return (args.largura, args.altura, args.qtd, args.lado, args.xf, args.yf)

    if any(v is not None for v in campos):
        parser.error("Informe todos os parametros ou nenhum deles.")

    print("\n=== GERADOR DE MAPAS TRIANGULARES ===\n")
    largura = float(input("Largura do mapa: "))
    altura = float(input("Altura do mapa: "))
    qtd = int(input("Quantidade de triangulos: "))
    lado = float(input("Tamanho do lado do triangulo: "))
    xf = float(input("Coordenada X do ponto final: "))
    yf = float(input("Coordenada Y do ponto final: "))
    
    validar_parametros(largura, altura, qtd, lado, xf, yf)
    return largura, altura, qtd, lado, xf, yf

def main():
    print("\n" + "="*50)
    print("GERADOR DE MAPAS COM TRIANGULOS")
    print("="*50 + "\n")
    
    inicio_total = time.time()
    
    # Le parametros
    largura, altura, qtd, lado, xf, yf = ler_parametros()
    ponto_final = (xf, yf)
    
    print(f"\nConfiguracao:")
    print(f"- Mapa: {largura} x {altura}")
    print(f"- Triangulos: {qtd} (lado {lado})")
    print(f"- Ponto final: ({xf}, {yf})")
    
    # Gera triangulos (ja passando o ponto final para garantir que fique livre)
    print("\nGerando triangulos sem colisao...")
    inicio_geracao = time.time()
    triangulos = gerar_triangulos_sem_colisao(qtd, lado, largura, altura, ponto_final)
    tempo_geracao = time.time() - inicio_geracao
    
    print(f"Geracao concluida em {tempo_geracao:.2f} segundos")
    print(f"Triangulos gerados: {len(triangulos)}")
    
    # Verifica ponto final (dupla verificacao)
    print("\nVerificando seguranca do ponto final...")
    ponto_seguro = verificar_ponto_final(ponto_final, triangulos)
    
    if not ponto_seguro:
        print("\n!!! CRITICO: Ponto final esta dentro de um obstaculo !!!")
        print("Isso nao deveria acontecer com a versao corrigida.")
        print("Verifique se usou o triangle_generator.py atualizado.")
        resposta = input("Deseja continuar mesmo assim? (s/n): ").lower()
        if resposta != 's':
            print("Programa encerrado.")
            return
    
    # Verifica colisoes entre triangulos
    print("\nVerificando colisoes entre triangulos...")
    colisoes = 0
    for i in range(len(triangulos)):
        for j in range(i+1, len(triangulos)):
            if triangulos_colidem(triangulos[i], triangulos[j]):
                colisoes += 1
                print(f"Colisao entre triangulo {i} e {j}")
    
    if colisoes == 0:
        print("✓ Nenhuma colisao entre triangulos encontrada")
    else:
        print(f"✗ Encontradas {colisoes} colisoes entre triangulos")
    
    # Plota
    print("\nPlotando mapa...")
    inicio = (0, 0)
    plotar_mapa(triangulos, largura, altura, inicio, ponto_final)
    
    tempo_total = time.time() - inicio_total
    print(f"\nTempo total: {tempo_total:.2f} segundos")
    print("Fim do programa.")

if __name__ == "__main__":
    garantir_ambiente_execucao()
    main()
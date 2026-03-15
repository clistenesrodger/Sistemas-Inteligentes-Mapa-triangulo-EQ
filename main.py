"""Ponto de entrada da aplicacao de geracao e plotagem do mapa triangular."""

import argparse
import os
from pathlib import Path
import subprocess
import sys

from plotter import plotar_mapa
from triangle_generator import gerar_triangulos_sem_colisao

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
BOOTSTRAP_FLAG = "MAPA_TRIANGULOS_BOOTSTRAPPED"


def _venv_python_executable():
    """Retorna o caminho do executavel Python dentro do venv do projeto.

    O caminho varia por sistema operacional:
    - Windows: .venv/Scripts/python.exe
    - Unix-like: .venv/bin/python

    Returns:
        Path: caminho absoluto esperado para o interpretador do venv local.
    """
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def _esta_em_venv():
    """Indica se o processo Python atual esta executando em ambiente virtual.

    Returns:
        bool: True quando o interpretador atual pertence a um venv, False caso contrario.
    """
    return (getattr(sys, "base_prefix", sys.prefix) != sys.prefix) or hasattr(sys, "real_prefix")


def _instalar_dependencias(python_executable):
    """Instala as dependencias declaradas do projeto via pip.

    Args:
        python_executable (str | Path): interpretador Python que executara o pip.

    Raises:
        subprocess.CalledProcessError: se a instalacao falhar.
    """
    subprocess.check_call([str(python_executable), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)])


def _dependencias_instaladas():
    """Verifica se os modulos minimos para execucao ja estao instalados.

    Atualmente valida a presenca do matplotlib, utilizado para plotagem do mapa.

    Returns:
        bool: True quando as dependencias obrigatorias estao disponiveis.
    """
    try:
        import matplotlib  # noqa: F401
    except ModuleNotFoundError:
        return False
    return True


def garantir_ambiente_execucao():
    """Garante venv local e dependencias instaladas antes da execucao.

    Comportamento:
    1. Se o script estiver fora de venv, cria `.venv` (quando necessario), instala
       dependencias e relanca o proprio programa usando o Python do venv.
    2. Se ja estiver em venv, apenas garante dependencias instaladas.
    3. Usa uma flag de ambiente para evitar relancamentos em loop.

    Raises:
        subprocess.CalledProcessError: se criacao de venv, instalacao ou relancamento falhar.
    """
    if os.environ.get(BOOTSTRAP_FLAG) == "1":
        return

    python_venv = _venv_python_executable()

    if not _esta_em_venv():
        if not python_venv.exists():
            subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])

        _instalar_dependencias(python_venv)

        env = os.environ.copy()
        env[BOOTSTRAP_FLAG] = "1"
        subprocess.check_call([str(python_venv), str(Path(__file__).resolve()), *sys.argv[1:]], env=env)
        sys.exit(0)

    if not _dependencias_instaladas():
        _instalar_dependencias(sys.executable)


def ler_parametros():
    """Le parametros de entrada por linha de comando ou modo interativo.

    Regras:
    - Se todos os parametros forem informados na CLI, usa-os diretamente.
    - Se nenhum parametro for informado, solicita tudo no terminal.
    - Se apenas parte for informada, encerra com erro de validacao.

    Returns:
        tuple[float, float, int, float, float, float]:
            largura do mapa, altura do mapa, quantidade de triangulos,
            lado do triangulo equilatero, coordenada x do ponto final e
            coordenada y do ponto final.

    Raises:
        SystemExit: quando a validacao dos argumentos da CLI falha.
        ValueError: quando alguma entrada interativa nao pode ser convertida.
    """
    parser = argparse.ArgumentParser(
        description="Gera um único mapa com obstáculos triangulares."
    )
    parser.add_argument("--largura", type=float)
    parser.add_argument("--altura", type=float)
    parser.add_argument("--qtd", type=int, help="Quantidade de triângulos")
    parser.add_argument("--lado", type=float, help="Tamanho do lado do triângulo")
    parser.add_argument("--xf", type=float, help="Coordenada X do ponto final")
    parser.add_argument("--yf", type=float, help="Coordenada Y do ponto final")
    args = parser.parse_args()

    campos = [args.largura, args.altura, args.qtd, args.lado, args.xf, args.yf]

    if all(v is not None for v in campos):
        return (
            args.largura,
            args.altura,
            args.qtd,
            args.lado,
            args.xf,
            args.yf,
        )

    if any(v is not None for v in campos):
        parser.error("Informe todos os parâmetros (--largura, --altura, --qtd, --lado, --xf, --yf) ou nenhum deles.")

    largura = float(input("Largura do mapa: "))
    altura = float(input("Altura do mapa: "))
    qtd = int(input("Quantidade de triângulos: "))
    lado = float(input("Tamanho do lado do triângulo: "))
    xf = float(input("Coordenada X do ponto final: "))
    yf = float(input("Coordenada Y do ponto final: "))
    return largura, altura, qtd, lado, xf, yf


def main():
    """Executa o fluxo principal do programa.

    Etapas:
    1. Leitura e validacao de parametros.
    2. Definicao dos pontos inicial e final.
    3. Geracao do conjunto de triangulos sem colisao.
    4. Plotagem do mapa resultante.
    """
    largura, altura, qtd, lado, xf, yf = ler_parametros()

    inicio = (0, 0)
    fim = (xf, yf)

    triangulos = gerar_triangulos_sem_colisao(qtd, lado, largura, altura)
    plotar_mapa(triangulos, largura, altura, inicio, fim)


if __name__ == "__main__":
    garantir_ambiente_execucao()
    main()
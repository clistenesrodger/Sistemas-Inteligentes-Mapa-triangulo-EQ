import argparse
from plotter import plotar_mapa
from triangle_generator import gerar_triangulos_sem_colisao


def ler_parametros():
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
    largura, altura, qtd, lado, xf, yf = ler_parametros()

    inicio = (0, 0)
    fim = (xf, yf)

    triangulos = gerar_triangulos_sem_colisao(qtd, lado, largura, altura)
    plotar_mapa(triangulos, largura, altura, inicio, fim)


if __name__ == "__main__":
    main()
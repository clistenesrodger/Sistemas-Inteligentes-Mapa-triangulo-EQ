# Mapa de Triangulos Equilateros

## 1. Descricao

Este projeto gera um mapa bidimensional com obstaculos no formato de triangulos
equilateros, garantindo que os triangulos nao colidam entre si. O resultado e
plotado em grafico com os pontos de inicio e fim marcados.

## 2. Como executar

### 2.1 Execucao simples (recomendada)

Na raiz do projeto, execute:

```bash
python main.py
```

O programa foi preparado para:

- criar automaticamente o ambiente virtual `.venv` (se nao existir);
- instalar automaticamente as dependencias de `requirements.txt`;
- relancar o script dentro do ambiente virtual.

Depois disso, ele pedira os valores no terminal.

### 2.2 Execucao com parametros

Voce tambem pode executar informando tudo pela linha de comando:

```bash
python main.py --largura 30 --altura 30 --qtd 8 --lado 3 --xf 28 --yf 28
```

Parametros:

- `--largura`: largura do mapa.
- `--altura`: altura do mapa.
- `--qtd`: quantidade de triangulos.
- `--lado`: tamanho do lado do triangulo equilatero.
- `--xf`: coordenada X do ponto final.
- `--yf`: coordenada Y do ponto final.

Se voce informar apenas parte dos parametros, o programa encerra com erro de
validacao.

## 3. Saida do programa

- Em ambiente com backend grafico interativo, o mapa e exibido na tela.
- Em ambiente sem backend interativo, a figura e salva em:

```text
mapa_triangulos.png
```

## 4. Dependencias

As dependencias do projeto estao em `requirements.txt`.

Instalacao manual (opcional):

```bash
python -m pip install -r requirements.txt
```

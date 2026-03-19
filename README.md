# Gerador de Mapas com Triângulos

## Sobre o projeto

Este projeto gera mapas 2D com obstáculos em formato de triângulos equiláteros, evitando colisão entre eles e validando o ponto final informado.

Principais características:
- Suporte a grandes volumes (ex.: 300+ triângulos)
- Geração automática sem sobreposição
- Validação dos parâmetros de entrada
- Aviso quando a configuração tende a ser inviável

## Requisitos

- Python 3.10+ (recomendado)
- Dependências listadas em `requirements.txt`

## Como executar

O script principal é o `main.py`. Ele já prepara ambiente virtual e instala dependências automaticamente quando necessário.

### 1. Modo interativo (sem parâmetros)

Execute:

```bash
python main.py
```

Depois disso, o programa vai solicitar os valores no terminal:
- largura do mapa
- altura do mapa
- quantidade de triângulos
- tamanho do lado do triângulo
- coordenadas `x` e `y` do ponto final

### 2. Modo por parâmetros (linha de comando)

Você pode passar todos os valores diretamente no comando.

Exemplo:

```bash
python main.py --largura 500 --altura 500 --qtd 300 --lado 20 --xf 450 --yf 450
```

Parâmetros disponíveis:
- `--largura`: largura do mapa (float)
- `--altura`: altura do mapa (float)
- `--qtd`: quantidade de triângulos (int)
- `--lado`: tamanho do lado do triângulo (float)
- `--xf`: coordenada X do ponto final (float)
- `--yf`: coordenada Y do ponto final (float)
- `--plotar-retas`: força o cálculo e plotagem das retas de visibilidade
- `--max-retas`: limita o número máximo de retas de visibilidade (padrão: `12000`)

Observação importante:
- Informe **todos os parâmetros** ou **nenhum**. Se você passar só parte deles, o programa retorna erro.

## Parâmetros avançados de performance

Para mapas grandes, o projeto aplica otimizações automaticamente para evitar demora excessiva:

- O cálculo de retas de visibilidade é pulado automaticamente quando há muitos triângulos.
- Você pode forçar esse cálculo com `--plotar-retas`.
- Para controlar o custo, use `--max-retas`.

Exemplo forçando retas com limite:

```bash
python main.py --largura 1000 --altura 1000 --qtd 1000 --lado 20 --xf 900 --yf 900 --plotar-retas --max-retas 3000
```

Exemplo recomendado para execução mais rápida em mapas grandes:

```bash
python main.py --largura 1000 --altura 1000 --qtd 1000 --lado 20 --xf 900 --yf 900
```

## Exemplo completo

```bash
python main.py --largura 800 --altura 600 --qtd 350 --lado 18 --xf 760 --yf 560
```

## Saída esperada

Durante a execução, o programa mostra:
- configuração escolhida
- tempo de geração
- quantidade de triângulos gerados
- validação do ponto final
- checagem de colisões
- quantidade de retas visíveis (quando habilitadas)

Ao final, o mapa é exibido em uma janela com os triângulos, pontos inicial/final e, quando solicitado, as retas de visibilidade.

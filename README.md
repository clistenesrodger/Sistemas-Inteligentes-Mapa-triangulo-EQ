# MapaTriangularEQ: Gerador Inteligente de Mapas com Triângulos

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**Um gerador avançado de mapas 2D com obstáculos triangulares equiláteros e cálculo automático de caminhos de visibilidade, pensado para uso acadêmico no Brasil.**

[Recursos](#-recursos) • [Instalação](#-instalação) • [Uso](#-uso) • [Exemplos](#-exemplos) • [Estrutura](#-estrutura-do-projeto)

</div>

---

## 📋 Sobre o Projeto

**MapaTriangularEQ** é uma ferramenta inteligente que gera mapas 2D com obstáculos em formato de **triângulos equiláteros**, sem colisão entre eles, e calcula automaticamente os **caminhos de visibilidade** entre pontos no mapa. É ideal para:

- 🎮 Desenvolvimento de sistemas de pathfinding em jogos
- 🤖 Planejamento de movimento em robótica
- 📊 Estudos de algoritmos de visibilidade e geometria computacional
- 🧠 Pesquisa em sistemas inteligentes e inteligência artificial

## ✨ Recursos

- ✅ **Geração automática de mapas** com 300+ triângulos sem sobreposição
- ✅ **Cálculo de grafo de visibilidade** otimizado para grandes volumes
- ✅ **Validação inteligente** de parâmetros e configurações inviáveis
- ✅ **Modo interativo e linha de comando** para máxima flexibilidade
- ✅ **Visualização gráfica** automática dos resultados
- ✅ **Ambiente virtual autoconfigurado** - nenhuma instalação manual necessária
- ✅ **Suporte multiplataforma** (Windows, macOS, Linux)

## 🛠️ Requisitos

- **Python 3.10+** (recomendado)
- Dependências: `matplotlib`, `numpy` (instaladas automaticamente)

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/MapaTriangularEQ.git
cd MapaTriangularEQ
```

Nenhuma instalação adicional necessária! O script `main.py` configura tudo automaticamente.

## 🚀 Como Usar

### 1. Modo interativo

Para iniciar o programa em modo interativo:

```bash
python main.py
```

O programa solicitará os seguintes parâmetros:
- **Largura do mapa** (float): dimensão horizontal em unidades
- **Altura do mapa** (float): dimensão vertical em unidades  
- **Quantidade de triângulos** (int): número de obstáculos a gerar
- **Tamanho do lado** (float): comprimento dos lados do triângulo equilátero
- **Coordenada X final** (float): posição X do ponto de destino
- **Coordenada Y final** (float): posição Y do ponto de destino

Exemplo de entrada:
```
Largura do mapa: 500
Altura do mapa: 500
Quantidade de triângulos: 50
Tamanho do lado: 20
Ponto final X: 450
Ponto final Y: 450
```

### 2. Modo linha de comando

Para automatizar ou usar em scripts, passe todos os parâmetros na linha de comando:

```bash
python main.py --largura 500 --altura 500 --qtd 300 --lado 20 --xf 450 --yf 450
```

**Parâmetros disponíveis:**

| Parâmetro | Tipo | Descrição | Exemplo |
|-----------|------|-----------|---------|
| `--largura` | float | Largura do mapa | `500` |
| `--altura` | float | Altura do mapa | `500` |
| `--qtd` | int | Quantidade de triângulos | `300` |
| `--lado` | float | Tamanho do lado do triângulo | `20` |
| `--xf` | float | Coordenada X do ponto final | `450` |
| `--yf` | float | Coordenada Y do ponto final | `450` |
| `--plotar-retas` | flag | Força plotagem das retas de visibilidade | — |
| `--max-retas` | int | Limite máximo de retas (padrão: 12000) | `5000` |

> ⚠️ **Importante:** Informe **todos os parâmetros** ou **nenhum**. Se passar apenas alguns, o programa retornará erro.

## 💡 Exemplos Práticos

### Exemplo 1: mapa pequeno
```bash
python main.py --largura 500 --altura 500 --qtd 50 --lado 20 --xf 450 --yf 450
```

### Exemplo 2: mapa grande com otimização
```bash
python main.py --largura 1000 --altura 1000 --qtd 300 --lado 25 --xf 950 --yf 950
```

### Exemplo 3: mapa complexo com retas de visibilidade
```bash
python main.py --largura 800 --altura 600 --qtd 100 --lado 18 --xf 760 --yf 560 --plotar-retas --max-retas 5000
```

## 🎯 Saída do Programa

Durante a execução, o programa exibe:
- ✔️ Configuração validada
- ✔️ Tempo de geração dos triângulos
- ✔️ Quantidade total de triângulos gerados
- ✔️ Validação do ponto final (dentro/fora de obstáculos)
- ✔️ Análise de colisões
- ✔️ Quantidade de retas de visibilidade calculadas

**Ao final:** Uma janela gráfica exibindo:
- 🔺 Todos os triângulos (obstáculos)
- 🔴 Ponto inicial (origem)
- 🟢 Ponto final (destino)
- 📍 Retas de visibilidade (quando habilitadas)

## 🔧 Otimizações Inteligentes

O sistema aplica otimizações automáticas para mapas grandes:

| Cenário | Comportamento |
|---------|---------------|
| Triângulos < 250 | Calcula retas automaticamente |
| Triângulos ≥ 250 | Pula cálculo de retas para ganhar velocidade |
| Com `--plotar-retas` | Força o cálculo mesmo em mapas grandes |
| Com `--max-retas N` | Limita o custo computacional |

## 📁 Estrutura do Projeto

```
TriangleMaze/
├── main.py                  # Ponto de entrada principal
├── triangle_generator.py    # Geração de triângulos e retas
├── geometry.py              # Funções geométricas de colisão
├── visibility_graph.py      # Cálculo de grafo de visibilidade
├── plotter.py               # Visualização gráfica
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 🧮 Algoritmos Utilizados

- **Detecção de colisão:** teste ponto-em-triângulo e intersecção triângulo-triângulo
- **Grafo de visibilidade:** construção otimizada com verificação de bloqueios por obstáculos
- **Pathfinding:** cálculo de caminho direto entre origem e destino
- **Geometria computacional:** cálculos de distância, interseção de segmentos e validação

## 📊 Desempenho

| Volume | Tempo Aprox | Recursos |
|--------|-------------|----------|
| 50 triângulos | < 1s | Mínimo |
| 150 triângulos | 1-3s | Baixo |
| 300 triângulos | 5-10s | Médio |
| 500+ triângulos | 15-30s | Alto |

*Os tempos variam conforme o hardware e as configurações do mapa.*

## 🐛 Solução de Problemas

### Problema: "ModuleNotFoundError: No module named 'matplotlib'"
**Solução:** Execute novamente o programa. O ambiente virtual será recriado e as dependências reinstaladas.

```bash
python main.py
```

### Problema: o programa está muito lento
**Solução:** O cálculo de retas de visibilidade em mapas grandes é custoso. Opções:

1. Reduza a quantidade de triângulos
2. Remova a flag `--plotar-retas`
3. Aumente `--max-retas` para limitar o processamento

### Problema: o ponto final está dentro de um obstáculo
**Solução:** O programa alertará se isso ocorrer. Escolha um ponto final diferente ou ajuste os parâmetros.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Otimizações de desempenho
- Novos tipos de obstáculos

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato e Suporte

Para dúvidas, sugestões ou relatórios de bugs, abra uma issue no repositório.

---

<div align="center">

**Desenvolvido no Brasil com ❤️ para pesquisa em Sistemas Inteligentes**

⭐ Se este projeto foi útil para você, considere deixar uma estrela!

</div>

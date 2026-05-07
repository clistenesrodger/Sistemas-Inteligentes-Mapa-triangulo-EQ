# Contribuindo para TriangleMaze

Obrigado por considerar contribuir para o **TriangleMaze**! Contribuições são o que tornam este projeto melhor.

## 🎯 Como Contribuir

### Reportando Bugs

Antes de criar um relatório de bug, verifique se o problema já foi reportado. Se encontrar seu bug, aumente o tópico adicionando um comentário.

Quando cria um novo relatório de bug, inclua:

- **Descrição clara**: explique qual é o problema
- **Passos reproduzíveis**: liste as etapas exatas que reproduzem o problema
- **Exemplos específicos**: forneça exemplos específicos para demonstrar os passos
- **Ambiente**: inclua seu sistema operacional, versão Python, etc.

### Sugestões de Melhoria

Sugestões de melhoria são sempre bem-vindas! Ao criar uma sugestão, inclua:

- **Uma descrição clara** da melhoria proposta
- **Exemplos de código** se aplicável
- **Referências** a problemas relacionados

### Pull Requests

- Siga o estilo de código do projeto (PEP 8)
- Atualize a documentação conforme necessário
- Adicione testes se possível
- Mantenha o histórico de commits limpo

## 📋 Processo de Desenvolvimento

1. **Fork** o repositório
2. **Clone** seu fork: `git clone https://github.com/seu-usuario/TriangleMaze.git`
3. **Crie uma branch** para sua feature: `git checkout -b feature/descricao`
4. **Faça suas mudanças** e **commit**: `git commit -m "Descrição clara da mudança"`
5. **Push** para sua branch: `git push origin feature/descricao`
6. **Abra um Pull Request** descrevendo suas mudanças

## 🐍 Padrões de Código

- Seguir **PEP 8** (Python)
- Usar nomes descritivos para variáveis e funções
- Adicionar docstrings em funções e classes
- Manter comentários claros e úteis

### Exemplo de Docstring

```python
def calcular_distancia(ponto_a, ponto_b):
    """Calcula a distância euclidiana entre dois pontos.
    
    Args:
        ponto_a (tuple): Ponto inicial (x, y)
        ponto_b (tuple): Ponto final (x, y)
    
    Returns:
        float: Distância entre os pontos
    """
    dx = ponto_b[0] - ponto_a[0]
    dy = ponto_b[1] - ponto_a[1]
    return (dx**2 + dy**2) ** 0.5
```

## 🧪 Testando Mudanças

Antes de submeter um PR:

```bash
# Clone ou atualize seu ambiente
python main.py --largura 500 --altura 500 --qtd 50 --lado 20 --xf 450 --yf 450

# Teste com diferentes configurações
python main.py --largura 1000 --altura 1000 --qtd 300 --lado 25 --xf 950 --yf 950
```

## 📝 Commit Messages

Use commit messages descritivas:

✅ **Bom:**
```
Adiciona validação de ponto final no mapa

- Verifica se o ponto está dentro dos limites
- Alerta se ponto está sobre obstáculo
- Melhora performance em mapas grandes
```

❌ **Ruim:**
```
Fix bug
Atualiza código
```

## 🤝 Diretrizes Gerais

- Seja respeitoso e construtivo
- Foque na solução, não em críticas pessoais
- Aceite críticas de boa fé
- Dê crédito ao trabalho dos outros

## 📞 Dúvidas?

Abra uma **Issue** com sua dúvida e use a label `question`.

---

Obrigado por contribuir! 🙏

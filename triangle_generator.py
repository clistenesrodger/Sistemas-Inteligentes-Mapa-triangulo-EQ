"""Geracao de triangulos sem colisao com otimizacao para muitos triangulos."""

import random # Usada para gerar posições aleatórias dos triângulos
import math

# Funções de geometria para verificar colisões e calcular distâncias
from geometry import altura_triangulo, triangulos_colidem, distancia_segmentos, ponto_no_triangulo

# Esta classe encapsula todo o estado e lógica necessários para gerar triângulos
class GeradorTriangulos:
    """Classe que gerencia a geracao de triangulos com otimizacoes."""
    
    # O construtor serve para inicializar os parâmetros do gerador, como o tamanho do lado dos triângulos, as dimensões do mapa, a altura dos triângulos (calculada a partir do lado) e uma margem visual para considerar quando os triângulos estão muito próximos. Ele também recebe um ponto final opcional que deve permanecer livre de obstáculos.
    def __init__(self, lado_triangulo, largura_mapa, altura_mapa, ponto_final_obrigatorio=None):
        self.lado = lado_triangulo
        self.largura = largura_mapa
        self.altura = altura_mapa
        self.altura_tri = altura_triangulo(lado_triangulo)
        self.margem_visual = max(1e-6, lado_triangulo * 0.1)  # Margem para considerar proximidade
        self.celula_tamanho = lado_triangulo * 2
        self.ponto_final = ponto_final_obrigatorio  # Ponto que deve ficar livre
    
    # Mede o tamanho dos triângulos para garantir que eles caibam dentro do mapa
    def bbox_triangulo(self, triangulo):
        """Retorna bounding box (xmin, ymin, xmax, ymax) do triangulo."""
        coordenadas_x = [vertice[0] for vertice in triangulo]
        coordenadas_y = [vertice[1] for vertice in triangulo]
        # Retorna os limites da bounding box do triângulo, que é usada para uma verificação rápida de segurança antes de realizar testes geométricos mais complexos
        return (min(coordenadas_x), min(coordenadas_y), max(coordenadas_x), max(coordenadas_y))
    
    # Esta função calcula a distância mínima entre duas bounding boxes
    def bbox_distancia(self, bounding_box1, bounding_box2):
        """Distancia minima entre duas bounding boxes."""
        # bounding_box = (xmin, ymin, xmax, ymax)
        xmin1, ymin1, xmax1, ymax1 = bounding_box1
        xmin2, ymin2, xmax2, ymax2 = bounding_box2
        
        # Se as bboxes não se sobrepõem, a distância é zero
        if not (xmax1 < xmin2 or xmax2 < xmin1 or ymax1 < ymin2 or ymax2 < ymin1):
            return 0.0  # As caixas se sobrepõem
        
        # Calcula a distância mínima entre as bboxes
        distancia_x = 0.0
        if xmax1 < xmin2:  # bbox1 está à esquerda
            distancia_x = xmin2 - xmax1
        elif xmax2 < xmin1:  # bbox2 está à esquerda
            distancia_x = xmin1 - xmax2
        
        # A distância vertical é calculada de forma similar
        distancia_y = 0.0
        if ymax1 < ymin2:  # bbox1 está abaixo
            distancia_y = ymin2 - ymax1
        elif ymax2 < ymin1:  # bbox2 está abaixo
            distancia_y = ymin1 - ymax2
        
        return math.sqrt(distancia_x*distancia_x + distancia_y*distancia_y)
    
    def triangulos_sao_seguros(self, triangulo1, triangulo2, bbox1=None, bbox2=None):
        """Verifica se dois triangulos sao seguros (nao colidem e nao estao muito proximos)."""
        if bbox1 is None:
            bbox1 = self.bbox_triangulo(triangulo1)
        if bbox2 is None:
            bbox2 = self.bbox_triangulo(triangulo2)
        
        # Se as bboxes estao longe, nem testa geometria
        if self.bbox_distancia(bbox1, bbox2) > self.margem_visual:
            return True  # Seguro: estão longe demais para colidir
        
        # Teste de colisao
        if triangulos_colidem(triangulo1, triangulo2):
            return False  # Não seguro: colidem
        
        # Teste de distancia entre arestas
        arestas1 = [(triangulo1[i], triangulo1[(i + 1) % 3]) for i in range(3)]
        arestas2 = [(triangulo2[i], triangulo2[(i + 1) % 3]) for i in range(3)]
        
        for aresta1 in arestas1:
            for aresta2 in arestas2:
                if distancia_segmentos(aresta1[0], aresta1[1], aresta2[0], aresta2[1]) < self.margem_visual:
                    return False  # Não seguro: arestas muito próximas
        return True  # Seguro: passou em todos os testes
    
    def gerar_triangulo_aleatorio(self):
        """Gera um triangulo aleatorio dentro dos limites do mapa."""
        if self.lado > self.largura or self.altura_tri > self.altura:
            return None  # Triângulo não cabe no mapa
        
        posicao_x = random.uniform(0, self.largura - self.lado)
        posicao_y = random.uniform(0, self.altura - self.altura_tri)
        
        # Retorna os 3 vértices do triângulo equilátero (base horizontal)
        return [(posicao_x, posicao_y),                              # Vértice inferior esquerdo
                (posicao_x + self.lado, posicao_y),                  # Vértice inferior direito
                (posicao_x + self.lado / 2, posicao_y + self.altura_tri)]  # Vértice superior
    
    def calcular_tentativas_necessarias(self, quantidade_desejada):
        """Calcula numero de tentativas baseado na ocupacao do mapa."""
        area_mapa = self.largura * self.altura
        area_triangulo = (self.lado * self.altura_tri) / 2
        area_estimada = area_triangulo * quantidade_desejada * 1.5  # Fator de segurança 1.5x
        
        if area_estimada > area_mapa * 0.8:  # Mapa muito cheio (>80% ocupado)
            return quantidade_desejada * 500  # Muitas tentativas
        elif area_estimada > area_mapa * 0.5:  # Mapa médio (50-80% ocupado)
            return quantidade_desejada * 200   # Tentativas médias
        else:  # Mapa folgado (<50% ocupado)
            return quantidade_desejada * 50    # Poucas tentativas
    
    def gerar_muitos_triangulos(self, quantidade_desejada):
        """Gera muitos triangulos sem colisao usando otimizacoes."""
        tentativas_maximas = self.calcular_tentativas_necessarias(quantidade_desejada)
        
        lista_triangulos = []      # Lista dos triângulos gerados com sucesso
        lista_bounding_boxes = []  # Lista das bounding boxes (mesmo índice dos triângulos)
        grade_espacial = {}         # Dicionário: célula → lista de índices dos triângulos naquela célula
        
        tentativas_realizadas = 0
        
        # Continua tentando até atingir a quantidade desejada ou esgotar as tentativas
        while len(lista_triangulos) < quantidade_desejada and tentativas_realizadas < tentativas_maximas:
            novo_triangulo = self.gerar_triangulo_aleatorio()
            tentativas_realizadas += 1
            
            if novo_triangulo is None:
                continue  # Não cabe no mapa, tenta outro
            
            # VERIFICACAO IMPORTANTE: ponto final nao pode estar dentro deste triangulo
            if self.ponto_final is not None:
                if ponto_no_triangulo(self.ponto_final, novo_triangulo):
                    continue  # Este triangulo cobriria o ponto final, descarta
            
            # Calcula célula do grid baseada no centro do triângulo
            centro_x = (novo_triangulo[0][0] + novo_triangulo[1][0] + novo_triangulo[2][0]) / 3
            centro_y = (novo_triangulo[0][1] + novo_triangulo[1][1] + novo_triangulo[2][1]) / 3
            celula_x = int(centro_x / self.celula_tamanho)
            celula_y = int(centro_y / self.celula_tamanho)
            celula_atual = (celula_x, celula_y)
            
            # Calcula bounding box do novo triângulo
            bbox_novo = self.bbox_triangulo(novo_triangulo)
            triangulo_seguro = True
            
            # Verifica apenas células vizinhas (incluindo a própria)
            for deslocamento_x in [-1, 0, 1]:
                for deslocamento_y in [-1, 0, 1]:
                    celula_vizinha = (celula_x + deslocamento_x, celula_y + deslocamento_y)
                    
                    # Se há triângulos nesta célula vizinha
                    if celula_vizinha in grade_espacial:
                        for indice_triangulo_existente in grade_espacial[celula_vizinha]:
                            # Verifica se o novo triângulo é seguro com este existente
                            if not self.triangulos_sao_seguros(
                                novo_triangulo, 
                                lista_triangulos[indice_triangulo_existente],
                                bbox_novo, 
                                lista_bounding_boxes[indice_triangulo_existente]
                            ):
                                triangulo_seguro = False
                                break
                    if not triangulo_seguro:
                        break
                if not triangulo_seguro:
                    break
            
            # Se passou em todas as verificações, adiciona o triângulo
            if triangulo_seguro:
                indice_novo = len(lista_triangulos)
                lista_triangulos.append(novo_triangulo)
                lista_bounding_boxes.append(bbox_novo)
                
                # Atualiza a grade espacial
                if celula_atual not in grade_espacial:
                    grade_espacial[celula_atual] = []
                grade_espacial[celula_atual].append(indice_novo)
        
        return lista_triangulos, tentativas_realizadas


def gerar_triangulos_sem_colisao(quantidade, lado, largura, altura, ponto_final=None):
    """Interface principal para gerar triangulos sem colisao.
    
    Args:
        quantidade: quantidade de triangulos desejada
        lado: tamanho do lado dos triangulos
        largura: largura do mapa
        altura: altura do mapa
        ponto_final: tupla (x, y) do ponto que deve ficar livre (opcional)
    """
    # Cria uma instância do gerador com os parâmetros fornecidos
    gerador = GeradorTriangulos(lado, largura, altura, ponto_final)
    
    # Gera os triângulos
    triangulos_gerados, tentativas_usadas = gerador.gerar_muitos_triangulos(quantidade)
    
    # Aviso se não conseguiu gerar todos os triângulos desejados
    if len(triangulos_gerados) < quantidade:
        print(f"\n--- AVISO IMPORTANTE ---")
        print(f"Foram gerados {len(triangulos_gerados)} de {quantidade} triangulos")
        print(f"Tentativas realizadas: {tentativas_usadas}")
        print(f"Motivo: O mapa pode estar muito cheio para {quantidade} triangulos de lado {lado}")
        print(f"Sugestao: Aumente o tamanho do mapa ou diminua a quantidade")
        print("------------------------\n")
    
    return triangulos_gerados
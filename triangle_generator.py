"""Geracao de triangulos sem colisao com otimizacao para muitos triangulos."""

import random
import math
from geometry import altura_triangulo, triangulos_colidem, distancia_segmentos, ponto_no_triangulo

class GeradorTriangulos:
    """Classe que gerencia a geracao de triangulos com otimizacoes."""
    
    def __init__(self, lado, largura, altura, ponto_final=None):
        self.lado = lado
        self.largura = largura
        self.altura = altura
        self.altura_tri = altura_triangulo(lado)
        self.margem_visual = max(1e-6, lado * 0.1)  # Margem para considerar proximidade
        self.celula_tamanho = lado * 2
        self.ponto_final = ponto_final  # Ponto que deve ficar livre
        
    def bbox_triangulo(self, t):
        """Retorna bounding box (xmin, ymin, xmax, ymax) do triangulo."""
        xs = [p[0] for p in t]
        ys = [p[1] for p in t]
        return (min(xs), min(ys), max(xs), max(ys))
    
    def bbox_distancia(self, bbox1, bbox2):
        """Distancia minima entre duas bounding boxes."""
        if not (bbox1[2] < bbox2[0] or bbox2[2] < bbox1[0] or 
                bbox1[3] < bbox2[1] or bbox2[3] < bbox1[1]):
            return 0.0
        
        dx = 0.0
        if bbox1[2] < bbox2[0]:
            dx = bbox2[0] - bbox1[2]
        elif bbox2[2] < bbox1[0]:
            dx = bbox1[0] - bbox2[2]
        
        dy = 0.0
        if bbox1[3] < bbox2[1]:
            dy = bbox2[1] - bbox1[3]
        elif bbox2[3] < bbox1[1]:
            dy = bbox1[1] - bbox2[3]
        
        return math.sqrt(dx*dx + dy*dy)
    
    def triangulos_sao_seguros(self, t1, t2, bbox1=None, bbox2=None):
        """Verifica se dois triangulos sao seguros (nao colidem e nao estao muito proximos)."""
        if bbox1 is None:
            bbox1 = self.bbox_triangulo(t1)
        if bbox2 is None:
            bbox2 = self.bbox_triangulo(t2)
        
        # Se as bboxes estao longe, nem testa geometria
        if self.bbox_distancia(bbox1, bbox2) > self.margem_visual:
            return True
        
        # Teste de colisao
        if triangulos_colidem(t1, t2):
            return False
        
        # Teste de distancia entre arestas
        edges1 = [(t1[i], t1[(i + 1) % 3]) for i in range(3)]
        edges2 = [(t2[i], t2[(i + 1) % 3]) for i in range(3)]
        
        for e1 in edges1:
            for e2 in edges2:
                if distancia_segmentos(e1[0], e1[1], e2[0], e2[1]) < self.margem_visual:
                    return False
        return True
    
    def gerar_triangulo_aleatorio(self):
        """Gera um triangulo aleatorio dentro dos limites do mapa."""
        if self.lado > self.largura or self.altura_tri > self.altura:
            return None
        
        x = random.uniform(0, self.largura - self.lado)
        y = random.uniform(0, self.altura - self.altura_tri)
        
        return [(x, y), 
                (x + self.lado, y), 
                (x + self.lado / 2, y + self.altura_tri)]
    
    def calcular_tentativas_necessarias(self, qtd):
        """Calcula numero de tentativas baseado na ocupacao do mapa."""
        area_mapa = self.largura * self.altura
        area_triangulo = (self.lado * self.altura_tri) / 2
        area_estimada = area_triangulo * qtd * 1.5
        
        if area_estimada > area_mapa * 0.8:
            return qtd * 500  # Mapa muito cheio, muitas tentativas
        elif area_estimada > area_mapa * 0.5:
            return qtd * 200   # Mapa medio
        else:
            return qtd * 50    # Mapa folgado
    
    def gerar_muitos_triangulos(self, qtd):
        """Gera muitos triangulos sem colisao usando otimizacoes."""
        tentativas_max = self.calcular_tentativas_necessarias(qtd)
        
        triangulos = []
        bboxes = []
        grid = {}  # celula -> lista de indices
        
        tentativas = 0
        while len(triangulos) < qtd and tentativas < tentativas_max:
            novo = self.gerar_triangulo_aleatorio()
            tentativas += 1
            
            if novo is None:
                continue
            
            # VERIFICACAO IMPORTANTE: ponto final nao pode estar dentro deste triangulo
            if self.ponto_final is not None:
                if ponto_no_triangulo(self.ponto_final, novo):
                    continue  # Este triangulo cobriria o ponto final, descarta
            
            # Calcula celula do grid
            centro_x = (novo[0][0] + novo[1][0] + novo[2][0]) / 3
            centro_y = (novo[0][1] + novo[1][1] + novo[2][1]) / 3
            celula_x = int(centro_x / self.celula_tamanho)
            celula_y = int(centro_y / self.celula_tamanho)
            celula = (celula_x, celula_y)
            
            bbox_novo = self.bbox_triangulo(novo)
            seguro = True
            
            # Verifica apenas celulas vizinhas
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    celula_viz = (celula_x + dx, celula_y + dy)
                    if celula_viz in grid:
                        for idx in grid[celula_viz]:
                            if not self.triangulos_sao_seguros(novo, triangulos[idx], 
                                                              bbox_novo, bboxes[idx]):
                                seguro = False
                                break
                    if not seguro:
                        break
                if not seguro:
                    break
            
            if seguro:
                idx = len(triangulos)
                triangulos.append(novo)
                bboxes.append(bbox_novo)
                
                if celula not in grid:
                    grid[celula] = []
                grid[celula].append(idx)
        
        return triangulos, tentativas

def gerar_triangulos_sem_colisao(qtd, lado, largura, altura, ponto_final=None):
    """Interface principal para gerar triangulos sem colisao.
    
    Args:
        qtd: quantidade de triangulos
        lado: tamanho do lado
        largura: largura do mapa
        altura: altura do mapa
        ponto_final: tupla (x, y) do ponto que deve ficar livre (opcional)
    """
    gerador = GeradorTriangulos(lado, largura, altura, ponto_final)
    triangulos, tentativas = gerador.gerar_muitos_triangulos(qtd)
    
    if len(triangulos) < qtd:
        print(f"\n--- AVISO IMPORTANTE ---")
        print(f"Foram gerados {len(triangulos)} de {qtd} triangulos")
        print(f"Tentativas realizadas: {tentativas}")
        print(f"Motivo: O mapa pode estar muito cheio para {qtd} triangulos de lado {lado}")
        print(f"Sugestao: Aumente o tamanho do mapa ou diminua a quantidade")
        print("------------------------\n")
    
    return triangulos
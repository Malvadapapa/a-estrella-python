import heapq

class GrafoCalles:
    def __init__(self, tamaño):
        """
        Inicializa el grafo de calles.
        
        :param tamaño: Tamaño de la matriz cuadrada que representa el grafo.
        :return: No retorna nada.
        """
        self.tamaño = tamaño
        # Crea una matriz donde las calles están representadas por 1 y los edificios por 0
        self.grafo = [[1 if i % 3 == 0 or j % 3 == 0 else 0 for j in range(tamaño)] for i in range(tamaño)]

    def es_valido(self, x, y):
        """
        Verifica si una posición está dentro del grafo y es una calle.
        
        :param x: Coordenada x de la posición.
        :param y: Coordenada y de la posición.
        :return: True si la posición es válida, False en caso contrario.
        """
        return 0 <= x < self.tamaño and 0 <= y < self.tamaño and self.grafo[y][x] == 1

    def obtener_vecinos(self, x, y):
        """
        Obtiene los vecinos válidos de una posición dada.
        
        :param x: Coordenada x de la posición.
        :param y: Coordenada y de la posición.
        :return: Lista de tuplas con las coordenadas de los vecinos válidos.
        """
        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return [(x + dx, y + dy) for dx, dy in direcciones if self.es_valido(x + dx, y + dy)]

def heuristica(a, b):
    """
    Calcula la distancia heurística entre dos puntos (distancia de Chebyshev).
    
    :param a: Tupla con las coordenadas del primer punto.
    :param b: Tupla con las coordenadas del segundo punto.
    :return: Valor de la distancia heurística.
    """
    return max(abs(b[0] - a[0]), abs(b[1] - a[1]))

def a_estrella(grafo, inicio, meta, callback=None):
    """
    Implementación del algoritmo A*.
    
    :param grafo: Instancia de GrafoCalles.
    :param inicio: Tupla con las coordenadas del punto de inicio.
    :param meta: Tupla con las coordenadas del punto de destino.
    :param callback: Función a llamar en cada iteración para actualizar la vista.
    :return: Tupla con el camino encontrado (lista de coordenadas), costo_g y costo_f.
    """
    vecinos = [(0, inicio)]
    vino_de = {}
    costo_g = {inicio: 0}
    costo_f = {inicio: heuristica(inicio, meta)}
    conjunto_cerrado = set()

    while vecinos:
        actual = heapq.heappop(vecinos)[1]

        if actual == meta:
            camino = []
            while actual in vino_de:
                camino.append(actual)
                actual = vino_de[actual]
            camino.append(inicio)
            return camino[::-1], costo_g, costo_f

        conjunto_cerrado.add(actual)

        for vecino in grafo.obtener_vecinos(*actual):
            if vecino in conjunto_cerrado:
                continue

            # Calcula el costo g tentativo
            costo_g_tentativo = costo_g[actual] + (1 if vecino[0] == actual[0] or vecino[1] == actual[1] else 1.4)

            if vecino not in costo_g or costo_g_tentativo < costo_g[vecino]:
                vino_de[vecino] = actual
                costo_g[vecino] = costo_g_tentativo
                costo_f[vecino] = costo_g[vecino] + heuristica(vecino, meta)
                heapq.heappush(vecinos, (costo_f[vecino], vecino))

        if callback:
            callback(conjunto_cerrado, costo_g, costo_f)

    return None, costo_g, costo_f
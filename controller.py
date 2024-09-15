from model import GrafoCalles, a_estrella

class Controlador:
    def __init__(self, vista):
        """
        Inicializa el controlador.
        
        :param vista: Instancia de la vista (InterfazPathfinding).
        :return: No retorna nada.
        """
        self.vista = vista
        self.grafo = None
        self.inicio = None
        self.meta = None
        self.camino_actual = None
        self.costo_g = {}
        self.costo_f = {}

    def generar_matriz(self):
        """
        Genera una nueva matriz basada en el tamaño ingresado por el usuario.
        
        :return: No retorna nada.
        """
        try:
            tamaño = int(self.vista.obtener_tamaño_matriz())
            if tamaño <= 0 or tamaño > 50:
                raise ValueError("El tamaño de la matriz debe estar entre 1 y 50")

            self.grafo = GrafoCalles(tamaño)
            self.vista.actualizar_tamaño_celda(tamaño)
            self.inicio = None
            self.meta = None
            self.camino_actual = None
            self.costo_g = {}
            self.costo_f = {}
            self.vista.actualizar_instrucciones("Haga clic para seleccionar el punto de inicio")
            self.vista.dibujar_grafo(self.grafo, self.inicio, self.meta, self.camino_actual, self.costo_g, self.costo_f)
        except ValueError as e:
            self.vista.actualizar_resultados(str(e))

    def al_hacer_clic_canvas(self, evento):
        """
        Maneja los clics en el canvas para seleccionar inicio y meta.
        
        :param evento: Evento de clic del mouse.
        :return: No retorna nada.
        """
        if not self.grafo:
            return

        x = evento.x // self.vista.tamaño_celda
        y = evento.y // self.vista.tamaño_celda
        if not self.grafo.es_valido(x, y):
            self.vista.actualizar_resultados("Posición no válida. Seleccione una calle (celda blanca).")
            return

        if not self.inicio:
            self.inicio = (x, y)
            self.vista.actualizar_instrucciones("Haga clic para seleccionar el punto final")
        elif not self.meta:
            self.meta = (x, y)
            self.encontrar_camino()
        else:
            self.inicio = (x, y)
            self.meta = None
            self.camino_actual = None
            self.costo_g = {}
            self.costo_f = {}
            self.vista.actualizar_instrucciones("Haga clic para seleccionar el punto final")
        
        self.vista.dibujar_grafo(self.grafo, self.inicio, self.meta, self.camino_actual, self.costo_g, self.costo_f)

    def encontrar_camino(self):
        """
        Ejecuta el algoritmo A* y actualiza la visualización.
        
        :return: No retorna nada.
        """
        camino, self.costo_g, self.costo_f = a_estrella(self.grafo, self.inicio, self.meta)
        if camino:
            self.camino_actual = camino
            self.vista.actualizar_resultados(f"Ruta encontrada. Longitud: {len(camino) - 1}")
            self.vista.dibujar_grafo(self.grafo, self.inicio, self.meta, self.camino_actual, self.costo_g, self.costo_f)
        else:
            self.vista.actualizar_resultados("No se encontró una ruta.")
        self.vista.actualizar_instrucciones("Haga clic para seleccionar un nuevo punto de inicio")
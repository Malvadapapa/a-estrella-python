import tkinter as tk
from tkinter import ttk, Text, Scrollbar
import colorsys

class InterfazPathfinding:
    def __init__(self, maestro, controlador):
        """
        Inicializa la interfaz gráfica del pathfinding.
        
        :param maestro: Ventana principal de Tkinter.
        :param controlador: Instancia del controlador.
        :return: No retorna nada.
        """
        self.maestro = maestro
        self.controlador = controlador
        self.maestro.title("Aplicacion Algoritmo A* para encontrar la ruta mas corta")
        self.maestro.geometry("1000x800")

        self.tamaño_celda = 20
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        :return: No retorna nada.
        """
        self.marco_principal = ttk.Frame(self.maestro, padding="10")
        self.marco_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.maestro.grid_rowconfigure(0, weight=1)
        self.maestro.grid_columnconfigure(0, weight=1)

        # Entrada para el tamaño de la matriz
        ttk.Label(self.marco_principal, text="Tamaño de la matriz:").grid(row=0, column=0, sticky=tk.W)
        self.entrada_tamaño = ttk.Entry(self.marco_principal, width=10)
        self.entrada_tamaño.grid(row=0, column=1, sticky=tk.W)
        self.entrada_tamaño.insert(0, "14")

        # Botón para generar la matriz
        ttk.Button(self.marco_principal, text="Generar Matriz", command=self.controlador.generar_matriz).grid(row=0, column=2, sticky=tk.W)

        # Etiquetas para instrucciones y resultados
        self.etiqueta_instrucciones = ttk.Label(self.marco_principal, text="Haga clic para seleccionar el punto de inicio")
        self.etiqueta_instrucciones.grid(row=1, column=0, columnspan=3, sticky=tk.W)

        self.etiqueta_resultados = ttk.Label(self.marco_principal, text="")
        self.etiqueta_resultados.grid(row=2, column=0, columnspan=3, sticky=tk.W)

        # Marco para el canvas y la leyenda
        self.marco_canvas_leyenda = ttk.Frame(self.marco_principal)
        self.marco_canvas_leyenda.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.marco_principal.grid_rowconfigure(3, weight=1)
        self.marco_principal.grid_columnconfigure(0, weight=1)

        # Canvas para dibujar la matriz
        self.canvas = tk.Canvas(self.marco_canvas_leyenda, width=600, height=600)
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.canvas.bind("<Button-1>", self.controlador.al_hacer_clic_canvas)

        # Marco para la leyenda y listas
        self.marco_leyenda_listas = ttk.Frame(self.marco_canvas_leyenda, padding="10")
        self.marco_leyenda_listas.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E))

        # Leyenda
        ttk.Label(self.marco_leyenda_listas, text="Leyenda:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.marco_leyenda_listas, text="Verde: Inicio").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self.marco_leyenda_listas, text="Rojo: Fin").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(self.marco_leyenda_listas, text="Recuadro Azul: Ruta mas corta encontrada").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(self.marco_leyenda_listas, text="Tonos cálidos: Mientras mas calido representan mas costo").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(self.marco_leyenda_listas, text="Tonos fríos: Mientras mas frio representan menor costo").grid(row=5, column=0, sticky=tk.W)
        ttk.Label(self.marco_leyenda_listas, text="g: Costo desde inicio").grid(row=6, column=0, sticky=tk.W)
        ttk.Label(self.marco_leyenda_listas, text="f: Costo estimado total").grid(row=7, column=0, sticky=tk.W)

        # Listas abiertas y cerradas
        ttk.Label(self.marco_leyenda_listas, text="Lista Abierta:", font=("Arial", 12, "bold")).grid(row=8, column=0, sticky=tk.W)
        
        # Crear un marco para la lista abierta con barra de desplazamiento
        self.marco_lista_abierta = ttk.Frame(self.marco_leyenda_listas)
        self.marco_lista_abierta.grid(row=9, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.scrollbar_lista_abierta = Scrollbar(self.marco_lista_abierta)
        self.scrollbar_lista_abierta.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.texto_lista_abierta = Text(self.marco_lista_abierta, height=10, wrap=tk.WORD, yscrollcommand=self.scrollbar_lista_abierta.set)
        self.texto_lista_abierta.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar_lista_abierta.config(command=self.texto_lista_abierta.yview)

        ttk.Label(self.marco_leyenda_listas, text="Lista Cerrada:", font=("Arial", 12, "bold")).grid(row=10, column=0, sticky=tk.W)
        
        # Crear un marco para la lista cerrada con barra de desplazamiento
        self.marco_lista_cerrada = ttk.Frame(self.marco_leyenda_listas)
        self.marco_lista_cerrada.grid(row=11, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.scrollbar_lista_cerrada = Scrollbar(self.marco_lista_cerrada)
        self.scrollbar_lista_cerrada.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.texto_lista_cerrada = Text(self.marco_lista_cerrada, height=10, wrap=tk.WORD, yscrollcommand=self.scrollbar_lista_cerrada.set)
        self.texto_lista_cerrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar_lista_cerrada.config(command=self.texto_lista_cerrada.yview)

    def obtener_color(self, valor, valor_minimo, valor_maximo):
        """
        Calcula el color basado en el valor, desde verde (bajo costo) hasta rojo (alto costo).
        
        :param valor: Valor para el cual se calcula el color.
        :param valor_minimo: Valor mínimo del rango.
        :param valor_maximo: Valor máximo del rango.
        :return: Color en formato hexadecimal.
        """
        rango = valor_maximo - valor_minimo
        if rango == 0:
            normalizado = 0
        else:
            normalizado = 1 - (valor - valor_minimo) / rango
        
        hue = normalizado * 0.3  # 0.3 es verde en HSV
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        return f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'

    def dibujar_grafo(self, grafo, inicio, meta, camino_actual, costo_g, costo_f):
        """
        Dibuja el grafo en el canvas.
        
        :param grafo: Instancia de GrafoCalles.
        :param inicio: Tupla con las coordenadas del punto de inicio.
        :param meta: Tupla con las coordenadas del punto de destino.
        :param camino_actual: Lista de coordenadas que forman el camino encontrado.
        :param costo_g: Diccionario con los costos g de cada nodo.
        :param costo_f: Diccionario con los costos f de cada nodo.
        :return: No retorna nada.
        """
        self.canvas.delete("all")
        if not costo_f:
            # Si no hay costos calculados, dibuja la matriz inicial
            for y in range(grafo.tamaño):
                for x in range(grafo.tamaño):
                    color = "white" if grafo.grafo[y][x] == 1 else "black"
                    self.canvas.create_rectangle(x*self.tamaño_celda, y*self.tamaño_celda, 
                                                 (x+1)*self.tamaño_celda, (y+1)*self.tamaño_celda, 
                                                 fill=color, outline="gray")
        else:
            # Si hay costos calculados, colorea basado en los costos
            costo_f_minimo = min(costo_f.values())
            costo_f_maximo = max(costo_f.values())
            
            for y in range(grafo.tamaño):
                for x in range(grafo.tamaño):
                    if grafo.grafo[y][x] == 1:
                        if (x, y) in costo_f:
                            color = self.obtener_color(costo_f[(x, y)], costo_f_minimo, costo_f_maximo)
                        else:
                            color = "white"
                        
                        self.canvas.create_rectangle(x*self.tamaño_celda, y*self.tamaño_celda, 
                                                     (x+1)*self.tamaño_celda, (y+1)*self.tamaño_celda, 
                                                     fill=color, outline="gray")
                        
                        if (x, y) in costo_g and (x, y) in costo_f:
                            self.canvas.create_text(x*self.tamaño_celda + self.tamaño_celda/2, 
                                                    y*self.tamaño_celda + self.tamaño_celda/2,
                                                    text=f"g:{costo_g[(x,y)]:.1f}\nf:{costo_f[(x,y)]:.1f}",
                                                    font=("Arial", 8), fill="black")
                    else:
                        self.canvas.create_rectangle(x*self.tamaño_celda, y*self.tamaño_celda, 
                                                     (x+1)*self.tamaño_celda, (y+1)*self.tamaño_celda, 
                                                     fill="black", outline="gray")

            # Dibuja el camino más corto con borde azul
            if camino_actual:
                for x, y in camino_actual:
                    color = self.obtener_color(costo_f[(x, y)], costo_f_minimo, costo_f_maximo)
                    self.canvas.create_rectangle(x*self.tamaño_celda, y*self.tamaño_celda, 
                                                 (x+1)*self.tamaño_celda, (y+1)*self.tamaño_celda, 
                                                 fill=color, outline="blue", width=2)
                    if (x, y) in costo_g and (x, y) in costo_f:
                        self.canvas.create_text(x*self.tamaño_celda + self.tamaño_celda/2, 
                                                y*self.tamaño_celda + self.tamaño_celda/2,
                                                text=f"g:{costo_g[(x,y)]:.1f}\nf:{costo_f[(x,y)]:.1f}",
                                                font=("Arial", 8), fill="black")

        # Dibuja el punto de inicio y meta
        if inicio:
            self.canvas.create_rectangle(inicio[0]*self.tamaño_celda, inicio[1]*self.tamaño_celda, 
                                         (inicio[0]+1)*self.tamaño_celda, (inicio[1]+1)*self.tamaño_celda, 
                                         fill="green", outline="gray")

        if meta:
            self.canvas.create_rectangle(meta[0]*self.tamaño_celda, meta[1]*self.tamaño_celda, 
                                         (meta[0]+1)*self.tamaño_celda, (meta[1]+1)*self.tamaño_celda, 
                                         fill="red", outline="gray")

    def actualizar_instrucciones(self, texto):
        """
        Actualiza el texto de las instrucciones.
        
        :param texto: Nuevo texto de instrucciones.
        :return: No retorna nada.
        """
        self.etiqueta_instrucciones.config(text=texto)

    def actualizar_resultados(self, texto):
        """
        Actualiza el texto de los resultados.
        
        :param texto: Nuevo texto de resultados.
        :return: No retorna nada.
        """
        self.etiqueta_resultados.config(text=texto)

    def obtener_tamaño_matriz(self):
        """
        Obtiene el tamaño de la matriz ingresado por el usuario.
        
        :return: Tamaño de la matriz como string.
        """
        return self.entrada_tamaño.get()

    def actualizar_tamaño_celda(self, tamaño):
        """
        Actualiza el tamaño de las celdas y del canvas.
        
        :param tamaño: Nuevo tamaño de la matriz.
        :return: No retorna nada.
        """
        self.tamaño_celda = min(600 // tamaño, 30)
        tamaño_canvas = self.tamaño_celda * tamaño
        self.canvas.config(width=tamaño_canvas, height=tamaño_canvas)

    def actualizar_listas(self, lista_abierta, lista_cerrada):
        """
        Actualiza las etiquetas de las listas abiertas y cerradas.
        
        :param lista_abierta: Lista de nodos en la lista abierta.
        :param lista_cerrada: Lista de nodos en la lista cerrada.
        :return: No retorna nada.
        """
        self.texto_lista_abierta.config(state=tk.NORMAL)
        self.texto_lista_abierta.delete(1.0, tk.END)
        self.texto_lista_abierta.insert(tk.END, str(lista_abierta))
        self.texto_lista_abierta.config(state=tk.DISABLED)

        self.texto_lista_cerrada.config(state=tk.NORMAL)
        self.texto_lista_cerrada.delete(1.0, tk.END)
        self.texto_lista_cerrada.insert(tk.END, str(lista_cerrada))
        self.texto_lista_cerrada.config(state=tk.DISABLED)

    def seleccionar_punto_final(self, punto):
        """
        Cambia el color del punto final seleccionado a azul.
        
        :param punto: Coordenadas del punto final seleccionado.
        :return: No retorna nada.
        """
        self.canvas.create_rectangle(punto[0]*self.tamaño_celda, punto[1]*self.tamaño_celda, 
                                     (punto[0]+1)*self.tamaño_celda, (punto[1]+1)*self.tamaño_celda, 
                                     fill="blue", outline="gray")
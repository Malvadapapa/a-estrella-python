﻿# Documentación del Proyecto de Pathfinding A*

## Bienvenida/o!!

Bienvenido al proyecto de Pathfinding A*. Este proyecto tiene licencia libre de uso y fue creado con la ayuda de la IA v0 de Vercel por Cristian Vargas (https://github.com/Malvadapapa/) para el proyecto final de matemáticas de la Tecnicatura Superior en Desarrollo de Software del ISPC (Instituto Superior Politécnico Córdoba).

## Descripción General

Este proyecto implementa una visualización interactiva del algoritmo de pathfinding A* utilizando Python y Tkinter. El programa permite a los usuarios generar un grafo de calles, seleccionar puntos de inicio y fin, y visualizar el camino más corto encontrado por el algoritmo A*.

## Estructura del Proyecto

El proyecto está dividido en cuatro archivos principales:

1. model.py: Contiene la lógica del grafo y el algoritmo A*.
2. view.py: Maneja la interfaz gráfica de usuario.
3. controller.py: Actúa como intermediario entre el modelo y la vista.
4. main.py: Punto de entrada de la aplicación.

## Detalles de Implementación

### model.py

#### Clase GrafoCalles

- __init__(self, tamaño):
  - Inicializa el grafo de calles.
  - Parámetros:
    - tamaño: int, tamaño de la matriz cuadrada que representa el grafo.
  - Variables:
    - self.tamaño: Almacena el tamaño de la matriz.
    - self.grafo: Lista bidimensional que representa el grafo. 1 representa una calle, 0 un edificio.

- es_valido(self, x, y):
  - Verifica si una posición está dentro del grafo y es una calle.
  - Parámetros:
    - x: int, coordenada x de la posición.
    - y: int, coordenada y de la posición.
  - Retorna: bool, True si la posición es válida, False en caso contrario.

- obtener_vecinos(self, x, y):
  - Obtiene los vecinos válidos de una posición dada.
  - Parámetros:
    - x: int, coordenada x de la posición.
    - y: int, coordenada y de la posición.
  - Retorna: list, lista de tuplas con las coordenadas de los vecinos válidos.
  - Variables:
    - direcciones: Lista de tuplas que representan las 8 direcciones posibles (incluyendo diagonales).

#### Función heuristica(a, b)

- Calcula la distancia heurística entre dos puntos (distancia de Chebyshev).
- Parámetros:
  - a: tuple, coordenadas del primer punto.
  - b: tuple, coordenadas del segundo punto.
- Retorna: int, valor de la distancia heurística.

#### Función a_estrella(grafo, inicio, meta)

- Implementación del algoritmo A*.
- Parámetros:
  - grafo: GrafoCalles, instancia del grafo.
  - inicio: tuple, coordenadas del punto de inicio.
  - meta: tuple, coordenadas del punto de destino.
- Retorna: tuple, (camino, costo_g, costo_f) donde camino es la lista de coordenadas del camino encontrado.
- Variables principales:
  - vecinos: Lista de prioridad (heap) para almacenar nodos a explorar.
  - vino_de: Diccionario para reconstruir el camino.
  - costo_g: Diccionario que almacena el costo real desde el inicio hasta cada nodo.
  - costo_f: Diccionario que almacena el costo estimado total (g + h) para cada nodo.
  - conjunto_cerrado: Conjunto de nodos ya explorados.

### view.py

#### Clase InterfazPathfinding

- __init__(self, maestro, controlador):
  - Inicializa la interfaz gráfica del pathfinding.
  - Parámetros:
    - maestro: tk.Tk, ventana principal de Tkinter.
    - controlador: Controlador, instancia del controlador.
  - Variables principales:
    - self.maestro: Ventana principal de Tkinter.
    - self.controlador: Instancia del controlador para manejar la lógica.
    - self.tamaño_celda: Tamaño inicial de cada celda en el canvas.

- crear_widgets(self):
  - Crea y configura todos los widgets de la interfaz.
  - Crea y configura elementos como etiquetas, botones, canvas y leyenda.

- obtener_color(self, valor, valor_minimo, valor_maximo):
  - Calcula el color basado en el valor, desde verde (bajo costo) hasta rojo (alto costo).
  - Parámetros:
    - valor: float, valor para el cual se calcula el color.
    - valor_minimo: float, valor mínimo del rango.
    - valor_maximo: float, valor máximo del rango.
  - Retorna: str, color en formato hexadecimal.

- dibujar_grafo(self, grafo, inicio, meta, camino_actual, costo_g, costo_f):
  - Dibuja el grafo en el canvas.
  - Parámetros:
    - grafo: GrafoCalles, instancia del grafo.
    - inicio: tuple, coordenadas del punto de inicio.
    - meta: tuple, coordenadas del punto de destino.
    - camino_actual: list, lista de coordenadas que forman el camino encontrado.
    - costo_g: dict, diccionario con los costos g de cada nodo.
    - costo_f: dict, diccionario con los costos f de cada nodo.

- Métodos auxiliares:
  - actualizar_instrucciones(self, texto)
  - actualizar_resultados(self, texto)
  - obtener_tamaño_matriz(self)
  - actualizar_tamaño_celda(self, tamaño)

### controller.py

#### Clase Controlador

- __init__(self, vista):
  - Inicializa el controlador.
  - Parámetros:
    - vista: InterfazPathfinding, instancia de la vista.
  - Variables principales:
    - self.vista: Referencia a la vista.
    - self.grafo: Instancia de GrafoCalles.
    - self.inicio, self.meta: Puntos de inicio y fin del pathfinding.
    - self.camino_actual: Camino encontrado por el algoritmo.
    - self.costo_g, self.costo_f: Diccionarios de costos.

- generar_matriz(self):
  - Genera una nueva matriz basada en el tamaño ingresado por el usuario.
  - Valida el tamaño de la matriz.
  - Crea una nueva instancia de GrafoCalles.
  - Reinicia el estado del pathfinding.
  - Actualiza la vista con la nueva matriz.

- al_hacer_clic_canvas(self, evento):
  - Maneja los clics en el canvas para seleccionar inicio y meta.
  - Parámetros:
    - evento: Event, evento de clic del mouse.
  - Valida que los clics sean en posiciones válidas del grafo.
  - Actualiza el estado y la vista según la selección del usuario.

- encontrar_camino(self):
  - Ejecuta el algoritmo A* y actualiza la visualización.
  - Llama a la función a_estrella con los puntos de inicio y fin seleccionados.
  - Actualiza la vista con el resultado del algoritmo.

### main.py

- Función main():
  - Función principal para iniciar la aplicación.
  - Crea la ventana principal de Tkinter.
  - Inicializa el controlador y la vista, estableciendo las referencias cruzadas.
  - Inicia el bucle principal de la aplicación.

## Cómo ejecutar el proyecto

1. Asegúrate de tener Python instalado en tu sistema.
2. Coloca todos los archivos (model.py, view.py, controller.py y main.py) en el mismo directorio.
3. Ejecuta el archivo main.py:
   python main.py
4. La interfaz gráfica se abrirá, permitiéndote interactuar con la visualización de pathfinding.

## Notas adicionales

- El proyecto utiliza el patrón de diseño Modelo-Vista-Controlador (MVC) para separar la lógica de la interfaz de usuario.
- La implementación del algoritmo A* en model.py es genérica y puede ser reutilizada en otros proyectos de pathfinding.
- La visualización utiliza un esquema de colores para representar los costos, lo que ayuda a entender cómo funciona el algoritmo A*.
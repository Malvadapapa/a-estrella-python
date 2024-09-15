import tkinter as tk
from view import InterfazPathfinding
from controller import Controlador

def main():
    """
    Función principal para iniciar la aplicación.
    
    :return: No retorna nada.
    """
    raiz = tk.Tk()
    controlador = Controlador(None)
    vista = InterfazPathfinding(raiz, controlador)
    controlador.vista = vista
    raiz.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
import sys
import os
import random
from tkinter import simpledialog, messagebox
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tree_s.binary_search_tree import BinarySearchTree
from tree_s.avl_tree import AVLTree
from tree_s.b_tree import BTree
from tree_s.trie import Trie
from tree_s.n_ary_tree import NaryTree
from dashboards import TreeDashboard
class TreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Árboles")
        self.root.title("Menú de Árboles")
        self.root.geometry("400x400")
        self.create_main_menu()


    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()



    def create_main_menu(self):
        self.clear_window()
        
        # Configuración de la ventana principal
        self.root.title("Visualizador de Estructuras de Árboles")
        
        # Título principal
        title_label = tk.Label(self.root, text="Seleccione el Tipo de Árbol", 
                             font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Frame para los botones
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=20)
        
        # Botones para cada tipo de árbol
        button_style = {"font": ("Arial", 12), "width": 20, "height": 2}
        
        tk.Button(buttons_frame, text="Árbol Binario de Búsqueda", 
                 command=lambda: self.create_tree_dashboard("BST"), **button_style).grid(row=0, column=0, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Árbol AVL", 
                 command=lambda: self.create_tree_dashboard("AVL"), **button_style).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Árbol Trie", 
                 command=lambda: self.create_tree_dashboard("Trie"), **button_style).grid(row=1, column=0, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Árbol B", 
                 command=lambda: self.create_tree_dashboard("BTree"), **button_style).grid(row=1, column=1, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Árbol N-ario", 
                 command=lambda: self.create_tree_dashboard("Nary"), **button_style).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Botón de salida
        exit_button = tk.Button(self.root, text="Salir", font=("Arial", 12), 
                              command=self.root.quit, width=15, height=1)
        exit_button.pack(pady=20)
    
    def create_tree_dashboard(self, tree_type, order_b=0):
            if tree_type == "BST":
                tree = BinarySearchTree()
                self.current_dashboard = TreeDashboard(self.root, tree)
                self.current_dashboard.create_main_menu = self.create_main_menu
                self.current_dashboard.show_dashboard("Árbol Binario de Búsqueda")
            elif tree_type == "AVL":

                tree = AVLTree()
                self.current_dashboard = TreeDashboard(self.root, tree)
                self.current_dashboard.create_main_menu = self.create_main_menu
                self.current_dashboard.show_dashboard("Árbol AVL")
            elif tree_type == "Trie":

                tree = Trie()
                self.current_dashboard = TreeDashboard(self.root, tree)
                self.current_dashboard.create_main_menu = self.create_main_menu
                self.current_dashboard.show_dashboard("Árbol Trie")
            elif tree_type == "BTree":
                order = simpledialog.askinteger(
                "Orden del Árbol B",
                "Ingrese el orden (t) del Árbol B (t ≥ 2):",
                parent=self.root,
                minvalue=2,
                initialvalue=3
                )
                
                # Validar la entrada
                if order is None:  # El usuario canceló
                    return
                elif order < 2:
                    raise ValueError("El orden debe ser un entero ≥ 2")
                tree = BTree(t=order)  # Ejemplo con orden 3
                self.current_dashboard = TreeDashboard(self.root, tree)
                self.current_dashboard.create_main_menu = self.create_main_menu
                self.current_dashboard.show_dashboard("Árbol B (Orden "+str(order)+")")
            elif tree_type == "Nary":

                tree = NaryTree()
                self.current_dashboard = TreeDashboard(self.root, tree)
                self.current_dashboard.create_main_menu = self.create_main_menu
                self.current_dashboard.show_dashboard("Árbol N-ario")
        
    
if __name__ == "__main__":
    root = tk.Tk()
    app = TreeApp(root)
    root.mainloop()

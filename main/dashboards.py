import tkinter as tk
import sys
import os
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, messagebox
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tree_s.binary_search_tree import BinarySearchTree as BST
from tree_s.avl_tree import AVLTree
from tree_s.b_tree import BTree
from tree_s.trie import Trie
from tree_s.n_ary_tree import NaryTree
class TreeDashboard:
    def __init__(self, root, tree):
        self.root = root
        self.tree = tree
        self.canvas = None
        self.value_entry = None
        self.plot_frame = None
    
    def show_dashboard(self, title):
        self.clear_window()

        tk.Label(self.root, text=title, font=("Arial", 16)).pack(pady=10)

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Configuración específica para cada tipo de árbol
        if isinstance(self.tree, AVLTree):
            self._setup_avl_controls(control_frame)
        elif isinstance(self.tree, Trie):
            self._setup_trie_controls(control_frame)
        elif isinstance(self.tree, BTree):
            self._setup_btree_controls(control_frame)
        elif isinstance(self.tree, NaryTree):
            self._setup_nary_controls(control_frame)
        else:  # BST por defecto
            self._setup_bst_controls(control_frame)

        # Controles comunes
        tk.Button(self.root, text="Mostrar Recorridos", font=("Arial", 12), 
                 command=self.show_traversals).pack(pady=5)
        tk.Button(self.root, text="Volver al menú principal", font=("Arial", 12), 
                 command=self.create_main_menu).pack(pady=5)

        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        self.draw_tree()

    def _setup_bst_controls(self, frame):
        tk.Label(frame, text="Valor a insertar:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.value_entry = tk.Entry(frame, font=("Arial", 12))
        self.value_entry.grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Insertar", font=("Arial", 12), 
                command=self.insert_value).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Eliminar", font=("Arial", 12), 
                command=self.delete_value).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Insertar Aleatorios", font=("Arial", 12), 
                command=self.insert_random_values).grid(row=1, column=0, columnspan=4, pady=10)

    def _setup_avl_controls(self, frame):
        tk.Label(frame, text="Valor a insertar:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.value_entry = tk.Entry(frame, font=("Arial", 12))
        self.value_entry.grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Insertar", font=("Arial", 12), 
                command=self.insert_value).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Eliminar", font=("Arial", 12), 
                command=self.delete_value).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Insertar Aleatorios", font=("Arial", 12), 
                command=self.insert_random_values).grid(row=1, column=0, columnspan=4, pady=10)

    def _setup_trie_controls(self, frame):
        tk.Label(frame, text="Palabra a insertar:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.value_entry = tk.Entry(frame, font=("Arial", 12))
        self.value_entry.grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Insertar", font=("Arial", 12), 
                command=self.insert_value).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Eliminar", font=("Arial", 12), 
                command=self.delete_value).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Insertar Aleatorios", font=("Arial", 12), 
                command=self.insert_random_words).grid(row=1, column=0, columnspan=4, pady=10)

    def _setup_btree_controls(self, frame):
        tk.Label(frame, text="Valor a insertar:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.value_entry = tk.Entry(frame, font=("Arial", 12))
        self.value_entry.grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Insertar", font=("Arial", 12), 
                command=self.insert_value).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Eliminar", font=("Arial", 12), 
                command=self.delete_value).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Insertar Aleatorios", font=("Arial", 12), 
                command=self.insert_random_values).grid(row=1, column=0, columnspan=4, pady=10)
        tk.Button(frame, text="Mostrar Orden", font=("Arial", 12), 
                command=self.show_order).grid(row=2, column=0, columnspan=4, pady=5)

    def _setup_nary_controls(self, frame):
        tk.Label(frame, text="Valor a insertar:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.value_entry = tk.Entry(frame, font=("Arial", 12))
        self.value_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Padre (opcional):", font=("Arial", 12)).grid(row=1, column=0, padx=5)
        self.parent_entry = tk.Entry(frame, font=("Arial", 12))
        self.parent_entry.grid(row=1, column=1, padx=5)

        tk.Button(frame, text="Insertar", font=("Arial", 12), 
                command=self.insert_value).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Insertar Aleatorios", font=("Arial", 12), 
                command=self.insert_random_values).grid(row=2, column=0, columnspan=4, pady=10)

    # Métodos comunes que pueden ser sobrescritos por clases específicas
    def insert_value(self):
        value = self.value_entry.get()
        if value:
            try:
                if isinstance(self.tree, Trie):
                    self.tree.insert(value)
                else:
                    val = int(value)
                    if isinstance(self.tree, NaryTree):
                        parent_val = self.parent_entry.get()
                        parent = None if not parent_val else int(parent_val)
                        self.tree.insert(value=val, parent_value=parent)
                    else:
                        self.tree.insert(val)
                
                self.value_entry.delete(0, tk.END)
                if hasattr(self, 'parent_entry'):
                    self.parent_entry.delete(0, tk.END)
                self.draw_tree()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un valor válido.")

    def delete_value(self):
        value = self.value_entry.get()
        if value:
            try:
                if isinstance (self.tree, Trie):
                    val = str(value)
                else:    
                    val = int(value)
                self.tree.delete(val)
                self.value_entry.delete(0, tk.END)
                self.draw_tree()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido.")

    def insert_random_values(self):
        cantidad = simpledialog.askinteger("Cantidad", "¿Cuántos valores aleatorios insertar?", 
                                        minvalue=1, maxvalue=100)
        if cantidad:
            for _ in range(cantidad):
                val = random.randint(0, 99)
                if isinstance(self.tree, NaryTree):
                    # Si el árbol está vacío, insertamos como raíz
                    if self.tree.root is None:
                        self.tree.insert(None, val)  # None indica que debe ser raíz
                    else:
                        # Seleccionamos un nodo padre existente al azar
                        nodes = self.tree.get_nodes()
                        parent = random.choice(nodes)
                        self.tree.insert(parent.value, val)
                else:
                    self.tree.insert(val)
            self.draw_tree()

    def insert_random_words(self):
        cantidad = simpledialog.askinteger("Cantidad", "¿Cuántas palabras aleatorias insertar?", 
                                         minvalue=1, maxvalue=20)
        if cantidad:
            words = ["hola", "adios", "arbol", "casa", "perro", "gato", "python", "java", 
                    "programa", "algoritmo", "estructura", "datos", "computadora", "teclado"]
            for _ in range(cantidad):
                word = random.choice(words) + str(random.randint(1, 100))
                self.tree.insert(word)
            self.draw_tree()

    def show_traversals(self):
            in_order = self.tree.inorder()
            pre_order = self.tree.preorder()
            post_order = self.tree.postorder()
            
            msg = f"Inorden: {' - '.join(map(str, in_order))}\n\n"
            msg += f"Preorden: {' - '.join(map(str, pre_order))}\n\n"
            msg += f"Postorden: {' - '.join(map(str, post_order))}"
            
            messagebox.showinfo("Recorridos", msg)

    
    def show_order(self):
        if isinstance(self.tree, BTree):
            order = self.tree.get_order()
            messagebox.showinfo("Orden del B-Tree", f"El orden (t) de este B-Tree es: {order}")
        else:
            messagebox.showerror("Error", "Esta función solo está disponible para B-Trees")

    def draw_tree(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.axis('off')

        if isinstance(self.tree, Trie):
            self._draw_trie(ax, self.tree.root, 0, 0, 1.5)
        elif isinstance(self.tree, BTree):
            self._draw_btree(ax, self.tree.root, 0, 0, 1.5, self.tree.t)
        elif isinstance(self.tree, NaryTree):
            self._draw_nary(ax, self.tree.root, 0, 0, 1.5)
        else:
            self._draw_binary_tree(ax, self.tree.root, 0, 0, 1.5)

        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _draw_binary_tree(self, ax, node, x, y, dx):
        if node is None:
            return
            
        # Para AVL, mostramos también la altura
        label = str(node.key) if hasattr(node, 'key') else str(node.val)
        if hasattr(node, 'height'):
            label += f"\nh={node.height}"
            
        ax.text(x, y, label, ha='center', va='center', 
               bbox=dict(boxstyle="circle", facecolor="lightblue"))
               
        if node.left:
            ax.plot([x, x - dx], [y - 0.1, y - 1], color='black')
            self._draw_binary_tree(ax, node.left, x - dx, y - 1, dx / 2)
        if node.right:
            ax.plot([x, x + dx], [y - 0.1, y - 1], color='black')
            self._draw_binary_tree(ax, node.right, x + dx, y - 1, dx / 2)

    def _draw_trie(self, ax, node, x, y, dx):
        if not node:
            return
            
        # Dibujar el nodo actual
        label = "root" if node.char is None else node.char
        color = "lightgreen" if node.is_end_of_word else "lightblue"
        boxstyle = "circle"
        
        # Si es el nodo raíz, hacerlo un poco más grande
        if node.char is None:
            ax.text(x, y, label, ha='center', va='center', 
                bbox=dict(boxstyle="circle", facecolor="lightblue", pad=1.5))
        else:
            ax.text(x, y, label, ha='center', va='center', 
                bbox=dict(boxstyle="circle", facecolor=color))
                
        # Dibujar hijos
        if node.children:
            num_children = len(node.children)
            if num_children > 0:
                # Calcular el espaciado entre nodos hijos
                child_dx = dx * 2 / max(1, num_children)
                child_x = x - dx + child_dx/2
                
                # Ordenar los hijos para consistencia en el dibujo
                sorted_children = sorted(node.children.items(), key=lambda item: item[0])
                
                for i, (char, child) in enumerate(sorted_children):
                    # Dibujar línea al hijo
                    ax.plot([x, child_x + i*child_dx], [y - 0.1, y - 1], color='black')
                    # Dibujar el hijo recursivamente
                    self._draw_trie(ax, child, child_x + i*child_dx, y - 1, dx / 1.8)
                    
                    
    def _draw_btree(self, ax, node, x, y, dx, depth=0):
        if not node:
            return
        
        # Ajustar el espaciado basado en la profundidad
        vertical_gap = 1.2 - (depth * 0.1)  # Reduce el espacio vertical en niveles más profundos
        horizontal_scale = 1.5  # Factor de escala horizontal
        
        # Calcular el ancho necesario basado en la cantidad de claves
        key_count = len(node.keys)
        node_width = 0.2 * key_count  # Ancho proporcional al número de claves
        
        # Dibujar las claves del nodo con formato mejorado
        keys_str = "|" + " ".join(f"{k:^3}" for k in node.keys) + "|"  # Formato centrado
        ax.text(x, y, keys_str, ha='center', va='center', 
            bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.7),
            fontsize=max(8, 10 - key_count//4))  # Ajustar tamaño de fuente
        
        # Dibujar hijos si no es hoja
        if not node.leaf:
            num_children = len(node.children)
            if num_children > 0:
                # Calcular espaciado entre nodos hijos
                total_width = dx * horizontal_scale * (1 + depth * 0.3)  # Aumentar espacio en niveles superiores
                child_dx = total_width / num_children
                child_x = x - total_width/2 + child_dx/2
                
                # Dibujar conexiones con los hijos
                for i, child in enumerate(node.children):
                    # Dibujar línea curva para mejor visualización
                    ax.plot([x, child_x + i*child_dx], 
                        [y - 0.1, y - vertical_gap], 
                        color='black', linewidth=0.8, alpha=0.6)
                    
                    # Llamada recursiva con profundidad incrementada
                    self._draw_btree(ax, child, child_x + i*child_dx, 
                                y - vertical_gap, dx * 0.7, depth + 1)   
                
                                 
    def _draw_nary(self, ax, node, x, y, dx):
        if not node:
            return
            
        ax.text(x, y, str(node.value), ha='center', va='center', 
               bbox=dict(boxstyle="circle", facecolor="lightblue"))
               
        if node.children:
            num_children = len(node.children)
            child_dx = dx * 2 / max(1, num_children)
            child_x = x - dx + child_dx/2
            
            for i, child in enumerate(node.children):
                ax.plot([x, child_x + i*child_dx], [y - 0.1, y - 1], color='black')
                self._draw_nary(ax, child, child_x + i*child_dx, y - 1, dx / 2)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        # Este método debería ser implementado por la clase principal
        pass
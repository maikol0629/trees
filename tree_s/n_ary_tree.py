import random
class NaryNode:
    def __init__(self, value):
        self.value = value
        self.children = []

class NaryTree:
    def __init__(self):
        self.root = None

    def insert_root(self, value):
        """Inserta el nodo raíz del árbol."""
        if self.root is not None:
            print("Error: El árbol ya tiene una raíz")
            return False
        self.root = NaryNode(value)
        return True
    
               
        

        
    def insert(self, parent_value, value):
        """Inserta un nuevo nodo como hijo del nodo padre especificado."""
        if value is None:
            return False

        # Caso especial para insertar la raíz
        if parent_value is None:
            if self.root is None:
                self.root = NaryNode(value)
                return True
            return False

        if self.root is None:
            return False  # No debería pasar si parent_value no es None

        parent = self._find_node(self.root, parent_value)

        if parent is None:
            # Si no encontramos el padre, insertamos como hijo de un nodo aleatorio
            nodes = self.get_nodes()
            if not nodes:
                return False
            parent = random.choice(nodes)

        parent.children.append(NaryNode(value))
        return True



    def _find_node(self, node, value):
        """Busca recursivamente un nodo con el valor especificado."""
        if node is None:
            return None
        if node.value == value:
            return node
        for child in node.children:
            found = self._find_node(child, value)
            if found:
                return found
        return None
    
    def get_nodes(self):
        """Devuelve una lista de todos los nodos del árbol."""
        nodes = []

        def traverse(node):
            if node:
                nodes.append(node)
                for child in node.children:
                    traverse(child)

        traverse(self.root)
        return nodes

        # DFS Methods
    def preorder(self):
        """Devuelve recorrido en preorden: raíz, luego hijos de izquierda a derecha."""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.value)
            for child in node.children:
                self._preorder_recursive(child, result)

    def inorder(self):
        """Devuelve recorrido en inorden: primer hijo, raíz, luego resto de hijos."""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            if node.children:
                self._inorder_recursive(node.children[0], result)
            result.append(node.value)
            for child in node.children[1:]:
                self._inorder_recursive(child, result)

    def postorder(self):
        """Devuelve recorrido en postorden: hijos de izquierda a derecha, luego raíz."""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            for child in node.children:
                self._postorder_recursive(child, result)
            result.append(node.value)

    # BFS Method
    def level_order(self):
        """Devuelve recorrido por niveles: de arriba hacia abajo, de izquierda a derecha."""
        result = []
        if self.root is None:
            return result

        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            queue.extend(node.children)
        return result

   
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Altura inicial es 1 para nodos nuevos

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        """Obtiene la altura de un nodo (0 si es None)."""
        return node.height if node else 0

    def _update_height(self, node):
        """Actualiza la altura de un nodo basado en sus hijos."""
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        """Calcula el factor de balance del árbol completo o de un nodo específico."""
        if node is None:
            return 0
        return self._get_node_balance(node)

    def _get_node_balance(self, node):
        """Calcula el balance para un nodo específico."""
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def get_tree_balance(self):
        """Devuelve el balance general del árbol (diferencia de altura entre subárboles)."""
        if self.root is None:
            return 0
        return self._get_node_balance(self.root)

    def left_rotate(self, z):
        """Rotación izquierda."""
        y = z.right
        T2 = y.left
        
        y.left = z
        z.right = T2
        
        self._update_height(z)
        self._update_height(y)
        
        return y

    def right_rotate(self, z):
        """Rotación derecha."""
        y = z.left
        T3 = y.right
        
        y.right = z
        z.left = T3
        
        self._update_height(z)
        self._update_height(y)
        
        return y

    def insert(self, key):
        """Inserta una clave manteniendo el balance AVL."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)
        
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # Claves duplicadas no permitidas
        
        self._update_height(node)
        
        return self._rebalance(node)

    def search(self, key):
        """Busca una clave en el árbol."""
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def delete(self, key):
        """Elimina una clave manteniendo el balance AVL."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
            
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Nodo con un hijo o sin hijos
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
                
            # Nodo con dos hijos: obtener sucesor inorder
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        
        self._update_height(node)
        return self._rebalance(node)

    def _min_value_node(self, node):
        """Obtiene el nodo con el valor mínimo (para eliminación)."""
        current = node
        while current.left:
            current = current.left
        return current

    def _rebalance(self, node):
        """Rebalancea el árbol si es necesario."""
        if not node:
            return node
            
        balance = self.get_balance(node)
        
        # Caso Left Left
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
            
        # Caso Right Right
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
            
        # Caso Left Right
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
            
        # Caso Right Left
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
            
        return node

    # Métodos de recorrido (se mantienen igual que los tuyos)
    def preorder(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.key)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

    def postorder(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.key)

    def level_order(self):
        result = []
        if self.root is None:
            return result

        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.key)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result
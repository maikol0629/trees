
class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Minimum degree
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def search(self, k):
        return self._search_recursive(self.root, k)

    def _search_recursive(self, node, k):
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return True
        if node.leaf:
            return False
        return self._search_recursive(node.children[i], k)

    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode(self.t, False)
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def _split_child(self, node, i):
        t = self.t
        y = node.children[i]
        z = BTreeNode(t, y.leaf)
        node.children.insert(i + 1, z)
        node.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t]

    # DFS Methods
    def preorder(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.extend(node.keys)
            if not node.leaf:
                for child in node.children:
                    self._preorder_recursive(child, result)

    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            for i in range(len(node.keys)):
                if not node.leaf:
                    self._inorder_recursive(node.children[i], result)
                result.append(node.keys[i])
            if not node.leaf:
                self._inorder_recursive(node.children[-1], result)

    def postorder(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            if not node.leaf:
                for child in node.children:
                    self._postorder_recursive(child, result)
            result.extend(node.keys)

    # BFS Method
    def level_order(self):
        result = []
        if self.root is None:
            return result

        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.extend(node.keys)
            if not node.leaf:
                queue.extend(node.children)
        return result



    def delete(self, k):
        self._delete_recursive(self.root, k)
        # Si la raíz queda sin claves y tiene hijos, hacer que el primer hijo sea la nueva raíz
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete_recursive(self, node, k):
        t = self.t
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        
        # Caso 1: La clave está en este nodo
        if i < len(node.keys) and node.keys[i] == k:
            if node.leaf:
                # Caso 1a: La clave está en un nodo hoja
                node.keys.pop(i)
            else:
                # Caso 1b: La clave está en un nodo interno
                # Encontrar predecesor
                pred = self._get_predecessor(node, i)
                node.keys[i] = pred
                # Eliminar el predecesor
                self._delete_recursive(node.children[i], pred)
        else:
            # Caso 2: La clave no está en este nodo
            if node.leaf:
                print(f"Key {k} not found in the tree")
                return
            
            # Verificar si el hijo donde debe estar la clave tiene suficientes claves
            if len(node.children[i].keys) < t:
                self._fill(node, i)
                # Después de llenar, puede que hayamos fusionado, así que actualizamos i
                if i > len(node.keys):
                    i -= 1
            
            # Si el último hijo fue fusionado, ir al anterior
            if i == len(node.keys):
                i -= 1
            
            self._delete_recursive(node.children[i], k)

    def _get_predecessor(self, node, index):
        # Ir al hijo izquierdo y luego todo a la derecha
        current = node.children[index]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node, index):
        # Ir al hijo derecho y luego todo a la izquierda
        current = node.children[index + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def _fill(self, node, index):
        t = self.t
        # Intentar tomar prestado del hermano izquierdo
        if index != 0 and len(node.children[index-1].keys) >= t:
            self._borrow_from_prev(node, index)
        # Intentar tomar prestado del hermano derecho
        elif index != len(node.children) - 1 and len(node.children[index+1].keys) >= t:
            self._borrow_from_next(node, index)
        # Fusionar con un hermano
        else:
            if index != len(node.children) - 1:
                self._merge(node, index)
            else:
                self._merge(node, index-1)

    def _borrow_from_prev(self, node, index):
        child = node.children[index]
        sibling = node.children[index-1]
        
        # Desplazar todas las claves e hijos del child una posición a la derecha
        child.keys.insert(0, node.keys[index-1])
        if not child.leaf:
            child.children.insert(0, sibling.children[-1])
            sibling.children.pop(-1)
        
        # Mover la clave del hermano al padre
        node.keys[index-1] = sibling.keys[-1]
        sibling.keys.pop(-1)

    def _borrow_from_next(self, node, index):
        child = node.children[index]
        sibling = node.children[index+1]
        
        # Mover la clave del padre al child
        child.keys.append(node.keys[index])
        if not child.leaf:
            child.children.append(sibling.children[0])
            sibling.children.pop(0)
        
        # Mover la clave del hermano al padre
        node.keys[index] = sibling.keys[0]
        sibling.keys.pop(0)

    def _merge(self, node, index):
        t = self.t
        child = node.children[index]
        sibling = node.children[index+1]
        
        # Mover la clave del padre al child
        child.keys.append(node.keys[index])
        
        # Copiar claves e hijos del hermano
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        
        # Eliminar la clave del padre y el puntero al hermano
        node.keys.pop(index)
        node.children.pop(index+1)
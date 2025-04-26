class TrieNode:
    def __init__(self, char=None):
        self.char = char
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)  # Pasa el carácter al crear el nodo
            node = node.children[char]
        node.is_end_of_word = True
        
        
    def search(self, word, return_node=False):
        node = self.root
        for char in word:
            if char not in node.children:
                return None if return_node else False
            node = node.children[char]
        if return_node:
            return node if node.is_end_of_word else None
        return node.is_end_of_word



    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def get_words(self):
        """Retorna todas las palabras almacenadas en el Trie"""
        words = []
        self._get_words_recursive(self.root, "", words)
        return words
    
    def _get_words_recursive(self, node, current_word, words):
        """Función auxiliar recursiva para recolectar palabras"""
        if node.is_end_of_word:
            words.append(current_word)
        
        for char, child in node.children.items():
            self._get_words_recursive(child, current_word + char, words)
    
    # DFS Methods modificados para retornar listas
    def preorder(self):
        """Recorrido preorden que retorna una lista de palabras"""
        result = []
        self._preorder_recursive(self.root, "", result)
        return result
    
    def _preorder_recursive(self, node, current_word, result):
        if node.is_end_of_word:
            result.append(current_word)
        for char, child in node.children.items():
            self._preorder_recursive(child, current_word + char, result)
    
    def inorder(self):
        """Recorrido inorden que retorna una lista de palabras (ordenadas)"""
        result = []
        self._inorder_recursive(self.root, "", result)
        return result
    
    def _inorder_recursive(self, node, current_word, result):
        if node.is_end_of_word:
            result.append(current_word)
        for char, child in sorted(node.children.items()):
            self._inorder_recursive(child, current_word + char, result)
    
    def postorder(self):
        """Recorrido postorden que retorna una lista de palabras"""
        result = []
        self._postorder_recursive(self.root, "", result)
        return result
    
    def _postorder_recursive(self, node, current_word, result):
        for char, child in node.children.items():
            self._postorder_recursive(child, current_word + char, result)
        if node.is_end_of_word:
            result.append(current_word)
    
    # BFS Method modificado para retornar lista
    def level_order(self):
        """Recorrido por niveles que retorna una lista de palabras"""
        if not self.root:
            return []
        
        result = []
        queue = [(self.root, "")]
        while queue:
            node, current_word = queue.pop(0)
            if node.is_end_of_word:
                result.append(current_word)
            for char, child in node.children.items():
                queue.append((child, current_word + char))
        return result
    
    
    def delete(self, word):
        def _delete_recursive(node, word, depth):
            if node is None:
                return False

            if depth == len(word):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0  # Si no tiene hijos, se puede borrar

            char = word[depth]
            child_node = node.children.get(char)
            if child_node is None:
                return False

            should_delete_child = _delete_recursive(child_node, word, depth + 1)

            if should_delete_child:
                del node.children[char]
                return not node.is_end_of_word and len(node.children) == 0

            return False

        if not word:
            return False

        return _delete_recursive(self.root, word, 0)

    
    def find_words_with_prefix(self, prefix):
        """
        Encuentra todas las palabras que comienzan con el prefijo dado.
        
        Args:
            prefix: Prefijo a buscar
        
        Returns:
            Lista de palabras que comienzan con el prefijo
        """
        # Primero encontramos el nodo donde termina el prefijo
        node = self.search(prefix, return_node=True)
        if not node:
            return []
        
        # Ahora recolectamos todas las palabras desde ese nodo
        words = []
        self._get_words_recursive(node, prefix, words)
        return words
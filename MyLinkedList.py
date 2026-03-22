"""
MyLinkedList - Implementación de Linked List en Python
======================================================
Biblioteca propia con Nodo, Lista Simplemente Enlazada y Lista Doblemente Enlazada.
"""


# ──────────────────────────────────────────────
# NODO
# ──────────────────────────────────────────────
class Node:
    """Nodo básico para lista simplemente enlazada."""

    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data!r})"


class DoubleNode:
    """Nodo para lista doblemente enlazada."""

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"DoubleNode({self.data!r})"


# ──────────────────────────────────────────────
# LISTA SIMPLEMENTE ENLAZADA
# ──────────────────────────────────────────────
class SinglyLinkedList:
    """
    Lista Simplemente Enlazada (Singly Linked List).

    Operaciones soportadas:
        append, prepend, insert_after, remove, search,
        get, reverse, to_list, __len__, __iter__, __str__
    """

    def __init__(self):
        self._head = None
        self._size = 0

    # ── Inserción ──────────────────────────────
    def append(self, data):
        """Agrega un nodo al final. O(n)"""
        new_node = Node(data)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, data):
        """Agrega un nodo al inicio. O(1)"""
        new_node = Node(data)
        new_node.next = self._head
        self._head = new_node
        self._size += 1

    def insert_after(self, target_data, new_data):
        """Inserta new_data después del nodo que contenga target_data. O(n)"""
        current = self._head
        while current:
            if current.data == target_data:
                new_node = Node(new_data)
                new_node.next = current.next
                current.next = new_node
                self._size += 1
                return True
            current = current.next
        raise ValueError(f"Valor '{target_data}' no encontrado en la lista.")

    def insert_at(self, index, data):
        """Inserta data en la posición dada (0-indexed). O(n)"""
        if index < 0 or index > self._size:
            raise IndexError(f"Índice {index} fuera de rango (tamaño={self._size}).")
        if index == 0:
            self.prepend(data)
            return
        new_node = Node(data)
        current = self._head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self._size += 1

    # ── Eliminación ────────────────────────────
    def remove(self, data):
        """Elimina el primer nodo con el valor dado. O(n)"""
        if self._head is None:
            raise ValueError("La lista está vacía.")
        if self._head.data == data:
            self._head = self._head.next
            self._size -= 1
            return
        current = self._head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return
            current = current.next
        raise ValueError(f"Valor '{data}' no encontrado en la lista.")

    def remove_at(self, index):
        """Elimina el nodo en la posición dada (0-indexed). O(n)"""
        if index < 0 or index >= self._size:
            raise IndexError(f"Índice {index} fuera de rango (tamaño={self._size}).")
        if index == 0:
            removed = self._head.data
            self._head = self._head.next
            self._size -= 1
            return removed
        current = self._head
        for _ in range(index - 1):
            current = current.next
        removed = current.next.data
        current.next = current.next.next
        self._size -= 1
        return removed

    # ── Búsqueda / Acceso ──────────────────────
    def search(self, data):
        """Retorna el índice del primer nodo con el valor dado, o -1. O(n)"""
        current = self._head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def get(self, index):
        """Retorna el dato en la posición dada (0-indexed). O(n)"""
        if index < 0 or index >= self._size:
            raise IndexError(f"Índice {index} fuera de rango (tamaño={self._size}).")
        current = self._head
        for _ in range(index):
            current = current.next
        return current.data

    # ── Utilidades ─────────────────────────────
    def reverse(self):
        """Invierte la lista en su lugar. O(n)"""
        prev = None
        current = self._head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self._head = prev

    def to_list(self):
        """Convierte la lista enlazada a una lista de Python. O(n)"""
        result = []
        current = self._head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def is_empty(self):
        return self._size == 0

    # ── Métodos especiales ─────────────────────
    def __len__(self):
        return self._size

    def __iter__(self):
        current = self._head
        while current:
            yield current.data
            current = current.next

    def __contains__(self, data):
        return self.search(data) != -1

    def __str__(self):
        nodes = " -> ".join(str(d) for d in self)
        return f"[{nodes}] -> None"

    def __repr__(self):
        return f"SinglyLinkedList({self.to_list()!r})"


# ──────────────────────────────────────────────
# LISTA DOBLEMENTE ENLAZADA
# ──────────────────────────────────────────────
class DoublyLinkedList:
    """
    Lista Doblemente Enlazada (Doubly Linked List).

    Operaciones soportadas:
        append, prepend, insert_after, remove, search,
        get, reverse, to_list, __len__, __iter__, __str__
    """

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    # ── Inserción ──────────────────────────────
    def append(self, data):
        """Agrega al final. O(1)"""
        new_node = DoubleNode(data)
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def prepend(self, data):
        """Agrega al inicio. O(1)"""
        new_node = DoubleNode(data)
        if self._head is None:
            self._head = self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._size += 1

    def insert_after(self, target_data, new_data):
        """Inserta new_data después del nodo con target_data. O(n)"""
        current = self._head
        while current:
            if current.data == target_data:
                new_node = DoubleNode(new_data)
                new_node.prev = current
                new_node.next = current.next
                if current.next:
                    current.next.prev = new_node
                else:
                    self._tail = new_node
                current.next = new_node
                self._size += 1
                return True
            current = current.next
        raise ValueError(f"Valor '{target_data}' no encontrado.")

    # ── Eliminación ────────────────────────────
    def remove(self, data):
        """Elimina el primer nodo con el valor dado. O(n)"""
        current = self._head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self._head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self._tail = current.prev
                self._size -= 1
                return
            current = current.next
        raise ValueError(f"Valor '{data}' no encontrado.")

    # ── Búsqueda / Acceso ──────────────────────
    def search(self, data):
        """Retorna el índice del primer nodo con el valor, o -1. O(n)"""
        current = self._head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def get(self, index):
        """Retorna el dato en la posición dada. O(n)"""
        if index < 0 or index >= self._size:
            raise IndexError(f"Índice {index} fuera de rango.")
        # Optimización: recorre desde el extremo más cercano
        if index <= self._size // 2:
            current = self._head
            for _ in range(index):
                current = current.next
        else:
            current = self._tail
            for _ in range(self._size - 1 - index):
                current = current.prev
        return current.data

    # ── Utilidades ─────────────────────────────
    def reverse(self):
        """Invierte la lista en su lugar. O(n)"""
        current = self._head
        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev          # avanza (era .next antes del swap)
        self._head, self._tail = self._tail, self._head

    def to_list(self):
        return [data for data in self]

    def to_list_reversed(self):
        """Recorre desde la cola hacia la cabeza. O(n)"""
        result = []
        current = self._tail
        while current:
            result.append(current.data)
            current = current.prev
        return result

    def is_empty(self):
        return self._size == 0

    # ── Métodos especiales ─────────────────────
    def __len__(self):
        return self._size

    def __iter__(self):
        current = self._head
        while current:
            yield current.data
            current = current.next

    def __contains__(self, data):
        return self.search(data) != -1

    def __str__(self):
        nodes = " <-> ".join(str(d) for d in self)
        return f"None <-> [{nodes}] <-> None"

    def __repr__(self):
        return f"DoublyLinkedList({self.to_list()!r})"


# ──────────────────────────────────────────────
# DEMO / PRUEBAS BÁSICAS
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  MyLinkedList — Demo")
    print("=" * 55)

    # ── Singly ──────────────────────────────────
    print("\n--- SinglyLinkedList ---")
    sll = SinglyLinkedList()
    for val in [10, 20, 30, 40, 50]:
        sll.append(val)
    print("Lista inicial :", sll)
    print("Longitud      :", len(sll))

    sll.prepend(5)
    print("Tras prepend(5):", sll)

    sll.insert_after(20, 25)
    print("insert_after(20, 25):", sll)

    sll.insert_at(0, 1)
    print("insert_at(0, 1):", sll)

    print("search(25)    :", sll.search(25))
    print("get(3)        :", sll.get(3))
    print("30 in sll     :", 30 in sll)

    sll.remove(25)
    print("Tras remove(25):", sll)

    removed = sll.remove_at(0)
    print(f"Tras remove_at(0) [extraído={removed}]:", sll)

    sll.reverse()
    print("Tras reverse():", sll)

    print("to_list()     :", sll.to_list())
    print("Iteración     :", list(sll))

    print("\n--- DoublyLinkedList ---")
    dll = DoublyLinkedList()
    for val in ["A", "B", "C", "D"]:
        dll.append(val)
    print("Lista inicial :", dll)

    dll.prepend("Z")
    print("Tras prepend('Z'):", dll)

    dll.insert_after("B", "B2")
    print("insert_after('B','B2'):", dll)

    dll.remove("B2")
    print("Tras remove('B2'):", dll)

    print("search('C')   :", dll.search("C"))
    print("get(2)        :", dll.get(2))

    dll.reverse()
    print("Tras reverse():", dll)
    print("Inverso       :", dll.to_list_reversed())
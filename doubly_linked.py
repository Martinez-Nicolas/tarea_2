class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insertar_al_frente(self, vuelo):
        nuevo = Node(vuelo)
        if not self.head:
            self.head = self.tail = nuevo
        else:
            nuevo.next = self.head
            self.head.prev = nuevo
            self.head = nuevo
        self.size += 1

    def insertar_al_final(self, vuelo):
        nuevo = Node(vuelo)
        if not self.tail:
            self.head = self.tail = nuevo
        else:
            nuevo.prev = self.tail
            self.tail.next = nuevo
            self.tail = nuevo
        self.size += 1

    def obtener_primero(self):
        return self.head.data if self.head else None

    def obtener_ultimo(self):
        return self.tail.data if self.tail else None

    def longitud(self):
        return self.size

    def insertar_en_posicion(self, vuelo, pos):
        if pos < 0 or pos > self.size:
            raise IndexError("Posición fuera de rango")
        if pos == 0:
            return self.insertar_al_frente(vuelo)
        if pos == self.size:
            return self.insertar_al_final(vuelo)

        nuevo = Node(vuelo)
        actual = self.head
        for _ in range(pos):
            actual = actual.next
        anterior = actual.prev
        nuevo.prev = anterior
        nuevo.next = actual
        anterior.next = nuevo
        actual.prev = nuevo
        self.size += 1

    def extraer_de_posicion(self, pos):
        if pos < 0 or pos >= self.size:
            raise IndexError("Posición fuera de rango")
        actual = self.head
        for _ in range(pos):
            actual = actual.next
        if actual.prev:
            actual.prev.next = actual.next
        if actual.next:
            actual.next.prev = actual.prev
        if actual == self.head:
            self.head = actual.next
        if actual == self.tail:
            self.tail = actual.prev
        self.size -= 1
        return actual.data

    def listar(self):
        vuelos = []
        actual = self.head
        while actual:
            vuelos.append(actual.data)
            actual = actual.next
        return vuelos

    def clear(self):
        self.head = self.tail = None
        self.size = 0

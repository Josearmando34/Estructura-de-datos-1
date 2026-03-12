# ─── 1. Order ─────────────────────────────────────────────
class Order:

    def __init__(self, qtty, customer):
        self.customer = customer
        self.qtty = qtty

    def print(self):
        print("     Customer:", self.getCustomer())
        print("     Quantity:", self.getQtty())
        print("     ------------")

    def getQtty(self):
        return self.qtty

    def getCustomer(self):
        return self.customer


# ─── 2. Node ──────────────────────────────────────────────
class Node:

    def __init__(self, info):
        self.info = info
        self.next = None

    def getInfo(self):
        return self.info

    def getNext(self):
        return self.next

    def setNext(self, n):
        self.next = n


# ─── 3. QueueInterface ────────────────────────────────────
class QueueInterface:

    def size(self):
        pass

    def isEmpty(self):
        pass

    def front(self):
        pass

    def enqueue(self, info):
        pass

    def dequeue(self):
        pass


# ─── 4. Queue (implementación con lista enlazada) ─────────
class Queue(QueueInterface):

    def __init__(self):
        self.front_node = None
        self.rear = None
        self.size_count = 0

    def size(self):
        return self.size_count

    def isEmpty(self):
        return self.size_count == 0

    def front(self):
        if self.isEmpty():
            return None
        return self.front_node.getInfo()

    def enqueue(self, info):

        newNode = Node(info)

        if self.isEmpty():
            self.front_node = newNode
            self.rear = newNode
        else:
            self.rear.setNext(newNode)
            self.rear = newNode

        self.size_count += 1

    def dequeue(self):

        if self.isEmpty():
            return None

        data = self.front_node.getInfo()
        self.front_node = self.front_node.getNext()

        if self.front_node is None:
            self.rear = None

        self.size_count -= 1
        return data

    # imprimir la cola completa
    def dump(self):

        print("\n     ********* QUEUE DUMP *********")
        print("     Size:", self.size())

        node = self.front_node
        i = 1

        while node is not None:
            print("   ** Element", i)
            o = node.getInfo()
            o.print()
            node = node.getNext()
            i += 1


# ─── 5. Main ──────────────────────────────────────────────
if __name__ == "__main__":

    q = Queue()

    # agregar órdenes
    q.enqueue(Order(20, "cust1"))
    q.enqueue(Order(30, "cust2"))
    q.enqueue(Order(40, "cust3"))
    q.enqueue(Order(50, "cust3"))

    # mostrar cola
    q.dump()

    # ver el primero sin eliminar
    print("\n   >> front() -> Customer:",
          q.front().getCustomer())

    # eliminar el primero
    removed = q.dequeue()

    print("   >> dequeue() removed -> Customer:",
          removed.getCustomer(),
          "| Qty:", removed.getQtty())

    # mostrar cola actualizada
    q.dump()
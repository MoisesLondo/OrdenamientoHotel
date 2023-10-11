
import pickle
from datetime import datetime

class factura:
    def __init__(self, nombre, ci, hotel, total, metodo, descripcion):
        self.nombre = nombre
        self.ci = ci
        self.fecha = datetime.now()
        self.hotel = hotel
        self.total = float(total)
        self.metodo = metodo
        self.desc = descripcion

"""ARBOL AVL PARA FACTURAS"""
class nodo:
   def __init__(self, data):
      self.data = data
      self.left = None
      self.right = None
      self.height = 1
      
class arbol:

    def __init__(self) -> None:
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)
   
    def _insert(self, root, key):
        if not root:
            return nodo(key)
        elif key.total < root.data.total:
            root.left = self._insert(root.left, key)
        else:
            root.right = self._insert(root.right, key)
        root.h = 1 + max(self.getHeight(root.left),
            self.getHeight(root.right))
        b = self.getBalance(root)
        if b > 1 and key < root.left.data:
            return self.rightRotate(root)
        if b < -1 and key > root.right.data:
            return self.leftRotate(root)
        if b > 1 and key > root.left.data:
            root.left = self.lefttRotate(root.left)
            return self.rightRotate(root)
        if b < -1 and key < root.right.data:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
        return root
   
    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
            self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
            self.getHeight(y.right))
        return y
   
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
            self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
            self.getHeight(y.right))
        return y
   
    def getHeight(self, root):
        if not root:
            return 0
        return root.height
    
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)
   
    def code(self):
        with open('facturas_serializadas.pkl', 'wb') as archivo:
            pickle.dump(self.root, archivo)

    def decode(self):
        with open('facturas_serializadas.pkl', 'rb') as archivo:
            self.root = pickle.load(archivo)
    
    """Este es el metodo para imprimir la informacion obteniendo la factura"""
    def postorden(self, nodo, param = None, key = None):
        if nodo is not None:
            self.postorden(nodo.left, param, key)
            self.postorden(nodo.right, param, key)

            if key is not None:
                if key(nodo.data) == param:
                    facturar(nodo.data)
            else:
                facturar(nodo.data)



def facturar(n):
    print(f"""
    ************************************
        FACTURA DEL: {n.fecha.day}/{n.fecha.month}/{n.fecha.year}
        HORA: {n.fecha.hour}:{n.fecha.minute}
        HOTEL {n.hotel}
        CLIENTE {n.nombre}

        TOTAL: {n.total}
        METODO DE PAGO: {n.metodo}

        {n.desc}""")
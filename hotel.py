import csv
import datetime
import os
import random
import pickle

class Pila:
    def __init__(self):
        self.tope = None
    
    def esta_vacia(self):
        return self.tope is None
    
    def agregarPila(self,valor):
        nodo_nuevo = Nodo(valor)
        nodo_nuevo.siguiente = self.tope
        self.tope = nodo_nuevo
    
    def recorrerPila(self):
        if self.esta_vacia():
            print("La pila está vacía")
        else:
            self._recorrer_aux(self.tope)
    
    def _recorrer_aux(self,nodo):
        while nodo:
            print("|FECHA|: ",nodo.valor.fecha,"|MÓDULO|: ",nodo.valor.modulo,"|ERROR|: ",nodo.valor.tipo)
            nodo = nodo.siguiente
    
    def recorrer2(self):
        if self.esta_vacia():
            print("La pila está vacía")
        else:
            self.aux2(self.tope)
    
    def aux2(self, nodo):
        while nodo:
            print("|FECHA| : ", nodo.valor.fecha,"|ACCIÓN| : ",nodo.valor.modulo)
            nodo = nodo.siguiente
    
    def exportar_a_archivo(self, archivo):
        with open(archivo, 'a', newline='',encoding="UTF-8") as file:
            writer = csv.writer(file)
            actual = self.tope
            while actual:
                accion = actual.valor
                writer.writerow([accion.fecha, accion.modulo, accion.tipo])
                actual = actual.siguiente
    
    def exportar_a_archivo2(self, archivo):
        with open(archivo, 'a', newline='',encoding="UTF-8") as file:
            writer = csv.writer(file)
            actual = self.tope
            while actual:
                accion = actual.valor
                writer.writerow([accion.fecha, accion.modulo])
                actual = actual.siguiente

def incializar():
    opcion = []
    valores = []
    try:
        with open(control.rta_cfg, "r") as doc:
            reader = csv.reader(doc,delimiter=";")
            for fila in reader:
                opcion.append(f"HOTEL: {fila[2]}, CONFIGURACION: {fila[1]}")
                valores.append(fila)

            op = menu("Seleccione una configuracion:",opcion,valores)
            
            control.id, control.cond, control.desc, control.rta_hotel, control.rta_hoteles = op
            control.id = int(control.id)
    except FileNotFoundError as e:
        print("\nNo es encontro el archivo de configuracion, verifique la ruta\n")
        listarErrores(errores,"Lectura del archivo",e)
        main()

def modificar():
    op = False
    lista = []
    with open(control.rta_cfg, "r") as doc:
        reader = csv.reader(doc,delimiter=";")
        for fila in reader:
            lista.append(fila)
    
    n = int(control.id) - 1
    op = menu("Indique que dato desea modificar: ",["Orden", "Descripcion", "Ruta del archivo de reservaciones", "Ruta del hotel"],[1,2,3,4])
    if op == 1:
        lista[n][1] = menu("Indique en que orden se organizaran los datos",["Ascendente","Descendente"],["asc","des"])
    if op == 2:
        lista[n][2] = input("Escriba la nueva descripcion: ")
    if op == 3:
        lista[n][3] = input("Escriba la nueva ruta del archivo de reservaciones: ")
    if op == 4:
        lista[n][4] = input("Escriba la nueva ruta del archivo del hotel: ")

    with open(control.rta_cfg, "w", newline="") as doc:
        writer = csv.writer(doc, delimiter=";")
        writer.writerows(lista)

    control.id, control.cond, control.desc, control.rta_hotel, control.rta_hoteles = lista[n]

    print("Operacion realizada exitosamente\n")

def modificar2(nombre, campo, valor):
    with open(control.rta_hoteles, "r") as doc:
        reader = csv.reader(doc,delimiter=";")
        datos = list(reader)

    with open(control.rta_hoteles, "w", newline="") as doc:
        writer = csv.writer(doc, delimiter=";")
        for hotel in datos:
            if hotel[0] == nombre:
                hotel[campo] = valor
            writer.writerow(hotel)

def crear():
    id = 0
    cfg = menu("Indique en que orden se organizaran los datos",["Ascendente","Descendente"],["asc","des"])
    desc = input("Escriba la nueva descripcion: ")
    ruta = input("Escriba la nueva ruta del archivo de reservaciones: ")
    ruta2 = input("Escriba la nueva ruta del archivo de hoteles: ")
    ruta3 = input("Escriba la nueva ruta del archivo de habitaciones: ")

    with open(control.rta_cfg, "r") as doc:
        reader = csv.reader(doc,delimiter=";")
        for i in reader:
            id += 1

    with open(control.rta_cfg, "a", newline="") as doc:
        writer = csv.writer(doc, delimiter=";")
        writer.writerow([id, cfg, desc, ruta,ruta2])

def crear2(nombre, hab, tel, dir):
    datos = [nombre, hab, tel, dir]
    with open(control.rta_hoteles, "r") as doc:
        reader = csv.reader(doc,delimiter=";")

    with open(control.rta_hoteles, "a", newline="") as doc:
        writer = csv.writer(doc, delimiter=";")
        writer.writerow(datos)

def borrar(nombre):
    with open(control.rta_hoteles, "r") as doc:
        reader = csv.reader(doc,delimiter=";")
        datos = list(reader)

    with open(control.rta_hoteles, "w", newline="") as doc:
        writer = csv.writer(doc, delimiter=";")
        for hotel in datos:
            if hotel[0] != nombre:
                writer.writerow(hotel)


"""Funcion que te crea un menu
    le tienen que enviar el mensaje de lo que pide, una lista de las opciones que va a mostrar,
    y una lista de valores que va a devolver
    
    EJ: se elije la opcion 6 de la lista de opciones, entonces devuelve el valor 6 de la lista de valores"""
def menu(msg, opciones, valores):
    c = 1
    op = 0
    print(msg)
    for i in opciones:
        print(f"    ({c}) - {i}")
        c += 1

    while op - 1 not in range(len(valores)):
        op = int(input("\n> "))

        if op - 1 in range(len(valores)):
            print()
            return(valores[op-1])
        print("Ingrese una opcion valida")

"""Bueno de aqui para abajo va todo lo relacionado a lo que es creacion modificacion y listado de Hoteles y Habitaciones """
class Nodo:
    def __init__(self,valor=None):
        self.valor = valor
        self.siguiente = None

class Hotel:
    def __init__(self, nombre, num_habitaciones, num_telf,direccion):
        self.nombre = nombre
        self.num_telf = num_telf
        self.num_habitaciones = num_habitaciones
        self.direccion = direccion

class Habitacion:
    def __init__(self, nombreC,nombreH, numero, tipo, disponible):
        self.nombreC = nombreC
        self.nombreH = nombreH
        self.numero = numero
        self.tipo = tipo
        self.disponible = disponible

class Error:
    def __init__(self, fecha, modulo, tipo):
        self.fecha = fecha
        self.modulo = modulo
        self.tipo = tipo

class Acción:
    def __init__(self,fecha,modulo):
        self.fecha = fecha
        self.modulo = modulo

class Empleado:
    def __init__(self,nombre, apellido ,posicion,salario,fecha, hotel):
        self.nombre = nombre
        self.apellido = apellido
        self.posicion = posicion
        self.salario = salario
        self.fecha = fecha
        self.hotel = hotel

    def __lt__(self, otro_empleado):
        return self.salario < otro_empleado.salario
        

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.longitud = 0
    def agregar(self,valor):
        nuevo_nodo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def imprimir_hoteles(self):
        actual = self.cabeza
        cadena = "| {:<20} | {:<15} | {:<15} | {:<20} |"
        print(cadena.format("NOMBRE", "HABITACIONES", "TELÉFONO", "DIRECCIÓN"))
        while actual:
            hotel = actual.valor
            print(cadena.format(hotel.nombre, hotel.num_habitaciones, hotel.num_telf, hotel.direccion))
            actual = actual.siguiente

    def buscar_por_nombre(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.valor.nombre == nombre:
                return actual.valor
            actual = actual.siguiente
        return None
    
    def modificar_atributo(self, nombre, atributo, nuevo_valor):
        objeto = self.buscar_por_nombre(nombre)
        if objeto:  # Si el objeto existe
            setattr(objeto, atributo, nuevo_valor)
        else:
            print(f"No se encontró el hotel {nombre} en la lista.")
            
    def eliminar(self, nombre):
        obj_a_eliminar = self.buscar_por_nombre(nombre)
        if obj_a_eliminar is None:
            print(f"No se encontró ningún objeto con el nombre {nombre} en la lista.")
            return
        anterior = None
        actual = self.cabeza
        while actual:
            if actual.valor == obj_a_eliminar:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                self.longitud -= 1
                print(f"Se eliminó el objeto {str(actual.valor)} de la lista.")
                return
            anterior = actual
            actual = actual.siguiente

"""Aqui termina"""

"""ARBOL BINARIO"""
class NodoArbol:
    def __init__(self,dato):
        self.valor = dato
        self.derecha = None
        self.izquierda = None

class Arbol:
    def __init__(self):
        self.raiz = None
    
    def agregar(self, dato):
        if self.raiz is None:
            self.raiz = NodoArbol(dato)
        else:
            self.agregarR(dato, self.raiz)

    def agregarR(self, dato, nodo_actual):
        if dato.nombre < nodo_actual.valor.nombre:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = NodoArbol(dato)
            else:
                self.agregarR(dato, nodo_actual.izquierda)
        elif dato.nombre > nodo_actual.valor.nombre:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = NodoArbol(dato)
            else:
                self.agregarR(dato, nodo_actual.derecha)
        else:
            pass
    def eliminar(self, nombre):
        self.raiz = self._eliminar_recursivo(nombre, self.raiz)

    def _eliminar_recursivo(self, nombre, nodo_actual):
        if nodo_actual is None:
            return None
        if nombre < nodo_actual.valor.nombre:
            nodo_actual.izquierda = self._eliminar_recursivo(nombre,nodo_actual.izquierda)
        elif nombre > nodo_actual.valor.nombre:
            nodo_actual.derecha = self._eliminar_recursivo(nombre,nodo_actual.derecha)
        else:
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha
            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda
            else:
                sucesor = self._encontrar_minimo(nodo_actual.derecha)
                nodo_actual.valor = sucesor.valor
                nodo_actual.derecha = self._eliminar_recursivo(sucesor.valor.nombre, nodo_actual.derecha)
        return nodo_actual
    
    def _encontrar_minimo(self, nodo_actual):
        if nodo_actual.izquierda is None:
            return nodo_actual
        return self._encontrar_minimo(nodo_actual.izquierda)
    
    def modificarArbol(self, nombre, atributo,cambio):
        nodo = self.buscar(nombre)
        if nodo:
            setattr(nodo.valor, atributo, cambio)

    def buscar(self, nombre):
        return self._buscar_recursivo(nombre, self.raiz)
    
    def _buscar_recursivo(self, nombre, nodo_actual):
        if nodo_actual is None or nodo_actual.valor.nombre == nombre:
            return nodo_actual
        if nombre < nodo_actual.valor.nombre:
            return self._buscar_recursivo(nombre, nodo_actual.izquierda)
        return self._buscar_recursivo(nombre, nodo_actual.derecha)
    
    def serializar(self, nombre_archivo):
        with open(nombre_archivo, 'wb') as archivo:
            pickle.dump(self.raiz, archivo)
    @classmethod
    def deserializar(cls, nombre_archivo):
        arbol = Arbol()
        with open(nombre_archivo, 'rb') as archivo:
            arbol.raiz = pickle.load(archivo)
        return arbol
    
    def recorrer_en_profundidad(arbol):
        if arbol is None:
            return
        pila = []
        pila.append(arbol.raiz)

        while len(pila) > 0:
            nodo = pila.pop()
            print(cadena2.format(nodo.valor.nombre, nodo.valor.apellido, nodo.valor.posicion, nodo.valor.salario, nodo.valor.fecha, nodo.valor.hotel))

            if nodo.izquierda is not None:
                pila.append(nodo.izquierda)
            if nodo.derecha is not None:
                pila.append(nodo.derecha)
def igualdad(nodo1, nodo2):
        return nodo1.valor.hotel == nodo2.valor.hotel

"""ARBOL AVL PARA FACTURAS"""
class AVLNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insertArbol(self, data):
        self.root = self._inserta(data, self.root)

    def _inserta(self, data, node):
        if node is None:
            return AVLNode(data)
        if data < node.data:
            node.left = self._inserta(data, node.left)
        else:
            node.right = self._inserta(data, node.right)
        node.height = 1 + max(self.altura(node.left), self.altura(node.right))
        balance = self.balance(node)
        if balance > 1:
            if data < node.left.data:
                return self.rotaDer(node)
            else:
                return self._left_right_rotate(node)
        if balance < -1:
            if data > node.right.data:
                return self.rotaIzq(node)
            else:
                return self._right_left_rotate(node)
        return node
    
    def altura(self, node):
        if node is None:
            return 0
        return node.height
    
    def balance(self, node):
        if node is None:
            return 0
        return self.altura(node.left) - self.altura(node.right)
    
    def rotaDer(self, node):
        hijoIzq = node.left
        node.left = hijoIzq.right
        hijoIzq.right = node
        node.height = 1 + max(self.altura(node.left), self.altura(node.right))
        hijoIzq.height = 1 + max(self.altura(hijoIzq.left), self.altura(hijoIzq.right))
        return hijoIzq
        
    def rotaIzq(self, nodoDer):
        hijoDer = nodoDer.right
        nodoDer.right = hijoDer.left
        hijoDer
   

"""COLAS"""

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class Cola:
    def __init__(self):
        self.frente = None
        self.fin = None
        
    def esta_vacia(self):
        return self.frente is None
    
    def eliminar(self):
        if self.esta_vacia():
            return None
        else:
            valor_eliminado = self.frente.valor
            self.frente = self.frente.siguiente
            if self.frente is None:
                self.fin = None
            return valor_eliminado
        
    def agregar(self, valor):
        nodo_nuevo = Nodo(valor)
        if self.esta_vacia():
            self.frente = nodo_nuevo
        else:
            self.fin.siguiente = nodo_nuevo
        self.fin = nodo_nuevo

    def ver_frente(self):
        if self.esta_vacia():
            return None
        else:
            return self.frente.valor
        
    def recorrer(self, x = False):
        if self.esta_vacia():
            print("La cola está vacía")
        else:
            if x:
                self._recorrer_lista(self.frente)
            else:
                linea = header()

                self._recorrer_print(self.frente)

                print(linea + "\n")
    
    def _recorrer_lista(self, nodo):
        if nodo is not None:
            r = nodo.valor
            control.lista_cola.append([r.id, r.nombre, r.cedula, r.habitacion, r.tipo, str(r.precio), r.num_personas, convertir_fecha(r.reserva), convertir_fecha(r.entrada), convertir_fecha(r.salida), r.hotel])
            self._recorrer_lista(nodo.siguiente)

    def _recorrer_print(self, nodo):
        if nodo is not None:
            r = nodo.valor
            print_cadena(r)
            self._recorrer_print(nodo.siguiente)

    def recorrer_por_parametro(self, param, key):
        if self.esta_vacia():
            print("La cola está vacía")
        else:
            linea = header()

            self._recorrer_parametro_auxiliar(self.frente, param, key)

            print(linea + "\n")
            input("Presione ENTER para continuar ")
    
    def _recorrer_parametro_auxiliar(self, nodo, param, key):
        if nodo is not None:
            r = nodo.valor
            if param == key(r):
                print_cadena(r)
            self._recorrer_parametro_auxiliar(nodo.siguiente, param, key)

def print_cadena(r):
    print(cadena.format(r.id, r.nombre, r.cedula, r.habitacion, r.tipo, str(r.precio), r.num_personas,Reservacion.re_clientes[r.cedula], imprimir_fecha(r.reserva), imprimir_fecha(r.entrada), imprimir_fecha(r.salida), r.duracion)) 


class control:
    cond = ""
    desc = ""
    rta_cfg = ""
    rta_hotel = ""
    rta_hoteles = ""
    rta_empleado = ""
    val_rta = False
    
    cola = Cola()
    lista_cola = []

    def __init__(self, lista):
        self.lista = lista

    """ALGORITMO SHELLSHORT PARA ORGANIZAR POR NUM DE RESERVACIONES (2)
        UTILIZA DICCIONARIO re_clientes PARA COMPARAR"""
    
    def shellSort(self, lista, n):
        dic = Reservacion.re_clientes
        interval = n // 2

        while interval > 0:
            for i in range(interval, n):
                temp = lista[i]
                j = i
                while j >= interval and control.compare(dic[lista[j - interval].cedula], dic[temp.cedula]):
                    lista[j] = lista[j - interval]
                    j -= interval
                lista[j] = temp
            interval //= 2

    @staticmethod
    def compare(x, y):
        if control.cond == "asc":
            return x > y
        
        if control.cond == "des":
            return x < y

    """HEAPSORT"""
    def heapify_two_swap(self,lista, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and control.compare(lista[left].duracion, lista[largest].duracion):
            largest = left

        if right < n and control.compare(lista[right].duracion, lista[largest].duracion):
            largest = right

        if largest != i:
            if largest == left:
                lista[i], lista[left] = lista[left], lista[i]
            else:
                lista[i], lista[right] = lista[right], lista[i]
                lista[left], lista[right] = lista[right], lista[left]
            self.heapify_two_swap(lista, n, largest)


    def heapSort(self, lista):
        n = len(lista)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify_two_swap(lista, n, i)

        for i in range(n - 1, 0, -1):
            lista[i], lista[0] = lista[0], lista[i]  # swap
            self.heapify_two_swap(lista, i, 0)
            
"""QUICKSORT"""
def quicksort(lista, inicio, fin, key=lambda x: x.habitacion):
    if inicio < fin:
        p = particionar(lista, inicio, fin, key=key)
        quicksort(lista, inicio, p - 1, key=key)
        quicksort(lista, p + 1, fin, key=key)

def particionar(lista, inicio, fin, key=lambda x: x.habitacion):
    pivote = key(lista[inicio])
    i = inicio + 1
    j = fin
    while i <= j:
        if control.cond == "asc":
            while i <= j and key(lista[i]) <= pivote:
                i += 1
            while i <= j and key(lista[j]) > pivote:
                j -= 1
        if control.cond == "des":
            while i <= j and key(lista[i]) >= pivote:
                i += 1
            while i <= j and key(lista[j]) < pivote:
                j -= 1
        if i <= j:
            lista[i], lista[j] = lista[j], lista[i]
            i += 1
            j -= 1
    lista[inicio], lista[j] = lista[j], lista[inicio]
    return j

"""MERGESORT"""
def merge_sort(list, compare_func):
    list_length = len(list)
    if list_length == 1:
        return list
    mid_point = list_length // 2
    left_partition = merge_sort(list[:mid_point], compare_func)
    right_partition = merge_sort(list[mid_point:], compare_func)
    return merge(left_partition, right_partition, compare_func)

def merge(left, right, compare_func):
    output = []
    i = j = 0
    while i < len(left) and j < len(right):
        if compare_func(left[i], right[j]):
            output.append(left[i])
            i += 1
        else:
            output.append(right[j])
            j += 1
    output.extend(left[i:])
    output.extend(right[j:])
    return output

""""""
class Reservacion:
    re_clientes = {}
    """Diccionario que guarda el numero de reservaciones que tiene el cliente
       Se accede usando - Reservacion.re_clientes -"""

    def __init__(self,id, nombre, cedula, habitacion, tipo, precio, num_personas, reserva, entrada, salida, hotel):
        self.id = id
        self.nombre = nombre
        self.cedula = cedula
        self.habitacion = habitacion
        self.tipo = tipo
        self.precio = float(precio)
        self.num_personas = num_personas
        self.reserva = fecha(reserva)
        self.entrada = fecha(entrada)
        self.salida = fecha(salida)
        self.hotel = hotel
        self.duracion = calcular_duracion(fecha(entrada),fecha(salida))

        """IF que busca si la cedula del cliente esta en el diccionario, si esta le asigna 1
           si no le suma 1"""
        if cedula not in Reservacion.re_clientes.keys():
            Reservacion.re_clientes[cedula] = 1
        else:
            Reservacion.re_clientes[cedula] += 1

def leerArchivo(personas, x = False):
    try:
        if x:
            control.cola = Cola()
        
        with open(control.rta_hotel,"r", encoding="UTF-8") as archivo:
            lector_csv = csv.reader(archivo,delimiter=";")
            Reservacion.re_clientes = {}

            for fila in lector_csv:
                iden, nombre, cedula, habitacion, tipo, precio, num_personas, reserva, entrada, salida, hotel = fila
                #Las variables se pueden asignar solas, si tiene el mismo numero de datos

                reservacion = Reservacion(iden, nombre, cedula, habitacion, tipo, precio, num_personas, reserva, entrada, salida, hotel)

                personas.append(reservacion)

                if x:
                    control.cola.agregar(reservacion)

        control.val_rta = True
        return personas
        
    except FileNotFoundError as e:
        print("No se encontro el archivo del hotel, favor verificar la ruta\n")
        listarErrores(errores, "Lectura del archivo", e)
        control.val_rta = False

def guardar_reservaciones():

    control.cola.recorrer(True)

    with open(control.rta_hotel, "w", newline="", encoding="UTF-8") as doc:
        writer = csv.writer(doc, delimiter=";")
        writer.writerows(control.lista_cola)

def leer_hoteles(hoteles):
        with open(control.rta_hoteles,"r", encoding="UTF-8") as archivo:
            lector_csv = csv.reader(archivo,delimiter=";")

            for fila in lector_csv:
                nombreHotel, nHabitacion, nTelefono, direccion = fila

                hotel = Hotel(nombreHotel, nHabitacion, nTelefono, direccion)
                hoteles.agregar(hotel)
        return hoteles

def listarErrores(lista, mod, e):
    fecha = datetime.datetime.now()
    error = Error(fecha,mod,e)
    lista.agregarPila(error)

def listarAcciones(lista, mod):
    fecha =  datetime.datetime.now()
    accion = Acción(fecha,mod)
    lista.agregarPila(accion)



def imprimir_fecha(fecha):
    return "{}-{}-{}".format(fecha.day, fecha.month, fecha.year)

def header(x = False):
    linea = ""
    for i in [8,16,12,5,12,10,13,18,12,25,17]: # LOS ELEMENTOS DE LA LISTA SON LAS LONGUITUDES
        linea += "+" + "-"*i
    linea += "+"

    if x:
        return linea

    print(linea)
    print("| ID     | NOMBRE         | CEDULA     | HAB | TIPO       | PRECIO   | N° PERSONAS | N° RESERVACIONES | RESERVA    |     ENTRADA - SALIDA    | DURACION (DIAS) |")
    print(linea)

    return linea

def imprimir(personas = None):
    if control.cola.esta_vacia():
        print("NO HAY DATOS QUE MOSTRAR\n") 
        return

    if personas == None:
        linea = header(True)
        control.cola.recorrer()
    else:
        linea = header()
        for r in personas:
            print(cadena.format(r.id, r.nombre, r.cedula, r.habitacion, r.tipo, str(r.precio), r.num_personas,Reservacion.re_clientes[r.cedula], imprimir_fecha(r.reserva), imprimir_fecha(r.entrada), imprimir_fecha(r.salida), r.duracion)) 
        print(linea + "\n")
    input("Presione ENTER para continuar ")
    print()
  
def imprimir_habitacion(personas):
    # Ahora imprime solo la habitacion de cada reserva
    for r in personas:
        print(r.habitacion)

def fecha(texto):
    fecha = datetime.datetime.strptime(texto, '%d/%m/%Y')
    fecha2 = fecha.date()
    return fecha2

def calcular_duracion(fecha_entrada, fecha_salida):
    # Convertimos las fechas a objetos datetime
    diferencia = fecha_salida - fecha_entrada
    # Devolvemos la duración en días
    return diferencia.days

def convertir_fecha(fecha):
    return "{}/{}/{}".format(fecha.day, fecha.month, fecha.year)

def imprimir_r(personas, f1, f2=None):
    lista = []
    for r in personas:
        f3 = r.reserva
        if f2:
            if f1 <= f3 <= f2:
                lista.append(r)
        else:
            if f3 == f1:
                lista.append(r)
    imprimir(lista)

def compare_reservaciones(reservacion1, reservacion2):
    if control.cond == "asc":
        return reservacion1.precio < reservacion2.precio
    elif control.cond == "des":
        return reservacion1.precio > reservacion2.precio

def generar_id():
    return random.randint(100000,999999)

def listado():
    try:
        imprimir()
        # imprimir(personas.lista)
        listarAcciones(acciones,"Se imprimieron los datos")
    except Exception as e:
        print("\nSucedio un error")
        listarErrores(errores,"Impresión",e)

def gestion_reservas(lista_hoteles):
    try:
        subopciones = ['Crear', 'Eliminar', 'Listar','Buscar']
        submenu = menu('SELECCIONE UNA OPCIÓN', subopciones, [1,2,3,4])

        if submenu == 1:
            try:
                hotel = input('Diga para que hotel es esta reservacion: ')

                objeto = lista_hoteles.buscar_por_nombre(hotel)
                if objeto:  #1 Si el objeto existe
                    iden = generar_id()
                    nombre = input('Ingrese el nombre del cliente: ')
                    cedula = input('Ingrese la cedula del cliente: ')
                    habitacion = input('Ingrese la habitacion: ')
                    int(habitacion)
                    tipo = input('Ingrese el tipo de habitacion: ')
                    precio = input('Ingrese el precio de la habitacion: ')
                    float(precio)
                    num_personas = input('Ingrese el numero de personas: ')
                    int(num_personas)
                    reserva = input('Que dia fue la resrvacion? (dd/mm/AAAA):')
                    fecha(reserva)
                    entrada = input('Ingrese la fecha de entrada (dd/mm/AAAA):')
                    fecha(entrada)
                    salida = input('Ingrese la fecha de salida (dd/mm/AAAA):')
                    fecha(salida)

                    reservacion = Reservacion(iden, nombre, cedula, habitacion, tipo, precio, num_personas, reserva, entrada, salida, hotel)

                    control.cola.agregar(reservacion)
                    print("Operacion Exitosa")
                    listarAcciones(acciones,f"Se creó una nueva reserva en el hotel {hotel}")
                else:
                    print(f"No se encontró el hotel {hotel} en la lista.")

            except ValueError as e:
                print('\nPor favor introduzca un numero/fecha valida\n')
                listarErrores(errores,"Gestión de reserva", e)


        if submenu == 2:
            if control.cola.esta_vacia():
                print('No hay reservaciones disponibles')
            else:
                res = control.cola.ver_frente()
                msg = f'Desea la eliminar la reservacion de {res.nombre}, reservado el dia {res.reserva} ?'

                submenu = menu(msg, ['si', 'no'], [True, False])

                if submenu:
                    control.cola.eliminar()
                    print('Operacion realizada exitosamente')
                    listarAcciones(acciones,"Se eliminó una reserva")
                else:
                    print('Operacion cancelada')

        if submenu == 3:
            hotel = input('Diga para de cual hotel se va a listar las reservaciones: ')
            print()

            objeto = lista_hoteles.buscar_por_nombre(hotel)
            if objeto:  #1 Si el objeto existe
                control.cola.recorrer_por_parametro(hotel, key=lambda x: x.hotel)
                listarAcciones(acciones, 'Listado de Hoteles')
            else:
                print(f"No se encontró el hotel {hotel} en la lista.")

        try:
            if submenu == 4:
                subopcion = menu('Por cual parametro desea buscar?',['Nombre','Cedula','Habitacion',
                                'Tipo de Habitacion','Precio','Numero de Personas','Fecha de Reserva','Fecha de Entrada','Fecha de Salida'], [1,2,3,4,5,6,7,8,9])
                
                param = input('Diga el valor a buscar\n > ')

                if subopcion == 5: param = int(param)                            
                if subopcion in [7,8,9]: param = fecha(param)

                if subopcion == 1: control.cola.recorrer_por_parametro(param, key=lambda x: x.nombre)
                if subopcion == 2: control.cola.recorrer_por_parametro(param, key=lambda x: x.cedula)
                if subopcion == 3: control.cola.recorrer_por_parametro(param, key=lambda x: x.habitacion)
                if subopcion == 4: control.cola.recorrer_por_parametro(param, key=lambda x: x.tipo)
                if subopcion == 5: control.cola.recorrer_por_parametro(param, key=lambda x: x.precio)
                if subopcion == 6: control.cola.recorrer_por_parametro(param, key=lambda x: x.num_personas)
                if subopcion == 7: control.cola.recorrer_por_parametro(param, key=lambda x: x.reserva)
                if subopcion == 8: control.cola.recorrer_por_parametro(param, key=lambda x: x.entrada)
                if subopcion == 9: control.cola.recorrer_por_parametro(param, key=lambda x: x.salida)
                listarAcciones(acciones,'Busqueda Completada')

        except ValueError as e:
                print('\nPor favor introduzca un dato valido\n')
                listarErrores(errores,"Gestión de reserva", e)

    except Exception as e:
        print("\nIngrese un valor correcto")
        listarErrores(errores,"Gestión de reserva", e)

def gestion_hoteles(lista_hoteles):
    try:
        subopciones = ['Crear', 'Modificar', 'Listar', 'Eliminar']
        submenu = menu('SELECCIONE UNA OPCIÓN', subopciones, [1,2,3,4])

        if submenu == 1:
            nombre = input("Ingrese el nombre del hotel: ")
            habitaciones = input("Ingrese el número de habitaciones disponibles: ")
            telefono = input("Ingrese el número de teléfono del hotel: ")
            direccion = input("Ingrese la dirección del hotel: ")
            hotel = Hotel(nombre,habitaciones,telefono,direccion)
            lista_hoteles.agregar(hotel)
            crear2(nombre,habitaciones,telefono,direccion)
            print("\n\nCreado con éxito")
            listarAcciones(acciones,f"Se creo el hotel {nombre}")

        if submenu == 2:
            subopciones2 = ['Nombre', 'Habitacion', 'Teléfono', 'Dirección']

            submenu2 = menu('SELECCIONE UNA OPCIÓN', subopciones2, [1,2,3,4])
            nombre = input("\nEscriba el nombre del hotel: ")

            if submenu2 == 1:
                nuevo_valor = input("Escriba el nuevo nombre del hotel: ")
                atributo = "nombre"
            if submenu2 == 2:
                nuevo_valor = input("Escriba el nuevo número de habitaciones disponibles del hotel: ")
                atributo = "num_habitaciones"
            if submenu2 == 3:
                nuevo_valor = input("Escriba el nuevo número de teléfono del hotel: ")
                atributo = "num_telf"
            if submenu2 == 4:
                nuevo_valor = input("Escriba la nueva dirección del hotel: ")
                atributo = "direccion"    
            lista_hoteles.modificar_atributo(nombre, atributo, nuevo_valor)
            modificar2(nombre,(submenu2-1),nuevo_valor)
            print("\n\nModificado con éxito")
            listarAcciones(acciones,f"Se modificó un atributo del hotel {nombre}")

        if submenu == 3: 
            lista_hoteles.imprimir_hoteles()
            listarAcciones(acciones,"Se imprimió la lista de hoteles")

        if submenu == 4:
            nombre = input("Ingrese el nombre del hotel que quiere eliminar: ")
            lista_hoteles.eliminar(nombre)    
            borrar(nombre)
            listarAcciones(acciones,f"Se eliminó el hotel {nombre}")
    except Exception as e:
        print("\nIngrese un valor correcto")
        listarErrores(errores, "Gestión de hoteles", e)

def gestion_archivos():
    try:
        if opcion == 4:
            opcion = menu('ELIGA UNA OPCION: ', ['Cambiar','Modificar','Crear','Cambiar ruta'], [1,2,3,4])

            if opcion == 1: 
                incializar()
                listarAcciones(acciones, "Cambiar configuración")

            if opcion == 2: 
                modificar()
                listarAcciones(acciones, "Se modificó la configuración")

            if opcion == 3: 
                crear()
                listarAcciones(acciones, "Se creó la configuración")

            if opcion == 4: 
                inicializar_archivos()
                listarAcciones(acciones, "Cambiar ruta de archivo de configuracion")
    except Exception as e:
        print("\nIngrese un valor correcto")
        listarErrores(errores, "Configuración de archivos", e)

def algoritmos_ordenamiento(personas):
    try:
        subopciones = ['Selección de Criterios de Ordenamiento', "Ordenamiento Múltiple",
                'Ordenamiento por rango y precio (MERGESORT)', 
                "Ordenamiento por numero de reservas (SHELLSORT) ", "Ordenamiento por duracion de estancia (HEAPSORT)"]
        
        opcion = menu('Que Algoritmo desea utilizar?', subopciones, [1,2,3,4,5])

        if opcion == 1:
                subopciones = ['Ordenar por fecha de entrada', 'Ordenar por habitación']
                submenu = menu('SELECCIONES UNA OPCIÓN', subopciones, [1,2])
                f1 = input("Fecha (dd/mm/AAAA): ")
                fd1 = fecha(f1)
                if submenu == 1:
                    quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.entrada)
                    imprimir_r(personas.lista,fd1)
                    listarAcciones(acciones, "Ordenamiento múltiple - Fecha de entrada")
                elif submenu == 2:
                    quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.habitacion)
                    imprimir_r(personas.lista,fd1)
                    listarAcciones(acciones, "Ordenamiento múltiple - Habitación")
                else:
                    print("\nSeleccione una opción valida")  

    
        if opcion == 2:
                subopciones = ['Ordenar por fecha de entrada', 'Ordenar por habitación', 'Ordenar por duración de la estadía']
                submenu = menu('SELECCIONES UNA OPCIÓN', subopciones, [1,2,3])
                f1 = input("Fecha (dd/mm/AAAA): ")
                fd1 = fecha(f1)
                if submenu == 1:
                    quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.entrada)
                    imprimir_r(personas.lista,fd1)
                    listarAcciones(acciones, "Selección de criterios - Fecha de entrada")
                elif submenu == 2:
                    quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.habitacion)
                    imprimir_r(personas.lista,fd1)
                    listarAcciones(acciones, "Selección de criterios - Habitación")
                elif submenu == 3:
                    quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.duracion)
                    imprimir_r(personas.lista,fd1)
                    listarAcciones(acciones, "Selección de criterios - Duración")
                else:
                    print("\nIngrese una opción valida") 

        if opcion == 3:
                f1 = input("Rango inferior (dd/mm/AAAA): ")
                f2 = input("Rango superior (dd/mm/AAAA): ")
                fd1 = fecha(f1)
                fd2 = fecha(f2)
                if fd2 > fd1:
                    sorted = merge_sort(personas.lista,compare_reservaciones)
                    print("\n\n")
                    print("En el rango de ",f1, " a ", f2)
                    imprimir_r(sorted,fd1,fd2)
                    listarAcciones(acciones, "Ordenamiento por rango y precio")
                else:
                    print("\nRango no válido")
                print("\nEl valor ingresado no es válido, use el formato dd/mm/AAAA")
                
        if opcion == 4:
            personas.shellSort(personas.lista, len(personas.lista))
            imprimir(personas.lista)
            listarAcciones(acciones, "Ordenamiento por número de reservas")

        if opcion == 5:
            personas.heapSort(personas.lista)
            imprimir(personas.lista)
            listarAcciones(acciones, "Ordenamiento por duración de estancia")

    except Exception as e:
        print("\nIngrese un valor correcto")
        listarErrores(errores,"Algoritmos de ordenamiento", e)

def gestionEmpleados(Arbol):
    try:
        subopciones = ['Crear', 'Modificar', 'Listar', 'Eliminar']
        submenu = menu('SELECCIONE UNA OPCIÓN', subopciones, [1,2,3,4])
        if submenu == 1:
                nombre = input("Ingrese el nombre del empleado: ")
                apellido = input("Ingrese el apellido del empleado: ")
                posicion = input("Ingrese la posicion del empleado: ")
                salario = input("Ingrese el salario del empleado: ")
                fecha = input("Ingrese la fehca de contratación del empleado: ")
                nhotel = input("Ingrese el hotel donde trabaja el empleado: ")
                empleado = Empleado(nombre,apellido,posicion,salario,fecha,nhotel)
                Arbol.agregar(empleado)
                print("\n\nCreado con éxito")
                listarAcciones(acciones,f"Se creo el registro del empleado {nombre} {apellido}")
        if submenu == 2:
            subopciones2 = ['Nombre','Apellido','Salario', 'Posición', 'Fecha','Hotel']
            submenu2 = menu('SELECCIONE UNA OPCIÓN', subopciones2, [1,2,3,4,5,6])
            nombre = input("Ingrese el nombre del empleado: ")
            if submenu2 == 1:
                atributo = "nombre"
            if submenu2 == 2:
                atributo = "apellido"
            if submenu2 == 3:
                atributo = "salario"
            if submenu2 == 4:
                atributo = "posicion"
            if submenu2 == 5:
                atributo = "fecha"
            if submenu2 == 6:
                atributo = "hotel"
            nuevo = input(f"Ingrese el nuevo dato ({atributo}): ")
            Arbol.modificarArbol(nombre, atributo ,nuevo)
            print("\n\nModificado con éxito")
            listarAcciones(acciones,f"Se modificó el registro del empleado {nombre}")
        if submenu == 3:
            try:
                nhotel = input("Ingrese el hotel: ")
                print(cadena2.format("NOMBRE","APELLIDO","POSICIÓN","SALARIO","FECHA", "HOTEL"))
                Arbol.recorrer_en_profundidad()
                listarAcciones(acciones,"Se mostró la lista de empleados")
                Arbol.serializar("arbol_serializado.pkl")
            except AttributeError as e:
                print("\nLista vacia")
                listarErrores(errores,"Gestion de empleados", e)
        if submenu == 4:
            nombre = input("Ingrese el nombre del empleado: ")
            Arbol.eliminar(nombre)
            print("\n\nEliminado con éxito")
            listarAcciones(acciones,"Se eliminó un registro de la lista de empleados")
    except Exception as e:
        print("\nIngrese un valor correcto")
        listarErrores(errores,"Gestion de empleados", e)


def main():

    incializar() # CARGA EL ARCHIVO DE CONFIGURACION
    hoteles = ListaEnlazada()
    lista_hoteles = leer_hoteles(hoteles)
    arbolb = Arbol()
    

    personas = control(leerArchivo([], True))

    while True:
        #try:
            val = control.val_rta

            if control.cond == "asc": con = "Ascendente"
            if control.cond == "des": con = "Descendente"
            print(f"\nDESC: {control.desc}\nCFG: {con}\nRUTA: {control.rta_hotel}\n")

            
            opciones = ['Imprimir datos','Gestion de Reservaciones','Gestion de Hoteles', "Gestion de Archivos", 'Algortimos de Ordenamiento',
                        "Historial de errores","Historial de acciones","Gestión de empleados",'Terminar']
            opcion = menu("SELECCIONE UNA OPCIÓN: ", opciones, [1,2,3,4,5,6,7,8,9])
            

            if opcion == 1 and val: listado()

            """--------------------------------GESTION DE RESERVAS-------------------------"""
            if opcion == 2 and val: gestion_reservas(lista_hoteles)
                
            """--------------------------------GESTION DE HOTELES--------------------------"""
            if opcion == 3 and val: gestion_hoteles(lista_hoteles)

            """"---------------------------------GESTION DE ARCHIVOS DE CONFIGURACION------"""
            if opcion == 4 and val: gestion_archivos()

            """-------------------ALGORTIMOS DE ORDENAMIENTO---------------------"""
            if opcion == 5 and val: algoritmos_ordenamiento(personas)

            """----------------------LISTADO---------------------"""
            if opcion == 6: 
                errores.recorrerPila()
                errores.exportar_a_archivo("errores.csv")
                listarAcciones(acciones, "Listado de errores")

            if opcion == 7:
                acciones.recorrer2()
                acciones.exportar_a_archivo2("acciones.csv")
            
            if opcion == 8:
                gestionEmpleados(arbolb)

            if opcion == 9:
                print("Sesion Terminada")
                break

            personas = control(leerArchivo([])) # Lo pongo aqui para que se actualize la re despues de cada operacion
            """se sobreescribe el archivo hotel.csv"""


        #except Exception as e:
            #print("\nValor inválido, introduzca solo numeros")
            #listarErrores(errores,"Menu",e)

    guardar_reservaciones()

def inicializar_archivos():
    #try:
        op = menu("Utilizar la ruta por defecto del archivo de configuracion?",["Si","No"],[True,False])
        if op:
            control.rta_cfg = str(os.path.abspath(os.getcwd())) + "\config.csv"
        else:
            control.rta_cfg = input("Ingrese la ruta del archivo de configuracion: ")

        main() # <------------///

    #except Exception as e:
        #print("\nValor inválido, introduzca solo numeros")
        #listarErrores(errores,"Menu",e)

errores = Pila()
acciones = Pila()
cadena = "| {:<6} | {:<15}| {:<10} | {:>3} | {:<10} | {:>8} | {:>11} |{:>17} | {:<10} | {:<10} - {:>10} | {:>15} |"
cadena2 = "| {:<12} | {:<12} | {:<8} | {:<8} | {:<12} | {:<15} |"

inicializar_archivos()
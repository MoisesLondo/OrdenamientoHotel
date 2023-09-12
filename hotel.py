import csv
import datetime
class control:
    condicion = "d" # < ------------- MIENTRAS
    def __init__(self, lista):
        self.lista = lista

    """ALGORITMO SHELLSHORT PARA ORGANIZAR POR NUM DE RESERVACIONES (2)
        UTILIZA DICCIONARIO re_clientes PARA COMPARAR"""

    """SHELLSORT"""
    def shellSort(self, lista, n):
        dic = Reservacion.re_clientes
        interval = n // 2

        while interval > 0:
            for i in range(interval, n):
                temp = lista[i]
                j = i
                while j >= interval and control.shellsort_compare(dic[lista[j - interval].nombre], dic[temp.nombre]):
                    lista[j] = lista[j - interval]
                    j -= interval
                lista[j] = temp
            interval //= 2

    @staticmethod
    def shellsort_compare(x, y):
        if control.condicion == "a":
            return x > y
        
        if control.condicion == "d":
            return x < y

    """HEAPSORT"""
    def heapify(self, lista, n, i):
        largest = i  
        l = 2 * i + 1  
        r = 2 * i + 2  

        if l < n and lista[i].duracion < lista[l].duracion:
            largest = l

        if r < n and lista[largest].duracion < lista[r].duracion:
            largest = r
        
        if largest != i:
            lista[i], lista[largest] = lista[largest], lista[i]  # swap
            # Heapify the root.
            self.heapify(lista, n, largest)


    def heapSort(self, lista):
        n = len(lista)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(lista, n, i)

        for i in range(n - 1, 0, -1):
            lista[i], lista[0] = lista[0], lista[i]  # swap
            self.heapify(lista, i, 0)
            
"""QUICKSORT"""
def quicksort(lista, inicio, fin, key=lambda x: x.habitacion):
    if inicio < fin:
        pivote = lista[(inicio + fin) // 2]
        i = inicio
        j = fin
        while i < j:
            while key(lista[i]) < key(pivote) and i < fin:
                i += 1   
            while key(lista[j]) > key(pivote):
                j -= 1
            if i < j:
                lista[i], lista[j] = lista[j], lista[i]
                i += 1
                j -= 1
        quicksort(lista, inicio, i, key=key)
        quicksort(lista, i + 1, fin, key=key)

def particionar(lista, inicio, fin, key=lambda x: x.habitacion):
    i = inicio + 1
    j = fin
    while i <= j:
        pivote = lista[(inicio + fin) // 2]
        while key(lista[j]) <= key(pivote):
            j -= 1

        if i <= j:
            lista[i], lista[j] = lista[j], lista[i]
            i += 1
            j -= 1
    return i + 1


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

    def __init__(self,id, nombre, habitacion, tipo, precio, num_personas, reserva, entrada, salida, duracion):
        self.id = id
        self.nombre = nombre
        self.habitacion = habitacion
        self.tipo = tipo
        self.precio = float(precio)
        self.num_personas = num_personas
        self.reserva = reserva
        self.entrada = entrada
        self.salida = salida
        self.duracion = int(duracion)

        """IF que busca si el nombre del cliente esta en el diccionario, si esta le asigna 1
           si no le suma 1"""
        if nombre not in Reservacion.re_clientes.keys():
            Reservacion.re_clientes[nombre] = 1
        else:
            Reservacion.re_clientes[nombre] += 1

def leerArchivo(personas):
    with open("hotel.csv","r", encoding="UTF-8") as archivo:
        lector_csv = csv.reader(archivo,delimiter=";")
        for fila in lector_csv:
            iden, nombre, habitacion, tipo, precio, num_personas, reserva, entrada, salida, duracion = fila
            #Las variables se pueden asignar solas, si tiene el mismo numero de datos

            reservacion = Reservacion(iden, nombre, habitacion, tipo, precio, num_personas, reserva, entrada, salida, duracion)
            personas.append(reservacion)
    return personas

def imprimir(personas):
    for r in personas:

        print(" | ".join([r.id, r.nombre, r.habitacion, r.tipo, str(r.precio), r.num_personas, r.reserva, r.entrada, r.salida, str(r.duracion)])) 
  
def imprimir_habitacion(personas):
    # Ahora imprime solo la habitacion de cada reserva
    for r in personas:
        print(r.habitacion)

def fecha(texto):
    fecha = datetime.datetime.strptime(texto, '%d/%m/%Y')
    fecha2 = fecha.date()
    return fecha2

def imprimir_r(personas,f1,f2):
    for r in personas:
        f3 = fecha(r.reserva)
        if f3>= f1 and f3 <= f2:
            print(" | ".join([r.id, r.nombre, r.habitacion, r.tipo, str(r.precio), r.num_personas, r.reserva, r.entrada, r.salida, str(r.duracion)])) 

def compare_reservaciones(reservacion1, reservacion2):
    return reservacion1.precio < reservacion2.precio

def main():
    while True:
        personas = control(leerArchivo([])) # Lo pongo aqui para que se actualize la re despues de cada operacion

        print(
        """
        Seleccione una opcion:
        1 - Imprimir datos
        2 - SHELLSORT (por n de reservas) 
        3 - QUICKSORT (Prueba tambien XD) BRUUH
        4 - Ordenamiento por rango
        5 - HEAPSORT (por duracion)
        0 - salir
        """)
        
        opcion = int(input("> "))

        if opcion == 1:
            imprimir(personas.lista)

        if opcion == 2:
            print("ORIGINAL:\n")
            imprimir(personas.lista)
            print("SHELLSORT:\n")
            personas.shellSort(personas.lista, len(personas.lista))
            imprimir(personas.lista)
            print("\nORGANIZADO POR NUMERO DE RESERVACIONES\ncondicion: "+control.condicion)

        if opcion == 3:
            quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.habitacion)
            imprimir(personas.lista)

        if opcion == 4:
            try:
                f1 = input("Rango inferior (dd/mm/AAAA): ")
                f2 = input("Rango superior (dd/mm/AAAA): ")
                fd1 = fecha(f1)
                fd2 = fecha(f2)
                if fd2 > fd1:
                    sorted = merge_sort(personas.lista,compare_reservaciones)
                    print("\n\n")
                    print("En el rango de ",f1, " a ", f2)
                    imprimir_r(sorted,fd1,fd2)
                else:
                    print("\nRango no válido")
            except Exception as e:
                print("\nEl valor ingresado no es válido, use el formato dd/mm/AAAA")

        if opcion == 5:
            personas.heapSort(personas.lista)
            imprimir(personas.lista)

        if opcion == 0:
            break

main()

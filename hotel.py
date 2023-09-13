import csv
import datetime
import os

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
            
            control.id, control.cond, control.desc, control.rta_hotel = op
            control.id = int(control.id)
    except FileNotFoundError:
        print("No es encontro el archivo de configuracion, verifique la ruta\n")
        main()

def modificar():
    op = False
    lista = []
    with open(control.rta_cfg, "r") as doc:
        reader = csv.reader(doc,delimiter=";")
        for fila in reader:
            lista.append(fila)
    
    n = int(control.id) - 1
    op = menu("Indique que dato desea modificar: ",["Orden", "Descripcion", "Ruta del archivo"],[1,2,3])
    if op == 1:
        lista[n][1] = menu("Indique en que orden se organizaran los datos",["Ascendente","Descendente"],["asc","des"])
    if op == 2:
        lista[n][2] = input("Escriba la nueva descripcion: ")
    if op == 3:
        lista[n][3] = input("Escriba la nueva ruta del archivo: ")

    with open(control.rta_cfg, "w", newline="") as doc:
        writer = csv.writer(doc, delimiter=";")
        writer.writerows(lista)

    control.id, control.cond, control.desc, control.rta_hotel = lista[n]

    print("Operacion realizada exitosamente\n")

def crear():
    id = 0
    cfg = menu("Indique en que orden se organizaran los datos",["Ascendente","Descendente"],["asc","des"])
    desc = input("Escriba la nueva descripcion: ")
    ruta = input("Escriba la nueva ruta del archivo: ")

    with open(control.rta_cfg, "r") as doc:
        reader = csv.reader(doc,delimiter=";")
        for i in reader:
            id += 1

    with open(control.rta_cfg, "a", newline="") as doc:
        writer = csv.writer(doc, delimiter=";")
        writer.writerow([id, cfg, desc, ruta])

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

class control:
    cond = ""
    desc = ""
    rta_cfg = ""
    rta_hotel = ""
    val_rta = False

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
        if control.cond == "asc:":
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

    def __init__(self,id, nombre, cedula, habitacion, tipo, precio, num_personas, reserva, entrada, salida):
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
        self.duracion = calcular_duracion(fecha(entrada),fecha(salida))

        """IF que busca si la cedula del cliente esta en el diccionario, si esta le asigna 1
           si no le suma 1"""
        if cedula not in Reservacion.re_clientes.keys():
            Reservacion.re_clientes[cedula] = 1
        else:
            Reservacion.re_clientes[cedula] += 1

def leerArchivo(personas):
    try:
        with open(control.rta_hotel,"r", encoding="UTF-8") as archivo:
            lector_csv = csv.reader(archivo,delimiter=";")
            Reservacion.re_clientes = {}

            for fila in lector_csv:
                iden, nombre, cedula, habitacion, tipo, precio, num_personas, reserva, entrada, salida= fila
                #Las variables se pueden asignar solas, si tiene el mismo numero de datos

                reservacion = Reservacion(iden, nombre, cedula, habitacion, tipo, precio, num_personas, reserva, entrada, salida)
                personas.append(reservacion)
        control.val_rta = True
        return personas
    except FileNotFoundError:
        print("No se encontro el archivo del hotel, favor verificar la ruta\n")
        control.val_rta = False

def imprimir_fecha(fecha):
    return "{}-{}-{}".format(fecha.day, fecha.month, fecha.year)

def imprimir(personas):
    if len (personas) == 0:
        print("NO HAY DATOS QUE MOSTRAR\n") 
        return
    
    linea = ""
    for i in [8,16,12,5,12,10,13,18,12,25,17]: # LOS ELEMENTOS DE LA LISTA SON LAS LONGUITUDES
        linea += "+" + "-"*i
    linea += "+"

    print(linea)
    print("| ID     | NOMBRE         | CEDULA     | HAB | TIPO       | PRECIO   | N° PERSONAS | N° RESERVACIONES | RESERVA    |     ENTRADA - SALIDA    | DURACION (DIAS) |")
    print(linea)

    cadena = "| {:<6} | {:<15}| {:<10} | {:>3} | {:<10} | {:>8} | {:>11} |{:>17} | {:<10} | {:<10} - {:>10} | {:>15} |"

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

    """Moi cambie tu vaina para que sea compatible con la funcion de la tabla, igual es una estupidez XD"""

def compare_reservaciones(reservacion1, reservacion2):
    if control.cond == "asc":
        return reservacion1.precio < reservacion2.precio
    elif control.cond == "des":
        return reservacion1.precio > reservacion2.precio

def main(val = True):
    op = menu("Utilizar la ruta por defecto del archivo de configuracion?",["Si","No"],[True,False])
    if op:
        control.rta_cfg = str(os.path.abspath(os.getcwd())) + "\config.csv"
    else:
        control.rta_cfg = input("Ingrese la ruta del archivo de configuracion: ")


    incializar() # CARGA EL ARCHIVO DE CONFIGURACION

    while True:
        personas = control(leerArchivo([])) # Lo pongo aqui para que se actualize la re despues de cada operacion
        val = control.val_rta

        if control.cond == "asc": con = "Ascendente"
        if control.cond == "des": con = "Descendente"

        print(f"\nDESC: {control.desc}\nCFG: {con}\nRUTA: {control.rta_hotel}\n")

        opciones = ['Imprimir datos','Selección de Criterios de Ordenamiento', "Ordenamiento Múltiple",
                    'Ordenamiento por rango y precio (MERGESORT)', 
                    "Ordenamiento por numero de reservas (SHELLSORT) ", "Ordenamiento por duracion de estancia (HEAPSORT)",
                    "Cambiar configuracion","Modificar Configuracion Actual","Crear Configuracion",
                    "Cambiar ruta de archivo de configuracion"]
        
        opcion = menu("SELECCIONE UNA OPCIÓN: ", opciones, [1,2,3,4,5,6,7,8,9,10])

        if opcion == 1 and val:
            imprimir(personas.lista)

        if opcion == 2 and val:
            subopciones = ['Ordenar por fecha de entrada', 'Ordenar por habitación']
            submenu = menu('SELECCIONES UNA OPCIÓN', subopciones, [1,2])
            f1 = input("Fecha (dd/mm/AAAA): ")
            fd1 = fecha(f1)
            if submenu == 1:
                quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.entrada)
                imprimir_r(personas.lista,fd1)
            elif submenu == 2:
                quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.habitacion)
                imprimir_r(personas.lista,fd1)      
    
        if opcion == 3 and val:
            subopciones = ['Ordenar por fecha de entrada', 'Ordenar por habitación', 'Ordenar por duración de la estadía']
            submenu = menu('SELECCIONES UNA OPCIÓN', subopciones, [1,2,3])
            f1 = input("Fecha (dd/mm/AAAA): ")
            fd1 = fecha(f1)
            if submenu == 1:
                quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.entrada)
                imprimir_r(personas.lista,fd1)
            elif submenu == 2:
                quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.habitacion)
                imprimir_r(personas.lista,fd1)
            elif submenu == 3:
                quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.duracion)
                imprimir_r(personas.lista,fd1)
            else:
                print("Ingrese una opción valida")

        if opcion == 4 and val:
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

        if opcion == 5 and val:
            personas.shellSort(personas.lista, len(personas.lista))
            imprimir(personas.lista)

        if opcion == 6 and val:
            personas.heapSort(personas.lista)
            imprimir(personas.lista)

        if opcion == 7: incializar()

        if opcion == 8: modificar()

        if opcion == 9: crear()

        if opcion == 10: main()

main()
import csv
import datetime
import os

lista_errores = []
lista_acciones = []

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
        lista_errores.append([datetime.datetime.now(), "lectura del archivo", e])
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
    def __init__(self, numero, tipo, disponible):
        self.numero = numero
        self.tipo = tipo
        self.disponible = disponible

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
        
    def recorrer(self):
        if self.esta_vacia():
            print("La cola está vacía")
        else:
            self._recorrer_aux(self.frente)

    def _recorrer_aux(self, nodo):
        if nodo is not None:
            r = nodo.valor
            cadena = "| {:<6} | {:<15}| {:<10} | {:>3} | {:<10} | {:>8} | {:>11} |{:>17} | {:<10} | {:<10} - {:>10} | {:>15} |"
            print(cadena.format(r.id, r.nombre, r.cedula, r.habitacion, r.tipo, str(r.precio), r.num_personas,Reservacion.re_clientes[r.cedula], imprimir_fecha(r.reserva), imprimir_fecha(r.entrada), imprimir_fecha(r.salida), r.duracion)) 
            self._recorrer_aux(nodo.siguiente)

class control:
    cond = ""
    desc = ""
    rta_cfg = ""
    rta_hotel = ""
    rta_hoteles = ""
    val_rta = False
    
    cola = Cola()

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
        control.cola = Cola()
        
        with open(control.rta_hotel,"r", encoding="UTF-8") as archivo:
            lector_csv = csv.reader(archivo,delimiter=";")
            Reservacion.re_clientes = {}

            for fila in lector_csv:
                iden, nombre, cedula, habitacion, tipo, precio, num_personas, reserva, entrada, salida= fila
                #Las variables se pueden asignar solas, si tiene el mismo numero de datos

                reservacion = Reservacion(iden, nombre, cedula, habitacion, tipo, precio, num_personas, reserva, entrada, salida)
                personas.append(reservacion)
                control.cola.agregar(reservacion)
        control.val_rta = True
        return personas
        
    except FileNotFoundError as e:
        print("No se encontro el archivo del hotel, favor verificar la ruta\n")
        lista_errores.append([datetime.datetime.now(), "lectura del archivo", e])
        control.val_rta = False

def guardarArchivo1():
    pass

def leerArchivo2(hoteles):
        with open(control.rta_hoteles,"r", encoding="UTF-8") as archivo:
            lector_csv = csv.reader(archivo,delimiter=";")

            for fila in lector_csv:
                nombreHotel, nHabitacion, nTelefono, direccion = fila

                hotel = Hotel(nombreHotel, nHabitacion, nTelefono, direccion)
                hoteles.agregar(hotel)
        return hoteles

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
    
    cola.recorrer()

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

def compare_reservaciones(reservacion1, reservacion2):
    if control.cond == "asc":
        return reservacion1.precio < reservacion2.precio
    elif control.cond == "des":
        return reservacion1.precio > reservacion2.precio

def main():
    try:

        op = menu("Utilizar la ruta por defecto del archivo de configuracion?",["Si","No"],[True,False])
        if op:
            control.rta_cfg = str(os.path.abspath(os.getcwd())) + "\config.csv"
        else:
            control.rta_cfg = input("Ingrese la ruta del archivo de configuracion: ")

        incializar() # CARGA EL ARCHIVO DE CONFIGURACION
        hoteles = ListaEnlazada()
        lista_hoteles = leerArchivo2(hoteles)

        while True:
            personas = control(leerArchivo([])) # Lo pongo aqui para que se actualize la re despues de cada operacion
            val = control.val_rta

            if control.cond == "asc": con = "Ascendente"
            if control.cond == "des": con = "Descendente"


            print(f"\nDESC: {control.desc}\nCFG: {con}\nRUTA: {control.rta_hotel}\n")
            
            opciones = ['Imprimir datos','Gestion de Reservaciones','Gestion de Hoteles', "Gestion de Archivos", 'Algortimos de Ordenamiento',
                        "Historial de errores","Historial de acciones",'Terminar']
            
            opcion = menu("SELECCIONE UNA OPCIÓN: ", opciones, [1,2,3,4,5,6,7,8])

            if opcion == 1 and val:
                imprimir(personas.lista)
                lista_acciones.append([datetime.datetime.now(), "Acción: Se imprimieron los datos"])

            """--------------------------------GESTION DE RESERVAS-------------------------"""
            if opcion ==2:
                subopciones = ['Agregar','Eliminar','Buscar']

            """--------------------------------GESTION DE HOTELES--------------------------"""
            if opcion == 3:
                subopciones = ['Crear', 'Modificar', 'Listar', 'Eliminar']
                submenu = menu('SELECCIONES UNA OPCIÓN', subopciones, [1,2,3,4])

                if submenu == 1:
                    nombreHotel = input("Ingrese el nombre del hotel: ")
                    nHabitaciones = input("Ingrese el número de habitaciones disponibles: ")
                    nTelefono = input("Ingrese el número de teléfono del hotel: ")
                    direccion = input("Ingrese la dirección del hotel: ")
                    newHotel = Hotel(nombreHotel,nHabitaciones,nTelefono,direccion)
                    lista_hoteles.agregar(newHotel)
                    crear2(nombreHotel,nHabitaciones,nTelefono,direccion)
                    print("\n\nCreado con éxito")

                if submenu == 2:
                    subopciones2 = ['Nombre', 'Habitacion', 'Teléfono', 'Dirección']

                    submenu2 = menu('SELECCIONES UNA OPCIÓN', subopciones2, [1,2,3,4])
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

                if submenu == 3: 
                    lista_hoteles.imprimir_hoteles()

                if submenu == 4:
                    nombre = input("Ingrese el nombre del hotel que quiere eliminar: ")
                    lista_hoteles.eliminar(nombre)    
                    borrar(nombre)


            """"---------------------------------GESTION DE ARCHIVOS DE CONFIGURACION-----------------------------------"""
            if opcion == 4:
                opcion = menu('ELIGA UNA OPCION: ', ['Cambiar','Modificar','Crear','Cambiar ruta'], [1,2,3,4])

                if opcion == 1: 
                    incializar()
                    lista_acciones.append([datetime.datetime.now(), "Acción: Cambiar configuracion"])

                if opcion == 2: 
                    modificar()
                    lista_acciones.append([datetime.datetime.now(), "Acción: Modificar Configuracion Actual"])

                if opcion == 3: 
                    crear()
                    lista_acciones.append([datetime.datetime.now(), "Acción: Crear Configuracion"])

                if opcion == 4: 
                    main()
                    lista_acciones.append([datetime.datetime.now(), "Acción: Cambiar ruta de archivo de configuracion"])


            """-------------------ALGORTIMOS DE ORDENAMIENTO---------------------"""
            if opcion == 5 and val:

                subopciones = ['Selección de Criterios de Ordenamiento', "Ordenamiento Múltiple",
                        'Ordenamiento por rango y precio (MERGESORT)', 
                        "Ordenamiento por numero de reservas (SHELLSORT) ", "Ordenamiento por duracion de estancia (HEAPSORT)"]
                
                opcion = menu('Que Algoritmo desea utilizar?', subopciones, [1,2,3,4,5])

                if opcion == 1 and val:
                    try:
                        subopciones = ['Ordenar por fecha de entrada', 'Ordenar por habitación']
                        submenu = menu('SELECCIONES UNA OPCIÓN', subopciones, [1,2])
                        f1 = input("Fecha (dd/mm/AAAA): ")
                        fd1 = fecha(f1)
                        if submenu == 1:
                            quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.entrada)
                            imprimir_r(personas.lista,fd1)
                            lista_acciones.append([datetime.datetime.now(), "Acción: Ordenamiento Múltiple - Fecha de entrada"])
                        elif submenu == 2:
                            quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.habitacion)
                            imprimir_r(personas.lista,fd1)
                            lista_acciones.append([datetime.datetime.now(), "Acción: Ordenamiento Múltiple - Habitación"])
                        else:
                            print("\nSeleccione una opción valida")  
                    except Exception as e:
                        print("\nEl valor ingresado no es válido")
                        lista_errores.append([datetime.datetime.now(), "Ordenamiento Múltiple", e])      
            
                if opcion == 2 and val:
                    try:
                        subopciones = ['Ordenar por fecha de entrada', 'Ordenar por habitación', 'Ordenar por duración de la estadía']
                        submenu = menu('SELECCIONES UNA OPCIÓN', subopciones, [1,2,3])
                        f1 = input("Fecha (dd/mm/AAAA): ")
                        fd1 = fecha(f1)
                        if submenu == 1:
                            quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.entrada)
                            imprimir_r(personas.lista,fd1)
                            lista_acciones.append([datetime.datetime.now(), "Acción: Selección de Criterios - Fecha de entrada"])
                        elif submenu == 2:
                            quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.habitacion)
                            imprimir_r(personas.lista,fd1)
                            lista_acciones.append([datetime.datetime.now(), "Acción: Selección de Criterios - Habitación"])
                        elif submenu == 3:
                            quicksort(personas.lista, 0, len(personas.lista)-1, key=lambda x: x.duracion)
                            imprimir_r(personas.lista,fd1)
                            lista_acciones.append([datetime.datetime.now(), "Acción: Selección de Criterios - Duración"])
                        else:
                            print("\nIngrese una opción valida")
                    except Exception as e:
                        print("\nEl valor ingresado no es válido")
                        lista_errores.append([datetime.datetime.now(), "Criterios de Ordenamiento", e]) 

                if opcion == 3 and val:
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
                            lista_acciones.append([datetime.datetime.now(), "Acción: Ordenamiento por rango y precio"])
                        else:
                            print("\nRango no válido")
                    except Exception as e:
                        print("\nEl valor ingresado no es válido, use el formato dd/mm/AAAA")
                        lista_errores.append([datetime.datetime.now(), "Ordenamiento por rango y precio", e])
                        
                if opcion == 4 and val:
                    personas.shellSort(personas.lista, len(personas.lista))
                    imprimir(personas.lista)
                    lista_acciones.append([datetime.datetime.now(), "Acción: Ordenamiento por número de reservas"])

                if opcion == 5 and val:
                    personas.heapSort(personas.lista)
                    imprimir(personas.lista)
                    lista_acciones.append([datetime.datetime.now(), "Acción: Ordenamiento por duración de estancia"])

            """----------------------LISTADO---------------------"""
            if opcion == 6: 
                for i in lista_errores:
                    print(i)

            if opcion == 7:
                for i in lista_acciones:
                    print(i)

            if opcion == 8:
                print("Sesion Terminada")
                break
        
        """se sobreescribe el archivo hotel.csv"""
        guardarArchivo1()


    except ValueError as e:
        print("\nValor inválido, introduzca solo numeros/n")
        lista_errores.append([datetime.datetime.now(), "Menu", e])
        main()


main()
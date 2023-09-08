import csv

class control:
    def __init__(self, lista):
        self.lista = lista

    """ALGORITMO SHELLSHORT PARA ORGANIZAR POR NUM DE RESERVACIONES (2)
        UTILIZA DICCIONARIO re_clientes PARA COMPARAR"""
    
    """ASCENDENTE"""
    def shellSort_a(self, lista, n):
        dic = Reservacion.re_clientes
        interval = n // 2

        while interval > 0:
            for i in range(interval, n):
                temp = lista[i]
                j = i
                while j >= interval and dic[lista[j - interval].nombre] > dic[temp.nombre]:
                    lista[j] = lista[j - interval]
                    j -= interval
                lista[j] = temp
            interval //= 2
    """DESCENDENTE"""
    def shellSort_d(self, lista, n):
        dic = Reservacion.re_clientes
        interval = n // 2

        while interval > 0:
            for i in range(interval, n):
                temp = lista[i]
                j = i
                while j >= interval and dic[lista[j - interval].nombre] < dic[temp.nombre]:
                    lista[j] = lista[j - interval]
                    j -= interval
                lista[j] = temp
            interval //= 2
class Reservacion:
    re_clientes = {} 
    """Diccionario que guarda el numero de reservaciones que tiene el cliente
       Se accede usando - Reservacion.re_clientes -"""

    def __init__(self,id, nombre, habitacion, tipo, precio, num_personas, reserva, entrada, salida, duracion):
        self.id = id
        self.nombre = nombre
        self.habitacion = habitacion
        self.tipo = tipo
        self.precio = precio
        self.num_personas = num_personas
        self.reserva = reserva
        self.entrada = entrada
        self.salida = salida
        self.duracion = duracion

        """IF que busca si el nombre del cliente esta en el diccionario, si esta le asigna 1
           si no le suma 1"""
        if nombre not in Reservacion.re_clientes.keys():
            Reservacion.re_clientes[nombre] = 1
        else:
            Reservacion.re_clientes[nombre] += 1

def leerArchivo(personas):
    with open("hotel.csv","r") as archivo:
        lector_csv = csv.reader(archivo,delimiter=";")
        for fila in lector_csv:
            iden, nombre, habitacion, tipo, precio, num_personas, reserva, entrada, salida, duracion = fila
            #Las variables se pueden asignar solas, si tiene el mismo numero de datos

            reservacion = Reservacion(iden, nombre, habitacion, tipo, precio, num_personas, reserva, entrada, salida, duracion)
            personas.append(reservacion)
    return personas

def imprimir(personas):
    # Ahora imprime los nuevos datos (esto hay que cambiarlo despues para que lo imprima como tabla)
    for r in personas:
        print(" | ".join([r.id, r.nombre, r.habitacion, r.tipo, r.precio, r.num_personas, r.reserva, r.entrada, r.salida, r.duracion]))
        
def main():
    while True:
        personas = control(leerArchivo([])) # Lo pongo aqui para que se actualize la re despues de cada operacion

        print(
        """
        Seleccione una opcion:
        1 - Imprimir datos
        2 - SHELLSORT (PRUEBA)
        0 - salir
        """)
        
        opcion = int(input("> "))

        if opcion == 1:
            imprimir(personas)

        if opcion == 2:
            print("ORIGINAL:\n")
            imprimir(personas.lista)
            print("SHELLSORT (ascendente):\n")
            personas.shellSort_a(personas.lista, len(personas.lista))
            imprimir(personas.lista)
            print("SHELLSORT (descendente):\n")
            personas.shellSort_d(personas.lista, len(personas.lista))
            imprimir(personas.lista)
            print("\nORGANIZADO POR NUMERO DE RESERVACIONES")

        if opcion == 0:
            break
main()
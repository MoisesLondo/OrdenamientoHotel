import csv

class Reservacion:
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
        # Agregue los datos que faltaban

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
        personas = leerArchivo([]) # Lo pongo aqui para que se actualize la lista despues de cada operacion 

        print(
        """
        Seleccione una opcion:
        1 - Imprimir datos
        0 - salir
        """)
        
        opcion = int(input("> "))

        if opcion == 1:
            imprimir(personas)
main()
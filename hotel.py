import csv
class Reservacion:
    def __init__(self,nombre, edad,fecha):
        self.nombre = nombre
        self.edad = edad
        self.fecha = fecha

def leerArchivo(personas):
    with open("hotel.csv","r") as archivo:
        lector_csv = csv.reader(archivo,delimiter=";")
        for fila in lector_csv:
            nombre = fila[0]
            edad = fila[1]
            fecha = fila[2]
            reservacion = Reservacion(nombre,edad,fecha)
            personas.append(reservacion)
    return personas
def imprimir(personas):
    for r in personas:
        print(r.nombre, r.edad, r.fecha)
def main():
    while True:

        print(
    """
    Seleccione una opcion:
    1 - Imprimir datos
    0 - salir
    """)
        opcion = int(input("> "))

        if opcion == 1:
            personas = []
            leerArchivo(personas)
            imprimir(personas)
main()
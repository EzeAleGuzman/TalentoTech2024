from Menu import MostrarMenu
from colorama import Fore
from negocio import agregar,verProductos


MostrarMenu()
while (True):
    try:
        opcion = int(input(Fore.RESET + "Ingrese una opción: "))
    except ValueError:
        print(Fore.RED + "Ingrese un número válido")
        continue
    
    if opcion == 7:
        print(Fore.RED + "##### Gracias por usar la app #####")
        break
    elif (opcion == 1):
        print(Fore.RED+"Ingrese los datos del producto")
        nombre = input('Nombre del producto: ')
        cantidad = int(input('Ingrese la cantidad de producto: '))
        agregar(nombre,cantidad)
    elif (opcion == 2):
        print(Fore.BLUE+"-----------Productos---------")
        verProductos()
    else:
        print('Ingrese Una opcion valida')
    MostrarMenu()
    opcion = int(input())
print(Fore.BLACK)  


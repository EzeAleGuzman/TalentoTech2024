from Menu import MostrarMenu
from colorama import Fore
from negocio import *


MostrarMenu()
while (True):
    try:
        opcion = int(input(Fore.RESET + "Ingrese una opción: "))
    except ValueError:
        print(Fore.RED + "Ingrese un número válido")
        continue
    
    if opcion == 8:
        print(Fore.RED + "##### Gracias por usar la app #####")
        break
    elif (opcion == 1):
        print(Fore.RED+"Ingrese los datos del producto")
        nombre = input('Nombre del producto: ')
        cantidad = int(input('Ingrese la cantidad de producto: '))
        agregar(nombre,cantidad)
    elif (opcion == 2):
        print(Fore.BLUE+"-"* 35 +"Productos"+ "-" * 35)
        verProductos()
    elif (opcion == 3):
        print(Fore.CYAN+"-----------Compra de Productos---------")
        codigo = int(input("Ingrese codigo del producto:  "))
        cantidad = int(input("Ingrese la cantidad de producto comprado:  "))
        comprar(codigo,cantidad)
    elif (opcion == 4):
        print(Fore.CYAN+"-----------Venta de Productos---------")
        codigo = int(input("Ingrese codigo del producto:  "))
        cantidad = int(input("Ingrese la cantidad de producto comprado:  "))
        vender(codigo,cantidad)      
    else:
        print('Ingrese Una opcion valida')
    MostrarMenu()
print(Fore.BLACK)  


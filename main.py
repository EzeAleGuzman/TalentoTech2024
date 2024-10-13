
from colorama import Fore
from negocio.productos_negocio import *
from negocio.cliente_negocio import *
from negocio.proveedores_negocio import *
from utilitys import *

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
        codigo = int(input('Ingrese el codigo del producto: '))
        nombre = input('Nombre del producto: ')
        descripcion = (input('Ingrese breve descripcion: '))
        precio = float(input("Ingrese el precio de Venta: "))
        costo = float(input("Ingrese Precio de costo: "))
        agregar(codigo, nombre, descripcion, precio, costo)
    elif (opcion == 2):
        print(Fore.BLUE+"-"* 35 +"Productos"+ "-" * 35)
        verProductos()
    elif (opcion == 3):
        comprar()
    elif (opcion == 4):
        print(Fore.CYAN+"-----------Venta de Productos---------")
        codigo = int(input("Ingrese codigo del producto:  "))
        cantidad = int(input("Ingrese la cantidad de producto comprado:  "))
        vender(codigo,cantidad)
    elif (opcion == 5):
        codigo = int(input("Ingrese codigo del producto que desea eliminar:  "))
        eliminarProducto(codigo)
    elif (opcion == 6):
        nombre = input("Cual es el nombre del producto que deseas buscar").lower()
        buscarPorNombre(nombre) 
    elif (opcion == 7):
        verificarBajoStock()
    else:
        print('Ingrese Una opcion valida')
    MostrarMenu()

print(Fore.BLACK)  


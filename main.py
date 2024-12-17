
from colorama import Fore
from negocio.productos_negocio import *
from negocio.cliente_negocio import *
from negocio.proveedores_negocio import *
from utilitys import *
import os


def limpiar_consola():
    os.system('cls')


MostrarMenu()
while (True):
    try:
        opcion = int(input(Fore.RESET + "Ingrese una opción: "))
    except ValueError:
        print(Fore.RED + "Ingrese un número válido")
        continue
    
    limpiar_consola()
    
    if opcion == 9:
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
        print(Fore.BLUE+" Productos ".center(50, "-"))
        verProductos()
    elif (opcion == 3):
        print(Fore.BLUE+" Actualizar Producto ".center(50, "-"))
        print(Fore.LIGHTRED_EX +"Si desea omitir un campo solo dejelo vacio".center(50, "#"))
        print(Fore.RESET)
        codigo = int(input("Ingrese el codigo del producto: "))

        producto = buscarProducto(codigo)
        if producto is None:

            print(Fore.RED + "Producto no encontrado")
            print(Fore.RESET + "*"*50)
            print(Fore.RESET + "-"*50)
        else:
            print(Fore.LIGHTYELLOW_EX + f"Producto encontrado Nombre:  {producto[1]}".center(50, "-"))
            nombre = input("Ingrese el nombre del producto : ") or None
            descripcion = input("Ingrese la descripcion del producto: ") or None
            #Si stock no es un numero valido, se asigna None,tambien cuando se dea el campo vacio
            try:
                stock = int(input("Ingrese el stock del producto: ")) or None
            except  ValueError:
                stock = None
            try:
                precio = float(input("Ingrese el precio del producto: ")) or None
            except ValueError:
                precio = None
            try:
                costo = float(input("Ingrese el costo del producto: ")) or None
            except ValueError:
                costo = None
            actualizarProducto(codigo, nombre, descripcion, stock, precio, costo)
    elif (opcion == 4):
        comprar()
    elif (opcion == 5):
        print(Fore.CYAN+"-----------Venta de Productos---------")
        vender()
    elif (opcion == 6):
        codigo = int(input("Ingrese codigo del producto que desea eliminar:  "))
        eliminarProducto(codigo)
    elif (opcion == 7):
        nombre = input("Cual es el nombre del producto que deseas buscar").lower()
        buscarPorNombre(nombre) 
    elif (opcion == 8):
        verificarBajoStock()
    else:
        print(' Ingrese Una opcion valida '.center(50, "*"))
    MostrarMenu()

print(Fore.BLACK)  


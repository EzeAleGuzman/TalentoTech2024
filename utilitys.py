from beautifultable import BeautifulTable
from colorama import Fore


#funcion para crear una tabla
def crearTabla(productos):
    try:
        table = BeautifulTable()
        table.columns.header = ["Codigo", "nombre", "descripcion", "stock"]
        # Imprimimos los productos
        for producto in productos:
            table.rows.append(producto)
        print(table)
    #maneja la excepcion y la muestra en pantall
    except Exception as e:
        print(e)
    finally:
        pass

def MostrarMenu():
    print(Fore.GREEN + '*'*50)
    print(Fore.GREEN +  '                 Menu de Aplicacion' )
    print(Fore.GREEN + '*'*50)
    print(Fore.BLACK +'Seleccione una opcion')
    print('1--Agregar Producto')
    print('2--Mostar Productos')
    print('3--Actualizar Producto')
    print('4--Compra Productos')
    print('5--Vender Productos')
    print('6--Eliminar Producto')
    print('7--Buscar Producto')
    print('8--Reporte de Bajo Stock')
    print('9--Salir')
    print(Fore.GREEN + '*'*50)

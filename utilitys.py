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
    print('3--Compra Productos')
    print('4--Vender Productos')
    print('5--Eliminar Producto')
    print('6--Buscar Producto')
    print('7--Reporte de Bajo Stock')
    print('8--Salir')
    print(Fore.GREEN + '*'*50)

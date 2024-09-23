import sqlite3
import os
import datetime
from colorama import Fore

def conectar():
    con = sqlite3.connect('productos.db')
    cur = con.cursor()
    return con, cur


#Funcion para agregar producto
def agregar(codigo, nombre, descripcion, precio, costo):
        con, cur =conectar()
        #utilizo la funcion para ponerlo en minuscula
        nombre = nombre.lower()
        
        #Compruebo que el producto exista o no en la base de datos
        cur.execute("SELECT * FROM productos WHERE codigo=? OR nombre=? ",(codigo, nombre))
        resultado = cur.fetchone()
        
        #Si existe lanzo un msj por consola
        if resultado:
            print(f"El producto {nombre.upper()} ya existe en la lista de productos")
        #Sino agrego un nuevo producto a la base de datos
        else:
            cur.execute("INSERT INTO productos (codigo, nombre, descripcion, precio, costo) VALUES (?, ?, ?, ?, ?)", (codigo, nombre, descripcion, precio, costo))
            print(f"El producto {nombre.upper()} fue agregado correctamente")
        con.commit()
        cur.close()


def verProductos():
    con, cur =conectar()
    cur.execute("SELECT codigo, nombre, descripcion, stock FROM productos WHERE activo =TRUE")
    productos = cur.fetchall()
    # Si hay productos en la base de datos, los mostramos
    if productos:
        # Encabezados de las columnas
        print(f"{'Codigo':<20}  {'Nombre':<20}  {'Descripcion':<20} {'Stock':<10}")  # Encabezados con formato
        print("=" * 80)  # Línea divisoria

        # Imprimimos los productos
        for producto in productos:
            codigo, nombre, descripcion, stock = producto
            print(f" {codigo:<20} {nombre:<20}{descripcion or 'N/A':<20} {stock:<10}")  # Ajustamos el formato de cada fila
            print("-" * 80)
    else:
        print("No hay productos disponibles.")
    cur.close()
    con.close()


def buscarPorNombre(nombre):
    #llamo a la funcion conectar para definir mi conexion y usar la funcion cursor
    con, cur =conectar()
    #uso la funcion execute para buscar el producto por su nombre
    cur.execute("Select * from productos where nombre =? ", (nombre, ))
    #si
    producto = cur.fetchone()
    # Verificar si el producto existe
    if producto:
        # Encabezados de las columnas
        print(f"{'Nombre':<20} {'Cantidad':<10}")  # Encabezados con formato
        print("=" * 30)  # Línea divisoria
        # Imprimir nombre y cantidad (stock) formateado
        print(f"{producto[0]:<20} {producto[1]:<10}")
    else:
        print("Producto no encontrado.")
    cur.close()
    con.close()

#Funcion para realizar una compra en el sistema
def comprar():
    con, cur =conectar()
    productos_comprados=[]
    #Busca en la base de datos la ultima boleta y le suma 1
    cur.execute("SELECT id_boleta FROM boletas ORDER BY id_boleta DESC LIMIT 1")
    ultimo_id = cur.fetchone()

    # Iniciar el nuevo número de boleta
    if ultimo_id:
        nuevo_numero = ultimo_id[0] + 1
    else:
        nuevo_numero = 1 
    id_boleta = nuevo_numero
    fecha = datetime.date.today()
    total = 0
    sub_total = 0
    cur.execute("INSERT INTO boletas (id_boleta, fecha,total) values (?,?,?) ", (id_boleta, fecha, total))
    while True:
        opcion = int(input("""
                Elija una opcion:
                1--Agregar Nuevo Producto
                2--Finalizar Compra
"""))
        if opcion == 1:
            codigo=int(input("Ingrese Codigo de Producto: "))
            stock=int(input("Ingrese cantidad: "))
        #Valida por su codigo si el producto se encuentra en la base de datos
            cur.execute("SELECT * FROM productos WHERE codigo = ? ",
                    (codigo, ))
        #Trae la fila convertida en una tupla para poder mostrarla por pantalla
            producto = cur.fetchone()
            if producto:
                productos_comprados.append(producto)
            else:
            #Si el producto no existe envia un msj por consola
                print("El producto no existe")
            #Si el producto existe
            for producto in productos_comprados:
                sub_total=producto[5] * stock
            #Realiza una actualizacion del stock de la base de datos sumandole la cantidad ingresada en la compra
                cur.execute("UPDATE productos SET stock = stock + ? WHERE codigo = ?" 
                        ,(stock, codigo))
                cur.execute("INSERT INTO detalle_boleta (id_boleta,codigo_producto,cantidad,subtotal) VALUES (?,?,?,?)", (id_boleta,producto[0],stock,sub_total))
            #Envia  un mensaje de confirmacion
        elif opcion == 2:
                print("productos_comprados")
                
                break
        else:
            print("elija una opcion valida")
        total= sub_total + total
        print(total)
        cur.execute("UPDATE boletas SET total = ? WHERE id_boleta = ?", (total, id_boleta))
        print("Compra realizada correctamente")
        print(productos_comprados)
   
    con.commit()
    cur.close()
    con.close()

def vender(codigo, stock):
    try:
        con, cur =conectar()
        cur.execute("SELECT * FROM productos WHERE codigo = ? ", (codigo, ))
        producto = cur.fetchone()
        if producto:
            cur.execute("UPDATE productos SET stock = stock - ? WHERE codigo = ?" , (stock, codigo))
            print("Venta realizada correctamente")
        else:
            print("El producto no existe")
    except sqlite3.IntegrityError:
            print(Fore.RED+"Cantidad Insuficiente para realizar venta. Verifique el stock")
            print(Fore.RESET)
    finally:
        con.commit()
        cur.close()
        con.close()

def eliminarProducto(codigo):
    con, cur =conectar()
    cur.execute("SELECT * FROM productos WHERE codigo = ? ", (codigo, ))
    producto = cur.fetchone()
    if producto:
        cur.execute("DELETE FROM productos WHERE  codigo = ?" , ( codigo, ))
        print("Producto borrado correctamente")
    else:
        print("El producto no existe")
    con.commit()
    cur.close()
    con.close()

def verificarBajoStock():
    con, cur =conectar()
    cur.execute("SELECT * FROM productos WHERE stock < 6 AND activo =TRUE ")
    productos = cur.fetchall()
    if productos:
        # Encabezados de las columnas
        print(f"{'Nombre':<20} {'Cantidad':<10}")  # Encabezados con formato
        print("=" * 30)  # Línea divisoria
        # Imprimir nombre y cantidad (stock) formateado
        for producto in productos:
            print(f"{producto[1]:<20} {producto[3]:<10}")
    else:
        print("No hay productos con Baja Cantidad.")
    cur.close()
    con.close()


comprar()
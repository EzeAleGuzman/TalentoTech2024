import sqlite3
from colorama import Fore

def conectar():
    con = sqlite3.connect('productos.db')
    cur = con.cursor()
    return con, cur


#Funcion para agregar producto
def agregar(codigo, nombre, descripcion):
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
            cur.execute("INSERT INTO productos (codigo, nombre, descripcion) VALUES (?, ?, ?)", (codigo, nombre, descripcion))
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
def comprar(codigo, stock):
    con, cur =conectar()
    #Valida por su codigo si el producto se encuentra en la base de datos
    cur.execute("SELECT * FROM productos WHERE codigo = ? ",
                (codigo, ))
    #Trae la fila convertida en una tupla para poder mostrarla por pantalla
    producto = cur.fetchone()
    #Si el producto existe
    if producto:
        #Realiza una actualizacion del stock de la base de datos sumandole la cantidad ingresada en la compra
        cur.execute("UPDATE productos SET stock = stock + ? WHERE codigo = ?" 
                    ,(stock, codigo))
        #Envia  un mensaje de confirmacion
        print("Compra realizada correctamente")
    else:
        #Si el producto no existe envia un msj por consola
        print("El producto no existe")
    con.commit()
    cur.close()
    con.close()

def vender(codigo, stock):
    con, cur =conectar()
    cur.execute("SELECT * FROM productos WHERE codigo = ? ", (codigo, ))
    producto = cur.fetchone()
    if producto:
        cur.execute("UPDATE productos SET stock = stock - ? WHERE codigo = ?" , (stock, codigo))
        print("Compra realizada correctamente")
    else:
        print("El producto no existe")
    con.commit()
    cur.close()
    con.close()

def eliminarProducto(nombre):
    con, cur =conectar()
    cur.execute("SELECT * FROM productos WHERE nombre = ? ", (nombre, ))
    producto = cur.fetchone()
    if producto:
        cur.execute("DELETE FROM productos WHERE  nombre = ?" , ( nombre, ))
        print("Producto borrado correctamente")
    else:
        print("El producto no existe")
    con.commit()
    cur.close()
    con.close()
    

agregar(104,"Buzos","")
verProductos()
vender(104,30)
verProductos()


import sqlite3
import datetime
from colorama import Fore
#soluciona el problema de la ruta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utilitys import *
from bd import conectar


cur, con = conectar()

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

#Funcion Para visualizar Los productos Almacenados en la base de datos
def verProductos():
    con, cur =conectar()
    #Busco en la base de datos todos los productos activos
    cur.execute("SELECT codigo, nombre, descripcion, stock FROM productos WHERE activo =TRUE")
    #Obtengo los productos
    productos = cur.fetchall()
    #Creamos una tabla
    table = BeautifulTable()
    if productos:
        table.columns.header = ["Codigo", "nombre", "descripcion", "stock"]
        # Recorremos los productos
        for producto in productos:
            #Agrego la fila a la tabla
            table.rows.append(producto)
        print(table)
    else:
        print("No hay productos disponibles.")
    cur.close()
    con.close()

#funsion que se encarga de buscar por nombre un producto en la base de datos
def buscarPorNombre(nombre):
    #llamo a la funcion conectar para definir mi conexion y usar la funcion cursor
    con, cur =conectar()
    #uso la funcion execute para buscar el producto por su nombre
    cur.execute("Select * from productos where nombre =? ", (nombre, ))
    #si
    producto = cur.fetchone()
    if producto:
        table = BeautifulTable()
        table.columns.header = ["Codigo", "nombre", "descripcion", "stock", "activo", "precio", "costo"]
        table.rows.append(producto)
        print(table)
    # Verificar si el producto existe
    else:
        print("Producto no encontrado.")
    cur.close()
    con.close()

#Funcion para realizar una compra en el sistema
def comprar():
    con, cur = conectar()
    productos_comprados = [] #Lista para almacenar los productos comprados
    id_boleta = crearBoleta()  # Función que genera el ID de la boleta
    #Inicializo la fecha y el total
    fecha = datetime.date.today()
    total = 0

    while True:
        opcion = int(input("""
        Elija una opción:
    1--Agregar Nuevo Producto
    2--Finalizar Compra
        """))

        if opcion == 1:
            print(Fore.CYAN+"-----------Compra de Productos---------")
            codigo = int(input("Ingrese codigo del producto:  "))
            cantidad = int(input("Ingrese la cantidad de producto comprado:  "))
            
            # Validar si el producto existe
            cur.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
            producto = cur.fetchone()
            
            if producto:
                # Insertar boleta con el total inicial en 0
                cur.execute("INSERT INTO boletas (id_boleta, fecha, total) VALUES (?, ?, ?)", (id_boleta, fecha, total))
                precio_unitario = producto[6]  # Suponiendo que el precio está en la posición 5
                sub_total = precio_unitario * cantidad
                total += sub_total
                
                # Actualizar el stock del producto
                cur.execute("UPDATE productos SET stock = stock + ? WHERE codigo = ?" , (cantidad, codigo))
                print("Stock actualizado para la compra")
                
                # Insertar el detalle de la boleta
                cur.execute("INSERT INTO detalle_boleta (id_boleta, codigo_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                            (id_boleta, codigo, cantidad, sub_total))
                
                # Agregar el producto comprado a la lista
                productos_comprados.append({
                    'codigo': codigo,
                    'nombre': producto[1],
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': sub_total
                })
            else:
                print(Fore.RED +"El producto no existe")

        elif opcion == 2:
                    # Mostrar resumen de la compra
            print(Fore.LIGHTYELLOW_EX)
            # Crear una tabla
            tabla = BeautifulTable()

            # Configurar los encabezados de la tabla
            tabla.columns.header = ["Producto", "Cantidad", "Precio Unitario", "Subtotal"]

            # Agregar filas a la tabla
            for item in productos_comprados:
                tabla.rows.append([item['nombre'], item['cantidad'], f"${item['precio_unitario']:.2f}", f"${item['subtotal']:.2f}"])
            print(f"-" * 19 + " Resumen de la compra Boleta N°" + str(id_boleta) + " " + "-" * 19)
            print(tabla)
            print("-" * 80)

            print(f"Total de la compra: ${total:.2f}")

            # Actualizar el total en la boleta
            cur.execute("UPDATE boletas SET total = ? WHERE id_boleta = ?", (total, id_boleta))

            # Confirmar y finalizar la compra
            print("Falta Verificar proveedores")# Mostrar resumen de la compra
            break

        else:
            print("Elija una opción válida.")
    
    con.commit()
    cur.close()
    con.close()

def crearBoleta():
    con, cur =conectar()
    #Busca en la base de datos la ultima boleta y le suma 1
    cur.execute("SELECT id_boleta FROM boletas ORDER BY id_boleta DESC LIMIT 1")
    ultimo_id = cur.fetchone()

    # Iniciar el nuevo número de boleta
    if ultimo_id:
        nuevo_numero = ultimo_id[0] + 1
    else:
        nuevo_numero = 100000001 
    id_boleta = nuevo_numero
    cur.close()
    con.close()
    return id_boleta
    
def vender(codigo, stock):
    try:
        con, cur =conectar()
        cur.execute("SELECT * FROM productos WHERE codigo = ? ", (codigo, ))
        producto = cur.fetchone()
        if producto:
            cur.execute("UPDATE productos SET stock = stock - ? WHERE codigo = ?" , (stock, codigo))
            print("stock actualizado para la venta")
            
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
    cur.execute("SELECT codigo, nombre, descripcion, stock FROM productos WHERE stock < 6 AND activo =TRUE ")
    productos = cur.fetchall()
    if productos:
       crearTabla(productos)
    else:
        print("No hay productos con Baja Cantidad.")
    cur.close()
    con.close()


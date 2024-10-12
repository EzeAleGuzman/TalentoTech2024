
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

def comprar():
    con, cur = conectar()
    productos_comprados = []  # Lista para almacenar los productos comprados
    id_transaccion = crearBoleta()  # Función que genera el ID de la boleta
    fecha = datetime.date.today()  # Inicializo la fecha
    monto = 0  # Inicializo el total
    id_proveedor = int(input("Ingrese el ID del proveedor: "))

    # Insertar la transacción con monto 0 al inicio
    cur.execute("INSERT INTO transacciones (id_transaccion, fecha, monto, tipo_transaccion, id_cliente, id_proveedor) VALUES (?, ?, ?, ?, ?, ?)",
                (id_transaccion, fecha, monto, 'compra', 0, id_proveedor))

    while True:
        opcion = int(input("""
        Elija una opción:
        1--Agregar Nuevo Producto
        2--Finalizar Compra
        """))

        if opcion == 1:
            print(Fore.CYAN + "-----------Compra de Productos---------")
            codigo = int(input("Ingrese código del producto:  "))
            cantidad = int(input("Ingrese la cantidad de producto comprado:  "))

            # Validar si el producto existe
            cur.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
            producto = cur.fetchone()

            if producto:
                precio_unitario = producto[6]  # Suponiendo que el precio está en la posición 6
                sub_total = precio_unitario * cantidad
                monto += sub_total

                # Actualizar el stock del producto
                cur.execute("UPDATE productos SET stock = stock + ? WHERE codigo = ?", (cantidad, codigo))
                print("Stock actualizado para la compra")

                # Insertar el detalle de la boleta
                cur.execute("INSERT INTO detalle_transacciones (id_transaccion, codigo_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                            (id_transaccion, codigo, cantidad, sub_total))

                # Agregar el producto comprado a la lista
                productos_comprados.append({
                    'codigo': codigo,
                    'nombre': producto[1],
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': sub_total
                })
            else:
                print(Fore.RED + "El producto no existe")

        elif opcion == 2:
            # Mostrar resumen de la compra
            print(Fore.LIGHTYELLOW_EX)
            tabla = BeautifulTable()

            # Configurar los encabezados de la tabla
            tabla.columns.header = ["Producto", "Cantidad", "Precio Unitario", "Subtotal"]

            # Agregar filas a la tabla
            for item in productos_comprados:
                tabla.rows.append([item['nombre'], item['cantidad'], f"${item['precio_unitario']:.2f}", f"${item['subtotal']:.2f}"])
            print(f"-" * 19 + " Resumen de la compra Boleta N°" + str(id_transaccion) + " " + "-" * 19)
            print(tabla)
            print("-" * 80)

            print(f"Total de la compra: ${monto:.2f}")

            # Actualizar el total en la transacción
            cur.execute("UPDATE transacciones SET monto = ? WHERE id_transaccion = ?", (monto, id_transaccion))

            # Actualizar el estado de cuenta del proveedor
            cur.execute("UPDATE proveedores SET estado_cuenta = estado_cuenta - ? WHERE id_proveedor = ?", (monto, id_proveedor))

            print("Compra finalizada con éxito")
            break

        else:
            print("Elija una opción válida.")

    con.commit()
    cur.close()
    con.close()


def crearBoleta():
    con, cur =conectar()
    #Busca en la base de datos la ultima transaccion y le suma 1
    cur.execute("SELECT id_transaccion FROM transacciones ORDER BY id_transaccion DESC LIMIT 1")
    ultimo_id = cur.fetchone()

    # Iniciar el nuevo número de boleta
    if ultimo_id:
        nuevo_numero = ultimo_id[0] + 1
    else:
        nuevo_numero = 100000001 
    id_transaccion = nuevo_numero
    cur.close()
    con.close()
    return id_transaccion
    
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


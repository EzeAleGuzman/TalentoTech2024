import sqlite3
import datetime
from colorama import Fore
from beautifultable import BeautifulTable

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
import datetime

def comprar():
    con, cur = conectar()
    productos_comprados = []
    id_boleta = crearBoleta()  # Función que genera el ID de la boleta
    fecha = datetime.date.today()
    total = 0
    
    # Insertar boleta con el total inicial en 0
    cur.execute("INSERT INTO boletas (id_boleta, fecha, total) VALUES (?, ?, ?)", (id_boleta, fecha, total))

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
                precio_unitario = producto[6]  # Suponiendo que el precio está en la posición 5
                sub_total = precio_unitario * cantidad
                total += sub_total
                
                # Actualizar el stock del producto
                cur.execute("UPDATE productos SET stock = stock + ? WHERE codigo = ?", (cantidad, codigo))
                
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

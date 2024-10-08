
from beautifultable import BeautifulTable
from colorama import Fore
#soluciona el problema de la ruta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bd






#funcion para crear un cliente
def crearCliente(codigo,nombre, apellido, telefono, calle, altura,partido):
    con, cur = bd.conectar()
    try:
        cur.execute("INSERT INTO direccion (calle, altura, partido) VALUES (?, ?, ?)", (calle, altura, partido))
        id_direccion= cur.lastrowid
        cur.execute("INSERT INTO clientes (id_cliente,nombre, apellido, telefono,id_direccion) VALUES (?, ?, ?, ?,?)", (codigo, nombre, apellido, telefono, id_direccion))
        con.commit()
    except Exception as e:
        print(e)
        
    finally:
        cur.close()
        con.close()

def verClientes():
    con, cur = bd.conectar()
    cur.execute("SELECT * FROM clientes")
    clientes = cur.fetchall()
    table = BeautifulTable()
    
    if clientes:
        print(Fore.LIGHTYELLOW_EX)
        table.columns.header = ["ID","Nombre", "Apellido", "Telefono", "Direccion", "Estado Cuenta"]
        # Imprimimos los clientes
        for cliente in clientes:
            table.rows.append(cliente),
        print(table)
    print(Fore.RESET)
    

def buscarCliente(nombre):
    con, cur = bd.conectar()
    cur.execute("SELECT * FROM clientes WHERE nombre = ?", (nombre,))
    cliente = cur.fetchone()
    if cliente:
        table = BeautifulTable()
        table.columns.header = ["ID", "Nombre", "Apellido", "Telefono", "Direccion", "Estado Cuenta"]
        table.rows.append(cliente)
        print(table)
    else:
        print("Cliente no encontrado")

    cur.close()
    con.close()

def actualizarCliente(id_cliente, nombre, apellido, telefono, id_direccion, estado_cuenta): 
    con, cur = bd.conectar()
    try:
        cur.execute("UPDATE clientes SET nombre = ?, apellido = ?, telefono = ?, id_direccion = ?, estado_cuenta = ? WHERE id_cliente = ?", (nombre, apellido, telefono, id_direccion, estado_cuenta, id_cliente))
        print("Cliente actualizado correctamente")
        con.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()

def eliminarCliente(id_cliente):
    con, cur = bd.conectar()
    try:
        cur.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
        print("Cliente eliminado correctamente")
        con.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close() 
        con.close()

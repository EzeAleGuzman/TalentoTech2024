import sqlite3
from beautifultable import BeautifulTable
from colorama import Fore


def conexion():
    con = sqlite3.connect("produtos.db")
    cur = con.cursor()
    return con, cur

def crearProveedor(id_proveedor, nombre, apellido, telefono, id_direccion, estado_cuenta):
    con, cur = conexion()
    try:
        cur.execute("INSERT INTO proveedores (id_proveedor, nombre, apellido, telefono, id_direccion, estado_cuenta) VALUES (?, ?, ?, ?, ?, ?)", (id_proveedor, nombre, apellido, telefono, id_direccion, estado_cuenta))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close() 

def verProveedores():
    con, cur = conexion()
    cur.execute("SELECT * FROM proveedores")
    proveedores = cur.fetchall()
    table = BeautifulTable()
    if proveedores:
        print(Fore.LIGHTYELLOW_EX)
        table.columns.header = ["ID", "Nombre", "Apellido", "Telefono", "Direccion", "Estado Cuenta"]
        # Imprimimos los proveedores
        for proveedor in proveedores:
            table.rows.append(proveedor)
        print(table)
    print(Fore.RESET)

def buscarProveedor(nombre):
    con, cur = conexion()
    cur.execute("SELECT * FROM proveedores WHERE nombre = ?", (nombre,))
    proveedor = cur.fetchone()
    if proveedor:
        table = BeautifulTable()
        table.columns.header = ["ID", "Nombre", "Apellido", "Telefono", "Direccion", "Estado Cuenta"]
        table.rows.append(proveedor)
        print(table)
    else:
        print("Proveedor no encontrado")
    cur.close()
    con.close()

def actualizarProveedor(id_proveedor, nombre, apellido, telefono, id_direccion, estado_cuenta):
    con, cur = conexion()
    try:
        cur.execute("UPDATE proveedores SET nombre = ?, apellido = ?, telefono = ?, id_direccion = ?, estado_cuenta = ? WHERE id_proveedor = ?", (nombre, apellido, telefono, id_direccion, estado_cuenta, id_proveedor))
        print("Proveedor actualizado correctamente")
        con.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        
def eliminarProveedor(id_proveedor):
    con, cur = conexion()
    try:
        cur.execute("DELETE FROM proveedores WHERE id_proveedor = ?", (id_proveedor,))
        print("Proveedor eliminado correctamente")
        con.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
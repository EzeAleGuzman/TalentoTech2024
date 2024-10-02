from colorama import Fore
#soluciona el problema de la ruta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utilitys import *
from bd import conectar



con, cur = conectar()

def crearProveedor(id_proveedor, nombre, apellido, telefono, id_direccion, estado_cuenta):
    con, cur =  conectar()
    try:
        cur.execute("INSERT INTO proveedores (id_proveedor, nombre, apellido, telefono, id_direccion, estado_cuenta) VALUES (?, ?, ?, ?, ?, ?)", (id_proveedor, nombre, apellido, telefono, id_direccion, estado_cuenta))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close() 

def verProveedores():
    con, cur = conectar()
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
    con, cur = conectar()
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
    con, cur = conectar()
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
    con, cur = conectar()
    try:
        cur.execute("DELETE FROM proveedores WHERE id_proveedor = ?", (id_proveedor,))
        print("Proveedor eliminado correctamente")
        con.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
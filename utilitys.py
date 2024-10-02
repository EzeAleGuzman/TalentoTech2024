from beautifultable import BeautifulTable

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


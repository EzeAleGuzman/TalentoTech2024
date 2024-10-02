import sqlite3


#Esta funcion crea la coneccion a base de datos
def conectar():
    #conexion a la base, si noexiste, crea una nueva con ese nombre
    con = sqlite3.connect('productos.db')
    #inicializo la funcion cursor()
    cur = con.cursor()
    #retorno la conexion y el cursor
    return con, cur


con, cur  = conectar()
# Crear tabla productos
cur.execute('''
            CREATE TABLE IF NOT EXISTS productos(
                codigo BIGINT PRIMARY KEY,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                stock INT DEFAULT 0, 
                activo BOOLEAN DEFAULT TRUE,
                precio REAL NOT NULL, 
                costo REAL NOT NULL,   
                CHECK (stock >= 0)
            )
''')

# Crear tabla boletas
cur.execute('''
            CREATE TABLE IF NOT EXISTS boletas(
                id_boleta BIGINT PRIMARY KEY,
                fecha DATETIME NOT NULL,
                total REAL NOT NULL
            )
''')

# Crear tabla detalle_boleta
cur.execute('''
            CREATE TABLE IF NOT EXISTS detalle_boleta(
                id_detalle_boleta  INTEGER PRIMARY KEY AUTOINCREMENT,
                id_boleta BIGINT NOT NULL,
                codigo_producto BIGINT NOT NULL,
                cantidad INT NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (id_boleta) REFERENCES boletas(id_boleta),
                FOREIGN KEY (codigo_producto) REFERENCES productos(codigo)
            )
''')

# Crear tabla clientes
cur.execute('''
            CREATE TABLE IF NOT EXISTS clientes(
                id_cliente BIGINT PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                telefono TEXT NOT NULL,
                id_direccion BIGINT NOT NULL,
                estado_cuenta REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (id_direccion) REFERENCES direcciones(id_direccion)
            )
''')

# Crear tabla proveedores
cur.execute('''
            CREATE TABLE IF NOT EXISTS proveedores(
                id_proveedor BIGINT PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                telefono TEXT NOT NULL,
                id_direccion BIGINT NOT NULL,
                estado_cuenta REAL NOT NULL,
                FOREIGN KEY (id_direccion) REFERENCES direcciones(id_direccion)
            )
''')

# Crear tabla direccion
cur.execute(''' 
            CREATE TABLE IF NOT EXISTS direccion(
                id_direccion INTEGER PRIMARY KEY AUTOINCREMENT,
                calle TEXT NOT NULL,
                altura TEXT NOT NULL,
                partido TEXT NOT NULL
            )
''')

# Crear tabla transacciones
cur.execute('''
            CREATE TABLE IF NOT EXISTS transacciones(
                id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATETIME NOT NULL,
                monto REAL NOT NULL,
                tipo_transaccion TEXT NOT NULL CHECK (tipo_transaccion IN ('compra', 'venta', 'pago_cliente', 'pago_proveedor')),
                id_cliente INTEGER,
                id_proveedor INTEGER,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
            )
''')

# Confirmo los cambios en la base de datos
con.commit()

# Cierro la conexión
con.close()

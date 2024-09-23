import sqlite3

#Se crea coneccion o  si no existe se crea la base de datos
con = sqlite3.connect('productos.db')

cur = con.cursor()

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

cur.execute('''
            CREATE TABLE IF NOT EXISTS boletas(
                id_boleta INT BIGINT PRIMARY KEY,
                fecha DATETIME NOT NULL,
                total REAL NOT NULL
                
            )
            
''')


cur.execute('''
            CREATE TABLE IF NOT EXISTS detalle_boleta(
                id_detalle_boleta  INTEGER PRIMARY KEY AUTOINCREMENT,
                id_boleta INT NOT NULL,
                codigo_producto BIGINT NOT NULL,
                cantidad INT NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (id_boleta) REFERENCES boletas(id_boleta),
                FOREIGN KEY (codigo_producto) REFERENCES productos(codigo)
                
            )
            
            
''')

#Confirmo los cambios en la base de datos
con.commit()


#Cierro la conexion
con.close()
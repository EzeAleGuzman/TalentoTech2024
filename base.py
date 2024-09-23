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
                activo BOOLEAN DEFAULT TRUE
                CHECK (stock >= 0)
            )
''')



#Confirmo los cambios en la base de datos
con.commit()


#Cierro la conexion
con.close()
import sqlite3
import hashlib

# Funcion para crear la tabla que guardara a los usuarios que se registren
def CreateTable():
    con = sqlite3.connect('app/db/users.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users "
    "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    con.commit()
    con.close()

# Funcion para insertar un usuario en la base de datos
def InsertUser(name, email, password):
    con = sqlite3.connect('app/db/users.db')
    cur = con.cursor()
    hashedPassword = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashedPassword))
    con.commit()
    con.close()

# Funcion para obtener todos los usuarios de la base de datos
def GetUsers():
    con = sqlite3.connect('app/db/users.db')
    cur = con.cursor()
    cur.execute("SELECT id, name, email FROM users")
    rows = cur.fetchall()
    con.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
        })

    return users

# Funcion para actualizar un usuario en la base de datos
def UpdateUser(id, name, email, password):
    con = sqlite3.connect('app/db/users.db')
    cur = con.cursor()
    hashedPassword = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?", (name, email, hashedPassword, id))
    con.commit()
    con.close()

# Funcion para eliminar un usuario de la base de datos
def DeleteUser(id):
    con = sqlite3.connect('app/db/users.db')
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (id,))
    con.commit()
    con.close()
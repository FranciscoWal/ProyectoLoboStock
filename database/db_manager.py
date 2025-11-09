# db_manager.py
import sqlite3
from pathlib import Path

# base de datos 
DB_PATH = Path(__file__).parent.parent / "solicitudes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
   CREATE TABLE IF NOT EXISTS solicitudes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        expediente TEXT,
        carrera TEXT,
        material TEXT,
        laboratorio TEXT,
        hora_inicio TEXT,
        hora_entrega TEXT,
        fecha TEXT DEFAULT CURRENT_TIMESTAMP,
        estado TEXT DEFAULT 'Pendiente',
        almacen_destino TEXT
    );
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    expediente TEXT UNIQUE NOT NULL,
    carrera TEXT NOT NULL,
    adeudo INTEGER DEFAULT 0  -- 0 = sin adeudo, 1 = con adeudo
);
""")


    cursor.execute("""
CREATE TABLE IF NOT EXISTS administradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    carrera TEXT NOT NULL  -- Almacén o laboratorio que administra
   
);
""")


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_material TEXT UNIQUE,
        almacen TEXT,
        cantidad_total INTEGER DEFAULT 0,
        cantidad_en_uso INTEGER DEFAULT 0,
        cantidad_disponible INTEGER DEFAULT 0
    );
    """)
    # Usuarios
    insertar_usuario_default(cursor, "diego", "123", "2022143039","Tecnologías de la Información", 0)
    insertar_usuario_default(cursor, "Brenda", "123", "2022143040","Química", 0)
    insertar_usuario_default(cursor, "Pamela", "123", "2022143050","Mecatrónica", 0)
    insertar_usuario_default(cursor, "Angel", "123", "2022143060","Farmacéutica", 0)
    #Admins
    insertar_admin_default(cursor, "Pamela", "123", "Química")
    insertar_admin_default(cursor, "Angel", "123", "Mecatrónica")
    insertar_admin_default(cursor, "Diego", "123", "Farmacéutica")

    insertar_material_default(cursor, "Matraz Erlenmeyer 250ml", "Química", 15)
    insertar_material_default(cursor, "Arduino", "Mecatrónica", 15)
    conn.commit()
    conn.close()

def insertar_material_default(cursor, nombre_material, almacen, cantidad_total):
    """Inserta material por defecto si no existe"""
    try:
        cursor.execute("""
            INSERT INTO inventario (nombre_material, almacen, cantidad_total, cantidad_disponible)
            VALUES (?, ?, ?, ?)
        """, (nombre_material, almacen, cantidad_total, cantidad_total))
        print(f"Material {nombre_material} agregado correctamente al almacén {almacen}")
    except sqlite3.IntegrityError:
        print(f"Material {nombre_material} ya existe")

def insertar_usuario_default(cursor, username, password, expediente, carrera, adeudo):
    """Inserta usuario por defecto si no existe"""
    try:
        cursor.execute("INSERT INTO usuarios (username, password, expediente, carrera, adeudo) VALUES (?, ?, ?, ?, ?)",
                      (username, password, expediente, carrera, adeudo))
        print(f"Usuario {username} agregado correctamente")
    except sqlite3.IntegrityError:
        print(f"Usuario {username} ya existe")

def insertar_admin_default(cursor, username, password,carrera,):
    """Inserta usuario por defecto si no existe"""
    try:
        cursor.execute("INSERT INTO administradores (username, password, carrera) VALUES (?, ?, ?)",
                      (username, password, carrera,))
        print(f"Admin {username} agregado correctamente")
    except sqlite3.IntegrityError:
        print(f"Admin {username} ya existe")


def insertar_solicitud(nombre, expediente, carrera, material, laboratorio, hora_inicio, hora_entrega, almacen_destino):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO solicitudes (nombre, expediente, carrera, material, laboratorio, hora_inicio, hora_entrega, almacen_destino)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nombre, expediente, carrera, material, laboratorio, hora_inicio, hora_entrega, almacen_destino))
    conn.commit()
    conn.close()


def agregar_usuario(username, password, expediente, carrera, adeudo=0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password, expediente, carrera, adeudo) VALUES (?, ?, ?, ?, ?)",
                      (username, password, expediente, carrera, adeudo))
        conn.commit()
        print("Usuario agregado correctamente")
    except sqlite3.IntegrityError:
        print("Error: El usuario ya existe")
    finally:
        conn.close()

# --- VALIDAR LOGIN ---
def validar_usuario(username, password, rol):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if rol == "admin":
        cursor.execute("SELECT carrera FROM administradores WHERE username=? AND password=?", (username, password))
        admin = cursor.fetchone()
        conn.close()
        if admin:
            return {"rol": "admin", "carrera": admin[0]}
        else:
            return None

    elif rol == "estudiante":
        cursor.execute("SELECT expediente, carrera FROM usuarios WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return {"rol": "usuario", "expediente": user[0], "carrera": user[1]}
        else:
            return None

def verificar_adeudo(expediente):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT adeudo FROM usuarios WHERE expediente=?", (expediente,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0] == 1  
    return False

def asignar_adeudo(expediente):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET adeudo=1 WHERE expediente=?", (expediente,))
    conn.commit()
    conn.close()

def quitar_adeudo(expediente):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET adeudo=0 WHERE expediente=?", (expediente,))
    conn.commit()
    conn.close()

def obtener_estado_adeudo(expediente):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT adeudo FROM usuarios WHERE expediente=?", (expediente,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def buscar_materiales(termino):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre_material 
        FROM inventario 
        WHERE nombre_material LIKE ?
        ORDER BY nombre_material ASC
    """, (f"%{termino}%",))
    resultados = [r[0] for r in cursor.fetchall()]
    conn.close()
    return resultados


def restar_material(nombre_material, cantidad=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE inventario
        SET cantidad_en_uso = cantidad_en_uso + ?,
            cantidad_disponible = cantidad_total - (cantidad_en_uso + ?)
        WHERE nombre_material = ?
    """, (cantidad, cantidad, nombre_material))
    conn.commit()
    conn.close()


def devolver_material(nombre_material, cantidad=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE inventario
        SET cantidad_en_uso = MAX(cantidad_en_uso - ?, 0),
            cantidad_disponible = MIN(cantidad_total, cantidad_disponible + ?)
        WHERE nombre_material = ?
    """, (cantidad, cantidad, nombre_material))
    conn.commit()
    conn.close()


def obtener_almacen_por_material(material):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT almacen FROM inventario WHERE nombre_material = ?", (material,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Desconocido"

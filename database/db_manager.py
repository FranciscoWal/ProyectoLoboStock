# db_manager.py
import sqlite3
from pathlib import Path

# base de datos en proyect
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
        estado TEXT DEFAULT 'Pendiente'
    );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        rol TEXT CHECK(rol IN ('estudiante', 'admin')),
        expediente TEXT UNIQUE,
        adeudo INTEGER DEFAULT 0  -- 0 = sin adeudo, 1 = tiene adeudo
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_material TEXT UNIQUE,
        cantidad_total INTEGER DEFAULT 0,
        cantidad_en_uso INTEGER DEFAULT 0,
        cantidad_disponible INTEGER DEFAULT 0
    );
    """)
    #  por defecto
    insertar_usuario_default(cursor, "diego", "123", "estudiante", "2022143039", 0)
    insertar_usuario_default(cursor, "dani", "123", "admin", "admin001", 0)
    
    conn.commit()
    conn.close()

def insertar_usuario_default(cursor, username, password, rol, expediente, adeudo):
    """Inserta usuario por defecto si no existe"""
    try:
        cursor.execute("INSERT INTO usuarios (username, password, rol, expediente, adeudo) VALUES (?, ?, ?, ?, ?)",
                      (username, password, rol, expediente, adeudo))
        print(f"Usuario {username} agregado correctamente")
    except sqlite3.IntegrityError:
        print(f"Usuario {username} ya existe")

def insertar_solicitud(nombre, expediente, carrera, material, laboratorio, hora_inicio, hora_entrega):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO solicitudes (nombre, expediente, carrera, material, laboratorio, hora_inicio, hora_entrega)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, expediente, carrera, material, laboratorio, hora_inicio, hora_entrega))
    conn.commit()
    conn.close()

def agregar_usuario(username, password, rol, expediente, adeudo=0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password, rol, expediente, adeudo) VALUES (?, ?, ?, ?, ?)",
                      (username, password, rol, expediente, adeudo))
        conn.commit()
        print("Usuario agregado correctamente")
    except sqlite3.IntegrityError:
        print("Error: El usuario ya existe")
    finally:
        conn.close()

def validar_usuario(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]  
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

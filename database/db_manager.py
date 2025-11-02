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
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            estado TEXT DEFAULT 'Pendiente'
        );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        rol TEXT CHECK(rol IN ('estudiante', 'admin'))  -- SOLO permite estos dos valores
    )
    """)
    
    # Insertar usuarios por defecto
    insertar_usuario_default(cursor, "diego", "123", "estudiante")
    insertar_usuario_default(cursor, "dani", "123", "admin")
    
    conn.commit()
    conn.close()

def insertar_usuario_default(cursor, username, password, rol):
    """Inserta usuario por defecto si no existe"""
    try:
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                      (username, password, rol))
        print(f"Usuario {username} agregado correctamente")
    except sqlite3.IntegrityError:
        print(f"Usuario {username} ya existe")

def insertar_solicitud(nombre, expediente, carrera, material):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO solicitudes (nombre, expediente, carrera, material) VALUES (?, ?, ?, ?)",
                   (nombre, expediente, carrera, material))
    conn.commit()
    conn.close()

def agregar_usuario(username, password, rol):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                      (username, password, rol))
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


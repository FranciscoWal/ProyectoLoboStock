import mysql.connector
from mysql.connector import pooling
import os

# --- ¡IMPORTANTE! ---
# Edita esta configuración con tus credenciales de MariaDB/MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '301330057',
    'database': 'edustock_db'
}

try:
    # Creamos un "pool" de conexiones para eficiencia
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="edustock_pool",
        pool_size=5,
        **DB_CONFIG
    )
    print("Pool de conexiones a la base de datos creado exitosamente.")

except mysql.connector.Error as err:
    print(f"❌ Error al conectar a la base de datos: {err}")
    connection_pool = None

def get_db_connection():
    """Obtiene una conexión del pool."""
    if not connection_pool:
        print("El pool de conexiones no está disponible.")
        return None
    try:
        return connection_pool.get_connection()
    except mysql.connector.Error as err:
        print(f"Error al obtener conexión del pool: {err}")
        return None
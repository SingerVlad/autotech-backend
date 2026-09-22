import psycopg

# Reemplaza TU_CLAVE por tu contraseña de postgres
CLAVE = '123456'

try:
    conn = psycopg.connect(
        dbname="postgres",
        user="postgres",
        password=CLAVE,
        host="localhost",
        port=5432,
        autocommit=True
    )
    with conn.cursor() as cur:
        cur.execute("CREATE DATABASE autotech_db;")
    conn.close()
    print("BASE DE DATOS CREADA CON EXITO")
except Exception as e:
    print(f"Resultado: {e}")
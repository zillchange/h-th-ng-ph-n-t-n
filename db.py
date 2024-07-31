import mysql.connector
def connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Djeutrang21402#",
        database="distributed_system"
    )
import mysql.connector

def conectar():

    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mousepad20#",
        database="creche_db"
    )

    return conexao
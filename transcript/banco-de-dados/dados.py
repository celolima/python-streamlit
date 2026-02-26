import sqlite3

def conecta_db():
    conexao = sqlite3.connect('titulo.db')
    return conexao

def insere_dados(nome, ano, nota):
    conexao = conecta_db()
    cursor = conexao.cursor()
    cursor.execute(
    """
        INSERT INTO filmes(nome, ano , nota)
        VALUES (?,?,?);
    """,
    (nome,ano,nota)
    )
    conexao.commit()
    conexao.close
    
def obter_dados():
    conexao = conecta_db()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM filmes')
    dados = cursor.fetchall()
    conexao.close()
    return dados
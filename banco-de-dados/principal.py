import sqlite3

# 1 - Cria banco de dados
conexao = sqlite3.connect('titulo.db')

# 2 - Criando cursor
cursor = conexao.cursor()

# 3 - Criando a tabela
cursor.execute(
    """
    CREATE TABLE filmes (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        ano INTEGER NOT NULL,
        nota REAL NOT NULL
    );
    """
)
print("Tabela criada")

# 4 - Insere dados
cursor.execute(
    """
        INSERT INTO filmes(nome, ano , nota)
        VALUES ('Sonic', 2020, 8.0);
    """
)

cursor.execute(
    """
        INSERT INTO filmes(nome, ano , nota)
        VALUES ('Mario Bros', 2024, 9.5);
    """
)
conexao.commit()
print("Dados inseridos")

# 5 - Atualiza dados
id = 1
cursor.execute(
    """
        UPDATE filmes set nome = ?
        WHERE id = ?
    """,
    ("Homem Aranha", id)
)

conexao.commit()
print("Dados atualizados")

dados = cursor.execute('SELECT * FROM filmes')

print(dados.fetchall())

# 4 - Fecha conexão
conexao.close()
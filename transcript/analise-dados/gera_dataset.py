import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import names

datasets_folder = Path(__file__).parent / "datasets"
datasets_folder.mkdir(parents=True, exist_ok=True)

LOJAS = [
    {"estado": "SP", "cidade": "São Paulo",
     "vendedores": ["Ana Oliveira", "Lucas Pereira"]},
    {"estado": "MG", "cidade": "Belo Horizonte",
     "vendedores": ["Leticia", "Luiz"]},
    {"estado": "MG", "cidade": "São Brás",
     "vendedores": ["Cristina", "Carlos"]},
    {"estado": "MG", "cidade": "Juiz de Fora",
     "vendedores": ["Luiza", "Marcelo"]}
]

PRODUTOS = [
    {"nome": "Iphone", "id": 0, "preco": 2500},
    {"nome": "Geladeira", "id": 1, "preco": 4500},
    {"nome": "Smart Band 9 pro", "id": 2, "preco": 500},
    {"nome": "Guitar Condor", "id": 3, "preco": 2500}
]

FORMA_PGTO = ["cartão de crédito", "boleto", "pix", "dinheiro"]
GENDER = ["male", "female"]

compras = []

# Criando as compras
for _ in range(2000):
    loja = random.choice(LOJAS)
    vendedor = random.choice(loja["vendedores"])
    produto = random.choice(PRODUTOS)
    hora_compra = datetime.now() - timedelta(
        days = random.randint(1,365),
        hours = random.randint(-5,5),
        minutes = random.randint(-30,30),
    )
    gender_client = random.choice(GENDER)

    # Gera nomes aleatorios com base no genero
    nome_cliente = names.get_full_name(gender_client)

    forma_pgto = random.choice(FORMA_PGTO)

    compras.append({
        "data": hora_compra,
        "id_compra": 0,
        "loja": loja["cidade"],
        "vendedor": vendedor,
        "produto": produto["nome"],
        "cliente_nome": nome_cliente,
        "cliente_genero": gender_client.replace("female", "feminino").replace("male","masculino"),
        "forma_pagamento": forma_pgto
    })

df_compras = pd.DataFrame(compras).set_index("data").sort_index()
df_compras["id_compra"] = [i for i in range(len(df_compras))]

df_lojas = pd.DataFrame(LOJAS)
df_produtos = pd.DataFrame(PRODUTOS)

print(df_lojas)
print(df_produtos)
print(df_compras)

# Exportando dataFrames CSV
df_compras.to_csv(datasets_folder / "compras.csv", decimal=",", sep=";")
df_lojas.to_csv(datasets_folder / "lojas.csv", decimal=",", sep=";")
df_produtos.to_csv(datasets_folder / "produtos.csv", decimal=",", sep=";")

# Exportando dataFrames Excel
df_compras.to_csv(datasets_folder / "compras.xlsx")
df_lojas.to_csv(datasets_folder / "lojas.xlsx")
df_produtos.to_csv(datasets_folder / "produtos.xlsx")
import sqlite3 as lite

# conexão com bd
con = lite.connect('dados.db')

# criando tabelas de CATEGORIAS do bd
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Categoria(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")

# criando tabelas de RECEITAS do bd
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Receita(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor REAL)")

# criando tabelas de GASTOS do bd
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)")

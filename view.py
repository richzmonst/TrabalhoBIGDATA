import sqlite3 as lite
import pandas as pd

# conexão com bd
con = lite.connect('dados.db')

# inserir CATEGORIA
def inserirCategoria(i):
    with con:
        cur  = con.cursor()
        query = "INSERT INTO Categoria(nome) VALUES (?)"
        cur.execute(query, i)

# inserir RECEITAS
def inserirReceita(i):
    with con:
        cur  = con.cursor()
        query = "INSERT INTO Receita(categoria, adicionado_em, valor) VALUES (?, ?, ?)"
        cur.execute(query, i)

# inserir GASTOS
def inserirGastos(i):
    with con:
        cur  = con.cursor()
        query = "INSERT INTO Gastos(categoria, retirado_em, valor) VALUES (?, ?, ?)"
        cur.execute(query, i)

#############################################################################

# DELETAR Receitas
def deletarReceitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receita WHERE id=?"
        cur.execute(query, i)

def deletarGastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query, i)

#############################################################################
        
# Ver Categorias
def verCategorias():
        
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens

# Ver Receitas
def verReceitas():
        
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receita")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens


# Ver Gastos
def verGastos():
        
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Gastos")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens

# função dados da tabela
def tabela():
    gastos = verGastos()
    receitas = verReceitas()

    tabelaLista = []

    for i in gastos:
        tabelaLista.append(i)
    
    for i in receitas:
        tabelaLista.append(i)
    
    return tabelaLista

# função valores do grafico barras
def valoresBarra():
    # RECEITA total
    receitas = verReceitas()
    receitasLista = []

    for i in receitas:
        receitasLista.append(i[3])
    
    receitaTotal = sum(receitasLista)

    # DESPESA total
    despesas = verGastos()
    despesasLista = []

    for i in despesas:
        despesasLista.append(i[3])

    despesaTotal = sum(despesasLista)

    # SALDO total
    saldoTotal = receitaTotal - despesaTotal

    return [receitaTotal, despesaTotal, saldoTotal]


# função valores grafico pizza
def pizzaValores():
    gastos = verGastos()
    
    tabelaLista = []

    for i in gastos:
        tabelaLista.append(i)

    dataframe = pd.DataFrame(tabelaLista, columns=['id', 'Categoria', 'Data', 'valor'])
    dataframe = dataframe.groupby('Categoria')['valor'].sum()

    listaQuantias = dataframe.values.tolist()
    listaCategorias = []

    for i in dataframe.index:
        listaCategorias.append(i)

    return ([listaCategorias, listaQuantias])

# função grafico porcentagem
def porcentagemValor():
    # RECEITA total
    receitas = verReceitas()
    receitasLista = []

    for i in receitas:
        receitasLista.append(i[3])
    
    receitaTotal = sum(receitasLista)

    # DESPESA total
    despesas = verGastos()
    despesasLista = []

    for i in despesas:
        despesasLista.append(i[3])

    despesaTotal = sum(despesasLista)

    # SALDO total
    if receitaTotal != 0:
        total = ((receitaTotal - despesaTotal) / receitaTotal) * 100
        totalCerto = 100 - total
    else:
        totalCerto = 0  # Ou qualquer outro valor padrão que faça sentido para o seu aplicativo
    return (totalCerto)
import sqlite3 as lite

# conexão com bd
con = lite.connect('dados.db')

from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox
#importando pillow
from PIL import Image, ImageTk

# importando progressbar
from tkinter.ttk import Progressbar
#importando Matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#importando calendário
from tkcalendar import Calendar, DateEntry
from datetime import date

#importando funções view
from view import porcentagemValor, valoresBarra, pizzaValores, tabela, deletarReceitas, deletarGastos, inserirCategoria, verCategorias, inserirGastos, inserirReceita


# cores 
co0 = "#2e2d2b" 
co1 = "#feffff"  
co2 = "#4fa882" 
co3 = "#38576b"  
co4 = "#403d3d"   
co5 = "#e06636"   
co6 = "#038cfc"   
co7 = "#3fbfb9"   
co8 = "#263238"   
co9 = "#e9edf5"   

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

# criando janela
janela = Tk()
janela.title()
janela.geometry('900x650')
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use("clam")

# criando frames (DIVISÃO DA TELA)
frameCima = Frame(janela, width=1043, height=50, background=co1, relief="flat")
frameCima.grid(row=0, column=0)


frameMeio = Frame(janela, width=1043, height=361, background=co1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)


frameBaixo = Frame(janela, width=1043, height=300, background=co1, relief="flat")
frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)


# FRAME CIMA
# acessando a imagem
appImg = Image.open('log.png')
appImg = appImg.resize((200,45))
appImg = ImageTk.PhotoImage(appImg)

appLogo = Label(frameCima, image=appImg, text="          Controle de Finanças", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), bg=co1, fg=co4)
appLogo.place(x=0, y=0)

# definindo tree = global
global tree

# Função inserir categoria
def inserirCategoriaB():
    nome = eNovaCategoria.get()

    listaInserir = [nome]    
    
    for i in listaInserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos!')
            return
        
    # Passando lista para a funç inserir gastos na view
    inserirCategoria(listaInserir)
            
    messagebox.showinfo('Sucesso!', 'Os dados foram inseridos com sucesso.')

    eNovaCategoria.delete(0, 'end')

    # Pegando valores da categoria
    categoriasFuncao = verCategorias()
    categoria = []

    for i in categoriasFuncao:
        categoria.append(i[1])

    # Atualizando lista de categorias
    comboCategoriaDespesa['values'] = (categoria)


# Função inserir receitas
def inserirReceitaB():
    nome = 'Receitas'
    data = eCalendarioReceita.get()
    quantia = eValorReceitas.get()
    listaInserir = [nome, data, quantia]

    for i in listaInserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos!')
            return
# Chama funcao inserir receitas da view
    inserirReceita(listaInserir)
    messagebox.showinfo('Sucesso!', 'Os dados foram inseridos com sucesso.')

    eCalendarioReceita.delete(0, 'end')
    eValorReceitas.delete(0, 'end')

# Atualizando dados
    mostrarTabela()
    porcentagem()
    graficoBarras()
    resumo()
    graficoPizza()

# Função inserir despesas
def inserirDespesasB():
    nome = comboCategoriaDespesa.get()
    data = eCalendarioDespesa.get()
    quantia = eValorDespesas.get()
    listaInserir = [nome, data, quantia]

    for i in listaInserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos!')
            return
# Chama funcao inserir despesas da view
    inserirGastos(listaInserir)
    messagebox.showinfo('Sucesso!', 'Os dados foram inseridos com sucesso.')

    comboCategoriaDespesa.delete(0, 'end')
    eCalendarioDespesa.delete(0, 'end')
    eValorDespesas.delete(0, 'end')

# Atualizando dados
    mostrarTabela()
    porcentagem()
    graficoBarras()
    resumo()
    graficoPizza()


# Função deletar
def deletarDados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]
        
        if nome=='Receitas':
            deletarReceitas([valor])
            messagebox.showinfo('Sucesso!', 'Os dados foram deletados com sucesso.')
# Atualizando dados
            mostrarTabela()
            porcentagem()
            graficoBarras()
            resumo()
            graficoPizza()

        else:
            deletarGastos([valor])
            messagebox.showinfo('Sucesso!', 'Os dados foram deletados com sucesso.')
# Atualizando dados
            mostrarTabela()
            porcentagem()
            graficoBarras()
            resumo()
            graficoPizza()
    
    except IndexError:
        messagebox.showerror('Erro!', 'Selecione um dos dados na tabela.')


# Percentual
def porcentagem():
    labelNome = Label(frameMeio, text="Porcentagem da Receita gasta", height=1, anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    labelNome.place(x=7,y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#daed6b')
    style.configure("TProgressbar", thickness=25)
    
    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = porcentagemValor()

    valor = porcentagemValor()

    labelPorcentagem = Label(frameMeio, text="{:,.2f}%".format(valor), anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    labelPorcentagem.place(x=200,y=35)

# Função gráfico barras
def graficoBarras():
    listaCategorias = ['Renda', 'Despesas', 'Saldo']
    listaValores = valoresBarra()

    # faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    ax.autoscale(enable=True, axis='both', tight=None)

    ax.bar(listaCategorias, listaValores,  color=colors, width=0.9)
    
    # create a list to collect the plt.patches data

    c = 0
    
    # set individual bar lables using above list
    
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(listaValores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')
        c += 1

    ax.set_xticklabels(listaCategorias,fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)


# Função resumo total
def resumo():
    valor = valoresBarra()
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=52)
    l_sumario = Label(frameMeio, text="Total de renda mensal      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=35)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[0]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=70)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=132)
    l_sumario = Label(frameMeio, text="Total Despesas Mensais   ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=115)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[1]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=150)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=207)
    l_sumario = Label(frameMeio, text="Total de Saldo do caixa   ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=190)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[2]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=220)

# FRAME GRAFICO PIZZA

framePizza = Frame(frameMeio, width=580, height=250, bg=co2)
framePizza.place(x=415, y=5)


# Função Grafico Pizza
def graficoPizza():
    # faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pizzaValores()[1]
    lista_categorias = pizzaValores()[0]

    # only "explode" the 2nd slice (i.e. 'Hogs')

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, framePizza)
    canva_categoria.get_tk_widget().grid(row=0, column=0)



graficoBarras()
porcentagem()
resumo()
graficoPizza()

# Criando frames dentro do frameBaixo
frameRenda = Frame(frameBaixo, width=300, height=250, background=co1)
frameRenda.grid(row=0, column=0)

frameOperacoes = Frame(frameBaixo, width=220, height=250, background=co1)
frameOperacoes.grid(row=0, column=1, padx=5)

frameConfiguracao = Frame(frameBaixo, width=220, height=250, background=co1)
frameConfiguracao.grid(row=0, column=2, padx=5)

# Tabela despesas e receita
appTabela = Label(frameMeio, text="Tabela de Receitas e Despesas", anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
appTabela.place(x=5, y=309)

### Mostrar Tabela
def mostrarTabela():
    # criando uma tabela com duas barras de rolar
    tabela_head = ['#Id','Categoria','Data','Quantia']

    listaItens = tabela()
    
    global tree

    tree = ttk.Treeview(frameRenda, selectmode="extended",columns=tabela_head, show="headings")
    # barra de rolar vertical
    vsb = ttk.Scrollbar(frameRenda, orient="vertical", command=tree.yview)
    # barra de rolar horizontal
    hsb = ttk.Scrollbar(frameRenda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
    # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in listaItens:
        tree.insert('', 'end', values=item)


mostrarTabela()


# Configurações despesas
l_info = Label(frameOperacoes, text='Insira novas despesas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10,y=10)

# Categoria
l_categoria = Label(frameOperacoes, text='Categoria', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_categoria.place(x=10,y=40)

# Pegando categorias
categoria_funcao = verCategorias()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])

comboCategoriaDespesa = ttk.Combobox(frameOperacoes, width=10, font=('Ivy 10'))
comboCategoriaDespesa['values'] = (categoria)
comboCategoriaDespesa.place(x=110, y=41)


#Data
l_dataDespesas = Label(frameOperacoes, text='Data', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_dataDespesas.place(x=10,y=70)
eCalendarioDespesa = DateEntry(frameOperacoes, widht=12, background='darkblue', foreground='white', borderwidht=2, year=2022)
eCalendarioDespesa.place(x=110, y=71)

# VALOR
l_valorDespesas = Label(frameOperacoes, text='Quantia total', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valorDespesas.place(x=10,y=100)
eValorDespesas = Entry(frameOperacoes, width=14, justify='left', relief='solid')
eValorDespesas.place(x=110, y=101)

#Botao Adicionar Despesa
ImgAddDespesas = Image.open('add.png')
ImgAddDespesas = ImgAddDespesas.resize((17,17))
ImgAddDespesas = ImageTk.PhotoImage(ImgAddDespesas)
botaoAddDespesas = Button(frameOperacoes, command = inserirDespesasB, image=ImgAddDespesas, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botaoAddDespesas.place(x=110, y=131)

#Botao Excluir
l_Deletar = Label(frameOperacoes, text='Excluir ação', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_Deletar.place(x=10,y=181)

ImgDeletar = Image.open('delete.png')
ImgDeletar = ImgDeletar.resize((17,17))
ImgDeletar = ImageTk.PhotoImage(ImgDeletar)
botaoDelDespesas = Button(frameOperacoes, command=deletarDados, image=ImgDeletar, text=" Deletar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botaoDelDespesas.place(x=110, y=181)


########### Configurações RECEITAS ##########
l_info = Label(frameConfiguracao, text='Insira novas receitas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10,y=10)

#Data RECEITAS
l_dataReceitas = Label(frameConfiguracao, text='Data', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_dataReceitas.place(x=10,y=40)
eCalendarioReceita = DateEntry(frameConfiguracao, widht=12, background='darkblue', foreground='white', borderwidht=2, year=2022)
eCalendarioReceita.place(x=110, y=41)

# VALOR RECEITAS
l_valorReceitas = Label(frameConfiguracao, text='Quantia total', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valorReceitas.place(x=10,y=70)
eValorReceitas = Entry(frameConfiguracao, width=14, justify='left', relief='solid')
eValorReceitas.place(x=110, y=71)

#Botao Adicionar RECEITAS
ImgAddReceitas = Image.open('add.png')
ImgAddReceitas = ImgAddReceitas.resize((17,17))
ImgAddReceitas = ImageTk.PhotoImage(ImgAddReceitas)
botaoAddReceitas = Button(frameConfiguracao,command = inserirReceitaB, image=ImgAddReceitas, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botaoAddReceitas.place(x=110, y=100)

# Nova Categoria 
l_info = Label(frameConfiguracao, text='Categoria', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_info.place(x=10,y=145)
eNovaCategoria = Entry(frameConfiguracao, width=14, justify='left', relief='solid')
eNovaCategoria.place(x=110, y=145)

# Botao inserir Categoria
ImgAddCategoria = Image.open('add.png')
ImgAddCategoria = ImgAddCategoria.resize((17,17))
ImgAddCategoria = ImageTk.PhotoImage(ImgAddCategoria)
botaoAddCategoria = Button(frameConfiguracao,command = inserirCategoriaB, image=ImgAddCategoria, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botaoAddCategoria.place(x=110, y=181)



janela.mainloop()
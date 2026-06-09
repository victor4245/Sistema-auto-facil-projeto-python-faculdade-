# =========================================================
# Dashboard.py — Visão geral do negócio (BD)
# =========================================================

import tkinter as tk
from datetime import datetime
from Menu import cursor
from Submenus.Venda_Aluguel.Venda import clientes

# -------- CONFIGURAÇÕES BÁSICAS --------
AGORA = datetime.now().strftime("%d/%m/%Y")
AGORA2 = datetime.strptime(AGORA, "%d/%m/%Y")
MES = datetime.now().strftime("%m")
PAGINA = 1

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_CAMPO = "#1F2937"
COR_FUNDO = "#0B1220"

# ----------------------------------------------------------
# Ajusta a pagina atual
# ----------------------------------------------------------
def ajusta_pagina(valor, parent):
    global PAGINA
    PAGINA = valor
    mostrar_formulario(parent)

# ----------------------------------------------------------
# Lê todos os clientes do BD
# ----------------------------------------------------------
def ler_numcli():
    cursor.execute("""SELECT * FROM clientes""")
    clientes = cursor.fetchall()
    return len(clientes)

def ler_cli(cod):
    cursor.execute("""SELECT * FROM clientes WHERE cpf_cnpj = %s""",(cod,))
    cliente = cursor.fetchone()

    return cliente
    
# ----------------------------------------------------------
# Lê todos os veículos do BD
# ----------------------------------------------------------
def ler_numfro():
    cursor.execute("""SELECT * FROM frota""")
    veiculos = cursor.fetchall()
    return len(veiculos)

def ler_manfro():
    cursor.execute("""SELECT * FROM frota WHERE obs = 'precisa de manutenção'""")
    manutencao = cursor.fetchall()
    return len(manutencao)

def ler_fro(cod):
    cursor.execute("""SELECT * FROM frota WHERE codigo = %s""",(cod,))
    frota = cursor.fetchone()

    return frota
    
# ----------------------------------------------------------
# Lê todos os funcionários do BD
# ----------------------------------------------------------
def ler_numfunc():
    cursor.execute("""SELECT * FROM funcionarios""")
    funcionarios = cursor.fetchall()
    return len(funcionarios)

# ----------------------------------------------------------
# Lê todos os test drives do BD
# ----------------------------------------------------------
def ler_numtest():
    cursor.execute("""SELECT * FROM agentd""")
    tests = cursor.fetchall()
    return len(tests)

def ler_test():
    cursor.execute("""SELECT * FROM agentd""")
    tests = cursor.fetchall()
    return tests

# ----------------------------------------------------------
# Lê todas as reuniões do BD
# ----------------------------------------------------------
def ler_numreu():
    cursor.execute("""SELECT * FROM agenreu""")
    reunioes = cursor.fetchall()
    return len(reunioes)

def ler_reu():
    cursor.execute("""SELECT * FROM agenreu""")
    reunioes = cursor.fetchall()
    return reunioes

# ----------------------------------------------------------
# Lê todas as vendas do BD
# ----------------------------------------------------------
def ler_numven():
    cursor.execute("""SELECT * FROM venda""")
    vendas = cursor.fetchall()
    venda = []  
    for linha in vendas:
        data = datetime.strptime(linha["data_venda"], "%d/%m/%Y")
        if  data.month == int(MES):
            venda.append(linha)
    return len(venda)
    
def ler_vendas():
    cursor.execute("""SELECT * FROM venda""")
    vendas = cursor.fetchall()
    return vendas

# ----------------------------------------------------------
# Lê todos os aluguéis do BD
# ----------------------------------------------------------
def ler_numalu():
    cursor.execute("""SELECT * FROM aluguel""")
    aluguel = cursor.fetchall()
    return len(aluguel)
    
def ler_aluguel():
    cursor.execute("""SELECT * FROM aluguel""")
    aluguel = cursor.fetchall()
    return aluguel

# ----------------------------------------------------------
# Lê todos os valores das vendas do BD
# ----------------------------------------------------------
def ler_receita():
    cursor.execute("""SELECT valor FROM venda""")
    valor = cursor.fetchall()
    # Criação de variável para o faturamento do mês (bruto)
    PRECO = "0.00"
    for linha in valor:
        PRECO = float(PRECO) + float(linha["valor"])
    PRECO = str(PRECO).replace(".", ",")
    return PRECO


# ----------------------------------------------------------
# Tela principal da pesquisa
# ----------------------------------------------------------
def mostrar_formulario(parent):

    # Limpa a área central
    for w in parent.winfo_children():
        w.destroy()
    # Controle de páginas
    if PAGINA == 1:
        COR_BOTAO = "#5C6883"
        COR_BOTAO2 = "#2563EB"
        COR_BOTAO3 = "#2563EB"
    elif PAGINA == 2:
        COR_BOTAO = "#2563EB"
        COR_BOTAO2 = "#5C6883"
        COR_BOTAO3 = "#2563EB"
    elif PAGINA == 3:
        COR_BOTAO = "#2563EB"
        COR_BOTAO2 = "#2563EB"
        COR_BOTAO3 = "#5C6883"
    # Container central
    container = tk.Frame(parent, bg=COR_FUNDO)
    container.pack(expand=True)
    # Ajuste de colunas
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    # ---------------- TÍTULO ----------------
    tk.Label(
        container,
        text="Resumo geral da empresa",
        font=("Segoe UI", 18, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(pady=15, padx=10, column=0, columnspan=4, row=0)
    
    # ---------------- BOTÕES ----------------
    caixaB = tk.Frame(container, bg=COR_FUNDO)
    caixaB.grid(padx=30, pady=10, column=0, row=3, columnspan=4)
    def crbt(texto, numero, back):
        tk.Button(
        caixaB,
        text=texto,
        font=("Segoe UI", 12, "bold"),
        bg=back,
        fg="white",
        activebackground="#1E40AF",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=lambda: ajusta_pagina(numero, parent),
        cursor="hand2"
        ).pack(side="left", padx=6)
    crbt("1", 1, COR_BOTAO)
    crbt("2", 2, COR_BOTAO2)
    crbt("3", 3, COR_BOTAO3)

    # Criador de caixas
    def criador_caixas(caixa: str, coluna, linha):
        caixas = {}
        
        caixas[caixa] = tk.Frame(container, bg=COR_CAMPO, width=400, height=200)
        caixas[caixa].grid(padx=30, pady=10, column=coluna, row=linha)
        caixas[caixa].grid_propagate(False)
        caixas[caixa].grid_columnconfigure(0, weight=1)
        return caixas[caixa]
    # Aplicador de informações nas caixas
    def criador_info(texto, caixa, tfont):
        info = {}
        
        info[texto] = tk.Label(
            caixa,
            text=texto,
            font=("Segoe UI", tfont, "bold"),
            bg=COR_CAMPO,
            fg=COR_TEXTO
        )
        info[texto].grid(pady=15, padx=10, sticky="nsew")
        return info[texto]    
    # Criador de listas
    def criador_lista(nome, caixa):
        lists = {}
        
        lists[nome] = tk.Listbox(caixa, width=70, height=30, bg=COR_CAMPO, fg=COR_TEXTO, borderwidth=0, highlightthickness=0, relief="flat", justify='center')
        lists[nome].grid(pady=15, padx=10, sticky="nsew")
        return lists[nome]
    # Caixas informativas 
    caixa1 = criador_caixas("caixa1", coluna=0, linha=1)
    caixa2 = criador_caixas("caixa2", coluna=1, linha=1)
    caixa3 = criador_caixas("caixa3", coluna=0, linha=2)
    caixa4 = criador_caixas("caixa4", coluna=1, linha=2)
    
    if PAGINA == 1 :
        NUMCLI = ler_numcli()
        NUMVEIC = ler_numfro()
        NUMFUNC = ler_numfunc()
        NUMMAN = ler_manfro()
        # ---------------- Caixa Cliente ----------------
        criador_info("Clientes cadastrados", caixa1, tfont = 18)
        criador_info(f"{NUMCLI}", caixa1, tfont = 46)
        
        # ---------------- Caixa Funcionário ----------------
        criador_info("Funcionários cadastrados", caixa2, tfont = 18)
        criador_info(f"{NUMFUNC}", caixa2, tfont = 46)
        
        # ---------------- Caixa Veículos --------------------
        criador_info("Veículos Disponíveis", caixa3, tfont = 18)
        criador_info(f"{NUMVEIC}", caixa3, tfont = 46)
        
        
        # ---------------- Caixa veículos em manutenção ----------------
        criador_info("Veículos em manutenção", caixa4, tfont = 18)
        criador_info(f"{NUMMAN}", caixa4, tfont = 46)
    elif PAGINA == 2 :
        NUMTD = ler_numtest()
        NUMREU = ler_numreu()
        NUMVEN = ler_numven()
        PRECO = ler_receita()
        # ---------------- Caixa Veículos vendidos ----------------
        criador_info("Veículos Vendidos / Meta Mensal", caixa1, tfont = 18)
        criador_info(f"{NUMVEN}/10", caixa1, tfont = 46)
        
        # ---------------- Caixa Faturamento -------------------
        criador_info("Faturamento do mês (bruto)", caixa2, tfont = 18)
        criador_info(f"R$ {PRECO}", caixa2, tfont = 32)
        
        # ---------------- Caixa Test drive ----------------
        criador_info("Test drives do dia", caixa3, tfont = 18)
        lista1 = criador_lista("lista1", caixa3)
        
        # Atualiza a lista de Test drives do dia automaticamente
        tests = ler_test()
        lista1.delete(0, tk.END)
        controle = 0
        TDconf = False
        for c in tests:
            controle = controle + 1
            if AGORA in c["data"]:
                texto = f"Cliente: {c['cliente']}  |  Veículo: {c['veiculo']} | Horário: {c['horario']}"
                if len(texto) > 60:
                    texto = f"Cliente: {c['cliente']}  |  Veículo: {c['veiculo']}" 
                    texto2 = f"Horário: {c['horario']}"
                    lista1.insert(tk.END, texto)
                    lista1.insert(tk.END, texto2)
                else:
                    lista1.insert(tk.END, texto)
                TDconf = True
            elif controle == NUMTD and TDconf == False:
                texto = "NÃO HÁ TEST DRIVES AGENDADOS PARA HOJE"
                lista1.insert(tk.END, texto)
        if tests == []:
            texto = "NÃO HÁ TEST DRIVES AGENDADOS PARA HOJE"
            lista1.insert(tk.END, texto)
        
        # ---------------- Caixa reuniões do dia ----------------
        
        criador_info("Reuniões do dia", caixa4, tfont = 18)
        lista2 = criador_lista("lista2", caixa4)
            
        # Atualiza a lista de Reuniões do dia automaticamente
        reuns = ler_reu()
        lista2.delete(0, tk.END)
        controle2 = 0
        Rconf = False
        for c in reuns:
            controle2 = controle2 + 1
            if AGORA in c["data"]:
                texto = f"Cliente: {c['cliente']}  |  Local: {c['local']} | Horário: {c['horario']}"
                if len(texto) > 60:
                    texto = f"Cliente: {c['cliente']}  |  Local: {c['local']}" 
                    texto2 = f"Horário: {c['horario']}"
                    lista2.insert(tk.END, texto)
                    lista2.insert(tk.END, texto2)
                else:
                    lista2.insert(tk.END, texto)
                Rconf = True
            elif controle2 == NUMREU and Rconf == False:
                texto = "NÃO HÁ REUNIÕES AGENDADAS PARA HOJE"
                lista2.insert(tk.END, texto)
        if reuns == []:
            texto = "NÃO HÁ REUNIÕES AGENDADAS PARA HOJE"
            lista2.insert(tk.END, texto)
    elif PAGINA == 3:
        NUMVEN = ler_numven()
        NUMALU = ler_numalu()
        # ---------------- Caixa Vendas ----------------
        
        criador_info("Vendas do mês", caixa1, tfont = 18)
        lista1 = criador_lista("lista1", caixa1)
        
        # Atualiza a lista de Vendas do mês automaticamente
        vendas = ler_vendas()
        lista1.delete(0, tk.END)
        controle = 0
        Vconf = False
        for v in vendas:
            controle = controle + 1
            data = datetime.strptime(v["data_venda"], "%d/%m/%Y")
            if  data.month == int(MES):
                c = ler_cli(v["cod_cliente"])
                f = ler_fro(v["cod_veiculo"])
                texto = f"Cliente: {c['nome']}  |  Veículo: {v['nome_veiculo']} | Data: {v['data_venda']}"
                if len(texto) > 60:
                    texto = f"Cliente: {c['nome']}  |  Veículo: {v['nome_veiculo']}" 
                    texto2 = f"Data: {v['data_venda']}"
                    lista1.insert(tk.END, texto)
                    lista1.insert(tk.END, texto2)
                else:
                    lista1.insert(tk.END, texto)
                Vconf = True
            elif controle == NUMVEN and Vconf == False:
                texto = "NÃO HÁ VENDAS REALIZADAS ESSE MÊS"
                lista1.insert(tk.END, texto)
        if vendas == []:
            texto = "NÃO HÁ VENDAS REALIZADAS ESSE MÊS"
            lista1.insert(tk.END, texto)
            
        # ---------------- Caixa Aluguel ----------------
        
        criador_info("Aluguéis do mês", caixa2, tfont = 18)
        lista2 = criador_lista("lista2", caixa2)
        
        # Atualiza a lista de Aluguéis do mês automaticamente
        aluguel = ler_aluguel()
        lista2.delete(0, tk.END)
        controle = 0
        Aconf = False
        for a in aluguel:
            controle = controle + 1
            data = datetime.strptime(a["data_final"], "%d/%m/%Y")
            if  data.month == int(MES):
                c = ler_cli(a["cpf_cliente"])
                f = ler_fro(a["cod_veiculo"])
                texto = f"Cliente: {c['nome']}  |  Veículo: {f['nome']} | Data final: {a['data_final']}"
                if len(texto) > 60:
                    texto = f"Cliente: {c['nome']}  |  Veículo: {f['nome']}" 
                    texto2 = f"Data final: {a['data_final']}"
                    lista2.insert(tk.END, texto)
                    lista2.insert(tk.END, texto2)
                else:
                    lista2.insert(tk.END, texto)
                Aconf = True
            elif controle == NUMALU and Aconf == False:
                texto = "NÃO HÁ ALUGUÉIS AGENDADOS NO MÊS"
                lista2.insert(tk.END, texto)
        if aluguel == []:
            texto = "NÃO HÁ ALUGUÉIS AGENDADOS NO MÊS"
            lista2.insert(tk.END, texto)
            
        # ---------------- Caixa Aluguel2 ----------------
        
        criador_info("Aluguéis atrasados do mês", caixa3, tfont = 18)
        lista3 = criador_lista("lista3", caixa3)
        
        # Atualiza a lista de Aluguéis atrasados do mês automaticamente
        aluguel = ler_aluguel()
        lista3.delete(0, tk.END)
        controle = 0
        Aconf2 = False
        for a in aluguel:
            controle = controle + 1
            if  datetime.strptime(a["data_final"], "%d/%m/%Y") < AGORA2:
                c = ler_cli(a["cpf_cliente"])
                f = ler_fro(a["cod_veiculo"])
                texto = f"Cliente: {c['nome']}  |  Veículo: {f['nome']} | Data final: {a['data_final']}"
                if len(texto) > 60:
                    texto = f"Cliente: {c['nome']}  |  Veículo: {f['nome']}" 
                    texto2 = f"Data final: {a['data_final']}"
                    lista3.insert(tk.END, texto)
                    lista3.insert(tk.END, texto2)
                else:
                    lista3.insert(tk.END, texto)
                Aconf2 = True
            elif controle == NUMALU and Aconf2 == False:
                texto = "NÃO HÁ ALUGUÉIS ATRASADOS NO MÊS"
                lista3.insert(tk.END, texto)
        if aluguel == []:
            texto = "NÃO HÁ ALUGUÉIS ATRASADOS NO MÊS"
            lista3.insert(tk.END, texto)
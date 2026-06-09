# ========================================================
# Aluguel.py — Aluguel de veículos
#
# Aluguel.mostrar_formulario(area_conteudo)
# ========================================================

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from Menu import conn, cursor
from tkcalendar import DateEntry
import importlib

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# -------- CAPTURA DE DADOS --------

# Captura de veículos disponíveis
def frota():
    cursor.execute("""SELECT * FROM frota WHERE obs != 'Alugado'""")
    return cursor.fetchall()

# Captura de clientes disponíveis
def clientes():
    cursor.execute("""SELECT * FROM clientes""")
    return cursor.fetchall()

# Captura de vendedores
def vendedores():
    VENDAS = ["Gerente", "Assistente administrativo", "Vendedor"]
    cursor.execute("""SELECT * FROM funcionarios WHERE cargo IN (%s, %s, %s)""", tuple(VENDAS))
    return cursor.fetchall()

# --------------------------------------------------------
# SALVA OS DADOS NO BD
# --------------------------------------------------------
def salvar(cliente, veiculo, funcionario, datas, parent):
    obs2 = "Alugado"
    conn.autocommit = False
    try:
        cursor.execute("""INSERT INTO aluguel (nome_veiculo,cod_veiculo,nome_cliente,cpf_cliente,vendedor,data_inicio,data_final,horario_inicio,horario_final)
                       VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                       """,(
                        veiculo["nome"],
                        int(veiculo["codigo"]),
                        cliente["nome"],
                        cliente["cpf_cnpj"],
                        funcionario["nome"],
                        datas["data_inicio"],
                        datas["data_final"],
                        datas["horario_recebimento"],
                        datas["horario_devolucao"]
                       ))
        cursor.execute("""
            UPDATE frota
            SET 
                obs = %s
            WHERE codigo = %s
            """, (
                obs2,
                veiculo['codigo']
            ))
        conn.commit()
        messagebox.showinfo("Sucesso", "Aluguel cadastrado com sucesso!")
        mostrar_formulario(parent)
    except Exception as erro:
        conn.rollback()
        messagebox.showerror("Erro", f"O seguinte erro aconteceu: {erro}")
        return
    finally:
        conn.autocommit = True
        
def limpartela(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy() 
        
def abrir_indice(area_conteudo: tk.Frame):
    for w in area_conteudo.winfo_children():
        w.destroy()
    # Abre o Indice.py e mostra o índice na tela
    try:
        modulo = importlib.import_module("Indice")
        modulo.mostrar_formulario(area_conteudo)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao abrir a tela de Índice:\n{e}")
        
def mostrar_formulario(parent: tk.Frame):
    """Constrói o formulário de aluguel de veículos dentro do 'parent' (área central) página de clientes."""

    # Limpa qualquer conteúdo anterior
    limpartela(parent)

    CLIENTES = clientes()
    
    # Um container centralizado
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container auxiliar para melhor controle
    container2 = tk.Frame(container, bg=COR_FUNDO, width=730, height=580)
    container2.pack(expand=True)
    container2.pack_propagate(False)

    caixa = tk.Frame(container2, bg=COR_FUNDO)
    caixa.pack(expand=True)

    # ---------------- TÍTULO ----------------
    tk.Label(
        caixa,
        text="Aluguel de veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))

    # ---------------- TÍTULO2 ----------------
    tk.Label(
        caixa,
        text="Selecione o cliente",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=1, column=0, columnspan=4, pady=15)

    # ---------------- ENTRADAS ----------------
    entrada_pesq = [None] * 4
    def add_linha(rotulo, linha, col_inicio, largura=40, index=0):
        """Cria um par Label + Entry numa posição da grade."""
        tk.Label(
            caixa,
            text=rotulo,
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).grid(row=linha, column=col_inicio, sticky="w", padx=(4, 8), pady=6)

        entry = tk.Entry(
                caixa,
                width=largura,
                background=COR_CAMPO,
                foreground=COR_TEXTO2,
                insertbackground=COR_TEXTO2,
                relief="flat"
            )
        entry.grid(row=linha, column=col_inicio + 1, sticky="w", padx=(0, 10), pady=6)
        entrada_pesq[index] = entry
        
    # Linha 1
    add_linha("Nome", linha=2, col_inicio=0, largura=40, index=0)
    add_linha("CPF/CNPJ", linha=2, col_inicio=2, largura=24, index=1)

    # Linha 2
    add_linha("E-mail", linha=3, col_inicio=0, largura=40, index=2)
    add_linha("Telefone", linha=3, col_inicio=2, largura=24, index=3)
    

    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=90, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    clientes_filtrados = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        clientes_filtrados.clear()

        cursor.execute("""
        SELECT *
        FROM clientes
        WHERE
            nome LIKE %s
            OR cpf_cnpj LIKE %s
            OR REPLACE(REPLACE(REPLACE(cpf_cnpj, '.', ''), '-', ''), '/', '') LIKE %s
            OR email LIKE %s
            OR telefone LIKE %s
        """, (
            f"%{filtro[0]}%",
            f"%{filtro[1]}%",
            f"%{filtro[1]}%",
            f"%{filtro[2]}%",
            f"%{filtro[3]}%"
        ))

        clientes = cursor.fetchall()
        
        for c in clientes:
            texto = f"   {c['nome']}  |  Telefone: {c['telefone']}  |  E-mail: {c['email']}"
            lista.insert(tk.END, texto)
            clientes_filtrados.append(c)

    # Pesquisa dinâmica (a cada tecla)
    def ao_digitar(event):
        valores = [''] * 4
        for i in range(len(entrada_pesq)):
            valores[i] = (entrada_pesq[i].get().strip())
        for i in range(len(valores)):
            if valores[i] == '':
                valores[i] = '*'
        atualizar_lista(valores)
       
    for i in range(len(entrada_pesq)):
        entrada_pesq[i].bind("<KeyRelease>", ao_digitar)

    # ---------------- BOTÕES ----------------
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=5, column=0, columnspan=4, pady=15)

    # -------- LISTAGEM COMPLETA --------
    def listar_todos():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)
        clientes_filtrados.clear()

        for c in CLIENTES:          
            texto = f"   {c['nome']}  |  Telefone: {c['telefone']}  |  E-mail: {c['email']}"
            lista.insert(tk.END, texto)
            clientes_filtrados.append(c)

    # -------- LIMPAR --------
    def limpar():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)

    # -------- NOVA CONSULTA --------
    def nova_consulta():
        limpar()
        entrada_pesq[0].focus()
    
    # -------- FECHAR --------
    def fechar():
        abrir_indice(parent)
    
    # -------- AVANÇAR --------
    def avancar():
        if not lista.curselection():
            messagebox.showwarning("Nenhum cliente selecionado", "Por favor, selecione um cliente para prosseguir.")
            return
        selecionar_fro(clientes_filtrados[lista.curselection()[0]], parent)

    tk.Button(
        botoes,
        text="Fechar",
        font=("Segoe UI", 10, "bold"),
        bg="#C90202",
        fg="white",
        activebackground="#8D0202",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=fechar,
        cursor="hand2").pack(side="left", padx=6)
    tk.Button(botoes,
        text="Nova Consulta", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=nova_consulta,
        bg="#6B7280",  
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
        text="Listagem", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=listar_todos,
        bg="#6B7280", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
        text="Avançar", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=avancar, 
        bg="#2563EB", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    
def selecionar_fro(cliente, parent):
    """Reconstrói o formulário de aluguel de veículos dentro do 'parent' (área central) página de veículos."""

    # Limpa qualquer conteúdo anterior
    limpartela(parent)
    
    FROTA = frota()

    # Um container centralizado
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container auxiliar para melhor controle
    container2 = tk.Frame(container, bg=COR_FUNDO, width=730, height=580)
    container2.pack(expand=True)
    container2.pack_propagate(False)

    caixa = tk.Frame(container2, bg=COR_FUNDO)
    caixa.pack(expand=True)

    # ---------------- TÍTULO ----------------
    tk.Label(
        caixa,
        text="Aluguel de veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))
    
    # ---------------- TÍTULO2 ----------------
    tk.Label(
        caixa,
        text="Selecione o veículo",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=1, column=0, columnspan=4, pady=15)

    # ---------------- ENTRADAS ----------------
    entrada_pesq = [None] * 7
    def add_linha(rotulo, linha, col_inicio, largura=40, index=0):
        """Cria um par Label + Entry numa posição da grade."""
        tk.Label(
            caixa,
            text=rotulo,
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).grid(row=linha, column=col_inicio, sticky="w", padx=(4, 8), pady=6)

        entry = tk.Entry(
                caixa,
                width=largura,
                background=COR_CAMPO,
                foreground=COR_TEXTO2,
                insertbackground=COR_TEXTO2,
                relief="flat"
            )
        entry.grid(row=linha, column=col_inicio + 1, sticky="w", padx=(0, 10), pady=6)
        entrada_pesq[index] = entry
        
    # Linha 1
    add_linha("Nome", linha=2, col_inicio=0, largura=24, index=0)
    add_linha("Marca", linha=2, col_inicio=2, largura=24, index=1)

    # Linha 2
    add_linha("Modelo", linha=3, col_inicio=0, largura=24, index=2)
    add_linha("Motorização", linha=3, col_inicio=2, largura=21, index=3)

    # Linha 3
    add_linha("Condição", linha=4, col_inicio=0, largura=10, index=4)
    add_linha("Cor", linha=4, col_inicio=2, largura=10, index=5)

    # Linha 4
    add_linha("Ano", linha=5, col_inicio=0, largura=6, index=6)
    
    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=90, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

    veiculos_filtrados = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        veiculos_filtrados.clear()
        
        cursor.execute("""
        SELECT *
        FROM frota
        WHERE
            obs != 'Alugado' AND
            (nome LIKE %s
            OR placa LIKE %s
            OR marca LIKE %s
            OR modelo LIKE %s
            OR motorizacao LIKE %s)
        """, (
            f"%{filtro[0]}%",
            f"%{filtro[1]}%",
            f"%{filtro[2]}%",
            f"%{filtro[3]}%",
            f"%{filtro[4]}%"
        ))

        veiculos = cursor.fetchall()
        for c in veiculos:
            texto = f"   {c['marca']} {c['nome']}  |  Placa: {c['placa']}  |  Condição: {c['condicao']}  |  KM: {c['quilometragem']}  |  Preço: R$ {c['preco_aluguel']}"
            lista.insert(tk.END, texto)
            veiculos_filtrados.append(c)

    # Pesquisa dinâmica (a cada tecla)
    def ao_digitar(event):
        valores = [''] * 7
        for i in range(len(entrada_pesq)):
            valores[i] = (entrada_pesq[i].get().strip())
        for i in range(len(valores)):
            if valores[i] == '':
                valores[i] = '*'
        atualizar_lista(valores)
       
    for i in range(len(entrada_pesq)):
        entrada_pesq[i].bind("<KeyRelease>", ao_digitar)

    # ---------------- BOTÕES ----------------
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=7, column=0, columnspan=4, pady=15)

    # -------- LISTAGEM COMPLETA --------
    def listar_todos():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)
        veiculos_filtrados.clear()

        for c in FROTA:          
            texto = f"   {c['marca']} {c['nome']}  |  Placa: {c['placa']}  |  Condição: {c['condicao']}  |  KM: {c['quilometragem']}  |  Preço: {c['preco_aluguel']}"
            lista.insert(tk.END, texto)
            veiculos_filtrados.append(c)

    # -------- LIMPAR --------
    def limpar():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)

    # -------- NOVA CONSULTA --------
    def nova_consulta():
        limpar()
        entrada_pesq[0].focus()
        
    # -------- AVANÇAR --------
    def avancar():
        if not lista.curselection():
            messagebox.showwarning("Nenhum veículo selecionado", "Por favor, selecione um veículo para prosseguir.")
            return
        selecionar_fun(cliente, veiculos_filtrados[lista.curselection()[0]], parent)

    tk.Button(botoes, 
        text="Voltar", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=lambda: mostrar_formulario(parent), 
        bg="#C90202", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes,
        text="Nova Consulta", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=nova_consulta,
        bg="#6B7280",  
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
        text="Listagem", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=listar_todos,
        bg="#6B7280", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
        text="Avançar", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=avancar, 
        bg="#2563EB", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    
def selecionar_fun(cliente, veiculo, parent):
    """Reconstrói o formulário de Aluguel de veículos dentro do 'parent' (área central) página de vendedores."""

    # Limpa qualquer conteúdo anterior
    limpartela(parent)
    
    VENDEDORES = vendedores()

    # Um container centralizado
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container auxiliar para melhor controle
    container2 = tk.Frame(container, bg=COR_FUNDO, width=730, height=580)
    container2.pack(expand=True)
    container2.pack_propagate(False)

    caixa = tk.Frame(container2, bg=COR_FUNDO)
    caixa.pack(expand=True)

    # ---------------- TÍTULO ----------------
    tk.Label(
        caixa,
        text="Aluguel de veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))
    
    # ---------------- TÍTULO2 ----------------
    tk.Label(
        caixa,
        text="Selecione o vendedor",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=1, column=0, columnspan=4, pady=15)

    # ---------------- ENTRADAS ----------------
    entrada_pesq = [None] * 6
    def add_linha(rotulo, linha, col_inicio, largura=40, index=0):
        """Cria um par Label + Entry numa posição da grade."""
        tk.Label(
            caixa,
            text=rotulo,
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).grid(row=linha, column=col_inicio, sticky="w", padx=(4, 8), pady=6)

        entry = tk.Entry(
                caixa,
                width=largura,
                background=COR_CAMPO,
                foreground=COR_TEXTO2,
                insertbackground=COR_TEXTO2,
                relief="flat"
            )
        entry.grid(row=linha, column=col_inicio + 1, sticky="w", padx=(0, 10), pady=6)
        entrada_pesq[index] = entry
        
        # Linha 1
    add_linha("Nome", linha=2, col_inicio=0, largura=40, index=0)
    add_linha("CPF", linha=2, col_inicio=2, largura=24, index=1)

    # Linha 2
    add_linha("E-mail", linha=3, col_inicio=0, largura=40, index=2)
    add_linha("Telefone", linha=3, col_inicio=2, largura=24, index=3)

    # Linha 3
    add_linha("Cargo", linha=4, col_inicio=0, largura=24, index=4)
    add_linha("ID da empresa", linha=4, col_inicio=2, largura=24, index=5)
    

    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=90, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    funcionarios_filtrados = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        funcionarios_filtrados.clear()
        
        cursor.execute("""
        SELECT *
        FROM funcionarios
        WHERE
            nome LIKE %s
            OR cpf LIKE %s
            OR REPLACE(REPLACE(REPLACE(cpf, '.', ''), '-', ''), '/', '') LIKE %s
            OR email LIKE %s
            OR telefone LIKE %s
            OR cargo LIKE %s
            OR id_empresa LIKE %s
        """, (
            f"%{filtro[0]}%",
            f"%{filtro[1]}%",
            f"%{filtro[1]}%",
            f"%{filtro[2]}%",
            f"%{filtro[3]}%",
            f"%{filtro[4]}%",
            f"%{filtro[5]}%",
        ))
        
        funcionarios = cursor.fetchall()
        
        for c in funcionarios:
            texto = f"   {c['nome']}  |  ID da empresa: {c['id_empresa']}  |  Cargo: {c['cargo']}"
            lista.insert(tk.END, texto)
            funcionarios_filtrados.append(c)

    # Pesquisa dinâmica (a cada tecla)
    def ao_digitar(event):
        valores = [''] * 6
        for i in range(len(entrada_pesq)):
            valores[i] = (entrada_pesq[i].get().strip())
        for i in range(len(valores)):
            if valores[i] == '':
                valores[i] = '*'
        atualizar_lista(valores)
       
    for i in range(len(entrada_pesq)):
        entrada_pesq[i].bind("<KeyRelease>", ao_digitar)

    # ---------------- BOTÕES ----------------
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=6, column=0, columnspan=4, pady=15)

    # -------- LISTAGEM COMPLETA --------
    def listar_todos():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)
        funcionarios_filtrados.clear()

        for c in VENDEDORES:          
            texto = f"   {c['nome']}  |  ID da empresa: {c['id_empresa']}  |  Cargo: {c['cargo']}"
            lista.insert(tk.END, texto)
            funcionarios_filtrados.append(c)

    # -------- LIMPAR --------
    def limpar():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)

    # -------- NOVA CONSULTA --------
    def nova_consulta():
        limpar()
        entrada_pesq[0].focus()
        
    # -------- AVANÇAR --------
    def avancar():
        if not lista.curselection():
            messagebox.showwarning("Nenhum vendedor selecionado", "Por favor, selecione um vendedor para prosseguir.")
            return
        agendamento(cliente, veiculo, funcionarios_filtrados[lista.curselection()[0]], parent)

    tk.Button(botoes, 
        text="Voltar", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=lambda: selecionar_fro(cliente, parent), 
        bg="#C90202", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes,
        text="Nova Consulta", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=nova_consulta,
        bg="#6B7280",  
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
        text="Listagem", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=listar_todos,
        bg="#6B7280", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
        text="Avançar", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=avancar,
        bg="#2563EB", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    
def agendamento(cliente, veiculo, vendedor, parent):

    """Reconstrói o formulário de Aluguel de veículos dentro do 'parent' (área central)."""
    if vendedor == "":
        messagebox.showwarning("Nenhum vendedor selecionado", "Por favor, selecione um vendedor para prosseguir.")
        return
    # Limpa qualquer conteúdo anterior
    limpartela(parent)

    # Um container centralizado
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container auxiliar para melhor controle
    container2 = tk.Frame(container, bg=COR_FUNDO, width=730, height=580)
    container2.pack(expand=True)
    container2.pack_propagate(False)

    caixa = tk.Frame(container2, bg=COR_FUNDO)
    caixa.pack(expand=True)

    # ---------------- TÍTULO ----------------
    tk.Label(
        caixa,
        text="Aluguel de veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))
    
    # ---------------- TÍTULO2 ----------------
    tk.Label(
        caixa,
        text="Informações de agendamento",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=1, column=0, columnspan=4, pady=(0, 10))
    tk.Label(
        caixa,
        text="Selecione a data de agendamento",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=2, column=0, columnspan=4, pady=(0, 10))
    # ------- CAMPOS -------
    entradas = {}

    def add_linha(rotulo, rotuloBD, linha, col_inicio, largura=40):
        """Cria um par Label + Entry numa posição da grade."""
        tk.Label(
            caixa,
            text=rotulo,
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).grid(row=linha, column=col_inicio, sticky="w", padx=(4, 8), pady=6)
        if rotuloBD in ["horario_recebimento", "horario_devolucao"]:
            entry = tk.Entry(
                caixa,
                width=largura,
                background=COR_CAMPO,
                foreground=COR_TEXTO2,
                insertbackground=COR_TEXTO2,
                relief="flat"
            )
        else:
            entry = DateEntry(
                caixa,
                width=largura,
                foreground=COR_TEXTO,
                borderwidth=2,
                date_pattern='dd/mm/yyyy'  # Formato BR
            )
        entry.grid(row=linha, column=col_inicio + 1, sticky="w", padx=(0, 10), pady=6)
        # "rotuloBD" somente para trabalhar melhor com o dicionário no momento de salvar no BD
        entradas[rotuloBD] = entry

    # Linha 1
    add_linha("Data de início", "data_inicio", linha=3, col_inicio=0, largura=21)
    add_linha("Horário de recebimento", "horario_recebimento", linha=3, col_inicio=2, largura=24)

    # Linha 2
    add_linha("Data de devolução", "data_final", linha=4, col_inicio=0, largura=21)
    add_linha("Horário de devolução", "horario_devolucao", linha=4, col_inicio=2, largura=24)
    
    def on_salvar():
        AGORA = datetime.now().strftime("%d/%m/%Y")
        datas = {add_linha: entrada.get().strip() for add_linha, entrada in entradas.items()}
        if datas["data_inicio"] == "" or datas["data_final"] == "" or datas["horario_recebimento"] == "" or datas["horario_devolucao"] == "":
            messagebox.showwarning("Campos incompletos", "Por favor, preencha todos os campos para prosseguir.")
            return
        if datetime.strptime(datas["data_inicio"], "%d/%m/%Y") < datetime.strptime(AGORA, "%d/%m/%Y"):
            messagebox.showwarning(
                "Data inválida",
                "A data de início do aluguel não pode ser   anterior ao momento atual."
            )
            return
        elif datetime.strptime(datas["data_final"], "%d/%m/%Y") < datetime.strptime(AGORA, "%d/%m/%Y"):
            messagebox.showwarning(
                "Data inválida",
                "A data de devolução não pode ser anterior ao   momento atual."
            )
            return
        elif datetime.strptime(datas["data_final"], "%d/%m/%Y") < datetime.strptime(datas["data_inicio"], "%d/%m/%Y"):
            messagebox.showwarning(
                "Data inválida",
                "A data de devolução não pode ser anterior a data de início do aluguel."
            )
            return
        finalizar(cliente, veiculo, vendedor, datas, parent)
        
    def on_limpar():
        for ent in entradas.values():
            if isinstance(ent, DateEntry):
                ent.set_date(datetime.now())
            else:
                ent.delete(0, "end")
        
    # ---------------- BOTÕES ----------------
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=5, column=0, columnspan=4, pady=15)
    
    tk.Button(
        botoes,
        text="Salvar",
        font=("Segoe UI", 10, "bold"),
        bg="#2563EB",
        fg="white",
        activebackground="#1E40AF",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=lambda:on_salvar(),
        cursor="hand2"
    ).pack(side="left", padx=6)

    tk.Button(
        botoes,
        text="Limpar",
        font=("Segoe UI", 10, "bold"),
        bg="#6B7280",
        fg="white",
        activebackground="#4B5563",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=on_limpar,
        cursor="hand2"
    ).pack(side="left", padx=6)
    
def finalizar(cliente, veiculo, vendedor, datas, parent):
    """Reconstrói o formulário de Aluguel de veículos dentro do 'parent' (área central)."""
    
    # Limpa qualquer conteúdo anterior
    limpartela(parent)

    # Um container centralizado
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container auxiliar para melhor controle
    container2 = tk.Frame(container, bg=COR_FUNDO, width=730, height=580)
    container2.pack(expand=True)
    container2.pack_propagate(False)

    caixa = tk.Frame(container2, bg=COR_FUNDO)
    caixa.pack(expand=True)

    # ---------------- TÍTULO ----------------
    tk.Label(
        caixa,
        text="Aluguel de veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))
    
    # ---------------- TÍTULO2 ----------------
    tk.Label(
        caixa,
        text="Resumo do aluguel",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=1, column=0, columnspan=4, pady=(0, 10))
    def add_linha(rotulo, linha):
        """Cria um par Label + Entry numa posição da grade."""
        tk.Label(
            caixa,
            text=rotulo,
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).grid(row=linha, column=0, sticky="w", padx=(4, 8), pady=6)
    add_linha(f"Cliente: {cliente['nome']} - {cliente['cpf_cnpj']}", linha=2)
    add_linha(f"Veículo: {veiculo['marca']} - {veiculo['nome']} - {veiculo['modelo']}", linha=3)
    add_linha(f"Vendedor: {vendedor['nome']}", linha=4)
    add_linha(f"Data de início: {datas['data_inicio']}", linha=5)
    add_linha(f"Data de devolução: {datas['data_final']}", linha=6)
    
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=7, column=0, columnspan=4, pady=15)
        
    tk.Button(botoes, 
        text="Salvar aluguel", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=lambda: salvar(cliente, veiculo, vendedor, datas, parent),
        bg="#2563EB", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)       
    
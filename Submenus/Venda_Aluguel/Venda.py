# ========================================================
# Venda.py — Venda de veículos
#
# Venda.mostrar_formulario(area_conteudo)
# ========================================================

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from Menu import conn, cursor
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
def salvar(cliente, veiculo, funcionario, pagamento, parent):  
    AGORA = datetime.now().strftime("%d/%m/%Y")
    conn.autocommit = False
    try:
        cursor.execute("""INSERT INTO venda (nome_veiculo,cod_veiculo,data_venda,nome_cliente,cod_cliente,vendedor,pagamento,valor)
                       VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                       """,(
                        veiculo["nome"],
                        int(veiculo["codigo"]),
                        str(AGORA),
                        cliente["nome"],
                        cliente["cpf_cnpj"],
                        funcionario["nome"],
                        pagamento,
                        veiculo["preco"]
                       ))
        cursor.execute("""
            DELETE FROM frota
            WHERE codigo = %s
            """, (
                int(veiculo["codigo"]),
            ))
        conn.commit()
        messagebox.showinfo("Sucesso", "Venda realizada com sucesso!")
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
    """Constrói o formulário de Venda de veículos dentro do 'parent' (área central) página de clientes."""

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
        text="Venda de veículos",
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
    """Reconstrói o formulário de Venda de veículos dentro do 'parent' (área central) página de veículos."""

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
        text="Venda de veículos",
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
            texto = f"   {c['marca']} {c['nome']}  |  Placa: {c['placa']}  |  Condição: {c['condicao']}  |  KM: {c['quilometragem']}  |  Preço: {c['preco']}"
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
            texto = f"   {c['marca']} {c['nome']}  |  Placa: {c['placa']}  |  Condição: {c['condicao']}  |  KM: {c['quilometragem']}  |  Preço: {c['preco']}"
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
    """Reconstrói o formulário de Venda de veículos dentro do 'parent' (área central) página de vendedores."""
    
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
        text="Venda de veículos",
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
        pagamento(cliente, veiculo, funcionarios_filtrados[lista.curselection()[0]], parent)

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
    
def pagamento(cliente, veiculo, vendedor, parent):

    """Reconstrói o formulário de Venda de veículos dentro do 'parent' (área central) página de pagamentos."""

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
        text="Venda de veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))
    
    # ---------------- TÍTULO2 ----------------
    tk.Label(
        caixa,
        text="Informações de pagamento",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=1, column=0, columnspan=4, pady=(0, 10))
    tk.Label(
        caixa,
        text="Selecione o tipo de pagamento",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=2, column=0, columnspan=4, pady=(0, 10))
    # ---------------- BOTÕES ----------------
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=3, column=0, columnspan=4, pady=15)
    
    # Funcionando de forma simplificada somente para exemplificação
    tk.Button(botoes,
        text="À vista", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=lambda: finalizar(cliente, veiculo, vendedor, "À vista", parent),
        bg="#2563EB",  
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
        text="Parcelado", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=lambda: finalizar(cliente, veiculo, vendedor, "Parcelado", parent),
        bg="#2563EB", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)

def finalizar(cliente, veiculo, vendedor, pagamento, parent):
    """Reconstrói o formulário de Venda de veículos dentro do 'parent' (área central) página de resumo."""
    
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
        text="Venda de veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))
    
    # ---------------- TÍTULO2 ----------------
    tk.Label(
        caixa,
        text="Resumo da venda",
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
    add_linha(f"Pagamento: {pagamento}", linha=5)
    
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=6, column=0, columnspan=4, pady=15)

    tk.Button(botoes, 
        text="Salvar venda", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=lambda: salvar(cliente, veiculo, vendedor, pagamento, parent),
        bg="#2563EB", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
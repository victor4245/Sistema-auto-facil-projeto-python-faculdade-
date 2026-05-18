# =========================================================
# PesFun.py — Pesquisa / Consulta de Funcionários (BD)
# =========================================================

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import hashlib
# -------- CONFIGURAÇÕES BÁSICAS --------
# Conexão com o BD

try:
    conn = mysql.connector.connect(
        host="sql10.freesqldatabase.com",
        user="sql10826915",
        password="1lL7crlwDf",
        database="sql10826915",
        port=3306
    )
    conn.autocommit = True
    cursor = conn.cursor(dictionary=True)
except:
    messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados\n Verifique sua conexão com a internet")

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# ----------------------------------------------------------
# Lê TODOS os Funcionários do CSV e retorna uma lista de dicts
# ----------------------------------------------------------
def ler_Funcionarios():
    funcionarios = []

    cursor.execute("SELECT * FROM funcionarios")

    funcionarios = cursor.fetchall()

    return funcionarios

# ----------------------------------------------------------
# Tela principal da pesquisa
# ----------------------------------------------------------
def mostrar_formulario(parent):
    # Limpa a área central
    for w in parent.winfo_children():
        w.destroy()

    # Container central
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container redundante para melhor controle
    container2 = tk.Frame(container, bg=COR_FUNDO, width=700, height=500)
    container2.pack(expand=True)
    container2.pack_propagate(False)

    caixa = tk.Frame(container2, bg=COR_FUNDO)
    caixa.pack(expand=True)

    # ---------------- TÍTULO ----------------
    tk.Label(
        caixa,
        text="Pesquisa de Funcionários",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=15)

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
    add_linha("Nome", linha=1, col_inicio=0, largura=40, index=0)
    add_linha("CPF", linha=1, col_inicio=2, largura=24, index=1)

    # Linha 2
    add_linha("E-mail", linha=2, col_inicio=0, largura=40, index=2)
    add_linha("Telefone", linha=2, col_inicio=2, largura=24, index=3)

    # Linha 3
    add_linha("Cargo", linha=4, col_inicio=0, largura=24, index=4)
    add_linha("ID da empresa", linha=4, col_inicio=2, largura=24, index=5)
    

    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=90, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    funcionarios = ler_Funcionarios()
    funcionarios_filtrados = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        funcionarios_filtrados.clear()
        
        cursor.execute("""
        SELECT *
        FROM funcionarios
        WHERE
            nome ILIKE %s
            OR cpf ILIKE %s
            OR REPLACE(REPLACE(REPLACE(cpf, '.', ''), '-', ''), '/', '') ILIKE %s
            OR email ILIKE %s
            OR telefone ILIKE %s
            OR cargo ILIKE %s
            OR id_empresa ILIKE %s
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

        for c in funcionarios:          
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

    # -------- EDITAR --------
    def editar():
        if not lista.curselection():
            messagebox.showwarning("Atenção", "Selecione um funcionário.")
            return

        indice = lista.curselection()[0]
        funcionarios = funcionarios_filtrados[indice]

        abrir_edicao(funcionarios)

    # -------- FECHAR --------
    def fechar():
        for w in parent.winfo_children():
            w.destroy()

    tk.Button(botoes,
              text="Editar", 
              font=("Segoe UI", 10, "bold"),
              width=10, 
              command=editar,
              bg="#6B7280",  
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
              bg="#2563EB", 
              fg="white", 
              relief="flat",
              padx=14,
              pady=8,
              cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
              text="Limpar", 
              font=("Segoe UI", 10, "bold"),
              width=10, 
              command=limpar, 
              bg="#C90202", 
              fg="white", 
              relief="flat",
              padx=14,
              pady=8,
              cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
              text="Fechar", 
              font=("Segoe UI", 10, "bold"),
              width=10, 
              command=fechar,
              bg="#C90202",  
              fg="white", 
              relief="flat",
              padx=14,
              pady=8,
              cursor="hand2").pack(side="left", padx=4)

# ----------------------------------------------------------
# Tela de EDIÇÃO do funcionário
# ----------------------------------------------------------
def abrir_edicao(funcionario):
    janela = tk.Toplevel()
    janela.title("Editar Funcionário")
    janela.grab_set()

    entradas = {}

    def campo(texto, linha, valor=""):
        if texto == "senha":
            return
        tk.Label(janela, text=texto).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="e")
        e = tk.Entry(janela, width=40)
        e.grid(row=linha, column=1, padx=(5, 8), pady=6)
        e.insert(0, valor)
        entradas[texto] = e

    linha = 0
    def Tsenha(texto, linha, valor=""):
        janela2 = tk.Toplevel()
        janela2.title("Editar Senha")
        janela2.grab_set()
        entrada = {}
        tk.Label(janela2, text=texto).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="e")
        e = tk.Entry(janela2, width=40)
        e.grid(row=linha, column=1, padx=(5, 8), pady=6)
        e.insert(0, valor)
        def salvar2(janela2):
            entrada['senha'] = hashlib.sha256(e.get().strip().encode()).hexdigest()
            janela2.destroy()
        tk.Button(janela2, text="Salvar", command=lambda:salvar2(janela2)).grid(row=linha+1, column=0, columnspan=2, pady=10)
        janela2.wait_window()
        return entrada['senha']
        
    for k in funcionario:
        if k != "senha":
            campo(k, linha, funcionario[k])
            linha += 1
        elif k == "senha":
            tk.Button(janela, text="Trocar senha", command=lambda:entradas.update({"senha": Tsenha(k, linha, funcionario[k])})).grid(row=linha, column=0, columnspan=2, pady=10)
    linha += 1
    def salvar():
        funcionarios = ler_Funcionarios()

        for c in funcionarios:
            for k in entradas:
                if k != "senha":
                    c[k] = entradas[k].get()
                else:
                    c[k] = entradas[k]
            cursor.execute("""
            UPDATE funcionarios
            SET nome = %s,
                cpf = %s,
                email = %s,
                telefone = %s,
                cargo = %s,
                senha = %s,
                obs = %s
            WHERE id_empresa = %s
            """, (
                c['nome'],
                c['cpf'],
                c['email'],
                c['telefone'],
                c['cargo'],
                c['senha'],
                c['obs'],
                c['id_empresa']
            ))

        conn.commit()

        messagebox.showinfo("Sucesso", "Dados atualizados.")
        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar).grid(row=linha, column=0, columnspan=2, pady=10)
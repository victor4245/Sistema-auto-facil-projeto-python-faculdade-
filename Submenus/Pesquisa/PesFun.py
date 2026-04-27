# =========================================================
# PesFun.py — Pesquisa / Consulta de Funcionários (CSV)
# =========================================================

import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
# -------- CONFIGURAÇÕES BÁSICAS --------
CAMINHO_BD = os.getcwd() + "/BD_interno"

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# ----------------------------------------------------------
# Lê TODOS os Funcionários do CSV e retorna uma lista de dicts
# ----------------------------------------------------------
def ler_Funcionarios():
    caminho = CAMINHO_BD + "/CadFun.csv"
    funcionarios = []

    with open(caminho, "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            funcionarios.append(linha)

    return funcionarios

# ----------------------------------------------------------
# Salva TODOS os funcionários novamente no CSV (usado no Editar)
# ----------------------------------------------------------
def salvar_todos(funcionarios):
    if not funcionarios:
        return

    caminho = CAMINHO_BD + "/CadFun.csv"

    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=funcionarios[0].keys())
        escritor.writeheader()
        escritor.writerows(funcionarios)

# ----------------------------------------------------------
# Tela principal da pesquisa
# ----------------------------------------------------------
def mostrar_formulario(parent):
    # Limpa a área central
    for w in parent.winfo_children():
        w.destroy()

    # Container central
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(expand=True)

    caixa = tk.Frame(container, bg=COR_FUNDO, bd=1, relief="solid")
    caixa.pack(padx=40, pady=30, fill="both", expand=True)
    # Ajuste de colunas
    for c in range(4):
        caixa.grid_columnconfigure(c, weight=0)

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
                foreground=COR_TEXTO,
                insertbackground=COR_TEXTO,
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
    add_linha("Carteira de Trabalho", linha=4, col_inicio=2, largura=24, index=5)
    

    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=80, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    funcionarios = ler_Funcionarios()
    funcionarios_filtrados = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro=""):
        lista.delete(0, tk.END)
        funcionarios_filtrados.clear()
        
        for f in range(len(filtro)):
            filtro[f] = filtro[f].lower() # Transforma tudo em minusculo

        for c in funcionarios:
            if (filtro[0] in c["Nome"] or filtro[1] in c["CPF"] or filtro[2] in c["Email"] or filtro[3] in c["Telefone"] or filtro[4] in c["Cargo"] or filtro[5] in c["Carteira de Trabalho"]):
                texto = f"{c['Nome']}  |  Carteira de Trabalho: {c['Carteira de Trabalho']}"
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
            texto = f"{c['Nome']}  |  Carteira de Trabalho: {c['Carteira de Trabalho']}"
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
        tk.Label(janela, text=texto).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="e")
        e = tk.Entry(janela, width=40)
        e.grid(row=linha, column=1, padx=(5, 8), pady=6)
        e.insert(0, valor)
        entradas[texto] = e

    linha = 0
    for k in funcionario:
        campo(k, linha, funcionario[k])
        linha += 1

    def salvar():
        funcionarios = ler_Funcionarios()

        for c in funcionarios:
            if c["Carteira de Trabalho"] == funcionario["Carteira de Trabalho"]:
                for k in entradas:
                    c[k] = entradas[k].get()

        salvar_todos(funcionarios)
        messagebox.showinfo("Sucesso", "Dados atualizados.")
        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar).grid(row=linha, column=0, columnspan=2, pady=10)
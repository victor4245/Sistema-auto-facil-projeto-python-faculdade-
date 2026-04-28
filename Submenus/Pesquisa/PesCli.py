# =========================================================
# PesqCli.py — Pesquisa / Consulta de Clientes (CSV)
# =========================================================

import tkinter as tk
from tkinter import messagebox
import csv
import os
# -------- CONFIGURAÇÕES BÁSICAS --------
CAMINHO_BD = os.getcwd() + "/BD_interno"

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# ----------------------------------------------------------
# Lê TODOS os clientes do CSV e retorna uma lista de dicts
# ----------------------------------------------------------
def ler_clientes():
    caminho = CAMINHO_BD + "/CadCli.csv"
    clientes = []

    with open(caminho, "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            clientes.append(linha)

    return clientes

# ----------------------------------------------------------
# Salva TODOS os clientes novamente no CSV (usado no Editar)
# ----------------------------------------------------------
def salvar_todos(clientes):
    if not clientes:
        return

    caminho = CAMINHO_BD + "/CadCli.csv"

    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=clientes[0].keys())
        escritor.writeheader()
        escritor.writerows(clientes)

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
        text="Pesquisa de Clientes",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=15)

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
    add_linha("Nome", linha=1, col_inicio=0, largura=40, index=0)
    add_linha("CPF/CNPJ", linha=1, col_inicio=2, largura=24, index=1)

    # Linha 2
    add_linha("E-mail", linha=2, col_inicio=0, largura=40, index=2)
    add_linha("Telefone", linha=2, col_inicio=2, largura=24, index=3)
    

    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=80, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    clientes = ler_clientes()
    clientes_filtrados = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        clientes_filtrados.clear()
        
        for f in range(len(filtro)):
            filtro[f] = filtro[f].lower() # Transforma tudo em minusculo

        for c in clientes:
            if (filtro[0] in c["Nome"] or filtro[1] in c["CPF/CNPJ"] or filtro[2] in c["Email"] or filtro[3] in c["Telefone"]):
                texto = f"   {c['Nome']}  |  CPF/CNPJ: {c['CPF/CNPJ']}  |  E-mail: {c['Email']}"
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

        for c in clientes:          
            texto = f"   {c['Nome']}  |  CPF/CNPJ: {c['CPF/CNPJ']}  |  E-mail: {c['Email']}"
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

    # -------- EDITAR --------
    def editar():
        if not lista.curselection():
            messagebox.showwarning("Atenção", "Selecione um cliente.")
            return

        indice = lista.curselection()[0]
        cliente = clientes_filtrados[indice]

        abrir_edicao(cliente)

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
# Tela de EDIÇÃO do cliente
# ----------------------------------------------------------
def abrir_edicao(cliente):
    janela = tk.Toplevel()
    janela.title("Editar Cliente")
    janela.grab_set()

    entradas = {}

    def campo(texto, linha, valor=""):
        tk.Label(janela, text=texto).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="e")
        e = tk.Entry(janela, width=40)
        e.grid(row=linha, column=1, padx=(5, 8), pady=6)
        e.insert(0, valor)
        entradas[texto] = e

    linha = 0
    for k in cliente:
        campo(k, linha, cliente[k])
        linha += 1

    def salvar():
        # Armazena todos os cliente em um dicionario chamado clientes
        clientes = ler_clientes()

        for c in clientes:
            # Verifica se o CPF/CNPJ que foi editado é igual a algum dentro do dicionário clientes
            if c["CPF/CNPJ"] == cliente["CPF/CNPJ"]:
                for k in entradas:
                    # Pega o valor que foi capturado na entrada e salva no dicionário clientes
                    c[k] = entradas[k].get()

        salvar_todos(clientes)
        messagebox.showinfo("Sucesso", "Dados atualizados.")
        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar).grid(row=linha, column=0, columnspan=2, pady=10)
    
    
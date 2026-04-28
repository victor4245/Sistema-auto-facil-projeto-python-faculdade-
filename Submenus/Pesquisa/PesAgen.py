# =========================================================
# PesAgen.py — Pesquisa / Consulta de Reuniões/tests drives (CSV)
# =========================================================

import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime
# -------- CONFIGURAÇÕES BÁSICAS --------
CAMINHO_BD = os.getcwd() + "/BD_interno"
AGORA = datetime.now().strftime("%d/%m/%Y")
# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"
PAGINA = 1
def ajusta_pagina(valor):
    global PAGINA
    PAGINA = valor

        

# ----------------------------------------------------------
# Lê TODAS as reuniões do CSV e retorna uma lista de dicts
# ----------------------------------------------------------
def ler_reun():
    caminho = CAMINHO_BD + "/AgenReu.csv"
    reunioes = []

    with open(caminho, "r", newline="", encoding="utf-8", errors='ignore') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            reunioes.append(linha)

    return reunioes

# ----------------------------------------------------------
# Salva TODOS as reuniões novamente no CSV (usado no Editar)
# ----------------------------------------------------------
def salvar_reun(reuniões):
    if not reuniões:
        return

    caminho = CAMINHO_BD + "/AgenReu.csv"

    with open(caminho, "w", newline="", encoding="utf-8", errors='ignore') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=reuniões[0].keys())
        escritor.writeheader()
        escritor.writerows(reuniões)
        
# ----------------------------------------------------------
# Lê TODAS os tests drive do CSV e retorna uma lista de dicts
# ----------------------------------------------------------
def ler_TD():
    caminho = CAMINHO_BD + "/AgenTD.csv"
    Td = []

    with open(caminho, "r", newline="", encoding="utf-8", errors='ignore') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            Td.append(linha)

    return Td

# ----------------------------------------------------------
# Salva TODOS os tests drive novamente no CSV (usado no Editar)
# ----------------------------------------------------------
def salvar_TD(TD):
    if not TD:
        return

    caminho = CAMINHO_BD + "/AgendTD.csv"

    with open(caminho, "w", newline="", encoding="utf-8", errors='ignore') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=TD[0].keys())
        escritor.writeheader()
        escritor.writerows(TD)

# ----------------------------------------------------------
# Tela principal da pesquisa
# ----------------------------------------------------------
def mostrar_formulario(parent):
    if PAGINA == 1:
        NOME = "reuniões"
        LISTA = ler_reun()
        cab = "Local"
    elif PAGINA == 2:
        NOME = "test drives"
        LISTA = ler_TD()
        cab = "Veículo"
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
        text=f"Pesquisa de {NOME}",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=15)

    # ---------------- ENTRADAS ----------------
    entrada_pesq = [None] * 2
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
    add_linha("Cliente", linha=1, col_inicio=0, largura=24, index=0)
    add_linha("Data", linha=1, col_inicio=2, largura=24, index=1)

    
    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=80, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    lista_filtrada = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        lista_filtrada.clear()
        
        for f in range(len(filtro)):
            filtro[f] = filtro[f].lower() # Transforma tudo em minusculo

        for c in LISTA:
            if (filtro[0] in c["Cliente"] or filtro[1] in c["Data"]):
                texto = f"   {c['Cliente']}  |  Data: {c['Data']}  |  {cab}: {c[cab]}"
                lista.insert(tk.END, texto)
                lista_filtrada.append(c)

    # Pesquisa dinâmica (a cada tecla)
    def ao_digitar(event):
        valores = [''] * 2
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
    botoes.grid(row=3, column=0, columnspan=4, pady=15)
    
    botoes2 = tk.Frame(caixa, bg=COR_FUNDO)
    botoes2.grid(row=4, column=0, columnspan=4, pady=15)

    # -------- LISTAGEM COMPLETA --------
    def listar_todos():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)
        lista_filtrada.clear()

        for c in LISTA:          
            texto = f"   {c['Cliente']}  |  Data: {c['Data']}  |  {cab}: {c[cab]}"
            lista.insert(tk.END, texto)
            lista_filtrada.append(c)

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
            messagebox.showwarning("Atenção", "Selecione um veículo.")
            return

        indice = lista.curselection()[0]
        lis = lista_filtrada[indice]

        abrir_edicao(lis, NOME)

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
    tk.Button(
        botoes2,
        text="Reuniões",
        font=("Segoe UI", 10, "bold"),
        bg="#2563EB",
        fg="white",
        activebackground="#1E40AF",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=lambda:[ajusta_pagina(1),mostrar_formulario(parent)],
        cursor="hand2"
    ).pack(side="left", padx=6)
    tk.Button(
        botoes2,
        text="Test Drives",
        font=("Segoe UI", 10, "bold"),
        bg="#2563EB",
        fg="white",
        activebackground="#1E40AF",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=lambda:[ajusta_pagina(2),mostrar_formulario(parent)],
        cursor="hand2"
    ).pack(side="left", padx=6)

# ----------------------------------------------------------
# Tela de EDIÇÃO da reunião
# ----------------------------------------------------------
def abrir_edicao(reunioes, NOME):
    
    janela = tk.Toplevel()
    janela.title(f"Editar {NOME}")
    janela.grab_set()

    entradas = {}

    def campo(texto, linha, valor=""):
        tk.Label(janela, text=texto).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="e")
        e = tk.Entry(janela, width=40)
        e.grid(row=linha, column=1, padx=(5, 8), pady=6)
        e.insert(0, valor)
        entradas[texto] = e

    linha = 0
    for k in reunioes:
        campo(k, linha, reunioes[k])
        linha += 1

    def salvar():
        if PAGINA == 1:
            reus = ler_reun()
        elif PAGINA == 2:
            reus = ler_TD()

        for c in reus:
            if c["Cliente"] == reunioes["Cliente"]:
                for k in entradas:
                    c[k] = entradas[k].get()
        if datetime.strptime(c["Data"], "%d/%m/%Y") < datetime.strptime(AGORA, "%d/%m/%Y"):
            messagebox.showwarning("Data inválida", "A data da reunião não pode ser anterior ao momento atual.")
            return
        if PAGINA == 1:
            reus = salvar_reun(reus)
        elif PAGINA == 2:
            reus = salvar_TD(reus)
        
        messagebox.showinfo("Sucesso", "Dados atualizados.")
        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar).grid(row=linha, column=0, columnspan=2, pady=10)
    

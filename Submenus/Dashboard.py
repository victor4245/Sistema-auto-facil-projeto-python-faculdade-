# =========================================================
# Dashboard.py — Visão geral do negócio (CSV)
# =========================================================

import tkinter as tk
import csv
import os
from datetime import datetime

# -------- CONFIGURAÇÕES BÁSICAS --------

AGORA = datetime.now().strftime("%d/%m/%Y")
CAMINHO_BD = os.getcwd() + "/BD_interno"
PAGINA = 1
# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_CAMPO = "#1F2937"
COR_FUNDO = "#0B1220"

# ----------------------------------------------------------
# Aumenta ou diminui a quantidade de pagina
# ----------------------------------------------------------
def ajusta_pagina(valor):
    global PAGINA
    PAGINA = valor
# ----------------------------------------------------------
# Lê TODOS os clientes do CSV e retorna a quantidade
# ----------------------------------------------------------
with open(CAMINHO_BD + "/CadCli.csv", "r", encoding="utf-8") as arquivo:
    linhas = arquivo.readlines()
    NUMCLI = 0 + len(linhas) - 1
    
# ----------------------------------------------------------
# Lê TODOS os Veículos do CSV e retorna a quantidade
# ----------------------------------------------------------
with open(CAMINHO_BD + "/CadFro.csv", "r", encoding="utf-8") as arquivo:
    linhas = arquivo.readlines()
    NUMVEIC = 0 + len(linhas) - 1
    
# ----------------------------------------------------------
# Lê TODOS os funcionários do CSV e retorna a quantidade
# ----------------------------------------------------------
with open(CAMINHO_BD + "/CadFun.csv", "r", encoding="utf-8") as arquivo:
    linhas = arquivo.readlines()
    NUMFUNC = 0 + len(linhas) - 1

# ----------------------------------------------------------
# Lê TODOS os test drives do CSV e retorna uma lista de dicts
# ----------------------------------------------------------
with open(CAMINHO_BD + "/AgenTD.csv", "r", encoding="utf-8") as arquivo:
    linhas = arquivo.readlines()
    NUMTD = 0 + len(linhas) - 1
    
def ler_test():
    caminho = CAMINHO_BD + "/AgenTD.csv"
    test = []

    with open(caminho, "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            test.append(linha)

    return test

# ----------------------------------------------------------
# Lê TODOS as reuniões do CSV e retorna uma lista de dicts
# ----------------------------------------------------------
with open(CAMINHO_BD + "/AgenReu.csv", "r", encoding="utf-8") as arquivo:
    linhas = arquivo.readlines()
    NUMTD = 0 + len(linhas) - 1
    
def ler_reu():
    caminho = CAMINHO_BD + "/AgenReu.csv"
    reun = []

    with open(caminho, "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            reun.append(linha)

    return reun

# ----------------------------------------------------------
# Tela principal da pesquisa
# ----------------------------------------------------------
def mostrar_formulario(parent):
    # Limpa a área central
    for w in parent.winfo_children():
        w.destroy()

    # Container central
    container = tk.Frame(parent, bg=COR_FUNDO)
    container.pack(expand=True)
    # Ajuste de colunas
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    # Título 
    tk.Label(
        container,
        text="Resumo geral da empresa",
        font=("Segoe UI", 18, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(pady=15, padx=10, column=0, columnspan=4, row=0)
    # Botão de páginas
    caixaB = tk.Frame(container, bg=COR_FUNDO)
    caixaB.grid(padx=30, pady=10, column=0, row=3, columnspan=4)
    tk.Button(
        caixaB,
        text="1",
        font=("Segoe UI", 12, "bold"),
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
        caixaB,
        text="2",
        font=("Segoe UI", 12, "bold"),
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
        
        lists[nome] = tk.Listbox(caixa, width=70, height=30,bg=COR_CAMPO, fg=COR_TEXTO, borderwidth=0, highlightthickness=0, relief="flat", justify='center')
        lists[nome].grid(pady=15, padx=10, sticky="nsew")
        return lists[nome]
    # Caixas informativas 
    caixa1 = criador_caixas("caixa1", coluna=0, linha=1)
    caixa2 = criador_caixas("caixa2", coluna=1, linha=1)
    caixa3 = criador_caixas("caixa3", coluna=0, linha=2)
    caixa4 = criador_caixas("caixa4", coluna=1, linha=2)
    
    if (PAGINA == 1):
        
        # ---------------- Caixa Cliente ----------------
        
        criador_info("Clientes cadastrados", caixa1, tfont = 18)
        criador_info(f"{NUMCLI}", caixa1, tfont = 46)
        
        # ---------------- Caixa Funcionário ----------------
        
        criador_info("Funcionários cadastrados", caixa2, tfont = 18)
        criador_info(f"{NUMFUNC}", caixa2, tfont = 46)
        
        # ---------------- Caixa Veículos --------------------
        
        criador_info("Veículos Disponíveis", caixa3, tfont = 18)
        criador_info(f"{NUMVEIC}", caixa3, tfont = 46)
        
        # ---------------- Caixa Test drive ----------------
        
        criador_info("Test drives do dia", caixa4, tfont = 18)
        lista3 = criador_lista("lista3", caixa4)
        
        # Atualiza a lista de Test drives do dia automaticamente
        tests = ler_test()
        lista3.delete(0, tk.END)
        controle = 0
        for c in tests:
            controle = controle + 1
            if (AGORA in c["Data"]):
                texto = f"Cliente: {c['Cliente']}  |  Veículo: {c['Veículo']} | Horário: {c['Horario']}"
                lista3.insert(tk.END, texto)
            elif (controle == NUMTD):
                texto = "NÃO HÁ TEST DRIVES AGENDADOS PARA HOJE"
                lista3.insert(tk.END, texto)
    elif(PAGINA == 2):

        # ---------------- Caixa Veículos vendidos ----------------
        
        criador_info("Veículos Vendidos", caixa1, tfont = 18)
        criador_info("200", caixa1, tfont = 46)
        
        # ---------------- Caixa Faturamento ----------------

        criador_info("Faturamento do mês", caixa2, tfont = 18)
        criador_info("R$ 1.000.000,00", caixa2, tfont = 32)
        
        # ---------------- Caixa veículos em manutenção ----------------
        
        criador_info("Veículos em manutenção", caixa3, tfont = 18)
        criador_info("0", caixa3, tfont = 46)
        
        # ---------------- Caixa reuniões do dia ----------------
        
        criador_info("Reuniões do dia", caixa4, tfont = 18)
        lista4 = criador_lista("lista4", caixa4)
        
        # Atualiza a lista de Reuniões do dia automaticamente
        reuns = ler_reu()
        lista4.delete(0, tk.END)
        controle2 = 0
        for c in reuns:
            controle2 = controle2 + 1
            if (AGORA in c["Data"]):
                texto = f"Cliente: {c['Cliente']}  |  Local: {c['Local']} | Horário: {c['Horario']}"
                lista4.insert(tk.END, texto)
            elif (controle2 == NUMTD):
                texto = "NÃO HÁ REUNIÕES AGENDADAS PARA HOJE"
                lista4.insert(tk.END, texto)
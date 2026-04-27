# =========================================================
# Dashboard.py — Visão geral do negócio (CSV)
# =========================================================

import tkinter as tk
from tkinter import messagebox, ttk
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
# Lê TODOS os trst drives do CSV e retorna uma lista de dicts
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
        text="<<",
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
        caixaB,
        text=">>",
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
    if (PAGINA == 1):
        # Caixas informativas
        def criador_caixas(caixa: str, coluna, linha):
            caixas = {}
            if caixa == "caixa4":
                caixas[caixa] = tk.Frame(container, bg=COR_CAMPO, width=400, height=200)
                caixas[caixa].grid(padx=30, pady=10, column=coluna, row=linha)
                caixas[caixa].grid_propagate(False)
                caixas[caixa].grid_columnconfigure(0, weight=1)
            else:
                caixas[caixa] = tk.Frame(container, bg=COR_CAMPO, width=400, height=200)
                caixas[caixa].grid(padx=30, pady=10, column=coluna, row=linha)
                caixas[caixa].grid_propagate(False)
                caixas[caixa].grid_columnconfigure(0, weight=1)
            return caixas[caixa]
 
        caixa1 = criador_caixas("caixa1", coluna=0, linha=1)
        caixa2 = criador_caixas("caixa2", coluna=1, linha=1)
        caixa3 = criador_caixas("caixa3", coluna=0, linha=2)
        caixa4 = criador_caixas("caixa4", coluna=1, linha=2)


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
        tk.Label(
            caixa4,
            text="Test drives do dia",
            font=("Segoe UI", 18, "bold"),
            bg=COR_CAMPO,
            fg=COR_TEXTO
        ).grid(pady=15, sticky="n")
        lista3 = tk.Listbox(caixa4, width=70, height=6,bg=COR_CAMPO, fg=COR_TEXTO, borderwidth=0, highlightthickness=0, relief="flat", justify='center')
        lista3.grid( padx=15, pady=10, sticky="n")
        tests = ler_test()
        lista3.delete(0, tk.END)
    
        # Atualiza a lista de Test drives do dia automaticamente
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
        # Caixa informativas 2
        def criador_caixas(caixa: str, coluna, linha):
            caixas = {}
            if caixa == "caixa4":
                caixas[caixa] = tk.Frame(container, bg=COR_CAMPO, width=400, height=200)
                caixas[caixa].grid(padx=30, pady=10, column=coluna, row=linha)
                caixas[caixa].grid_propagate(False)
                caixas[caixa].grid_columnconfigure(0, weight=1)
            else:
                caixas[caixa] = tk.Frame(container, bg=COR_CAMPO, width=400, height=200)
                caixas[caixa].grid(padx=30, pady=10, column=coluna, row=linha)
                caixas[caixa].grid_propagate(False)
                caixas[caixa].grid_columnconfigure(0, weight=1)
            return caixas[caixa]
        caixa5 = criador_caixas("caixa5", coluna=0, linha=1)
        
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

        # ---------------- Caixa Veículos vendidos----------------
        
        criador_info("Veículos Vendidos", caixa5, tfont = 18)
        criador_info("200", caixa5, tfont = 46)

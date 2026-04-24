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
    container = tk.Frame(parent, bg="#FFFFFF")
    container.pack(expand=True)
    # Ajuste de colunas
    for c in range(2):
        container.grid_columnconfigure(c, weight=1)
    # Título 
    tk.Label(
        container,
        text="Resumo geral da empresa",
        font=("Segoe UI", 18, "bold"),
        bg="#FFFFFF"
    ).grid(pady=15, padx=10, sticky="nsew", column=0, columnspan=3, row=0)
    # Botão de páginas
    caixaB = tk.Frame(container, bg="#FFFFFF")
    caixaB.grid(padx=30, pady=10, column=0, row=3, columnspan=3)
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
        caixa1 = tk.Frame(container, bg="#F9FAFB", bd=1, relief="solid")
        caixa1.grid(padx=30, pady=10, column=0, row=1, ipadx=70)
        caixa2 = tk.Frame(container, bg="#F9FAFB", bd=1, relief="solid")
        caixa2.grid(padx=30, pady=10, column=2, row=1, ipadx=70)
        caixa3 = tk.Frame(container, bg="#F9FAFB", bd=1, relief="solid")
        caixa3.grid(padx=30, pady=10, column=0, row=2, ipadx=70)
        caixa4 = tk.Frame(container, bg="#F9FAFB", bd=1, relief="solid")
        caixa4.grid(padx=30, pady=10, column=2, row=2)
        
        # Ajuste de colunas
        caixa1.grid_columnconfigure(0, weight=1)
        caixa2.grid_columnconfigure(0, weight=1)
        caixa3.grid_columnconfigure(0, weight=1)
        caixa4.grid_columnconfigure(0, weight=1)
            # ---------------- Caixa Cliente ----------------
        tk.Label(
            caixa1,
            text="Clientes cadastrados",
            font=("Segoe UI", 18, "bold"),
            bg="#F9FAFB"
        ).grid(pady=15, padx=10, sticky="nsew")
        tk.Label(
            caixa1,
            text=f"{NUMCLI}",
            font=("Segoe UI", 46, "bold"),
            bg="#F9FAFB"
        ).grid(pady=15, sticky="nsew")
        # ---------------- Caixa Funcionário ----------------
        tk.Label(
            caixa2,
            text="Funcionários cadastrados",
            font=("Segoe UI", 18, "bold"),
            bg="#F9FAFB"
        ).grid(pady=15, padx=10, sticky="nsew")
        tk.Label(
            caixa2,
            text=f"{NUMFUNC}",
            font=("Segoe UI", 46, "bold"),
            bg="#F9FAFB"
        ).grid(pady=15, sticky="nsew")
        # ---------------- Caixa Veículos ----------------
        tk.Label(
            caixa3,
            text="Veículos Disponíveis",
            font=("Segoe UI", 18, "bold"),
            bg="#F9FAFB"
        ).grid(pady=15, padx=10, sticky="nsew")
        tk.Label(
            caixa3,
            text=f"{NUMVEIC}",
            font=("Segoe UI", 46, "bold"),
            bg="#F9FAFB"
        ).grid(pady=15, sticky="nsew")
        # ---------------- Caixa Test drive ----------------
        tk.Label(
            caixa4,
            text="Test drives do dia",
            font=("Segoe UI", 18, "bold"),
            bg="#F9FAFB"
        ).grid(pady=15, sticky="nsew")
        lista3 = tk.Listbox(caixa4, width=70, height=6)
        lista3.grid( padx=15, pady=10, sticky="nsew")
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
        caixa5 = tk.Frame(container, bg="#F9FAFB", bd=1, relief="solid")
        caixa5.grid(padx=30, pady=10, column=0, row=1, ipadx=80)
        
        # Ajuste de colunas
        caixa5.grid_columnconfigure(0, weight=1)

        # ---------------- Caixa Veículos vendidos----------------
        tk.Label(
            caixa5,
            text="Veículos Vendidos",
            font=("Segoe UI", 18, "bold"),
            bg="#F9FAFB"
        ).grid(pady=15, padx=10, sticky="nsew")
        tk.Label(
            caixa5,
            text="200",
            font=("Segoe UI", 46, "bold"),
            bg="#F9FAFB"
        ).grid(pady=15, sticky="nsew")

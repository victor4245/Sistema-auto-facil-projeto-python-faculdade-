# =========================================================
# PesFro.py — Pesquisa / Consulta de Veículos (CSV)
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
# Lê TODOS os Veículos do CSV e retorna uma lista de dicts
# ----------------------------------------------------------
def ler_veiculos():
    caminho = CAMINHO_BD + "/CadFro.csv"
    veiculos = []

    with open(caminho, "r", newline="", encoding="utf-8", errors='ignore') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            veiculos.append(linha)

    return veiculos

# ----------------------------------------------------------
# Salva TODOS os veículos novamente no CSV (usado no Editar)
# ----------------------------------------------------------
def salvar_todos(veiculos):
    if not veiculos:
        return

    caminho = CAMINHO_BD + "/CadFro.csv"

    with open(caminho, "w", newline="", encoding="utf-8", errors='ignore') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=veiculos[0].keys())
        escritor.writeheader()
        escritor.writerows(veiculos)

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
        text="Pesquisa de Veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=15)

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
                insertbackground=COR_TEXTO,
                relief="flat"
            )
        entry.grid(row=linha, column=col_inicio + 1, sticky="w", padx=(0, 10), pady=6)
        entrada_pesq[index] = entry
        
    # Linha 1
    add_linha("Nome", linha=1, col_inicio=0, largura=24, index=0)
    add_linha("Marca", linha=1, col_inicio=2, largura=24, index=1)

    # Linha 2
    add_linha("Modelo", linha=2, col_inicio=0, largura=24, index=2)
    add_linha("Motorização", linha=2, col_inicio=2, largura=21, index=3)

    # Linha 3
    add_linha("Condição", linha=3, col_inicio=0, largura=10, index=4)
    add_linha("Cor", linha=3, col_inicio=2, largura=10, index=5)

    # Linha 4
    
    add_linha("Ano", linha=4, col_inicio=0, largura=6, index=6)

    
    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=80, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    veiculos = ler_veiculos()
    veiculos_filtrados = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        veiculos_filtrados.clear()
        
        for f in range(len(filtro)):
            filtro[f] = filtro[f].lower() # Transforma tudo em minusculo

        for c in veiculos:
            if (filtro[0] in c["Nome"] or filtro[1] in c["Marca"] or filtro[2] in c["Modelo"] or filtro[3] in c["Motorização"]) or (filtro[4] in c["Condição"] or filtro[5] in c["Cor"] or filtro[6] in c["Ano"]):
                texto = f"   {c['Nome']}  |  Placa: {c['Placa']}  |  Marca: {c['Marca']}  |  Condição: {c['Condição']}"
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
    botoes.grid(row=6, column=0, columnspan=4, pady=15)

    # -------- LISTAGEM COMPLETA --------
    def listar_todos():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)
        veiculos_filtrados.clear()

        for c in veiculos:          
            texto = f"   {c['Nome']}  |  Placa: {c['Placa']}  |  Marca: {c['Marca']}  |  Condição: {c['Condição']}"
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

    # -------- EDITAR --------
    def editar():
        if not lista.curselection():
            messagebox.showwarning("Atenção", "Selecione um veículo.")
            return

        indice = lista.curselection()[0]
        veiculo = veiculos_filtrados[indice]

        abrir_edicao(veiculo)

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
def abrir_edicao(veiculo):
    janela = tk.Toplevel()
    janela.title("Editar Veículo")
    janela.grab_set()

    entradas = {}

    def campo(texto, linha, valor=""):
        tk.Label(janela, text=texto).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="e")
        e = tk.Entry(janela, width=40)
        e.grid(row=linha, column=1, padx=(5, 8), pady=6)
        e.insert(0, valor)
        entradas[texto] = e

    linha = 0
    for k in veiculo:
        campo(k, linha, veiculo[k])
        linha += 1

    def salvar():
        veiculos = ler_veiculos()

        for c in veiculos:
            if c["Placa"] == veiculo["Placa"]:
                for k in entradas:
                    c[k] = entradas[k].get()

        salvar_todos(veiculos)
        messagebox.showinfo("Sucesso", "Dados atualizados.")
        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar).grid(row=linha, column=0, columnspan=2, pady=10)
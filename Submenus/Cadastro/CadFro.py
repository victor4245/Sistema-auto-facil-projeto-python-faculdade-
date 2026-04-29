# ========================================================
# CadFro.py — Formulário de Veículo
#
# CadFro.mostrar_formulario(area_conteudo)
# ========================================================

import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
# -------- CONFIGURAÇÕES BÁSICAS --------
CAMINHO_BD = os.getcwd() + "/BD_interno"

def limpar(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()
        
# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# --------------------------------------------------------
# SALVA OS DADOS NO ARQUIVO CSV
# --------------------------------------------------------
def salvar(dados):
    # Verificação simples (iniciante)
    if dados["Nome"] == "" or dados["Placa"] == "":
        messagebox.showwarning(
            "Campos obrigatórios faltando",
            "Preencha pelo menos o Nome e a Placa."
        )
        return

    caminho = CAMINHO_BD + "/CadFro.csv"

    # Verifica se o arquivo existe
    arquivo_existe = os.path.exists(caminho)
    if not arquivo_existe:
        messagebox.showwarning(
            "Banco de dados não encontrado",
            "Procure o arquivo CadFro.csv dentro da pasta BD_interno"
        )
        return

    for f in dados:
        dados[f] = dados[f].lower() # Transforma tudo em minusculo
    try:
        with open(caminho, "a", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo, delimiter=",")

            # Se o arquivo NÃO existir, escreve o cabeçalho
            if not arquivo_existe:
                escritor.writerow(dados.keys())

            # Escreve os dados do cliente
            escritor.writerow(dados.values())

        messagebox.showinfo(
            "Sucesso",
            "Veículo salvo com sucesso no banco de dados interno!"
        )
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))

def mostrar_formulario(parent: tk.Frame):
    """
    Constrói o formulário de Veículo dentro do 'parent' (área central).
    """

    # Limpa qualquer conteúdo anterior
    limpar(parent)

    # Um container centralizado
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container redundante para melhor controle
    container2 = tk.Frame(container, bg=COR_FUNDO, width=700, height=500)
    container2.pack(expand=True)
    container2.pack_propagate(False)

    caixa = tk.Frame(container2, bg=COR_FUNDO)
    caixa.pack(expand=True)


    # Título
    tk.Label(
        caixa,
        text="Cadastro de Veículo",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))

    # ------- CAMPOS -------
    entradas = {}

    def add_linha(rotulo, linha, col_inicio, largura=40):
        """Cria um par Label + Entry numa posição da grade."""
        tk.Label(
            caixa,
            text=rotulo,
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).grid(row=linha, column=col_inicio, sticky="w", padx=(4, 8), pady=6)
        if rotulo == "Cor":
            entry = ttk.Combobox(caixa, values=[' ', 'Amarelo', 'Azul', 'Bege', 'Branco', 'Cinza', 
                                                'Fantasia', 'Laranja', 'Marrom', 'Preto', 'Prata', 
                                                'Roxo', 'Verde', 'Vermelho', 'Vinho'], width=largura, state="readonly")
            entry.current(0)
        elif rotulo == "Condição":
            entry = ttk.Combobox(caixa, values=[' ', 'Novo', 'Usado', 'Semi-novo'], width=largura, state="readonly")  
            entry.current(0)
        elif rotulo == "Motorização":
            entry = ttk.Combobox(caixa, values=[' ', 'Combustão Flex', 'Combustão Álcool', 
                                                'Combustão Gasolina', 'Combustão Diesel', 'Híbrido', 'Elétrico', 'Combustão GNV'], width=largura, state="readonly")      
            entry.current(0)
        else:    
            entry = tk.Entry(
                caixa,
                width=largura,
                background=COR_CAMPO,
                foreground=COR_TEXTO2,
                insertbackground=COR_TEXTO2,
                relief="flat"
            )
        entry.grid(row=linha, column=col_inicio + 1, sticky="w", padx=(0, 10), pady=6)

        entradas[rotulo] = entry

    # Linha 1
    add_linha("Nome", linha=1, col_inicio=0, largura=24)
    add_linha("Marca", linha=1, col_inicio=2, largura=24)

    # Linha 2
    add_linha("Modelo", linha=2, col_inicio=0, largura=24)
    add_linha("Motorização", linha=2, col_inicio=2, largura=21)

    # Linha 3
    add_linha("Condição", linha=3, col_inicio=0, largura=10)
    add_linha("Placa", linha=3, col_inicio=2, largura=12)
    
    # Linha 4
    add_linha("Cor", linha=4, col_inicio=0, largura=10)
    add_linha("Ano", linha=4, col_inicio=2, largura=6)

    # Observações
    tk.Label(
        caixa,
        text="Observações",
        font=("Segoe UI", 10, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=5, column=0, columnspan=4, sticky="", padx=(8, 8), pady=6)

    txt_obs = tk.Text(caixa, width=66, height=5, background=COR_CAMPO,foreground=COR_TEXTO2,insertbackground=COR_TEXTO2, relief="flat")
    txt_obs.grid(row=6, column=0, columnspan=4, sticky="", padx=(10, 10), pady=6)
    
    entradas["Nome"].focus()
    
    # Botões
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=7, column=0, columnspan=4, pady=(16, 0))

    def on_salvar():
        dados = {add_linha: entrada.get().strip() for add_linha, entrada in entradas.items()}
        dados["Observações"] = txt_obs.get("1.0", "end-1c").strip()
        salvar(dados)

    def on_limpar():
        for ent in entradas.values():
            ent.delete(0, "end")
        txt_obs.delete("1.0", "end-1c")

    def on_cancelar():
        limpar(parent)

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
        command=on_salvar,
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

    tk.Button(
        botoes,
        text="Cancelar",
        font=("Segoe UI", 10, "bold"),
        bg="#C90202",
        fg="white",
        activebackground="#8D0202",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=on_cancelar,
        cursor="hand2"
    ).pack(side="left", padx=6)

    # Ajuste de colunas
    for c in range(4):
        caixa.grid_columnconfigure(c, weight=0)
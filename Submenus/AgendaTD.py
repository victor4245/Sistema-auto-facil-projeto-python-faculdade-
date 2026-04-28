# ========================================================
# AgendaTD.py — Agendamento de Test Drive
#
# AgendaTD.mostrar_formulario(area_conteudo)
# ========================================================

import tkinter as tk
from tkinter import messagebox, ttk
# tkcalendar é necessário para o campo de data
try:
    from tkcalendar import DateEntry
    DATE_OK = True
except Exception:
    DATE_OK = False
import csv
import os

# -------- CONFIGURAÇÕES BÁSICAS --------

CAMINHO_BD = os.getcwd() + "/BD_interno"
# Criação de código automática
with open(CAMINHO_BD + "/AgenTD.csv", "r", encoding="utf-8") as arquivo:
    linhas = arquivo.readlines()
    AUX = 0 + len(linhas)

def limpar(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()
# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# --------------------------------------------------------
# SALVA OS DADOS NO ARQUIVO CSV
# --------------------------------------------------------
def salvar(dados):
    # Verificação simples (iniciante)
    if dados["Data"] == "" or dados["Cliente"] == "":
        messagebox.showwarning(
            "Campos obrigatórios",
            "Preencha pelo menos a Data e o Cliente."
        )
        return

    caminho = CAMINHO_BD + "/AgenTD.csv"

    # Verifica se o arquivo existe
    arquivo_existe = os.path.exists(caminho)
    if not arquivo_existe:
        messagebox.showwarning(
            "Banco de dados não encontrado",
            "Procure o arquivo AgenTD.csv dentro da pasta BD_interno"
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

            # Escreve os dados do Test Drive
            escritor.writerow(dados.values())

        messagebox.showinfo(
            "Sucesso",
            "Test Drive salvo com sucesso!\n\nArquivo:\n/BD_interno/AgendaTD.csv"
        )

    except Exception as erro:
        messagebox.showerror("Erro", str(erro))
    

def mostrar_formulario(parent: tk.Frame):
    if not DATE_OK:
        messagebox.showwarning("Pillow não encontrado", "Para exibir a imagem de fundo, instale a biblioteca Pillow:\n\npip install pillow")
        return None
    """
    Constrói o formulário de Test Drive dentro do 'parent' (área central).
    """

    # Limpa qualquer conteúdo anterior
    limpar(parent)

    # Um container centralizado
    container = tk.Frame(parent, bg=COR_FUNDO)
    container.pack(expand=True, ipadx=30, ipady=20)

    caixa = tk.Frame(container, bg=COR_FUNDO)
    caixa.pack(padx=40, pady=30, expand=True)

    # Título
    tk.Label(
        caixa,
        text="Agendamento de Test Drive",
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
        if rotulo == "Data":
            entry = DateEntry(
                caixa,
                width=largura,
                background=COR_CAMPO,
                foreground=COR_TEXTO,
                borderwidth=2,
                date_pattern='dd/mm/yyyy'  # formato BR
            )
        else:
            entry = ttk.Entry(
                caixa,
                width=largura
            )
        entry.grid(row=linha, column=col_inicio + 1, sticky="w", padx=(0, 10), pady=6)

        entradas[rotulo] = entry

    # Linha 1
    add_linha("Cliente", linha=1, col_inicio=0, largura=40)
    add_linha("Horário", linha=1, col_inicio=2, largura=24)

    # Linha 2
    add_linha("Data", linha=2, col_inicio=0, largura=24)
    add_linha("Veículo", linha=2, col_inicio=2, largura=24)

    # Observações
    tk.Label(
        caixa,
        text="Observações",
        font=("Segoe UI", 10, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=3, column=0, columnspan=4, sticky="", padx=(8, 8), pady=6)

    txt_obs = tk.Text(caixa, width=66, height=5, bd=1, relief="solid")
    txt_obs.grid(row=4, column=0, columnspan=4, sticky="", padx=(10, 10), pady=6)

    # Botões
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=5, column=0, columnspan=4, pady=16)

    def on_salvar():
        dados = {add_linha: entrada.get().strip() for add_linha, entrada in entradas.items()}
        dados["Código"] = str(AUX)
        dados["Observações"] = txt_obs.get("1.0", "end").strip()
        salvar(dados)

    def on_limpar():
        for ent in entradas.values():
            ent.delete(0, "end")
        txt_obs.delete("1.0", "end")

    def on_cancelar():
        limpar(parent)

    tk.Button(
        botoes,
        text="Salvar",
        bg="#2563EB",
        fg="white",
        activebackground="#1E40AF",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=lambda:[on_salvar(), on_limpar()],
        cursor="hand2"
    ).pack(side="left", padx=6)

    tk.Button(
        botoes,
        text="Limpar",
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
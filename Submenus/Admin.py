# ========================================================
# Admin.py — Formulário de Administrador
#
# Admin.mostrar_formulario(area_conteudo)
# ========================================================

import tkinter as tk
import os
from tkinter import messagebox

# -------- CONFIGURAÇÕES BÁSICAS --------

LOGIN_ADM = "admin"
SENHA_ADM = "123"
CAMINHO_BD = os.getcwd() + "/BD_interno"
PERMITIDOS = ["Administrador", "Marcos Silva"]

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_CAMPO = "#1F2937"
COR_FUNDO = "#0B1220"

def limpar(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()
        
def abrir_bd(nome_arquivo: str):
    try:
        os.startfile(f"{CAMINHO_BD}/{nome_arquivo}")
    except:
        messagebox.showerror("Erro", f"Não foi possível abrir o arquivo {nome_arquivo}.\nVerifique se ele existe dentro da pasta BD_interno.")
        return

def limpar_log():
    resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja limpar o log? Esta ação não pode ser desfeita.")
    if resposta:

        with open(f"{CAMINHO_BD}/Log.txt", "w") as f:
            f.write("")
        messagebox.showinfo("Sucesso", "Log limpo com sucesso.")
    else:
        return        
    
def ao_acessar(campo_login: tk.Entry, campo_senha: tk.Entry, janela: tk.Frame):
    """Ação do botão Acessar (e tecla Enter):
    - Verifica se os campos estão preenchidos
    - Valida credenciais
    - Se ok, abre o menu"""
    login = campo_login.get().strip()
    senha = campo_senha.get().strip()
    if not login or not senha:
        messagebox.showwarning("Campos obrigatórios", "Informe login e senha.")
        return

    # Mensagem de erro caso login ou senha estejam incorretos
    if not login == LOGIN_ADM or not senha == SENHA_ADM:
        messagebox.showerror("Acesso negado", "Login ou senha incorretos.")
        return
    
    mostrar_comandos(janela)
def mostrar_comandos(janela: tk.Frame):
    parent = janela
    # Limpa a área central
    limpar(parent)

    # Container central
    container = tk.Frame(parent, bg=COR_FUNDO)
    container.pack(expand=True)
    # Ajuste de colunas
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    # Título 
    tk.Label(
        container,
        text="Comandos do administrador",
        font=("Segoe UI", 18, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(pady=15, padx=10, column=0, columnspan=4, row=0)
    # Criador de botoes
    def criador_botoes(funcao: str, coluna, linha, comando=None):
        funcoes = {}
        
        funcoes[funcao] = tk.Button(container, 
                                    text=funcao, 
                                    font=("Segoe UI", 16, "bold"), 
                                    bg="#2563EB", fg=COR_TEXTO,
                                    activebackground="#1E40AF",
                                    activeforeground=COR_TEXTO,
                                    relief="flat",
                                    width=20,
                                    command= comando,
                                    cursor="hand2"
                                    )
        funcoes[funcao].grid(padx=30, pady=10, column=coluna, row=linha)
        return funcoes[funcao]
    criador_botoes("Abrir BD Clientes", coluna=0, linha=1, comando=lambda: abrir_bd("Cadcli.csv"))
    criador_botoes("Abrir BD Funcionários", coluna=1, linha=1, comando=lambda: abrir_bd("CadFun.csv"))
    criador_botoes("Abrir BD Frota", coluna=0, linha=2, comando=lambda: abrir_bd("CadFro.csv"))
    criador_botoes("Abrir BD Reunião", coluna=1, linha=2, comando=lambda: abrir_bd("AgenReu.csv"))
    criador_botoes("Abrir BD Test Drive", coluna=0, linha=3, comando=lambda: abrir_bd("AgenTD.csv"))
    criador_botoes("Limpar Logs", coluna=1, linha=3, comando=lambda: limpar_log())
def mostrar_formulario(parent: tk.Frame, pessoa = None):
    if pessoa in PERMITIDOS:
        mostrar_comandos(parent)
    else:
        # Limpa qualquer conteúdo anterior
        limpar(parent)

        # Um container centralizado
        container = tk.Frame(parent, bg=COR_FUNDO)
        container.pack(expand=True, ipadx=5, ipady=5)

        funcao = tk.Frame(container, bg=COR_FUNDO)
        funcao.pack(padx=15, pady=15)
        for col in range(6):
            funcao.grid_columnconfigure(col, weight=1)

        cor_faixa = "#0B1220"
        cor_campo = "#1F2937"
        cor_texto = "#FFFFFF"
        # Título
        tk.Label(
            funcao,
            text="Login administrativo",
            font=("Segoe UI", 16, "bold"),
            bg="#0B1220",
            fg=cor_texto
        ).grid(row=0, column=0, columnspan=4, pady=(0, 10))

        tk.Label(
            funcao, text="Login:", font=("Segoe UI", 11, "bold"),
            bg=cor_faixa, fg=cor_texto
        ).grid(row=1, column=0, sticky="", padx=(6, 6), pady=6)

        entrada_login = tk.Entry(
            funcao, font=("Segoe UI", 11),
            bg=cor_campo, fg=cor_texto,
            insertbackground=cor_texto, relief="flat"
        )
        entrada_login.grid(row=1, column=1, sticky="", padx=(0, 12), pady=6)
        entrada_login.focus()

        # Senha
        tk.Label(
            funcao, text="Senha:", font=("Segoe UI", 11, "bold"),
            bg=cor_faixa, fg=cor_texto
        ).grid(row=2, column=0, sticky="", padx=(6, 6), pady=6)

        entrada_senha = tk.Entry(
            funcao, show="*",
            font=("Segoe UI", 11),
            bg=cor_campo, fg=cor_texto,
            insertbackground=cor_texto, relief="flat"
        )
        entrada_senha.grid(row=2, column=1, sticky="", padx=(0, 12), pady=6)

        # Botão Acessar
        btn_acessar = tk.Button(
            funcao, text="Acessar",
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB", fg="white",
            activebackground="#1E40AF",
            activeforeground="white",
            relief="flat", padx=16, pady=8,
            command=lambda: ao_acessar(entrada_login, entrada_senha, parent),
            cursor="hand2"
        )
        btn_acessar.grid(row=3, column=0, sticky="ws", padx=(20, 0), pady=(25, 0))

        # Botão Cancelar
        btn_cancelar = tk.Button(
            funcao, text="Cancelar",
            font=("Segoe UI", 10, "bold"),
            bg="#374151", fg="white",
            activebackground="#1F2937",
            activeforeground="white",
            relief="flat", padx=16, pady=8,
            command=lambda: limpar(parent),
            cursor="hand2"
        )
        btn_cancelar.grid(row=3, column=1, sticky="es", padx=(0, 20), pady=(25, 0))
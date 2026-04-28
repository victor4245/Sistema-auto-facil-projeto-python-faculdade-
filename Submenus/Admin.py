# ========================================================
# Admin.py — Formulário de Administrador
#
# Admin.mostrar_formulario(area_conteudo)
# ========================================================

import tkinter as tk
from tkinter import messagebox
# -------- CONFIGURAÇÕES BÁSICAS --------
LOGIN_ADM = "admin"
SENHA_ADM = "123"
# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

def limpar(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()
def ao_acessar(campo_login: tk.Entry, campo_senha: tk.Entry, janela: tk.Tk):
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
    
    # Sem função por enquanto somente mensagem 
    messagebox.showinfo("Bem-vindo", "Acesso concedido.")

def mostrar_formulario(parent: tk.Frame):
    # Limpa qualquer conteúdo anterior
    limpar(parent)

    # Um container centralizado
    container = tk.Frame(parent, bg=COR_FUNDO)
    container.pack(expand=True, ipadx=5, ipady=5)

    caixa = tk.Frame(container, bg=COR_FUNDO)
    caixa.pack(padx=40, pady=30)
    for col in range(6):
        caixa.grid_columnconfigure(col, weight=1)

    cor_faixa = "#0B1220"
    cor_campo = "#1F2937"
    cor_texto = "#FFFFFF"
    # Título
    tk.Label(
        caixa,
        text="Login administrativo",
        font=("Segoe UI", 16, "bold"),
        bg="#0B1220",
        fg=cor_texto
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))

    tk.Label(
        caixa, text="Login:", font=("Segoe UI", 11, "bold"),
        bg=cor_faixa, fg=cor_texto
    ).grid(row=1, column=0, sticky="", padx=(6, 6), pady=6)

    entrada_login = tk.Entry(
        caixa, font=("Segoe UI", 11),
        bg=cor_campo, fg=cor_texto,
        insertbackground=cor_texto, relief="flat"
    )
    entrada_login.grid(row=1, column=1, sticky="", padx=(0, 12), pady=6)
    entrada_login.focus()

    # Senha
    tk.Label(
        caixa, text="Senha:", font=("Segoe UI", 11, "bold"),
        bg=cor_faixa, fg=cor_texto
    ).grid(row=2, column=0, sticky="", padx=(6, 6), pady=6)

    entrada_senha = tk.Entry(
        caixa, show="*",
        font=("Segoe UI", 11),
        bg=cor_campo, fg=cor_texto,
        insertbackground=cor_texto, relief="flat"
    )
    entrada_senha.grid(row=2, column=1, sticky="", padx=(0, 12), pady=6)

    # Botão Acessar
    btn_acessar = tk.Button(
        caixa, text="Acessar",
        font=("Segoe UI", 10, "bold"),
        bg="#2563EB", fg="white",
        activebackground="#1E40AF",
        activeforeground="white",
        relief="flat", padx=16, pady=8,
        command=lambda: ao_acessar(entrada_login, entrada_senha, parent),
        cursor="hand2"
    )
    btn_acessar.grid(row=3, column=1, sticky="es", padx=(0, 14), pady=(25, 0))

    # Botão Sair
    btn_sair = tk.Button(
        caixa, text="Sair",
        font=("Segoe UI", 10, "bold"),
        bg="#374151", fg="white",
        activebackground="#1F2937",
        activeforeground="white",
        relief="flat", padx=16, pady=8,
        #command=lambda: ao_sair(raiz),
        cursor="hand2"
    )
    btn_sair.grid(row=3, column=0, sticky="s", padx=(14, 0), pady=(25, 0))
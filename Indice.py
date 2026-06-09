# ========================================================
# Indice.py — Índice do menu principal
#
# Indice.mostrar_formulario(area_conteudo)
# ========================================================

import importlib
import tkinter as tk
from tkinter import messagebox

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

def abrir_aba_nova(area_conteudo: tk.Frame, titulo:str, nome:str):
    limpar(area_conteudo)
    try:
        modulo = importlib.import_module(titulo)
        modulo.mostrar_formulario(area_conteudo)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao abrir a tela de {nome}:\n{e}")
        return
def limpar(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()
def mostrar_formulario(parent: tk.Frame):
    """Constrói o Índice dentro do 'parent' (área central)."""

    # Limpa qualquer conteúdo anterior
    limpar(parent)

    # Um container centralizado
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container auxiliar para melhor controle
    container2 = tk.Frame(container, bg=COR_FUNDO, width=300, height=380)
    container2.pack(expand=True)
    container2.pack_propagate(False)

    caixa = tk.Frame(container2, bg=COR_FUNDO)
    caixa.pack(expand=True)

    # ---------------- TÍTULO ----------------
    tk.Label(
        caixa,
        text="Acesso rápido",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))

    def criar_item_menu(texto: str, icone: str, subitens=None, acao=None, acoes_subitens=None):
        """Cria um item de menu."""
        item = tk.Frame(caixa, bg="#0B1220")
        item.grid()

        btn = tk.Button(
            item,
            text=f"{icone} {texto}",
            font=("Segoe UI Emoji", 11, "bold"),
            bg="#093255", fg="#FFFFFF",
            activebackground="#1F2937", activeforeground="#FFFFFF",
            relief="flat", width=30, pady=10, cursor="hand2", justify="center"
        )
        btn.grid(padx=12, pady=6)
        btn.configure(command=lambda: acao())
        
    criar_item_menu(
        texto="Cadastro de cliente",
        icone="\U0001F464",
        subitens=None,
        acao=lambda: abrir_aba_nova(parent, "Submenus.Cadastro.CadCli", "Cadastro")
    )
    criar_item_menu(
        texto="Cadastro de veículo",
        icone="\U0001F699",
        subitens=None,
        acao=lambda: abrir_aba_nova(parent, "Submenus.Cadastro.CadFro", "Cadastro")
    )
    criar_item_menu(
        texto="Agendamento de Test Drive",
        icone="\U0001F698",
        subitens=None,
        acao=lambda: abrir_aba_nova(parent, "Submenus.Agendamento.AgendaTD", "Agendamento")
    )
    criar_item_menu(
        texto="Agendamento de Reunião",
        icone="\U0001F5D3",
        subitens=None,
        acao=lambda: abrir_aba_nova(parent, "Submenus.Agendamento.AgendaReu", "Agendamento")
    )

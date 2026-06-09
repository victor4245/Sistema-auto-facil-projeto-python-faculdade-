#=======================================================
# SISTEMA: Menu Principal (layout estilo "sistema web" com sidebar)
# Tecnologias gráficas: Python 3.x + Tkinter (somente biblioteca padrão)
# Menu.py
# ========================================================

import os
import sys
import tkinter as tk
from tkinter import messagebox
import importlib
from PIL import Image, ImageTk
import mysql.connector

# -------- CONFIGURAÇÕES BÁSICAS --------
# Conexão com o BD
try:
    conn = mysql.connector.connect(
        host="sql10.freesqldatabase.com",
        user="sql10829783",
        password="1LQCBWpLZR",
        database="sql10829783",
        port=3306
    )
    conn.autocommit = True
    cursor = conn.cursor(dictionary=True)
except Exception as e:
    messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados\n erro: {e}")
    
CAMINHO_IMAGENS = os.getcwd() + "/Imagens"
VERSION = "v 1.0.0"
ARQUIVO_MAIN = "Autofacil.py"
PERMITIDOS = ["Administrador", "Gerente", "Assistente administrativo"]
PERMITIDOS2 = ["Administrador", "Gerente", "Assistente administrativo", "Vendedor"]
ABAS = ["Dashboard", "Funcionarios"]
ABAS2 = ["Cadastro", "Venda/Aluguel", "Agendamento"]

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

def limpar_menu(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()
    abrir_aba_nova(parent, "Indice", nome="Menu Principal")
# -------------------- UTILITÁRIOS ---------------------------
def maximizar_janela(janela: tk.Tk):
    """Deixa a janela maximizada (Windows/Linux) com fallback."""
    try:
        janela.update_idletasks()
        try:
            janela.state("zoomed")  # Windows
        except Exception:
            pass
        try:
            janela.attributes("-zoomed", True)  # Linux
        except Exception:
            pass
        try:
            w = janela.winfo_screenwidth()
            h = janela.winfo_screenheight()
            janela.geometry(f"{w}x{h}+0+0")  # fallback
        except Exception:
            pass
    except Exception:
        pass

def limpar_area(area: tk.Frame):
    """Remove todos os widgets da área de conteúdo (limpa o centro)."""
    for w in area.winfo_children():
        w.destroy()

def abrir_aba_nova(area_conteudo: tk.Frame, titulo:str, nome:str):
    limpar_area(area_conteudo)
    # Controle de acesso simples baseado no cargo do usuário
    if (nome in ABAS and cargo not in PERMITIDOS) or (nome in ABAS2 and cargo not in PERMITIDOS2):
        messagebox.showwarning("Acesso Negado", "Você não tem permissão para acessar esta função.")
        return
    try:
        modulo = importlib.import_module(titulo)
        modulo.mostrar_formulario(area_conteudo)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao abrir a tela de {nome}:\n{e}")

def sair(raiz:tk.Tk):
    # Mensagem de confirmação
    confirma = tk.messagebox.askyesno("Logout", "Deseja sair do sistema?")
    if confirma:
        import subprocess
        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_main = os.path.join(base_dir, ARQUIVO_MAIN)
        if not os.path.exists(caminho_main):
            messagebox.showerror("Autofacil.py não encontrado",f"Coloque o arquivo 'Autofacil.py' no mesmo diretório deste script:\n{base_dir}")
            return
        try:
            subprocess.Popen([sys.executable, caminho_main])
            raiz.destroy()
        except Exception as e:
            messagebox.showerror("Erro ao abrir a tela de inicio",f"Não foi possível abrir 'Autofacil.py':\n{e}")
    else:
        return
# -------------------- ETAPA 1: JANELA + TOPO ----------------
def criar_janela_principal() -> tk.Tk:
    """Cria a janela principal e a faixa de topo azul, com título centralizado."""
    raiz = tk.Tk()
    raiz.title("Sistema de Gerenciamento de Autos")
    raiz.minsize(900, 580)
    raiz.iconbitmap(CAMINHO_IMAGENS + "/LogoA.ico")

    # Abre maximizada
    maximizar_janela(raiz)

    # GRID: 2 colunas (0 = sidebar | 1 = área direita)
    raiz.grid_columnconfigure(0, minsize=220)  # Sidebar fixa
    raiz.grid_columnconfigure(1, weight=1)     # Área direita expande
    raiz.grid_rowconfigure(1, weight=1)        # Linha do conteúdo expande

    return raiz

# ------------- ETAPA 2: SIDEBAR (azul) + MENU --------------
def criar_sidebar(raiz: tk.Tk) -> tk.Frame:
    """Cria a faixa lateral esquerda azul e retorna o container do menu."""
    sidebar = tk.Frame(raiz, bg=COR_FUNDO)
    sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

    topo_sidebar = tk.Frame(sidebar, bg=COR_FUNDO, height=170)
    topo_sidebar.pack(side="top", fill="x")
    topo_sidebar.pack_propagate(False)

    img = Image.open(CAMINHO_IMAGENS + "/Carro.png").convert("RGBA")
    img = img.resize((160, 140))
    img_logo = ImageTk.PhotoImage(img)
    lbl_logo = tk.Label(
        topo_sidebar,
        bg=COR_FUNDO,
        image=img_logo,
        cursor="hand2"
    )
    lbl_logo.image = img_logo
    lbl_logo.pack()
    # Torna o logo clicável para voltar ao menu principal
    lbl_logo.bind("<Button-1>",lambda e: limpar_menu(conteudo))
    
    lbl_nome = tk.Label(
        topo_sidebar, text=f"SysCar {VERSION}", font=("Segoe UI", 11, "bold"),
        bg=COR_FUNDO, fg="#E5E7EB"
    )
    lbl_nome.pack()

    menu_container = tk.Frame(sidebar, bg=COR_FUNDO)
    menu_container.pack(side="top", fill="both", expand=True, pady=(10, 12))

    return menu_container

# --------- ETAPA 3: MENU + SUBMENUS -------------------------
def criar_item_menu(texto: str, icone: str, subitens=None, acao=None, acoes_subitens=None):
    """Cria um item do menu."""
    item = tk.Frame(area_menu, bg=COR_FUNDO)
    item.pack(fill="x")

    btn = tk.Button(
        item,
        text=f"{icone} {texto}",
        font=("Segoe UI Emoji", 11, "bold"),
        bg="#093255", fg=COR_TEXTO,
        activebackground="#1F2937", activeforeground=COR_CAMPO,
        relief="flat", padx=12, pady=10, anchor="w", cursor="hand2"
    )
    btn.pack(fill="x", padx=12, pady=6)

    if not subitens:
        btn.configure(command=lambda: acao())
        return

    submenu = tk.Frame(item, bg=COR_FUNDO)
    submenu.pack(fill="x", padx=0, pady=(0, 6))
    submenu.pack_forget()

    for nome in subitens:
        acao_sub = acoes_subitens.get(nome)

        sub_btn = tk.Button(
            submenu,
            text=f" • {nome}",
            font=("Segoe UI", 10),
            bg="#0F172A", fg=COR_TEXTO,
            activebackground="#1F2937", activeforeground=COR_CAMPO,
            relief="flat", padx=14, pady=8, anchor="w", cursor="hand2",
            command=acao_sub
        )
        sub_btn.pack(fill="x", padx=22, pady=(0, 4))

    def alternar_submenu():
        if submenu.winfo_ismapped():
            submenu.pack_forget()
        else:
            submenu.pack(fill="x", padx=0, pady=(0, 6))

    btn.configure(command=alternar_submenu)

def montar_menu(area_conteudo: tk.Frame):
    """Monta os itens do menu lateral com suas ações."""
    criar_item_menu(
        texto="Cadastro",
        icone="\U0001F4CB",
        subitens=["Cliente", "Veículo", "Funcionário"],
        acoes_subitens={
            "Cliente": lambda: abrir_aba_nova(area_conteudo, "Submenus.Cadastro.CadCli", "Cadastro"),
            "Veículo": lambda: abrir_aba_nova(area_conteudo, "Submenus.Cadastro.CadFro", "Cadastro"),
            "Funcionário": lambda: abrir_aba_nova(area_conteudo, "Submenus.Cadastro.CadFun", "Funcionarios")
        }
    )
    
    criar_item_menu(
        texto="Pesquisa",
        icone="\U0001F50D",
        subitens=["Cliente", "Funcionário", "Frota", "Test Drive/Reunião"],
        acoes_subitens={
            "Cliente": lambda: abrir_aba_nova(area_conteudo, "Submenus.Pesquisa.PesCli", "Pesquisa"),
            "Funcionário": lambda: abrir_aba_nova(area_conteudo, "Submenus.Pesquisa.PesFun", "Funcionarios"),
            "Frota": lambda: abrir_aba_nova(area_conteudo, "Submenus.Pesquisa.PesFro", "Pesquisa"),
            "Test Drive/Reunião": lambda: abrir_aba_nova(area_conteudo, "Submenus.Pesquisa.PesAgen", "Pesquisa")
        }
    )
    
    criar_item_menu(
        texto="Agendamento",
        icone="\U0001F4C6",
        subitens=["Test Drive", "Reunião"],
        acoes_subitens={
            "Test Drive": lambda: abrir_aba_nova(area_conteudo, "Submenus.Agendamento.AgendaTD", "Agendamento"),
            "Reunião": lambda: abrir_aba_nova(area_conteudo, "Submenus.Agendamento.AgendaReu", "Agendamento")
        }
    )
    
    criar_item_menu(
        texto="Venda/Aluguel",
        icone="\U0001F4B2",
        subitens=["Venda", "Aluguel", "Devolução"],
        acoes_subitens={
            "Venda": lambda: abrir_aba_nova(area_conteudo, "Submenus.Venda_Aluguel.Venda", "Venda/Aluguel"),
            "Aluguel": lambda: abrir_aba_nova(area_conteudo, "Submenus.Venda_Aluguel.Aluguel", "Venda/Aluguel"),
            "Devolução": lambda: abrir_aba_nova(area_conteudo, "Submenus.Venda_Aluguel.Devolucao", "Venda/Aluguel")
        }
    )

    criar_item_menu(
        texto="Dashboard",
        icone="\U0001F4CA",
        subitens=None,
        acao=lambda: abrir_aba_nova(area_conteudo, "Submenus.Dashboard", "Dashboard")
    )
    
    criar_item_menu(
        texto="Logout",
        icone="\U0001F3C3",
        subitens=None,
        acao=lambda: sair(raiz)
    )

# -------------------- PONTO DE ENTRADA ----------------------
if __name__ == "__main__":
    raiz = criar_janela_principal()
    area_menu = criar_sidebar(raiz)

    conteudo = tk.Frame(raiz, bg="#1F2937")
    conteudo.grid(row=1, column=1, sticky="nsew")
    try:
        # Para a mensagem de saudação
        pessoa = sys.argv[1]
        # Para o controle de acesso
        cargo = sys.argv[2]
        messagebox.showinfo("Bem-vindo", f"Seja bem-vindo {pessoa}")
    except Exception:
        # Caso o usuário esteja executando o arquivo Menu.py diretamente pela IDE
        pessoa = "Administrador"
        cargo = "Administrador"
        messagebox.showinfo("Bem-vindo", f"Seja bem-vindo {pessoa}")
    finally:
        abrir_aba_nova(conteudo, "Indice", "Menu Principal")
        montar_menu(conteudo)
        raiz.mainloop()
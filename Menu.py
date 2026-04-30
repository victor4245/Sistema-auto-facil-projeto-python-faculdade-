#=======================================================
# SISTEMA: Menu Principal (layout estilo "sistema web" com sidebar)
# Tecnologias: Python 3.x + Tkinter (somente biblioteca padrão)
# menu.py
# ========================================================

import os
import sys
import tkinter as tk
from tkinter import messagebox
import importlib
import subprocess
try:
    from PIL import Image, ImageTk
except Exception:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    messagebox.showwarning("Ocorreu um Erro", "A biblioteca 'Pillow' teve que ser instalada para exibir a imagem de fundo.\nPor favor abra o programa novamente.")

# -------- CONFIGURAÇÕES BÁSICAS --------
CAMINHO_IMAGENS = os.getcwd() + "/Imagens"
VERSION = "v 0.7.5"
ARQUIVO_MAIN = "Autofacil.py"
PERMITIDOS = ["Administrador", "Marcos Silva"]

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
            janela.attributes("-zoomed", True)  # alguns Linux
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

def abrir_aba_nova(area_conteudo: tk.Frame, titulo:str):
    limpar_area(area_conteudo)
    if titulo == "Submenus.Dashboard" and not pessoa in PERMITIDOS:
        messagebox.showwarning("Acesso Negado", "Você não tem permissão para acessar esta função.")
        return

    try:
        modulo = importlib.import_module(titulo)
        if titulo == "Submenus.Admin":
            modulo.mostrar_formulario(area_conteudo, pessoa)
        else:
            modulo.mostrar_formulario(area_conteudo)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao abrir a tela de {titulo}:\n{e}")

def sair(raiz:tk.Tk):
    # Mensagem de confirmação
    confirma = tk.messagebox.askyesno("Logout", "Deseja sair do sistema?")
    if confirma == True:
        import subprocess
        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_main = os.path.join(base_dir, ARQUIVO_MAIN)
        if not os.path.exists(caminho_main):
            messagebox.showerror("Autofacil.py não encontrado",f"Coloque o arquivo '{ARQUIVO_MAIN}' no mesmo diretório deste script:\n{base_dir}")
            return
        try:
            subprocess.Popen([sys.executable, caminho_main])
            raiz.destroy()
        except Exception as e:
            messagebox.showerror("Erro ao abrir a tela de inicio",f"Não foi possível abrir '{ARQUIVO_MAIN}':\n{e}")
    else:
        return
# -------------------- ETAPA 1: JANELA + TOPO ----------------
def criar_janela_principal() -> tk.Tk:
    """
    Cria a janela principal e a faixa de topo PRETA, com título centralizado.
    """
    raiz = tk.Tk()
    raiz.title("Sistema de Gerenciamento de Autos")
    raiz.minsize(900, 580)

    # Abre maximizada
    maximizar_janela(raiz)

    # GRID: 2 colunas (0 = sidebar | 1 = área direita)
    raiz.grid_columnconfigure(0, minsize=220)  # sidebar fixa
    raiz.grid_columnconfigure(1, weight=1)     # área direita expande
    raiz.grid_rowconfigure(1, weight=1)        # linha do conteúdo expande

    return raiz

# ------------- ETAPA 2: SIDEBAR (preta) + MENU --------------
def criar_sidebar(raiz: tk.Tk) -> tk.Frame:
    """
    Cria a faixa lateral esquerda preta e retorna o container do menu.
    """
    sidebar = tk.Frame(raiz, bg="#0B1220")
    sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

    topo_sidebar = tk.Frame(sidebar, bg="#0B1220", height=170)
    topo_sidebar.pack(side="top", fill="x")
    topo_sidebar.pack_propagate(False)

    img_logo = Image.open(CAMINHO_IMAGENS + "/carro.png").convert("RGBA")
    img_logo = img_logo.resize((160, 140))
    img_logo = ImageTk.PhotoImage(img_logo)
    lbl_logo = tk.Label(
        topo_sidebar,
        bg="#0B1220",
        image = img_logo)
    lbl_logo.image = img_logo
    lbl_logo.pack()

    lbl_nome = tk.Label(
        topo_sidebar, text=f"SysCar {VERSION}", font=("Segoe UI", 11, "bold"),
        bg="#0B1220", fg="#E5E7EB"
    )
    lbl_nome.pack()

    menu_container = tk.Frame(sidebar, bg="#0B1220")
    menu_container.pack(side="top", fill="both", expand=True, pady=(10, 12))

    return menu_container

# --------- ETAPA 3: MENU + SUBMENUS -------------------------
def criar_item_menu(texto: str, icone: str, subitens=None, acao=None, acoes_subitens=None):
    """
    Cria um item do menu.
    """
    item = tk.Frame(area_menu, bg="#0B1220")
    item.pack(fill="x")

    btn = tk.Button(
        item,
        text=f"{icone} {texto}",
        font=("Segoe UI Emoji", 11, "bold"),
        bg="#093255", fg="#FFFFFF",
        activebackground="#1F2937", activeforeground="#FFFFFF",
        relief="flat", padx=12, pady=10, anchor="w", cursor="hand2"
    )
    btn.pack(fill="x", padx=12, pady=6)

    if not subitens:
        btn.configure(command=lambda: acao())
        return

    submenu = tk.Frame(item, bg="#0B1220")
    submenu.pack(fill="x", padx=0, pady=(0, 6))
    submenu.pack_forget()

    for nome in subitens:
        acao_sub = acoes_subitens.get(nome)

        sub_btn = tk.Button(
            submenu,
            text=f" • {nome}",
            font=("Segoe UI", 10),
            bg="#0F172A", fg="#E5E7EB",
            activebackground="#1F2937", activeforeground="#FFFFFF",
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
            "Cliente": lambda: abrir_aba_nova(area_conteudo, "Submenus.Cadastro.CadCli"),
            "Veículo": lambda: abrir_aba_nova(area_conteudo, "Submenus.Cadastro.CadFro"),
            "Funcionário": lambda: abrir_aba_nova(area_conteudo, "Submenus.Cadastro.CadFun")
        }
    )
    criar_item_menu(
        texto="Pesquisa",
        icone="\U0001F50D",
        subitens=["Cliente", "Funcionário", "Frota", "Test Drive/Reunião"],
        acoes_subitens={
            "Cliente": lambda: abrir_aba_nova(area_conteudo, "Submenus.Pesquisa.PesCli"),
            "Funcionário": lambda: abrir_aba_nova(area_conteudo, "Submenus.Pesquisa.PesFun"),
            "Frota": lambda: abrir_aba_nova(area_conteudo, "Submenus.Pesquisa.PesFro"),
            "Test Drive/Reunião": lambda: abrir_aba_nova(area_conteudo, "Submenus.Pesquisa.PesAgen")
        }
    )

    criar_item_menu(
        texto="Agendamento",
        icone="\U0001F4C6",
        subitens=["Test Drive", "Reunião"],
        acoes_subitens={
            "Test Drive": lambda: abrir_aba_nova(area_conteudo, "Submenus.AgendaTD"),
            "Reunião": lambda: abrir_aba_nova(area_conteudo, "Submenus.AgendaReu")
        }
    )

    criar_item_menu(
        texto="Dashboard",
        icone="\U0001F4CA",
        subitens=None,
        acao=lambda: abrir_aba_nova(area_conteudo, "Submenus.Dashboard")
    )

    criar_item_menu(
        texto="ADM",
        icone="\U0001F9F0",
        subitens=None,
        acao=lambda: abrir_aba_nova(area_conteudo, "Submenus.Admin")
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
        # Mensagem de saudação
        pessoa = sys.argv[1]
        messagebox.showinfo("Bem-vindo", f"Seja Bem-vindo {pessoa}")
    except:
        pessoa = "Administrador"
        messagebox.showinfo("Bem-vindo", f"Seja Bem-vindo {pessoa}")
    finally:
        montar_menu(conteudo)

        raiz.mainloop()
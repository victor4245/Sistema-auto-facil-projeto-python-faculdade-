# ====================================================
# SysCar - Sistema de Gerenciamento de Autos
#
# Login de teste:
# login = a
# senha = @a
#====================================================

import os
import sys
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import subprocess
import hashlib
try:
    import mysql.connector
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
    messagebox.showwarning("Ocorreu um Erro", "A biblioteca 'mysql-connector-python' teve que ser instalada para conectar ao banco de dados.\nPor favor abra o programa novamente.")
try:
    from PIL import Image, ImageTk
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    messagebox.showwarning("Ocorreu um Erro", "A biblioteca 'Pillow' teve que ser instalada para exibir a imagem de fundo.\nPor favor abra o programa novamente.")
try:
    from tkcalendar import DateEntry
except Exception:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tkcalendar"])
    messagebox.showwarning("Ocorreu um Erro", "A biblioteca 'tkcalendar' teve que ser instalada para uso de calendário.\nPor favor abra o programa novamente.")
# -------- CONFIGURAÇÕES BÁSICAS --------
# Conexão com o BD
try:
    conn = mysql.connector.connect(
        host="sql10.freesqldatabase.com",
        user="sql10826915",
        password="1lL7crlwDf",
        database="sql10826915",
        port=3306
    )
    conn.autocommit = True
    cursor = conn.cursor(dictionary=True)
except:
    messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados\n Verifique sua conexão com a internet")
AGORA = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
CAMINHO_IMAGENS = os.getcwd() + "/Imagens"
ARQUIVO_MENU = "Menu.py"
VERSION = "v 0.9.7"

# --------- CAPTURA DE EMAIL, SENHA E NOME DE FUNCIONÁRIOS ------------

login = []
LOGIN_EMAIL = []
LOGIN_CPF = []
LOGIN_ID = []
PESSOA = []
CARGO = []
SENHA_ESPERADA = []

cursor.execute("SELECT * FROM funcionarios")
leitor = cursor.fetchall()
for linha in leitor:
    login.append(linha) 

for i in range(len(login)):
    # Adição dos CPFs, IDs e Emails para verificação de login
    LOGIN_CPF.append(login[i]["cpf"].replace(".", "").replace("-", "").strip())
    LOGIN_EMAIL.append(login[i]["email"])
    LOGIN_ID.append(login[i]["id_empresa"])
    # Captura dos nomes para saudação
    PESSOA.append(login[i]["nome"])
    # Captura dos cargos para uso posterior no menu.py
    CARGO.append(login[i]["cargo"])
    # Adição das senhas para verificação de login
    SENHA_ESPERADA.append(login[i]["senha"])

# =======================================================
# FUNÇÕES (nomes simples, em português)
# =======================================================
def maximizar_janela(janela: tk.Tk):
    """Tenta abrir a janela já maximizada. Usa estratégias que funcionam em Windows e Linux."""
    try:
        janela.update_idletasks()
        try:
            janela.state("zoomed") # comum no Windows
        except Exception:
            pass
        try:
            janela.attributes("-zoomed", True) # alguns Linux
        except Exception:
            pass
# Fallback: força a janela a ocupar a tela (se necessário)
        try:
            w = janela.winfo_screenwidth()
            h = janela.winfo_screenheight()
            janela.geometry(f"{w}x{h}+0+0")
        except Exception:
            pass
    except Exception:
        pass
def carregar_imagem(caminho: str):
    """Carrega a imagem de fundo do disco. Retorna um objeto PIL.Image ou None se der erro."""
    if not os.path.exists(caminho):
        messagebox.showwarning("Imagem não encontrada",f"Não encontrei a imagem de fundo em:\n{caminho}\n\n""Verifique o caminho e o nome do arquivo.")
        return None
    try:
        return Image.open(caminho).convert("RGB")
    except Exception as e:
        messagebox.showwarning("Erro ao abrir imagem",f"Ocorreu um erro ao abrir a imagem:\n{caminho}\n\n{e}")
        return None
def atualizar_fundo(janela: tk.Tk, lbl_fundo: tk.Label, img_base):
    """Atualiza a imagem do fundo para cobrir toda a janela.
    - Faz um ajuste simples: redimensiona proporcionalmente para preencher a tela (estilo 'cover'), recortando as sobras se necessário.
    - Mantém a referência da imagem para não ser coletada pelo Python."""
    if img_base is None:
        return
# Tamanho atual da janela
    largura = max(1, janela.winfo_width())
    altura = max(1, janela.winfo_height())
# Cálculo simples de 'cover' (preencher sem distorcer)
    iw, ih = img_base.size
    if iw == 0 or ih == 0:
        return
    escala = max(largura / iw, altura / ih)
    novo_w = max(1, int(iw * escala))
    novo_h = max(1, int(ih * escala))
# Redimensiona
    try:
        img_red = img_base.resize((novo_w, novo_h), Image.LANCZOS)
    except Exception:
        img_red = img_base.resize((novo_w, novo_h))
# Recorta o centro para bater exatamente com a janela
    x0 = max(0, (novo_w - largura) // 2)
    y0 = max(0, (novo_h - altura) // 2)
    x1 = x0 + largura
    y1 = y0 + altura
    img_crop = img_red.crop((x0, y0, x1, y1))
# Converte para ImageTk e aplica no label
    img_tk = ImageTk.PhotoImage(img_crop)
    lbl_fundo.configure(image=img_tk)
    lbl_fundo._img_ref = img_tk # mantém referência

# Log para conferir funcionários logados anteriormente
def log_login(pessoa: str):
    texto = f"O usuário {pessoa} logou às {AGORA}"
    cursor.execute("""INSERT INTO log_login (texto) VALUES (%s)""", (texto,))
    conn.commit()
    return

def abrir_menu(janela: tk.Tk, pessoa:str, cargo:str):
    """Fecha esta janela e abre o arquivo 'menu.py' (no mesmo diretório)."""
    import subprocess
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_menu = os.path.join(base_dir, ARQUIVO_MENU)
    if not os.path.exists(caminho_menu):
        messagebox.showerror("menu.py não encontrado",f"Coloque o arquivo '{ARQUIVO_MENU}' no mesmo diretório deste script:\n{base_dir}")
        return
    # Abrindo o arquivo menu.py e passando o nome da pessoa que esta logando para ser usado na mensagem de boas vindas juntamento do cargo para controle de acesso a algumas abas do menu
    try:
        subprocess.Popen([sys.executable, caminho_menu, pessoa, cargo])
        janela.destroy()
    except Exception as e:
        messagebox.showerror("Erro ao abrir o menu",f"Não foi possível abrir '{ARQUIVO_MENU}':\n{e}")
def ao_acessar(campo_login: tk.Entry, campo_senha: tk.Entry, janela: tk.Tk):
    """Ação do botão Acessar (e tecla Enter):
    - Verifica se os campos estão preenchidos
    - Valida credenciais
    - Se ok, abre o menu"""
    login = campo_login.get().strip()
    if len(login) == 14:
        login = login.replace(".", "").replace("-", "")
    senha = campo_senha.get().strip()
    if not login or not senha:
        messagebox.showwarning("Campos obrigatórios", "Informe login e senha.")
        return
    
    # Validação de Login e senha
    i = 0
    while (i < len(LOGIN_EMAIL)):
        if login == LOGIN_EMAIL[i] or login == LOGIN_CPF[i] or login == LOGIN_ID[i]:
            if hashlib.sha256(senha.encode()).hexdigest() == SENHA_ESPERADA[i]:
                login2 = True
                pessoa = PESSOA[i]
                cargo = CARGO[i]
                log_login(pessoa)
                abrir_menu(janela, pessoa, cargo)
                break
            else:
                login2 = False
                break
        else:
            login2 = False
            i += 1
    # Mensagem de erro caso login ou senha estejam incorretos
    if not login2:
        messagebox.showerror("Acesso negado", "Login ou senha incorretos.")
        return
        
def ao_sair(janela: tk.Tk):
    """Fecha a aplicação."""
    janela.destroy()

#=======================================================
# INTERFACE GRÁFICA
#========================================================
def criar_janela():
    """Monta toda a interface e inicia o loop da aplicação.
    - Fundo com imagem (sem cor no centro)
    - Cabeçalho e rodapé com faixas coloridas
    - Barra de login no rodapé"""

    # Janela principal
    raiz = tk.Tk()
    raiz.title("SysCar - Sistema de Gerenciamento de Autos")
    raiz.minsize(980, 600)
    raiz.iconbitmap(CAMINHO_IMAGENS + "/LogoA.ico")

    # Não aplicamos cor de fundo na janela raiz para não cobrir o centro.
    # Somente cabeçalho e rodapé terão cor.

    # Maximiza a janela após criar
    raiz.after(50, lambda: maximizar_janela(raiz))

    # ------- FUNDO (ocupa toda a janela e fica por trás) -------
    lbl_fundo = tk.Label(raiz, bd=0, highlightthickness=0)
    lbl_fundo.place(x=0, y=0, relwidth=1, relheight=1)
    lbl_fundo.lower()  # envia o fundo para trás

    # Carrega a imagem local do fundo
    imagem_base = carregar_imagem(CAMINHO_IMAGENS + "/musta.jpg")

    # Atualiza o fundo inicialmente
    raiz.after(100, lambda: atualizar_fundo(raiz, lbl_fundo, imagem_base))

    # Atualiza o fundo sempre que a janela for redimensionada
    def ao_redimensionar(event):
        atualizar_fundo(raiz, lbl_fundo, imagem_base)

    raiz.bind("<Configure>", ao_redimensionar)

    # ----------------- CABEÇALHO -----------------
    cabecalho = tk.Frame(raiz, bg="#0B1220")
    cabecalho.pack(side="top", fill="x")
    cabecalho.grid_columnconfigure(0, weight=2)
    cabecalho.grid_columnconfigure(1, weight=1)
    cabecalho.grid_columnconfigure(2, weight=1)
    tit_fr = tk.Frame(cabecalho, bg="#0B1220")
    tit_fr.grid(row=0, column=1, sticky="nsew", pady=(30, 0))
    tit_fr.grid_columnconfigure(0, weight=1)

    lbl_titulo = tk.Label(
        tit_fr,
        text="AUTO FÁCIL - DF",
        font=("Segoe UI", 26, "bold"),
        bg="#0B1220",
        fg="#1561a1",
        pady=10
    )
    lbl_titulo.grid(row=0, column=0, sticky="ew")

    lbl_subtitulo = tk.Label(
        tit_fr,
        text="SysCar - Sistema de Gerenciamento de Autos",
        font=("Segoe UI", 13),
        bg="#0B1220",
        fg="#E5E7EB",
        pady=4
    )
    lbl_subtitulo.grid(row=1, column=0, sticky="ew")

    lbl_versao = tk.Label(
        cabecalho,
        text=VERSION,
        font=("Segoe UI", 13),
        bg="#0B1220",
        fg="#E5E7EB",
        pady=4
    )
    lbl_versao.grid(row=0, column=0, sticky="sw", pady=(30, 0))
    # Tratamento de erro caso a biblioteca pillow não esteja instalada
    try:
        img_logo = Image.open(CAMINHO_IMAGENS + "/carro.png").convert("RGBA")
        img_logo = img_logo.resize((220, 180))
        img_logo = ImageTk.PhotoImage(img_logo)
        lbl_logo = tk.Label(
            cabecalho,
            bg="#0B1220",
            image = img_logo)
        lbl_logo.grid(row=0, column=2, sticky="e")
    except:
        messagebox.showwarning("Ocorreu um erro", "Biblioteca pillow faltando. Fechando o programa")
        raiz.destroy()

    # ----------------- RODAPÉ -----------------
    rodape = tk.Frame(raiz, bg="#0B1220")
    rodape.pack(expand=True, ipadx=5, ipady=5)

    barra = tk.Frame(rodape, bg="#0B1220")
    barra.pack(padx=15, pady=15)

    # Colunas
    for col in range(6):
        barra.grid_columnconfigure(col, weight=1)

    cor_faixa = "#0B1220"
    cor_campo = "#1F2937"
    cor_texto = "white"

    # Login
    tk.Label(
        barra, text="Login:", font=("Segoe UI", 11, "bold"),
        bg=cor_faixa, fg=cor_texto
    ).grid(row=0, column=0, sticky="", padx=(6, 6), pady=6)

    entrada_login = tk.Entry(
        barra, font=("Segoe UI", 11),
        bg=cor_campo, fg=cor_texto,
        insertbackground=cor_texto, relief="flat"
    )
    entrada_login.grid(row=0, column=1, sticky="", padx=(0, 12), pady=6)
    entrada_login.focus()

    # Senha
    tk.Label(
        barra, text="Senha:", font=("Segoe UI", 11, "bold"),
        bg=cor_faixa, fg=cor_texto
    ).grid(row=1, column=0, sticky="", padx=(6, 6), pady=6)

    entrada_senha = tk.Entry(
        barra, show="*",
        font=("Segoe UI", 11),
        bg=cor_campo, fg=cor_texto,
        insertbackground=cor_texto, relief="flat"
    )
    entrada_senha.grid(row=1, column=1, sticky="", padx=(0, 12), pady=6)

    # Botão Acessar
    btn_acessar = tk.Button(
        barra, text="Acessar",
        font=("Segoe UI", 10, "bold"),
        bg="#2563EB", fg="white",
        activebackground="#1E40AF",
        activeforeground="white",
        relief="flat", padx=16, pady=8,
        command=lambda: ao_acessar(entrada_login, entrada_senha, raiz),
        cursor="hand2"
    )
    btn_acessar.grid(row=3, column=0, sticky="ws", padx=(12, 0), pady=(25, 0))

    # Botão Sair
    btn_sair = tk.Button(
        barra, text="Sair",
        font=("Segoe UI", 10, "bold"),
        bg="#374151", fg="white",
        activebackground="#1F2937",
        activeforeground="white",
        relief="flat", padx=16, pady=8,
        command=lambda: ao_sair(raiz),
        cursor="hand2"
    )
    btn_sair.grid(row=3, column=1, sticky="es", padx=(0, 20), pady=(25, 0))

    # ENTER aciona acessar
    raiz.bind("<Return>", lambda e: ao_acessar(entrada_login, entrada_senha, raiz))

    # Inicia a janela
    raiz.mainloop()
#=====================================================
# PONTO DE ENTRADA
# ====================================================
if __name__ == "__main__":
    criar_janela()
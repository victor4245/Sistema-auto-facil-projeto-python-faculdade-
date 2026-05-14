# ========================================================
# Devolucao.py — Devolução de veículos
#
# Devolucao.mostrar_formulario(area_conteudo)
# ========================================================

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
# -------- CONFIGURAÇÕES BÁSICAS --------
# Conexão com o BD
try:
    conn = psycopg2.connect(
        host="db.gipxlyvlobazrwuhxzep.supabase.co",
        database="postgres",
        user="postgres",
        password="S3nh4_DB@12",
        port="5432"
    )
    conn.autocommit = True
except:
    messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados\n Verifique sua conexão com a internet")
AGORA = datetime.now().strftime("%d/%m/%Y")

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# -------- CAPTURA DE DADOS --------

cursor = conn.cursor(cursor_factory=RealDictCursor)

# Captura dos aluguéis feitos

cursor.execute("""SELECT * FROM aluguel""")
ALUGUEL = cursor.fetchall()

# Captura de veículos disponíveis

def ler_fro(cod):
    cursor.execute("""SELECT nome FROM frota WHERE codigo = %s""", (cod,))
    FROTA = cursor.fetchone()
    return FROTA['nome']

# Captura de clientes disponíveis

def ler_cli(cod):
    cursor.execute("""SELECT nome FROM clientes WHERE cpf_cnpj = %s""", (cod,))
    CLIENTES = cursor.fetchone()
    return CLIENTES['nome']

# --------------------------------------------------------
# SALVA OS DADOS NO BD
# --------------------------------------------------------
def salvar(dados, indice):     
    cod_alu = indice['aluguel']
    coda = ALUGUEL[cod_alu]
    dados['codigo'] = coda['codigo']
    dados['cod_veiculo'] = coda['cod_veiculo']
    
    try:
        cursor.execute("""
            UPDATE frota
            SET 
                obs = %s
            WHERE codigo = %s
            """, (
                dados['obs2'],
                dados['cod_veiculo']
            ))
        conn.commit()
        cursor.execute("""DELETE FROM aluguel WHERE codigo = %s""", (dados['codigo'],))
        messagebox.showinfo("Sucesso", "Devolução feita com sucesso!")
    except Exception as erro:
        messagebox.showerror("Erro", "O seguinte erro aconteceu: " + str(erro))
        
def limpar(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()    
def mostrar_formulario(parent: tk.Frame):
    """
    Constrói o formulário de aluguel de veículos dentro do 'parent' (área central).
    """

    # Limpa qualquer conteúdo anterior
    limpar(parent)

    # Um container centralizado
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container redundante para melhor controle
    container2 = tk.Frame(container, bg=COR_FUNDO, width=730, height=580)
    container2.pack(expand=True)
    container2.pack_propagate(False)

    caixa = tk.Frame(container2, bg=COR_FUNDO)
    caixa.pack(expand=True)

    # Título
    tk.Label(
        caixa,
        text="Devolução de veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))

    # ------- CAMPOS -------
    entradas = {}

    def add_linha(rotulo, rotuloBD, linha, col_inicio):
        """Cria um par Label + Entry numa posição da grade."""
        tk.Label(
            caixa,
            text=rotulo,
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).grid(row=linha, column=col_inicio, columnspan=4, sticky="w", padx=(4, 8), pady=6) 
        entry = tk.Listbox(caixa, width=70, height=8,bg=COR_CAMPO, fg=COR_TEXTO2, borderwidth=0, highlightthickness=0, relief="flat", justify='left', exportselection=False)
        
        entry.grid(row=linha + 1, column=col_inicio, sticky="w", padx=(10, 10), pady=6)

        entradas[rotuloBD] = entry

    # Linha 1
    add_linha("Selecione o aluguel", "aluguel", linha=1, col_inicio=0)
    entradas['aluguel'].delete(0, tk.END)
    for c in ALUGUEL:
        c['nome_veic'] = ler_fro(c['cod_veiculo'])
        c['nome_cliente'] = ler_cli(c['cpf_cliente'])
        texto = f"Veículo: {c['nome_veic']}  |  Cliente: {c['nome_cliente']} | Data Devolução: {c['data_final']}"
        entradas['aluguel'].insert(tk.END, texto)

    # Botões
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=3, column=0, columnspan=4, pady=16)

    def on_salvar():
        indice = {"aluguel": entradas["aluguel"].curselection()[0]}
        dados = {}
        for campo, entrada in entradas.items():
            selecao = entrada.curselection()
            dados[campo] = entrada.get(selecao[0])
        dados["obs2"] = "Sem observações"
        salvar(dados, indice)

    def on_limpar():
        for ent in entradas.values():
            ent.delete(0, "end")

    def on_cancelar():
        limpar(parent)

    tk.Button(
        botoes,
        text="Devolver",
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
# ========================================================
# Aluguel.py — Aluguel de veículos
#
# Aluguel.mostrar_formulario(area_conteudo)
# ========================================================

import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
try:
    from tkcalendar import DateEntry
except Exception:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tkcalendar"])
    messagebox.showwarning("Ocorreu um Erro", "A biblioteca 'tkcalendar' teve que ser instalada para exibir a imagem de fundo.\nPor favor abra o programa novamente.")
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

def limpar(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()
# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# -------- CAPTURA DE DADOS --------

cursor = conn.cursor(cursor_factory=RealDictCursor)

# Captura de veículos disponíveis

cursor.execute("""SELECT * FROM frota""")
FROTA = cursor.fetchall()

# Captura de clientes disponíveis

cursor.execute("""SELECT * FROM clientes""")
CLIENTES = cursor.fetchall()


# Captura de vendedores

VENDAS = ["gerente", "assistente administrativo", "vendedor"]
cursor.execute("""SELECT nome FROM funcionarios WHERE cargo = any(%s)""", (VENDAS,))
VENDEDORES = cursor.fetchall()
# --------------------------------------------------------
# SALVA OS DADOS NO BD
# --------------------------------------------------------
def salvar(dados, indice):
    # Verificação simples (iniciante)      
    for data in dados:
        if dados[data] == "" and not dados["obs"]:
            messagebox.showwarning(
                "Campos obrigatórios faltando",
                "Preencha todos os campos para salvar o cliente."
            )
            return
    if datetime.strptime(dados["data_inicio"], "%d/%m/%Y") < datetime.strptime(AGORA, "%d/%m/%Y"):
        messagebox.showwarning(
            "Data inválida",
            "A data do aluguel não pode ser anterior ao momento atual."
        )
        return
    if datetime.strptime(dados["data_final"], "%d/%m/%Y") < datetime.strptime(AGORA, "%d/%m/%Y"):
        messagebox.showwarning(
            "Data inválida",
            "A data de devolução não pode ser anterior ao momento atual."
        )
        return
    cod_veic = indice['veiculo']
    cpf_cliente = indice['cliente']
    vend = indice['vendedor']
    codv = FROTA[cod_veic]
    codc = CLIENTES[cpf_cliente]
    nomv = VENDEDORES[vend]
    dados['cod_veiculo'] = codv['codigo']
    dados['cpf_cliente'] = codc['cpf_cnpj']
    dados['vendendor'] = nomv['nome']
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""INSERT INTO aluguel (cod_veiculo,data_inicio,data_final,cpf_cliente,vendedor,obs)
                       VALUES(%s,%s,%s,%s,%s,%s)
                       """,(
                        dados["cod_veiculo"],
                        dados["data_inicio"],
                        dados["data_final"],
                        dados["cpf_cliente"],
                        dados["vendedor"],
                        dados["obs"]
                       ))
        conn.commit()
        cursor.execute("""
            UPDATE frota
            SET 
                obs = %s
            
            WHERE codigo = %s
            """, (
                dados['obs2'],
                dados['cod_veiculo']
            ))
        messagebox.showinfo("Sucesso", "Aluguel cadastrado com sucesso!")
    except Exception as erro:
        messagebox.showerror("Erro", "O seguinte erro aconteceu: " + str(erro))
    

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
        text="Aluguel de veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))

    # ------- CAMPOS -------
    entradas = {}

    def add_linha(rotulo, rotuloBD, linha, col_inicio, largura=40):
        """Cria um par Label + Entry numa posição da grade."""
        tk.Label(
            caixa,
            text=rotulo,
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).grid(row=linha, column=col_inicio, sticky="w", padx=(4, 8), pady=6) 
        if rotulo in ["Data de Início", "Data de Finalização"]:
            entry = DateEntry(
                caixa,
                width=largura,
                background=COR_CAMPO,
                foreground=COR_TEXTO2,
                borderwidth=2,
                date_pattern='dd/mm/yyyy'  # Formato BR
            )
        else:
            entry = tk.Listbox(caixa, width=58, height=5,bg=COR_CAMPO, fg=COR_TEXTO2, borderwidth=0, highlightthickness=0, relief="flat", justify='left', exportselection=False)
            
        
        entry.grid(row=linha + 1, column=col_inicio, sticky="w", padx=(10, 10), pady=6)

        entradas[rotuloBD] = entry

    # Linha 1
    add_linha("Selecione o veículo", "nome_veiculo", linha=1, col_inicio=0, largura=24)
    entradas['nome_veiculo'].delete(0, tk.END)
    for c in FROTA:
        texto = f"Veículo: {c['nome']}  |  Preço: {c['preco']}  |  Quilometragem: {c['quilometragem']}"
        entradas['nome_veiculo'].insert(tk.END, texto)

    add_linha("Selecione o cliente", "nome_cliente", linha=1, col_inicio=2, largura=24)
    entradas['nome_cliente'].delete(0, tk.END)
    for c in CLIENTES:
        texto = f"Cliente: {c['nome']}  |  CPF/CNPJ: {c['cpf_cnpj']}"
        entradas['nome_cliente'].insert(tk.END, texto)

    # Linha 2
    add_linha("Data de Início", "data_inicio", linha=3, col_inicio=2, largura=24)
    add_linha("Data de Finalização", "data_final", linha=3, col_inicio=0, largura=24)
    
    # Linha 3
    add_linha("Selecione o vendedor", "vendedor", linha=5, col_inicio=0, largura=24)
    entradas['vendedor'].delete(0, tk.END)
    for c in VENDEDORES:
        texto = f"Nome: {c['nome']}"
        entradas['vendedor'].insert(tk.END, texto)

    # Observações
    tk.Label(
        caixa,
        text="Observações",
        font=("Segoe UI", 10, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=7, column=0, columnspan=4, sticky="", padx=(8, 8), pady=6)

    txt_obs = tk.Text(caixa, width=66, height=5, background=COR_CAMPO,foreground=COR_TEXTO2,insertbackground=COR_TEXTO2, relief="flat")
    txt_obs.grid(row=8, column=0, columnspan=4, sticky="", padx=(10, 10), pady=6)

    # Botões
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=9, column=0, columnspan=4, pady=16)

    def on_salvar():
        indice = {"veiculo": entradas["nome_veiculo"].curselection()[0], "cliente": entradas["nome_cliente"].curselection()[0], "vendedor": entradas["vendedor"].curselection()[0]}
        dados = {}
        for campo, entrada in entradas.items():     
            if isinstance(entrada, tk.Listbox):
                selecao = entrada.curselection()
                dados[campo] = entrada.get(selecao[0])
            else:
                dados[campo] = entrada.get().strip()
        dados["obs"] = txt_obs.get("1.0", "end-1c").strip()
        dados["obs2"] = "Alugado"
        salvar(dados, indice)

    def on_limpar():
        for ent in entradas.values():
            ent.delete(0, "end")
        txt_obs.delete("1.0", "end-1c")

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
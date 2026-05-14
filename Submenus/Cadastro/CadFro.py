# ========================================================
# CadFro.py — Formulário de Veículo
#
# CadFro.mostrar_formulario(area_conteudo)
# ========================================================

import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime
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

AGORA = datetime.now().strftime("%Y")  
# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# --------------------------------------------------------
# SALVA OS DADOS NO BD
# --------------------------------------------------------
def salvar(dados):
    # Verificação simples (iniciante)
    for data in dados:
        if dados[data] == "" and not dados["obs"]:
            messagebox.showwarning(
                "Campos obrigatórios faltando",
                "Preencha todos os campos para salvar o cliente."
            )
            return
    idade = datetime.strptime(dados['ano'], "%Y") - AGORA
    aluguel = (dados['preco'] * 0.0025) - (idade * 3)
    dados['preco_aluguel'] = round(aluguel)
    try:
        cursor.execute("""INSERT INTO veiculos (nome,marca,modelo,motorizacao,condicao,placa,cor,ano,quilometragem,preco,preco_aluguel,obs)
                       VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                       """,(
                        dados['nome'],
                        dados['marca'],
                        dados['modelo'],
                        dados['motorizacao'],
                        dados['condicao'],
                        dados['placa'],
                        dados['cor'],
                        dados['ano'],
                        dados['quilometragem'],
                        dados['preco'],
                        dados['preco_aluguel'],
                        dados['obs']
                       ))
        conn.commit()
        messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")
    except Exception as erro:
        messagebox.showerror("Erro", "O seguinte erro aconteceu: " + str(erro))

def limpar(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()
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

    def add_linha(rotulo, rotuloBD, linha, col_inicio, largura=40):
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
        # rotuloBD somente para trabalhar melhor com o dicionário no futuro
        entradas[rotuloBD] = entry

    # Linha 1
    add_linha("Nome", "nome", linha=1, col_inicio=0, largura=24)
    add_linha("Marca", "marca", linha=1, col_inicio=2, largura=24)

    # Linha 2
    add_linha("Modelo", "modelo", linha=2, col_inicio=0, largura=24)
    add_linha("Motorização", "motorizacao", linha=2, col_inicio=2, largura=21)

    # Linha 3
    add_linha("Condição", "condicao", linha=3, col_inicio=0, largura=10)
    add_linha("Placa", "placa", linha=3, col_inicio=2, largura=12)
    
    # Linha 4
    add_linha("Cor", "cor", linha=4, col_inicio=0, largura=10)
    add_linha("Ano", "ano",linha=4, col_inicio=2, largura=6)
    
    # Linha 5
    add_linha("Quilometragem", "quilometragem", linha=5, col_inicio=0, largura=12)
    add_linha("Preço", "preco", linha=5, col_inicio=2, largura=12)

    # Observações
    tk.Label(
        caixa,
        text="Observações",
        font=("Segoe UI", 10, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=6, column=0, columnspan=4, sticky="", padx=(8, 8), pady=6)

    txt_obs = tk.Text(caixa, width=66, height=5, background=COR_CAMPO,foreground=COR_TEXTO2,insertbackground=COR_TEXTO2, relief="flat")
    txt_obs.grid(row=7, column=0, columnspan=4, sticky="", padx=(10, 10), pady=6)
    
    entradas["nome"].focus()
    
    # Botões
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=8, column=0, columnspan=4, pady=(16, 0))

    def on_salvar():
        dados = {add_linha: entrada.get().strip() for add_linha, entrada in entradas.items()}
        dados["obs"] = txt_obs.get("1.0", "end-1c").strip()
        on_limpar()
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
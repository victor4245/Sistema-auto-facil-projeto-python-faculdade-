# ========================================================
# CadFro.py — Formulário de Veículo
#
# CadFro.mostrar_formulario(area_conteudo)
# ========================================================

import importlib
import tkinter as tk
from tkinter import messagebox, ttk
from Menu import conn, cursor
from datetime import datetime
import Submenus.Pesquisa.Verificacao as Verificacao

# -------- CONFIGURAÇÕES BÁSICAS --------
ANO = datetime.now().strftime("%Y")  

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# --------------------------------------------------------
# SALVA OS DADOS NO BD
# --------------------------------------------------------
def salvar(dados, parent):
    # Verificação simples (iniciante)
    for data in dados:
        if dados[data] == "" and data != "obs":
            messagebox.showwarning(
                "Campos obrigatórios faltando",
                "Preencha todos os campos para salvar o cliente."
            )
            return
    # Cálculo do preço do aluguel baseado na idade e preço do veículo
    idade = int(ANO) - int(dados['ano'])
    aluguel = (int(dados['preco']) * 0.0025) - (idade * 3)
    aluguel = max(50, round(aluguel))  # Garantindo um valor mínimo de aluguel de 50 reais
    dados['preco_aluguel'] = str(round(aluguel))
    
    # Verificação de existência da placa, para evitar duplicatas
    existe_placa = Verificacao.verificar_existe("Frota", placa=dados["placa"])
    if existe_placa:
        messagebox.showerror("Erro", "Placa já cadastrada.")
        return

    try:
        # Formatando os preços para o padrão float para uso na aba dashboard
        dados['preco'] = dados['preco'].replace(",", ".")
        dados['preco_aluguel'] = dados['preco_aluguel'].replace(",", ".")
        cursor.execute("""INSERT INTO veiculos (nome,marca,modelo,motorizacao,condicao,placa,cor,ano,quilometragem,preco,preco_aluguel,obs)
                       VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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
        mostrar_formulario(parent)
    except Exception as erro:
        messagebox.showerror("Erro", f"O seguinte erro aconteceu: {erro}")
        return

def limpar(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()
        
def abrir_indice(area_conteudo: tk.Frame):
    limpar(area_conteudo)
    # Abre o Indice.py e mostra o índice na tela
    try:
        modulo = importlib.import_module("Indice")
        modulo.mostrar_formulario(area_conteudo)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao abrir a tela de Índice:\n{e}")
        
def mostrar_formulario(parent: tk.Frame):
    """Constrói o formulário de Veículo dentro do 'parent' (área central)."""

    # Limpa qualquer conteúdo anterior
    limpar(parent)

    # Um container centralizado
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container auxiliar para melhor controle
    container2 = tk.Frame(container, bg=COR_FUNDO, width=700, height=500)
    container2.pack(expand=True)
    container2.pack_propagate(False)

    caixa = tk.Frame(container2, bg=COR_FUNDO)
    caixa.pack(expand=True)


    # ---------------- TÍTULO ----------------
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
        # "rotuloBD" somente para trabalhar melhor com o dicionário no momento de salvar no BD
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
    
    # ---------------- BOTÕES ----------------
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=8, column=0, columnspan=4, pady=(16, 0))

    def on_salvar():
        dados = {add_linha: entrada.get().strip() for add_linha, entrada in entradas.items()}
        dados["obs"] = txt_obs.get("1.0", "end-1c").strip()
        salvar(dados, parent)

    def on_limpar():
        for ent in entradas.values():
            if isinstance(ent, ttk.Combobox):
                ent.current(0)
            else:
                ent.delete(0, "end")
        txt_obs.delete("1.0", "end-1c")

    # -------- FECHAR --------
    def fechar():
        abrir_indice(parent)

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

    tk.Button(botoes, 
        text="Fechar", 
        font=("Segoe UI", 10, "bold"), 
        command=fechar,
        bg="#C90202",  
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2"
    ).pack(side="left", padx=4)

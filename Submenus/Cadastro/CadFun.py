# ========================================================
# CadFun.py — Formulário de Funcionário
#
# CadFun.mostrar_formulario(area_conteudo)
# ========================================================

import importlib
import tkinter as tk
from tkinter import messagebox, ttk
from Menu import conn, cursor
import hashlib
import Submenus.Pesquisa.Verificacao as Verificacao

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# --------------------------------------------------------
# SALVA OS DADOS NO BD
# --------------------------------------------------------
def salvar(dados, senha, adsenha, parent):
    if not senha.get().strip():
        messagebox.showwarning("Campo obrigatório", "Digite a senha.")
        return
    dados["senha"] = hashlib.sha256(senha.get().strip().encode()).hexdigest()
    # Verificação simples (iniciante)
    for data in dados:
        if dados[data] == "" and data != "obs":
            messagebox.showwarning(
                "Campos obrigatórios faltando",
                "Preencha todos os campos para salvar o cliente."
            )
            return
    # Verificação de existência do CPF e email, para evitar duplicatas
    existe_cpf = Verificacao.verificar_existe("Funcionarios", cpf=dados["cpf"])
    existe_email = Verificacao.verificar_existe("Funcionarios", email=dados["email"])
    existe_telefone = Verificacao.verificar_existe("Funcionarios", telefone=dados["telefone"])
    if existe_cpf:
        messagebox.showerror("Erro", "CPF já cadastrado.")
        return
    if existe_email:
        messagebox.showerror("Erro", "Email já cadastrado.")
        return
    if existe_telefone:
        messagebox.showerror("Erro", "Telefone já cadastrado.")
        return
    try:
        cursor.execute("""INSERT INTO funcionarios (nome,cpf,email,telefone,cargo,id_empresa,obs,senha)
                       VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                       """,(
                        dados['nome'],
                        dados['cpf'],
                        dados['email'],
                        dados['telefone'],
                        dados['cargo'],
                        dados['id_empresa'],
                        dados['obs'],
                        dados['senha']
                       ))
        conn.commit()
        adsenha.destroy()
        messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
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
    """Constrói o formulário de Funcionário dentro do 'parent' (área central)."""

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
        text="Cadastro de Funcionário",
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
        if rotulo == "Cargo":
            entry = ttk.Combobox(caixa, values=[' ', 'Gerente', 'Vendedor',
                                                'Mecânico', 'Assistente Administrativo', 'Lavador'],width=largura, state="readonly")
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
    add_linha("Nome", "nome", linha=1, col_inicio=0, largura=40)
    add_linha("CPF", "cpf", linha=1, col_inicio=2, largura=24)

    # Linha 2
    add_linha("E-mail", "email", linha=2, col_inicio=0, largura=40)
    add_linha("Telefone", "telefone", linha=2, col_inicio=2, largura=24)

    # Linha 3
    add_linha("Cargo", "cargo", linha=3, col_inicio=0, largura=24)

    entradas["nome"].focus()
    
    # Observações
    tk.Label(
        caixa,
        text="Observações",
        font=("Segoe UI", 10, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=4, column=0, columnspan=4, sticky="", padx=(8, 8), pady=6)

    txt_obs = tk.Text(caixa, width=66, height=5, background=COR_CAMPO,foreground=COR_TEXTO2,insertbackground=COR_TEXTO2, relief="flat")
    txt_obs.grid(row=5, column=0, columnspan=4, sticky="", padx=(10, 10), pady=6)

    # ---------------- BOTÕES ----------------
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=6, column=0, columnspan=4, pady=(16, 0))

    def on_salvar():
        dados = {add_linha: entrada.get().strip() for add_linha, entrada in entradas.items()}
        try:
            dados["id_empresa"] = dados["cpf"].replace("-", "").replace(".", "") # O ID sera definido como a metade do CPF somente como um exemplo
            dados["id_empresa"] = str(int(dados["id_empresa"]) // 1000000)
        except Exception:
            messagebox.showerror("Erro", "Digite um CPF válido")
            return
        dados["obs"] = txt_obs.get("1.0", "end-1c").strip()  
        dados["senha"] = "*"
        ad_senha(dados, parent)

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
    
# ----------------------------------------------------------
# Tela de adição da senha do login do funcionário
# ----------------------------------------------------------
def ad_senha(dados, parent):
    adsenha = tk.Toplevel()
    adsenha.title("Adicionar senha de login do funcionário")
    adsenha.grab_set()
    tk.Label(adsenha, text="Adicione a senha de login do funcionário").grid(row=0, column=0, columnspan=2, padx=(8, 2), pady=6)
    tk.Label(adsenha, text="Senha:").grid(row=1, column=0, padx=(8, 2), pady=6, sticky="e")
    senha = tk.Entry(adsenha, width=40)
    senha.grid(row=1, column=1, padx=(5, 8), pady=6)
    tk.Button(adsenha, text="Salvar", command=lambda:salvar(dados, senha, adsenha, parent)).grid(row=2, column=0, columnspan=2, pady=10)
    
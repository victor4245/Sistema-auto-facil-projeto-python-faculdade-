# =========================================================
# PesFun.py — Consulta de Funcionários (BD)
# =========================================================

import importlib
import tkinter as tk
from tkinter import messagebox
from Menu import conn, cursor
import hashlib
from . import Verificacao

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# ----------------------------------------------------------
# Lê todos os Funcionários do CSV e retorna uma lista de dicts
# ----------------------------------------------------------
def ler_Funcionarios():
    funcionarios = []
    cursor.execute("SELECT * FROM funcionarios")
    funcionarios = cursor.fetchall()
    return funcionarios

def abrir_indice(area_conteudo: tk.Frame):
    for w in area_conteudo.winfo_children():
        w.destroy()
    # Abre o Indice.py e mostra o índice na tela
    try:
        modulo = importlib.import_module("Indice")
        modulo.mostrar_formulario(area_conteudo)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao abrir a tela de Índice:\n{e}")
        
# ----------------------------------------------------------
# Tela principal da pesquisa
# ----------------------------------------------------------
def mostrar_formulario(parent):
    # Limpa a área central
    for w in parent.winfo_children():
        w.destroy()

    # Container central
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
        text="Pesquisa de Funcionários",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=15)

    # ---------------- ENTRADAS ----------------
    entrada_pesq = [None] * 6
    def add_linha(rotulo, linha, col_inicio, largura=40, index=0):
        """Cria um par Label + Entry numa posição da grade."""
        tk.Label(
            caixa,
            text=rotulo,
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).grid(row=linha, column=col_inicio, sticky="w", padx=(4, 8), pady=6)

        entry = tk.Entry(
                caixa,
                width=largura,
                background=COR_CAMPO,
                foreground=COR_TEXTO2,
                insertbackground=COR_TEXTO2,
                relief="flat"
            )
        entry.grid(row=linha, column=col_inicio + 1, sticky="w", padx=(0, 10), pady=6)
        entrada_pesq[index] = entry
        
        # Linha 1
    add_linha("Nome", linha=1, col_inicio=0, largura=40, index=0)
    add_linha("CPF", linha=1, col_inicio=2, largura=24, index=1)

    # Linha 2
    add_linha("E-mail", linha=2, col_inicio=0, largura=40, index=2)
    add_linha("Telefone", linha=2, col_inicio=2, largura=24, index=3)

    # Linha 3
    add_linha("Cargo", linha=3, col_inicio=0, largura=24, index=4)
    add_linha("ID da empresa", linha=3, col_inicio=2, largura=24, index=5)
    

    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=90, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    funcionarios = ler_Funcionarios()
    funcionarios_filtrados = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        funcionarios_filtrados.clear()
        
        cursor.execute("""
        SELECT *
        FROM funcionarios
        WHERE
            nome LIKE %s
            OR cpf LIKE %s
            OR REPLACE(REPLACE(REPLACE(cpf, '.', ''), '-', ''), '/', '') LIKE %s
            OR email LIKE %s
            OR telefone LIKE %s
            OR cargo LIKE %s
            OR id_empresa LIKE %s
        """, (
            f"%{filtro[0]}%",
            f"%{filtro[1]}%",
            f"%{filtro[1]}%",
            f"%{filtro[2]}%",
            f"%{filtro[3]}%",
            f"%{filtro[4]}%",
            f"%{filtro[5]}%",
        ))
        
        funcionarios = cursor.fetchall()
        
        for c in funcionarios:
            texto = f"   {c['nome']}  |  ID da empresa: {c['id_empresa']}  |  Cargo: {c['cargo']}"
            lista.insert(tk.END, texto)
            funcionarios_filtrados.append(c)

    # Pesquisa dinâmica (a cada tecla)
    def ao_digitar(event):
        valores = [''] * 6
        for i in range(len(entrada_pesq)):
            valores[i] = (entrada_pesq[i].get().strip())
        for i in range(len(valores)):
            if valores[i] == '':
                valores[i] = '*'
        atualizar_lista(valores)
       
    for i in range(len(entrada_pesq)):
        entrada_pesq[i].bind("<KeyRelease>", ao_digitar)

    # ---------------- BOTÕES ----------------
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=5, column=0, columnspan=4, pady=15)

    # -------- LISTAGEM COMPLETA --------
    def listar_todos():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)
        funcionarios_filtrados.clear()

        for c in funcionarios:          
            texto = f"   {c['nome']}  |  ID da empresa: {c['id_empresa']}  |  Cargo: {c['cargo']}"
            lista.insert(tk.END, texto)
            funcionarios_filtrados.append(c)

    # -------- LIMPAR --------
    def limpar():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)

    # -------- EDITAR --------
    def editar():
        if not lista.curselection():
            messagebox.showwarning("Atenção", "Selecione um funcionário.")
            return

        indice = lista.curselection()[0]
        funcionario = funcionarios_filtrados[indice]

        abrir_edicao(funcionario)

    # -------- FECHAR --------
    def fechar():
        abrir_indice(parent)

    tk.Button(botoes,
        text="Editar", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=editar,
        bg="#6B7280",  
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
        text="Listagem", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=listar_todos,
        bg="#2563EB", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
        text="Limpar", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=limpar, 
        bg="#C90202", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
    tk.Button(botoes, 
        text="Fechar", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=fechar,
        bg="#C90202",  
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)

# ----------------------------------------------------------
# Tela de edição do funcionário
# ----------------------------------------------------------
def abrir_edicao(funcionario):
    janela = tk.Toplevel()
    janela.title("Editar Funcionário")
    janela.grab_set()

    entradas = {}
    tk.Label(janela, text="Dados do Funcionário", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=2, padx=(8, 2), pady=6)
    def campo(texto, linha, valor=""):
        if texto == "senha":
            return
        tk.Label(janela, text=texto, font=("Segoe UI", 8, "bold")).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="w")
        e = tk.Entry(janela, width=40)
        e.grid(row=linha, column=1, padx=(5, 8), pady=6)
        e.insert(0, valor)
        entradas[texto] = e

    linha = 1
    def Tsenha(texto, linha, valor=""):
        janela2 = tk.Toplevel()
        janela2.title("Editar Senha")
        janela2.grab_set()
        entrada = {}
        tk.Label(janela2, text=texto, font=("Segoe UI", 8, "bold")).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="w")
        e = tk.Entry(janela2, width=40)
        e.grid(row=linha, column=1, padx=(5, 8), pady=6)
        e.insert(0, valor)
        def salvar2(janela2):
            entrada['senha'] = hashlib.sha256(e.get().strip().encode()).hexdigest()
            janela2.destroy()
        tk.Button(janela2, text="Salvar", command=lambda:salvar2(janela2)).grid(row=linha+1, column=0, columnspan=2, pady=10)
        janela2.wait_window()
        if 'senha' in entrada:
            return entrada['senha']
        return funcionario['senha']
        
    for k in funcionario:
        if k != "senha":
            campo(k, linha, funcionario[k])
            linha += 1
        elif k == "senha":
            tk.Button(janela, text="Trocar senha", command=lambda:entradas.update({"senha": Tsenha(k, linha, funcionario[k])})).grid(row=linha, column=0, columnspan=2, pady=10)
    linha += 1
    def salvar():
        c = funcionario
        for k in entradas:
            if k != "senha":
                c[k] = entradas[k].get()
            else:
                c[k] = entradas[k]
        try:
            cursor.execute("""
            UPDATE funcionarios
            SET nome = %s,
                cpf = %s,
                email = %s,
                telefone = %s,
                cargo = %s,
                senha = %s,
                obs = %s
            WHERE id_empresa = %s
            """, (
                c['nome'],
                c['cpf'],
                c['email'],
                c['telefone'],
                c['cargo'],
                c['senha'],
                c['obs'],
                c['id_empresa']
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", "Dados atualizados.")
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível atualizar os dados\n erro: {e}")
            return
    def excluir():
        c = funcionario
        resposta = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o funcionário: {c['nome']}?")
        if resposta:
            janela2 = tk.Toplevel()
            janela2.title("Insira o login e senha para excluir")
            janela2.grab_set()
            def fechar():
                janela2.destroy()
            def logar(login, senha):
                if not login or not senha:
                    messagebox.showerror("Erro", "Preencha ambos os campos.")
                    return
                login_ok = Verificacao.verificar_login(login, senha)
                if login_ok:
                    try:
                        cursor.execute("""
                        DELETE FROM funcionarios
                        WHERE id_empresa = %s
                        """, (
                            c["id_empresa"],))
                        conn.commit()
                        messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
                        janela.destroy()
                    except Exception as e:
                        messagebox.showerror("Erro", f"Não foi possível excluir o funcionário\n erro: {e}")
                        return
                else:
                    messagebox.showerror("Erro", "Login ou senha incorretos ou não possui permissão para excluir funcionários.")
                    return
            def campo(texto, linha):
                tk.Label(janela2, text=texto, font=("Segoe UI", 8, "bold")).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="w")
                e = tk.Entry(janela2, width=40)
                e.grid(row=linha, column=1, padx=(5, 8), pady=6)
                entradas[texto] = e
            campo("Login", 1)
            campo("Senha", 2)
            tk.Button(janela2, text="ENTRAR", command=lambda: logar(entradas["Login"].get(), entradas["Senha"].get())).grid(row=3, column=0, columnspan=2, pady=(20, 10), padx=(0, 110))
            tk.Button(janela2, text="CANCELAR", command=fechar).grid(row=3, column=1, columnspan=2, pady=(20, 10), padx=(30, 0))
        else: 
            return

    tk.Button(janela, text="Excluir", command=excluir).grid(row=linha, column=0, columnspan=2, pady=(20, 10), padx=(0, 110))
    tk.Button(janela, text="Salvar", command=salvar).grid(row=linha, column=1, columnspan=2, pady=(20, 10), padx=(30, 0))
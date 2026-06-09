# =========================================================
# PesFro.py — Consulta de Veículos (BD)
# =========================================================

import importlib
import tkinter as tk
from tkinter import messagebox
from Menu import conn, cursor
from . import Verificacao

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# ----------------------------------------------------------
# Lê todos os Veículos do BD e retorna uma lista de dicts
# ----------------------------------------------------------
def ler_veiculos():
    veiculos = []
    cursor.execute("SELECT * FROM frota")
    veiculos = cursor.fetchall()
    return veiculos

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
        text="Pesquisa de Veículos",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=15)

    # ---------------- ENTRADAS ----------------
    entrada_pesq = [None] * 7
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
    add_linha("Nome", linha=1, col_inicio=0, largura=24, index=0)
    add_linha("Marca", linha=1, col_inicio=2, largura=24, index=1)

    # Linha 2
    add_linha("Modelo", linha=2, col_inicio=0, largura=24, index=2)
    add_linha("Motorização", linha=2, col_inicio=2, largura=21, index=3)

    # Linha 3
    add_linha("Condição", linha=3, col_inicio=0, largura=10, index=4)
    add_linha("Cor", linha=3, col_inicio=2, largura=10, index=5)

    # Linha 4
    add_linha("Ano", linha=4, col_inicio=0, largura=6, index=6)
    
    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=90, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    veiculos = ler_veiculos()
    veiculos_filtrados = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        veiculos_filtrados.clear()
        
        cursor.execute("""
        SELECT *
        FROM frota
        WHERE
            nome LIKE %s
            OR marca LIKE %s
            OR modelo LIKE %s
            OR motorizacao LIKE %s
            OR condicao LIKE %s
            OR cor LIKE %s
            OR ano LIKE %s
        """, (
            f"%{filtro[0]}%",
            f"%{filtro[1]}%",
            f"%{filtro[2]}%",
            f"%{filtro[3]}%",
            f"%{filtro[4]}%",
            f"%{filtro[5]}%",
            f"%{filtro[6]}%"
        ))

        veiculos = cursor.fetchall()
        for c in veiculos:
            texto = f"   {c['marca']} {c['nome']}  |  Placa: {c['placa']}  |  Condição: {c['condicao']}  |  KM: {c['quilometragem']}  |  Preço: R$ {c['preco']}"
            lista.insert(tk.END, texto)
            veiculos_filtrados.append(c)

    # Pesquisa dinâmica (a cada tecla)
    def ao_digitar(event):
        valores = [''] * 7
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
    botoes.grid(row=6, column=0, columnspan=4, pady=15)

    # -------- LISTAGEM COMPLETA --------
    def listar_todos():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)
        veiculos_filtrados.clear()

        for c in veiculos:          
            texto = f"   {c['marca']} {c['nome']}  |  Placa: {c['placa']}  |  Condição: {c['condicao']}  |  KM: {c['quilometragem']}  |  Preço: R$ {c['preco']}"
            lista.insert(tk.END, texto)
            veiculos_filtrados.append(c)

    # -------- LIMPAR --------
    def limpar():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)

    # -------- EDITAR --------
    def editar():
        if not lista.curselection():
            messagebox.showwarning("Atenção", "Selecione um veículo.")
            return

        indice = lista.curselection()[0]
        veiculo = veiculos_filtrados[indice]

        abrir_edicao(veiculo)

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
# Tela de edição da frota
# ----------------------------------------------------------
def abrir_edicao(veiculo):
    janela = tk.Toplevel()
    janela.title("Editar Veículo")
    janela.grab_set()

    entradas = {}
    tk.Label(janela, text="Dados do Veículo", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=2, padx=(8, 2), pady=6)
    def campo(texto, linha, valor=""):
        tk.Label(janela, text=texto, font=("Segoe UI", 8, "bold")).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="w")
        e = tk.Entry(janela, width=40)
        e.grid(row=linha, column=1, padx=(5, 8), pady=6)
        e.insert(0, valor)
        entradas[texto] = e

    linha = 1
    for k in veiculo:
        campo(k, linha, veiculo[k])
        linha += 1

    def salvar():
        c = veiculo
        for k in entradas:
            c[k] = entradas[k].get()
        try:
            c['preco'] = c['preco'].replace(",", ".")
            c['preco_aluguel'] = c['preco_aluguel'].replace(",", ".")
            cursor.execute("""
            UPDATE frota
            SET nome = %s,
                placa = %s,
                marca = %s,
                modelo = %s,
                motorizacao = %s,
                condicao = %s,
                cor = %s,
                ano = %s,
                quilometragem = %s,
                preco = %s,
                preco_aluguel = %s,
                obs = %s
            WHERE codigo = %s
            """, (
                c['nome'],
                c["placa"],
                c['marca'],
                c['modelo'],
                c['motorizacao'],
                c['condicao'],
                c['cor'],
                c['ano'],
                c['quilometragem'],
                c['preco'],
                c['preco_aluguel'],
                c['obs'],
                c['codigo']
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", "Dados atualizados.")
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível atualizar os dados\n erro: {e}")
            return
        
    def excluir():
        c = veiculo
        resposta = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o veículo: {c['nome']}?")
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
                        DELETE FROM frota
                        WHERE codigo = %s
                        """, (
                            c["codigo"],))
                        conn.commit()
                        messagebox.showinfo("Sucesso", "Veículo excluído com sucesso!")
                        janela.destroy()
                    except Exception as e:
                        messagebox.showerror("Erro", f"Não foi possível excluir o veículo\n erro: {e}")
                        return
                else:
                    messagebox.showerror("Erro", "Login ou senha incorretos ou não possui permissão para excluir veículos.")
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
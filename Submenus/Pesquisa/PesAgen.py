# =========================================================
# PesAgen.py — Consulta de Reuniões/Tests Drives (BD)
# =========================================================

import importlib
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from Menu import conn, cursor
from . import Verificacao

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"
PAGINA = 1
def ajusta_pagina(valor):
    global PAGINA
    PAGINA = valor

# ----------------------------------------------------------
# Lê todas as reuniões do BD e retorna uma lista de dicts
# ----------------------------------------------------------
def ler_reun():
    reunioes = []
    cursor.execute("SELECT * FROM agenreu")
    reunioes = cursor.fetchall()
    return reunioes
        
# ----------------------------------------------------------
# Lê todas os tests drive do BD e retorna uma lista de dicts
# ----------------------------------------------------------
def ler_TD():
    Td = []
    cursor.execute("SELECT * FROM agentd")
    Td = cursor.fetchall()
    return Td

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
    if PAGINA == 1:
        NOME = "Reuniões"
        NOME2 = "Reunião"
        LISTA = ler_reun()
        cab = "Local"
        cab2 = 'local'
    elif PAGINA == 2:
        NOME = "Tests Drive"
        NOME2 = "Test Drive"
        LISTA = ler_TD()
        cab = "Veículo"
        cab2 = 'veiculo'
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
        text=f"Pesquisa de {NOME}",
        font=("Segoe UI", 16, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=0, column=0, columnspan=4, pady=15)

    # ---------------- ENTRADAS ----------------
    entrada_pesq = [None] * 2
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
    add_linha("Cliente", linha=1, col_inicio=0, largura=24, index=0)
    add_linha("Data", linha=1, col_inicio=2, largura=24, index=1)

    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=90, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    lista_filtrada = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        lista_filtrada.clear()
        
        if PAGINA == 1:
            cursor.execute("""
            SELECT *
            FROM agenreu
            WHERE
                cliente LIKE %s
                OR data LIKE %s
            """, (
                f"%{filtro[0]}%",
                f"%{filtro[1]}%"
            ))
        elif PAGINA == 2:
            cursor.execute("""
            SELECT *
            FROM agentd
            WHERE
                cliente LIKE %s
                OR data LIKE %s
            """, (
                f"%{filtro[0]}%",
                f"%{filtro[1]}%"
            ))
        LISTA = cursor.fetchall()
        for c in LISTA:
            texto = f"   {c['cliente']}  |  Data: {c['data']}  |  {cab}: {c[cab2]}"
            lista.insert(tk.END, texto)
            lista_filtrada.append(c)

    # Pesquisa dinâmica (a cada tecla)
    def ao_digitar(event):
        valores = [''] * 2
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
    botoes.grid(row=3, column=0, columnspan=4, pady=15)
    
    botoes2 = tk.Frame(caixa, bg=COR_FUNDO)
    botoes2.grid(row=4, column=0, columnspan=4, pady=15)

    # -------- LISTAGEM COMPLETA --------
    def listar_todos():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)
        lista_filtrada.clear()

        for c in LISTA:          
            texto = f"   {c['cliente']}  |  Data: {c['data']}  |  {cab}: {c[cab2]}"
            lista.insert(tk.END, texto)
            lista_filtrada.append(c)

    # -------- LIMPAR --------
    def limpar():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)

    # -------- EDITAR --------
    def editar():
        if not lista.curselection():
            messagebox.showwarning("Atenção", f"Selecione um(a) {NOME2}.")
            return

        indice = lista.curselection()[0]
        lis = lista_filtrada[indice]

        abrir_edicao(lis, NOME2)

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
    tk.Button(
        botoes2,
        text="Reuniões",
        font=("Segoe UI", 10, "bold"),
        bg="#2563EB",
        fg="white",
        activebackground="#1E40AF",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=lambda:[ajusta_pagina(1),mostrar_formulario(parent)],
        cursor="hand2").pack(side="left", padx=6)
    tk.Button(
        botoes2,
        text="Test Drives",
        font=("Segoe UI", 10, "bold"),
        bg="#2563EB",
        fg="white",
        activebackground="#1E40AF",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=lambda:[ajusta_pagina(2),mostrar_formulario(parent)],
        cursor="hand2").pack(side="left", padx=6)

# ----------------------------------------------------------
# Tela de edição de agendamento
# ----------------------------------------------------------
def abrir_edicao(agendamento, NOME):
    
    janela = tk.Toplevel()
    janela.title(f"Editar {NOME}")
    janela.grab_set()

    entradas = {}
    tk.Label(janela, text=f"Dados {NOME}", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=2, padx=(8, 2), pady=6)
    def campo(texto, linha, valor=""):
        tk.Label(janela, text=texto, font=("Segoe UI", 8, "bold")).grid(row=linha, column=0, padx=(8, 2), pady=6, sticky="w")
        e = tk.Entry(janela, width=40)
        e.grid(row=linha, column=1, padx=(5, 8), pady=6)
        e.insert(0, valor)
        entradas[texto] = e

    linha = 1
    for k in agendamento:
        campo(k, linha, agendamento[k])
        linha += 1

    def salvar():
        c = agendamento
        for k in entradas:
            c[k] = entradas[k].get()
        AGORA = datetime.now().strftime("%d/%m/%Y")
        if datetime.strptime(c["data"], "%d/%m/%Y") < datetime.strptime(AGORA, "%d/%m/%Y"):
            messagebox.showwarning("Data inválida", "A data do agendamento não pode ser anterior ao momento atual.")
            return
        if PAGINA == 1:
            try:
                cursor.execute("""
                UPDATE agenreu
                SET cliente = %s,
                    horario = %s,
                    data = %s,
                    local = %s,
                    obs = %s
                WHERE codigo = %s
                """, (
                    c['cliente'],
                    c['horario'],
                    c['data'],
                    c['local'],
                    c['obs'],
                    c["codigo"]
                ))

                conn.commit()
                messagebox.showinfo("Sucesso", "Dados atualizados.")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao tentar atualizar os dados.\n Erro: {e}")
                return
        elif PAGINA == 2:
            try:
                cursor.execute("""
                UPDATE agentd
                SET cliente = %s,
                    horario = %s,
                    data = %s,
                    veiculo = %s,
                    obs = %s
                WHERE codigo = %s
                """, (
                    c['cliente'],
                    c['horario'],
                    c['data'],
                    c['veiculo'],
                    c['obs'],
                    c["codigo"]
                ))

                conn.commit()
                messagebox.showinfo("Sucesso", "Dados atualizados.")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao tentar atualizar os dados.\n Erro: {e}")
                return
            
    def excluir():
        if PAGINA == 1:
            c = agendamento
            resposta = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir a reunião com o cliente: {c['cliente']}?")
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
                    if login_ok == True:
                        try:
                            cursor.execute("""
                            DELETE FROM agenreu
                            WHERE codigo = %s
                            """, (
                                c["codigo"],))
                            conn.commit()
                            messagebox.showinfo("Sucesso", "Reunião excluída com sucesso!")
                            janela.destroy()
                        except Exception as e:
                            messagebox.showerror("Erro", f"Não foi possível excluir a reunião\n erro: {e}")
                            return
                    else:
                        messagebox.showerror("Erro", "Login ou senha incorretos ou não possui permissão para excluir clientes.")
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
        if PAGINA == 2:
            c = agendamento
            resposta = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o test drive com o cliente: {c['cliente']}?")
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
                    if login_ok == True:
                        try:
                            cursor.execute("""
                            DELETE FROM agentd
                            WHERE codigo = %s
                            """, (
                            c["codigo"],))
                            conn.commit()
                            messagebox.showinfo("Sucesso", "Test Drive excluído com sucesso!")
                            janela.destroy()
                        except Exception as e:
                            messagebox.showerror("Erro", f"Não foi possível excluir o test drive\n erro: {e}")
                            return
                    else:
                        messagebox.showerror("Erro", "Login ou senha incorretos ou não possui permissão para excluir clientes.")
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
    
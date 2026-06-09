# ========================================================
# Devolucao.py — Devolução de veículos
#
# Devolucao.mostrar_formulario(area_conteudo)
# ========================================================

import importlib
import tkinter as tk
from tkinter import messagebox
from Menu import conn, cursor

# -------- CONFIGURAÇÕES BÁSICAS DE UI --------

COR_TEXTO = "#FFFFFF"
COR_TEXTO2 = "#000000"
COR_CAMPO = "#FFFFFF"
COR_FUNDO = "#0B1220"

# -------- CAPTURA DE DADOS --------

# Captura dos aluguéis feitos

def aluguel():
    cursor.execute("""SELECT * FROM aluguel""")
    return cursor.fetchall()


# --------------------------------------------------------
# SALVA OS DADOS NO BD
# --------------------------------------------------------
def salvar(aluguel, veiculo, parent):
    obs2 = "Sem observações"
    conn.autocommit = False
    try:
        cursor.execute("""
            UPDATE frota
            SET 
                obs = %s
            WHERE codigo = %s
            """, (
                obs2,
                veiculo['codigo']
            ))
        cursor.execute("""
                       DELETE FROM aluguel 
                       WHERE codigo = %s""", (aluguel['codigo'],))
        conn.commit()
        messagebox.showinfo("Sucesso", "Devolução feita com sucesso!")
        mostrar_formulario(parent)
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", f"Não foi possível atualizar os dados\n erro: {e}")
        return
    finally:
        conn.autocommit = True
        
def limpar(parent: tk.Frame):
    """Remove tudo que estiver no parent (caso queira reutilizar)."""
    for w in parent.winfo_children():
        w.destroy()   
        
def abrir_indice(area_conteudo: tk.Frame):
    for w in area_conteudo.winfo_children():
        w.destroy()
    # Abre o Indice.py e mostra o índice na tela
    try:
        modulo = importlib.import_module("Indice")
        modulo.mostrar_formulario(area_conteudo)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao abrir a tela de Índice:\n{e}")
         
def mostrar_formulario(parent: tk.Frame):
    """Constrói o formulário de devolução de veículos dentro do 'parent' (área central)."""

    # Limpa qualquer conteúdo anterior
    limpar(parent)

    ALUGUEL = aluguel()

    # Um container centralizado
    container = tk.Frame(parent, bg="#1F2937")
    container.pack(fill="both", expand=True)
    
    # Um container auxiliar para melhor controle
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
    add_linha("Nome do veiculo", linha=1, col_inicio=0, largura=30, index=0)
    add_linha("Nome do cliente", linha=1, col_inicio=2, largura=30, index=1)

    # ---------------- LISTBOX (RESULTADOS) ----------------
    lista = tk.Listbox(caixa, width=100, height=10, bg=COR_CAMPO, fg="black", borderwidth=0, highlightthickness=0)
    lista.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
    alugueis_filtrados = []

    # ---------------- FUNÇÃO: atualizar resultados ----------------
    def atualizar_lista(filtro):
        lista.delete(0, tk.END)
        alugueis_filtrados.clear()

        cursor.execute("""
        SELECT *
        FROM aluguel
        WHERE
            nome_veiculo LIKE %s
            OR nome_cliente LIKE %s
        """, (
            f"%{filtro[0]}%",
            f"%{filtro[1]}%",
        ))

        alugueis = cursor.fetchall()
        
        for c in alugueis:
            texto = f"   Veiculo: {c['nome_veiculo']}  |  Cliente: {c['nome_cliente']}  |  Data de devolução: {c['data_final']}  |  Horário de devolução: {c['horario_final']}"
            lista.insert(tk.END, texto)
            alugueis_filtrados.append(c)

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
    botoes.grid(row=4, column=0, columnspan=4, pady=16)

    # -------- LISTAGEM COMPLETA --------
    def listar_todos():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)
        alugueis_filtrados.clear()

        for c in ALUGUEL:          
            texto = f"   Veiculo: {c['nome_veiculo']}  |  Cliente: {c['nome_cliente']}  |  Data de devolução: {c['data_final']}  |  Horário de devolução: {c['horario_final']}"
            lista.insert(tk.END, texto)
            alugueis_filtrados.append(c)
            
    def on_salvar():
        if not lista.curselection():
            messagebox.showwarning("Atenção", "Selecione um aluguel para devolver.")
            return
        selecionado = lista.curselection()
        temp = alugueis_filtrados[selecionado[0]]
        R_aluguel = {'codigo': temp['codigo']}
        veiculo = {'codigo': temp['cod_veiculo']}
        salvar(R_aluguel, veiculo, parent)

    def on_limpar():
        for i in range(len(entrada_pesq)):
            entrada_pesq[i].delete(0, tk.END)
        lista.delete(0, tk.END)

    # -------- FECHAR --------
    def fechar():
        abrir_indice(parent)

    tk.Button(
        botoes,
        text="Devolver",
        font=("Segoe UI", 10, "bold"),
        bg="#2563EB",
        fg="white",
        activebackground="#1E40AF",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=on_salvar,
        cursor="hand2").pack(side="left", padx=6)
    tk.Button(botoes, 
        text="Listagem", 
        font=("Segoe UI", 10, "bold"),
        width=10, 
        command=listar_todos,
        bg="#6B7280", 
        fg="white", 
        relief="flat",
        padx=14,
        pady=8,
        cursor="hand2").pack(side="left", padx=4)
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
        text="Fechar",
        font=("Segoe UI", 10, "bold"),
        bg="#C90202",
        fg="white",
        activebackground="#8D0202",
        activeforeground="white",
        relief="flat",
        padx=14,
        pady=8,
        command=fechar,
        cursor="hand2"
    ).pack(side="left", padx=6)
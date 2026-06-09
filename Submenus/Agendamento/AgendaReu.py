# ========================================================
# AgendaReu.py — Agendamento de Reunião
#
# AgendaReu.mostrar_formulario(area_conteudo)
# ========================================================

import importlib
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry
from Menu import conn, cursor

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
                "Preencha todos os campos para salvar a reunião."
            )
            return
    AGORA = datetime.now().strftime("%d/%m/%Y")
    if datetime.strptime(dados["data"], "%d/%m/%Y") < datetime.strptime(AGORA, "%d/%m/%Y"):
        messagebox.showwarning(
            "Data inválida",
            "A data da reunião não pode ser anterior ao momento atual."
        )
        return

    try:
        cursor.execute("""INSERT INTO agenreu (cliente,horario,local,data,obs)
                       VALUES
                       (%s,%s,%s,%s,%s)
                       """,(
                        dados["cliente"],
                        dados["horario"],
                        dados["local"],
                        dados["data"],
                        dados["obs"]
                       ))
        conn.commit()
        messagebox.showinfo("Sucesso", "Reunião agendada com sucesso!")
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
    """Constrói o formulário de Reunião dentro do 'parent' (área central)."""

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
        text="Agendamento de Reunião",
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
        if rotulo == "Data":
            entry = DateEntry(
                caixa,
                width=largura,
                foreground=COR_TEXTO,
                borderwidth=2,
                date_pattern='dd/mm/yyyy'  # Formato BR
            )
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
    add_linha("Cliente", "cliente", linha=1, col_inicio=0, largura=40)
    add_linha("Horário", "horario", linha=1, col_inicio=2, largura=20)

    # Linha 2
    add_linha("Local", "local", linha=2, col_inicio=0, largura=40)
    add_linha("Data", "data", linha=2, col_inicio=2, largura=17)

    # Observações
    tk.Label(
        caixa,
        text="Observações",
        font=("Segoe UI", 10, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    ).grid(row=3, column=0, columnspan=4, sticky="", padx=(8, 8), pady=(15, 0))

    txt_obs = tk.Text(caixa, width=66, height=5, background=COR_CAMPO,foreground=COR_TEXTO2,insertbackground=COR_TEXTO2, relief="flat")
    txt_obs.grid(row=4, column=0, columnspan=4, sticky="", padx=(10, 10), pady=(15, 0))

    # ---------------- BOTÕES ----------------
    botoes = tk.Frame(caixa, bg=COR_FUNDO)
    botoes.grid(row=5, column=0, columnspan=4, pady=(16, 0))

    def on_salvar():
        dados = {add_linha: entrada.get().strip() for add_linha, entrada in entradas.items()}
        dados["obs"] = txt_obs.get("1.0", "end-1c").strip()
        salvar(dados, parent)

    def on_limpar():
        for ent in entradas.values():
            if isinstance(ent, DateEntry):
                ent.set_date(datetime.now())
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

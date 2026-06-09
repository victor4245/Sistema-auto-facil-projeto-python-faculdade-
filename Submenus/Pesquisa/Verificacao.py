# Arquivo auxiliar para funções de verificação.
import hashlib
from Menu import cursor

def verificar_login(login3, senha):
    
    login = []
    LOGIN_EMAIL = []
    LOGIN_CPF = []
    LOGIN_ID = []
    PESSOA = []
    CARGO = []
    SENHA_ESPERADA = []
    cursor.execute("""SELECT * FROM funcionarios""")
    leitor = cursor.fetchall()
    for linha in leitor:
        login.append(linha) 

    for i in range(len(login)):
        # Adição dos CPFs, IDs e Emails para verificação de login
        LOGIN_CPF.append(login[i]["cpf"].replace(".", "").replace("-", "").strip())
        LOGIN_EMAIL.append(login[i]["email"])
        LOGIN_ID.append(login[i]["id_empresa"])
        PESSOA.append(login[i]["nome"])
        CARGO.append(login[i]["cargo"])
        # Adição das senhas para verificação de login
        SENHA_ESPERADA.append(login[i]["senha"])
    if len(login3) == 14:
        login3 = login3.replace(".", "").replace("-", "")
    
    # Validação de Login e senha
    i = 0
    while (i < len(LOGIN_EMAIL)):
        if (login3 == LOGIN_EMAIL[i] or login3 == LOGIN_CPF[i] or login3 == LOGIN_ID[i]) and CARGO[i] in ["Administrador", "Gerente", "Assistente administrativo", "Vendedor"]:
            if hashlib.sha256(senha.encode()).hexdigest() == SENHA_ESPERADA[i]:
                login2 = True
                return True
            else:
                login2 = False
                break
        else:
            login2 = False
            i += 1
    if not login2:
        return False
def verificar_existe(tabela, cpf=None, email=None, placa=None, telefone=None):
    if tabela == "Clientes":
        if cpf:
            cursor.execute("""SELECT * FROM clientes WHERE cpf_cnpj = %s""", (cpf,))
            temp = cursor.fetchone()
            if temp:
                return True
            return False
        if email:
            cursor.execute("""SELECT * FROM clientes WHERE email = %s""", (email,))
            temp = cursor.fetchone()
            if temp:
                return True
            return False
        if telefone:
            cursor.execute("""SELECT * FROM clientes WHERE telefone = %s""", (telefone,))
            temp = cursor.fetchone()
            if temp:
                return True
            return False
    if tabela == "Frota":
        if placa:
            cursor.execute("""SELECT * FROM frota WHERE placa = %s""", (placa,))
            temp = cursor.fetchone()
            if temp:
                return True
            return False
    if tabela == "Funcionarios":
        if cpf:
            cursor.execute("""SELECT * FROM funcionarios WHERE cpf = %s""", (cpf,))
            temp = cursor.fetchone()
            if temp:
                return True
            return False
        if email:
            cursor.execute("""SELECT * FROM funcionarios WHERE email = %s""", (email,))
            temp = cursor.fetchone()
            if temp:
                return True
            return False
        if telefone:
            cursor.execute("""SELECT * FROM funcionarios WHERE telefone = %s""", (telefone,))
            temp = cursor.fetchone()
            if temp:
                return True
            return False
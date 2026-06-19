import random
import getpass
from datetime import datetime, timedelta

bd_usuarios = {}
bd_livros = {}

# Dados iniciais
bd_livros["001"] = {"Título": "Chamado de Cthulhu", "Autor": "H. P. Lovecraft", "Gênero": "Horror Cósmico", "Faixa Etária": "Livre", "Emprestado para": None, "Devolução em": None}
bd_livros["002"] = {"Título": "Livro dos Sith", "Autor": "Daniel Wallace", "Gênero": "Literatura e Ficção", "Faixa Etária": "Livre", "Emprestado para": None, "Devolução em": None}
bd_livros["003"] = {"Título": "1984", "Autor": "George Orwell", "Gênero": "Distopia", "Faixa Etária": "Livre", "Emprestado para": None, "Devolução em": None}
bd_livros["004"] = {"Título": "Por Quem Os Sinos Dobram", "Autor": "Ernest Hemingway", "Gênero": "Romance", "Faixa Etária": "Adulto", "Emprestado para": None, "Devolução em": None}

# Funções de regras de negócio e auxiliares

def calculo_multa(data_devolucao):
    if not data_devolucao:
        return 0, 0.0
    
    # Simulando atraso
    data_atual = datetime.now()
    if data_atual > data_devolucao:
        dias_atraso = (data_atual - data_devolucao).days
        multa = dias_atraso * 1.50
        return dias_atraso, multa
    return 0, 0.0

def contagem_livrosp(numero_registro):
    total = 0
    for livro in bd_livros.values():
        if livro["Emprestado para"] == numero_registro:
            total += 1
    return total
    
# Telas do Fluxo Público

def tela_inicial():
    while True:
        print("""==================================================
        BIBLIOTECA COMUNITÁRIA - CLI v1.0
==================================================
1. Ver Catálogo de Livros (Livre)
2. Criar Nova Conta (Gerar Registro)
3. Fazer Login
4. Acessar Painel Operador
5. Sair
--------------------------------------------------""")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            tela_catalogo(usuario_logado=None)
        elif opcao == "2":
            tela_cadastro()
        elif opcao == "3":
            usuario = tela_login()
            if usuario:
                tela_painel_usuario(usuario)
        elif opcao == "4":
            if login_operador():
                tela_poperador()
        elif opcao == "5":
            print("Saindo do sistema, volte sempre!")
            break

def tela_cadastro():
        print ("""==================================================
                CADASTRO DE USUÁRIO
==================================================""")
        nome = input("Digite seu Nome Completo: ")
        while True:
            cpf = input("Digite seu CPF (11 Números): ")
            if len(cpf) == 11 and cpf.isdigit():
                break
            print("[ERRO] CPF inválido!")
        while True:
            nascimento = input("Digite sua Data de Nascimento (AAAA/MM/DD): ")
            try:
                data_nasc = datetime.strptime(nascimento, "%Y/%m/%d").date()
                if data_nasc > datetime.now().date():
                    print("[ERRO] Data impossível!")
                else:
                    break
            except ValueError:
                print("[ERRO] Data impossível ou formato incorreto!")
        senha = getpass.getpass("Digite sua Senha: ")

# Gerando número registro
        ano_atual = datetime.now().year
        sufixo_a = random.randint(1000,9999)
        numero_r = f"{ano_atual}-{sufixo_a}"
        
# Salva no "Bando de Dados"
        bd_usuarios[numero_r] = {
            "nome": nome,
            "cpf": cpf,
            "senha": senha,
            "adulto_validado": False 
        }

        print("--------------------------------------------------")
        print(f"Guarde seu número de acesso para utilizar a biblioteca:\n")
        print(f"   >>> SEU NÚMERO DE REGISTRO: {numero_r} <<<")
        print("--------------------------------------------------")
        input("Pressione ENTER para voltar ao menu.")

def tela_login():
    print("""==================================================
                         LOGIN
    ==================================================""")
    registro = input("Número de Registro: ")
    senha = getpass.getpass("Digite sua Senha: ")

    if registro in bd_usuarios and bd_usuarios[registro]["senha"] == senha:
        print(f"Login bem-sucedido! Bem-vindo(a), {bd_usuarios[registro]['nome']}.")
        return registro
    else: 
        print("[Erro] Registro ou Senha incorretos.")
        input("Pressione ENTER para voltar ao menu.")
        return None
    
    # Tela Usuário Registrado

def tela_painel_usuario(numregistro):
    while True:
        user_dados = bd_usuarios[numregistro]
        livros_posse = contagem_livrosp(numregistro)
        status_idade = "Validada +18" if user_dados["adulto_validado"] else "Não Valido"

        print("""==================================================""")
        print(f"        PAINEL DO LEITOR - Olá, {user_dados['nome']}")
        print("""==================================================""")
        print(f"  REGISTRO:{numregistro} | Idade: {status_idade}")
        print(f"  Livros em sua Posse: {livros_posse}  /   3    ")
        print("""--------------------------------------------------
1. Pesquisar e ver Catálogo
2. Validar minha Idade
3. Cadastrar Livro
4. Ver Meus Emprestimos em Prazos
5. Fazer Logout
--------------------------------------------------""")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            tela_catalogo(usuario_logado=numregistro)
        elif opcao == "2":
            # Mera simulação de uma validação
            user_dados["adulto_validado"] = True
            print("Idade validada com sucesso atráves dos dados do governo!")
            input("Pressione ENTER")
        elif opcao == "3":
            tela_cadastrar_livro(numregistro)
        elif opcao == "4":
            tela_emprestimos(numregistro)
        elif opcao == "5":
            break

def tela_catalogo(usuario_logado):
    print("""==================================================
     CATÁLOGO DE LIVROS
==================================================""")
    
    ver_adulto = False
    if usuario_logado and bd_usuarios[usuario_logado]["adulto_validado"]:
        ver_adulto = True

    ha_livros = False
    for id_livro, dados in bd_livros.items():
            if dados["Faixa Etária"] == "Adulto" and not ver_adulto:
                continue
            
            status_disponivel = "Disponível" if dados["Emprestado para"] is None else "Emprestado"
            print(f"ID: {id_livro} | '{dados['Título']}' | Autor: {dados['Autor']} | Gênero: {dados['Gênero']} | [{dados['Faixa Etária']}] - ({status_disponivel})")
            ha_livros = True

    if not ha_livros:
            print("Nenhum livro disponível para sua faixa etária no momento!")

    print("--------------------------------------------------")
    input("Pressione ENTER para voltar ao Menu.")

def tela_cadastrar_livro(numregistro):
    print("""==================================================
    DISPONIBILIZAR LIVRO PARA EMPRÉSTIMO
==================================================""")
    titulo = input("Título do Livro: ")
    autor = input("Autor do Livro: ")
    genero = input("Gênero do Livro: ")
    while True:
        faixa_etaria = input("Faixa Etária do Livro (Livre ou Adulto): ").strip().capitalize()
        if faixa_etaria in ["Livre", "Adulto"]:
            break
        print("[ERRO] Selecione uma Faixa Etária valida!")

    novo_id = str(random.randint(200, 999))
    bd_livros[novo_id] = {
        "Título": titulo,
        "Autor": autor,
        "Gênero": genero,
        "Faixa Etária": faixa_etaria,
        "Emprestado para": None,
        "Devolução em": None,
    }
    print(f"Livro Cadastrado automaticamente com o ID: #{novo_id}")
    input("Pressione ENTER para voltar")

def tela_emprestimos(numregistro):
    print("""==================================================
        MEUS EMPRÉSTIMOS
==================================================""")
    possui_livros = False
    for id_livros, dados in bd_livros.items():
         if dados["Emprestado para"] == numregistro:
            possui_livros = True
            dias, multa = calculo_multa(dados["Devolução em"])
            data_str = dados["Devolução em"].strftime("%Y/%m/%d") if dados["Devolução em"] else "Sem prazo"
            print(f"Livro: '{dados['Título']}' | Devolução até: {data_str}")

            if dias > 3:
              print(f"  -> [ATRASADO] {dias} dias de atraso. Multa acumulada: R$ {multa:.2f}")
            else:
              print(f"  -> Dentro do prazo.")
    if not possui_livros:
        print("Você não possui nenhum empréstimo no momento!")
        input("Pressione ENTER para voltar")

# Telas do Operador

def tela_poperador():
    while True:
        print("""==================================================
     TELA DO OPERADOR
==================================================
1. Simulação Rápida
2. Consultar Usuário
3. Sair
--------------------------------------------------
""")
        opcao =  input("Escolhe uma opção: ")

        if opcao == "1":
            simular_bipagem()
        elif opcao == "2":
            tela_consulta_usuario() # type: ignore
        elif opcao == "3":
            break

def simular_bipagem():
    print("""Insira o ID do Livro.""")
    id_livro = input("Digite o ID do Livro: ")

    if id_livro not in bd_livros:
        print("[ERRO] Livro não cadastrado no sistema.")
        return
    
    livro = bd_livros[id_livro]

    # Devolução Automatica
    if livro["Emprestado para"] is not None:
        usuario_registrado = livro["Emprestado para"]
        dias, multa = calculo_multa(livro["Devolução em"])

        print(f"[Processando Devolução...] Livro encontrado com o Usuário {usuario_registrado}.")
        if dias > 0:
            print(f"[ALERTA] Livro atrasado, multa de R${multa:.2f}")

    # Empréstimo automatico
    else:
       print(f"[Emprestimo] livro '{livro['Título']}' está disponível")
       registro_user = input("Digite o ID do cliente: ")

    if registro_user not in bd_usuarios:
        print("[ERRO] ID inexistente.")
        return

    if contagem_livrosp(registro_user) >= 3:
        print("[BLOQUEADO] O usuário já atingiu o nível máximo de Livros em posse.")
        return

    if livro["Faixa Etária"] == "Adulto" and not bd_usuarios[registro_user]["adulto_validado"]:
        print("[BLOQUEADO] A idade do usuário não bate com a faixa etária do Livro")
        return

    # Resetando o estado do Livro
    livro["Emprestado para"] = None
    livro["Devolução em"] = None
    print("Livro de volta ao catálogo")

    # Executando empréstimo
    livro["Emprestado para"] = registro_user
    livro["Devolução em"] = datetime.now() + timedelta(days=7)
    data_limite_str = livro["Devolução em"].strftime("%Y/%m/%d")

    print(f"Emprestimo registrado, data de devolução: {data_limite_str}")

    input("Pressione ENTER para voltar")

def login_operador():
    print("""==================================================
                 LOGIN DO OPERADOR
==================================================""")
    usuario = input("Login: ")
    senha = getpass.getpass("Senha: ")

    if usuario == "operador" and senha == "4321":
        print("Acesso autorizado! Entrando no Painel do Operador...")
        input("Pressione ENTER para continuar.")
        return True
    else:
        print("[ERRO] Login ou senha incorretos! Acesso negado!")
        input("Pressione ENTER para continuar.")
        return False

def tela_consulta_usuario():
    print("\n==================================================")
    print("               CONSULTA DE USUÁRIO")
    print("==================================================")
    registroid = input("Digite o ID do Usuário: ")

    if registroid in bd_usuarios:
        user = bd_usuarios[registroid]
        print("------------------------------------------")
        print(f"Nome do Usuário: {user['nome']}")
        print(f"Idade: {'Maior de Idade(Validada)' if user['adulto_validado'] else 'Idade não Validada'}")
        print(f"Total de Livros em Posse: {contagem_livrosp(registroid)} / 3")
        print("Histórico atual de Livros em Posse:")

        possui_livros = False
        for id_livro, dados in bd_livros.items():
            if dados["Emprestado para"] == registroid:
                possui_livros = True 
                dias, multa = calculo_multa(dados["Devolução em"])
                status = f"Atrasado. multa aplicada de R${multa:.2f}" if dias > 0 else "Dentro do prazo"
                print(f" - ID #{id_livro}: '{dados['Título']}  |  Status: {status}")
            
        if not possui_livros:
            print("Nenhum livro em posse")
    else:
        print("[ERRO] Nenhum usuário encontrado")
        input("Pressione ENTER para voltar")


if __name__ == "__main__":
    tela_inicial()

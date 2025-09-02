import datetime
import sys

def separador():
    print(30 * '-===-')

def erro(msg):
    print(f'\033[31m{msg}\033[m')
    separador()

def sucesso(msg):
    print(f'\033[32m{msg}\033[m')
    separador()

def pedir_input(mensagem, obrigatorio=True):
    while True:
        valor = input(mensagem).strip()
        if obrigatorio and valor == '':
            erro('Por favor, insira um valor válido.')
        else:
            return valor

def pedir_numero(mensagem, minimo=None, maximo=None):
    while True:
        valor = input(mensagem).strip()
        try:
            numero = int(valor)
            if (minimo is not None and numero < minimo) or (maximo is not None and numero > maximo):
                erro(f'Por favor, insira um número entre {minimo} e {maximo}.')
            else:
                return numero
        except ValueError:
            erro('Por favor, insira um número válido.')

def converter_data(data_str):
    try:
        return datetime.datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        return None

def data_valida(data_str):
    return converter_data(data_str) is not None

# Verificação de usuário
def usuario_existe(nome, usuarios):
    for usuario in usuarios:
        if usuario['nome'] == nome:
            return usuario
    return None

# Exibição e listagem de atividades
def exibir_atividades(atividades):
    if not atividades:
        erro('Nenhuma atividade cadastrada.')
        return
    print("\033[36mAtividades cadastradas:\033[m")
    for i, atividade in enumerate(atividades, start=1):
        print(
            f"\033[33mAtividade Nº {i}\033[m\n"
            f"Nome: \033[36m{atividade['nome']}\033[m\n"
            f"Prazo: \033[36m{atividade['inicio'].strftime('%d/%m/%Y')} à {atividade['fim'].strftime('%d/%m/%Y')}\033[m\n"
            f"Descrição: \033[36m{atividade['descricao']}\033[m\n"
            f"Prioridade: \033[36m{atividade['prioridade']}\033[m\n"
        )
        separador()

# Painel de prioridade
def mostrar_painel_prioridade():
    print('\033[36mEscolha a prioridade da atividade:\033[m')
    print('\033[35m1 - Alta\n2 - Média\n3 - Baixa\033[m')

# Login de usuário
def user_login(usuarios):
    while True:
        nome = pedir_input('Digite seu nome de usuário (ou "sair" para encerrar): ')
        if nome.lower() == 'sair':
            sucesso('Encerrando o programa...')
            sys.exit()
        usuario = usuario_existe(nome, usuarios)
        if usuario:
            print('\033[32mNome de usuário encontrado!\033[m')
            break
        else:
            erro('Usuário ou nome não cadastrado. Tente novamente.')

    while True:
        senha = pedir_input('Digite sua senha: ')
        if senha == usuario['senha']:
            sucesso(f'Bem-vindo de volta, {usuario["nome_completo"].title()}!')
            return usuario
        else:
            erro('Senha incorreta. Tente novamente.')

# Cadastro de usuário
def user_cadastro(usuarios):
    while True:
        nome = pedir_input('Digite seu nome de usuário (4 a 12 caracteres): ')
        if usuario_existe(nome, usuarios):
            erro('Usuário já cadastrado. Tente outro nome.')
            continue
        if 4 <= len(nome) <= 12:
            break
        else:
            erro('O nome deve ter entre 4 e 12 caracteres.')

    while True:
        senha = pedir_input('Digite sua senha (6 a 12 caracteres): ')
        if 6 <= len(senha) <= 12:
            break
        else:
            erro('A senha deve ter entre 6 e 12 caracteres.')

    nome_completo = pedir_input('Informe seu nome completo: ')

    sucesso(f'Usuário {nome} cadastrado com sucesso!')

    return {'nome': nome, 'senha': senha, 'nome_completo': nome_completo}

# Menu
def menu():
    print(50 * '-=-')
    print('\033[36mO que deseja fazer?\n(C)adastrar / (E)ditar / (A)pagar / (V)isualizar / (S)air\033[m')
    return input('Escolha uma opção: ').strip().upper()

# Base do programa
def main():
    usuarios = []
    atividades = []

    print('\033[32mBem-vindo ao Gerenciador de Tarefas!\033[m')

    # Entrada para Login ou Cadastro inicial
    while True:
        opcao = input('Você já é cadastrado? (S)im / (N)ão / SAIR: \n').strip().upper()
        if opcao == 'SAIR':
            sucesso('Encerrando serviço de atividades.')
            sys.exit()
        elif opcao == 'S':
            usuario_logado = user_login(usuarios)
            break
        elif opcao == 'N':
            novo_usuario = user_cadastro(usuarios)
            usuarios.append(novo_usuario)
        else:
            erro('Opção inválida. Tente novamente.')

    # Loop de atividades
    while True:
        opcao = menu()
        # Sair
        if opcao == 'S':
            sucesso('Encerrando serviço de atividades.')
            exibir_atividades(atividades)
            break
        
        # Cadastro
        elif opcao == 'C':
            print('\033[36mCadastro de Atividades\033[m')
            separador()
            nome_atividade = pedir_input('Nome da atividade: ')
            descricao = pedir_input('Descrição da atividade: ')

            while True:
                inicio_str = pedir_input('Prazo inicial [dd/mm/aaaa]: ')
                inicio = converter_data(inicio_str)
                if inicio:
                    break
                erro('Data inválida. Use o formato dd/mm/aaaa.')

            while True:
                fim_str = pedir_input('Prazo final [dd/mm/aaaa]: ')
                fim = converter_data(fim_str)
                if fim and fim >= inicio:
                    break
                erro('Data inválida ou menor que o prazo inicial.')

            mostrar_painel_prioridade()
            prioridade = pedir_numero('Digite a prioridade (1-3): ', 1, 3)

            atividade = {
                'id': len(atividades) + 1,
                'nome': nome_atividade,
                'descricao': descricao,
                'inicio': inicio,
                'fim': fim,
                'prioridade': prioridade
            }
            atividades.append(atividade)
            sucesso(f'Atividade "{nome_atividade}" cadastrada com sucesso!')

        # Edição
        elif opcao == 'E':
            if not atividades:
                erro('Não há atividades para editar.')
                continue
            exibir_atividades(atividades)
            indice = pedir_numero('Digite o número da atividade que deseja editar: ', 1, len(atividades)) - 1
            atividade = atividades[indice]

            while True:
                print("\033[36mO que deseja editar?\033[m")
                print("1 - Nome\n2 - Descrição\n3 - Prazo inicial\n4 - Prazo final\n5 - Prioridade\n6 - Editar tudo\n0 - Cancelar")
                escolha = pedir_numero("Escolha uma opção: ", 0, 6)

                if escolha == 0:
                    sucesso("Edição cancelada.")
                    break
                elif escolha == 1:
                    atividade['nome'] = pedir_input("Novo nome da atividade: ")
                    sucesso("Nome atualizado com sucesso!")
                elif escolha == 2:
                    atividade['descricao'] = pedir_input("Nova descrição: ")
                    sucesso("Descrição atualizada com sucesso!")
                elif escolha == 3:
                    while True:
                        inicio_str = pedir_input("Novo prazo inicial [dd/mm/aaaa]: ")
                        inicio = converter_data(inicio_str)
                        if inicio:
                            atividade['inicio'] = inicio
                            sucesso("Prazo inicial atualizado com sucesso!")
                            break
                        erro("Data inválida. Use o formato dd/mm/aaaa.")
                elif escolha == 4:
                    while True:
                        fim_str = pedir_input("Novo prazo final [dd/mm/aaaa]: ")
                        fim = converter_data(fim_str)
                        if fim and fim >= atividade['inicio']:
                            atividade['fim'] = fim
                            sucesso("Prazo final atualizado com sucesso!")
                            break
                    erro("Data inválida ou menor que o prazo inicial.")
                elif escolha == 5:
                    mostrar_painel_prioridade()
                    atividade['prioridade'] = pedir_numero("Nova prioridade (1-3): ", 1, 3)
                    sucesso("Prioridade atualizada com sucesso!")
                elif escolha == 6:
                    atividade['nome'] = pedir_input("Novo nome da atividade: ")
                    atividade['descricao'] = pedir_input("Nova descrição: ")
                    while True:
                        inicio_str = pedir_input("Novo prazo inicial [dd/mm/aaaa]: ")
                        inicio = converter_data(inicio_str)
                        if inicio:
                            atividade['inicio'] = inicio
                            break
                    erro("Data inválida. Use o formato dd/mm/aaaa.")
                    while True:
                        fim_str = pedir_input("Novo prazo final [dd/mm/aaaa]: ")
                        fim = converter_data(fim_str)
                        if fim and fim >= atividade['inicio']:
                            atividade['fim'] = fim
                            break
                        erro("Data inválida ou menor que o prazo inicial.")

            sucesso("Atividade editada com sucesso!")
            break
        
        # Apagar atividades
        elif opcao == 'A':
            if not atividades:
                erro('Não há atividades para apagar.')
                continue
            exibir_atividades(atividades)
            indice = pedir_numero('Digite o número da atividade que deseja apagar: ', 1, len(atividades)) - 1
            atividades.pop(indice)
            sucesso('Atividade apagada com sucesso.')

        # Visualizar atividades
        elif opcao == 'V':
            if not atividades:
                erro('Não há atividades para visualizar.')
                continue
            # Exibe em ordem de prioridade
            atividades_ordenadas = sorted(atividades, key=lambda x: x['prioridade'])
            exibir_atividades(atividades_ordenadas)

        else:
            erro('Opção inválida.')

main()
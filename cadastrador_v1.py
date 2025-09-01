import datetime

print('\033[32mBem-vindo ao cadastro de atividades\033[m')
print(52 * '-=-')

# Validação da data do usuário
def data_valida(dia, mes, ano):
    if mes < 1 or mes > 12:
        return False
    if mes in (1, 3, 5, 7, 8, 10, 12) and dia > 31:
        return False
    if mes in (4, 6, 9, 11) and dia > 30:
        return False
    if mes == 2:
        if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
            return dia <= 29
        return dia <= 28
    return True

# Verifica se a data está no prazo
def data_no_prazo(dia, mes, ano):
    data_atual = datetime.datetime.now()
    data_inserida = datetime.datetime(ano, mes, dia)
    return data_inserida >= data_atual

# Função para login do usuário
def user_login(usuarios):
    nome = input('\033[36mDigite seu nome de usuário: \033[m')
    senha = input('\033[36mDigite sua senha: \033[m')
    for usuario in usuarios:
        if usuario['nome'] == nome and usuario['senha'] == senha:
            print(f'\033[32mBem-vindo de volta, {usuario["nome_completo"].title()}!\n\033[m')
            print(52 * '-=-')
            return True, usuario['nome_completo']
    print('\033[31mUsuário ou senha incorretos.\033[m')
    print(52 * '-=-')
    return False, None

# Função para cadastro do usuário
def user_cadastro(usuarios): 
    while True:
        nome = input('\033[36mDigite seu nome para cadastro (4 a 12 caracteres): \033[m')
        if any(usuario['nome'] == nome for usuario in usuarios):
            print('\033[31mERRO: Usuário já cadastrado. Tente outro nome.\033[m')
            print(52 * '-=-')
            continue
            
        if 4 <= len(nome) <= 12:
            break
        else:
            print('\033[31mO nome deve ter entre 4 e 12 caracteres. Tente novamente.\033[m')
            print(52 * '-=-')

    while True:
        senha = input('\033[36mDigite uma senha (6 a 12 caracteres):\033[m ')
        if 6 <= len(senha) <= 12:
            break
        else:
            print('\033[31mA senha deve ter entre 6 e 12 caracteres. Tente novamente.\033[m')
            print(52 * '-=-')
    
    while True:
        nome_completo = input('\033[36mInforme seu nome completo: \033[m')
        
        # Verificar se nome_completo não está vazio e não contém números
        if not nome_completo:
            print('\033[31mO nome completo não pode ser vazio. Tente novamente.\033[m')
        elif any(char.isdigit() for char in nome_completo):
            print('\033[31mO nome completo não pode conter números. Tente novamente.\033[m')
        else:
            break
    
    dados = {
        'nome': nome,
        'senha': senha,
        'nome_completo': nome_completo
    }
    print(f'\033[32mUsuário {nome} com senha cadastrada! \n\033[m')
    print(52 * '-=-')
    return dados

def converter_string_hora_para_hora_minuto(hora_minuto):
    partes = hora_minuto.split(':')
    if len(partes) == 1:
        hora = int(partes[0])
        minutos = 0
    elif len(partes) == 2:
        hora = int(partes[0])
        minutos = int(partes[1])
    return hora, minutos 

# Função para converter a string da data em inteiros
def converter_data(data_str):
    if len(data_str) != 10 or data_str[2] != '/' or data_str[5] != '/':
        return None, None, None
    try:
        dia, mes, ano = map(int, data_str.split('/'))
        return dia, mes, ano
    except ValueError:
        return None, None, None  


def formatar_data(dia, mes, ano):
    return f'{dia:02}/{mes:02}/{ano}'

# Função para mostrar painel de prioridade
def mostrar_painel_prioridade():
    print(52 * '-=-')
    print('\033[36mEscolha a prioridade da atividade:\033[m')
    print('\033[35m1 - Prioridade Alta\n'
          '2 - Prioridade Média\n'
          '3 - Prioridade Baixa\033[m')

# Função principal
def main():
    usuarios = []
    while True:
        opcao = input('\033[36mVocê já é um usuário cadastrado? (S)im / (N)ão: \033[m').upper()
        if opcao == 'S':
            usuario_logado, nome_completo = user_login(usuarios)
            if usuario_logado:
                break
        elif opcao == 'N':
            novo_usuario = user_cadastro(usuarios)  
            usuarios.append(novo_usuario)
        else:
            print('\033[31mOpção inválida. Tente novamente.\033[m')
            print(52 * '-=-')

    atividades = []
    while True:
            pergunta = input('\033[32mO que deseja fazer? (C)adastrar / (E)ditar / (A)pagar / (V)isualizar / (S)air: \033[m').upper().strip()
            print(52 * '-=-')  
            if pergunta not in 'CEAVS':
                print('\033[31mATENÇÃO.Informe apenas (C)adastrar / (E)ditar / (A)pagar / (V)isualizar / (S)air:\033[m ')
                continue
            
            # Sair/Encerrar o programa
            if pergunta == 'S':
                print('\033[32mEncerrando serviço de atividades.\033[m')
                print('\033[36mAtividades cadastradas em ordem de prioridade:\033[m')
                for i, atividade in enumerate(atividades_ordenadas, start=1):
                    print(f'\033[33mAtividade Nº {i}\033[m.\n'
                        f'\033[36mAtividade:\033[m \033[33m{atividade['nome']}\033[m\n'
                        f'\033[36mPeríodo da Atividade:\033[m \033[33mDas {atividade['horário']} à {atividade['prazo']}\033[m\n'  # Exibe "Das 16:00 à 17:00"
                        f'\033[36mPrazo:\033[m \033[33mDe {formatar_data(dia, mes, ano)} à {formatar_data(dia_fim, mes_fim, ano_fim)}\033[m\n'
                        f'\033[36mDesc:\033[m \033[33m{atividade['descrição']}\033[m\n'
                        f'\033[36mPrioridade:\033[m \033[33m{atividade['prioridade']}\033[m')

                    print(52 * '-=-')
                print(52 * '-=-')
                break
            
            # Visualizar atividades
            elif pergunta == 'V':
                if not atividades:
                    print('\033[31mNão há atividades cadastradas para Visualizar.\033[m')
                    continue
                print('\033[0;36mAtividades cadastradas em ordem de prioridade:\033[m')
                for i, atividade in enumerate(atividades_ordenadas, start=1):
                    print(f'\033[33mAtividade Nº {i}\033[m.\n'
                        f'\033[36mAtividade:\033[m \033[33m{atividade['nome']}\033[m\n'
                        f'\033[36mPeríodo da Atividade:\033[m \033[33mDas {atividade['horário']} à {atividade['prazo']}\033[m\n'  # Exibe "Das 16:00 à 17:00"
                        f'\033[36mPrazo:\033[m \033[33mDe {formatar_data(dia, mes, ano)} à {formatar_data(dia_fim, mes_fim, ano_fim)}\033[m\n'
                        f'\033[36mDesc:\033[m \033[33m{atividade['descrição']}\033[m\n'
                        f'\033[36mPrioridade:\033[m \033[33m{atividade['prioridade']}\033[m')
                    print(52 * '-=-')   
                
            # Apagar atividade   
            elif pergunta == 'A':
                if not atividades:
                    print('\033[31mNão há atividades cadastradas para Apagar.\033[m')
                    continue
                print('\033[0;36mAtividades cadastradas:\033[m')
                for i, atividade in enumerate(atividades_ordenadas, start=1):
                    print(f'\033[33mAtividade Nº {i}\033[m.\n'
                        f'\033[36mAtividade:\033[m \033[33m{atividade["nome"]}\033[m\n'
                        f'\033[36mPeríodo da Atividade:\033[m \033[33mDas {atividade["horário"]} à {atividade["prazo"]}\033[m\n' 
                        f'\033[36mPrazo:\033[m \033[33mDe {formatar_data(dia, mes, ano)} à {formatar_data(dia_fim, mes_fim, ano_fim)}\033[m\n'
                        f'\033[36mDesc:\033[m \033[33m{atividade["descrição"]}\033[m\n'
                        f'\033[36mPrioridade:\033[m \033[33m{atividade["prioridade"]}\033[m')
                    print(52 * '-=-')

                print(52 * '-=-')
                while True:
                    entrada = input('\033[36mDigite o número da atividade que deseja Apagar (para cancelar, digite F): \033[m')
                    
                    if entrada.upper() == 'F':  
                        print('\033[32mOperação cancelada pelo usuário.\033[m')
                        break
                    try:
                        indice = int(entrada) - 1  
                        if 0 <= indice < len(atividades):
                            atividades.pop(indice)
                            print('\033[32mAtividade apagada com sucesso.\033[m')
                            print(52 * '-=-') 
                            break
                        else:
                            print('\033[31mÍndice inválido. Nenhuma atividade foi apagada.\033[m')
                    except ValueError:
                        print('\033[31mEntrada inválida. Por favor, digite um número válido ou F para cancelar.\033[m')

       
            elif pergunta == 'E':
                while True:
                    try:
                        if not atividades:
                            print('\033[31mNão há atividades cadastradas para editar.\033[m')
                            continue

                        # Exibir atividades cadastradas
                        print('\033[0;36mAtividades cadastradas:\033[m')
                        for i, atividade in enumerate(atividades_ordenadas, start=1):
                            print(f'\033[33mAtividade Nº {i}\033[m.\n'
                                f'\033[36mAtividade:\033[m \033[33m{atividade["nome"]}\033[m\n'
                                f'\033[36mPeríodo da Atividade:\033[m \033[33mDas {atividade["horário"]} à {atividade["prazo"]}\033[m\n'
                                f'\033[36mPrazo:\033[m \033[33mDe {formatar_data(dia, mes, ano)} à {formatar_data(dia_fim, mes_fim, ano_fim)}\033[m\n'
                                f'\033[36mDesc:\033[m \033[33m{atividade["descrição"]}\033[m\n'
                                f'\033[36mPrioridade:\033[m \033[33m{atividade["prioridade"]}\033[m')
                            print(52 * '-=-')

                        # Solicitar a escolha da atividade
                        while True:
                            entrada = input('\033[36mDigite o número da atividade que deseja Editar (para cancelar, digite F):\033[m ').strip()

                            if entrada.upper() == 'F':  # Se o usuário digitar 'F', cancela
                                print('\033[32mEncerrando edição de atividades.\033[m')
                                break

                            try:
                                indice = int(entrada) - 1  # Convertendo a entrada para índice
                                if 0 <= indice < len(atividades_ordenadas):
                                    atividade = atividades_ordenadas[indice]
                                    print(f'\033[32mEditando a atividade: {atividade["nome"]}\033[m')
                                    break  # Se o índice for válido, sai do loop
                                else:
                                    print('\033[31mÍndice inválido. Tente novamente.\033[m')
                            except ValueError:
                                print('\033[31mValor inválido. Por favor, insira um número válido ou "F" para cancelar.\033[m')

                        if entrada.upper() == 'F':  # Verifica se a edição foi cancelada
                            break

                        # Editar o nome da atividade
                        while True:
                            try:
                                novo_nome = input(f'\033[0;35mNovo nome da atividade (atual: {atividade["nome"]}): \033[m').strip()
                                if novo_nome:  
                                    atividade['nome'] = novo_nome
                                    break
                                else:
                                    print('\033[31mO nome da atividade não pode ser vazio. Tente novamente.\033[m')
                            except:
                                print('\033[31mErro ao editar o nome. Tente novamente.\033[m')

                        # Editar a descrição da atividade
                        while True:
                            try:
                                nova_descricao = input(f'\033[35mNova descrição da atividade (atual: {atividade["descrição"]}): \033[m').strip()
                                if nova_descricao:
                                    atividade['descrição'] = nova_descricao
                                    break
                                else:
                                    print('\033[31mA descrição da atividade não pode ser vazia. Tente novamente.\033[m')
                            except:
                                print('\033[31mErro ao editar a descrição. Tente novamente.\033[m')

                        # Editar o prazo inicial
                        while True:
                            try:
                                novo_inicio = input(f'\033[35mNovo prazo inicial (atual: {atividade["inicio"]}): \033[m')
                                dia, mes, ano = converter_data(novo_inicio)
                                if dia and mes and ano and data_valida(dia, mes, ano) and data_no_prazo(dia, mes, ano):
                                    atividade['inicio'] = novo_inicio
                                    break
                                else:
                                    print('\033[31mData inválida. Tente novamente.\033[m')
                            except:
                                print('\033[31mErro ao editar o prazo inicial. Tente novamente.\033[m')

                        # Editar o prazo final
                        while True:
                            try:
                                novo_fim = input(f'\033[35mNovo prazo final (atual: {atividade["fim"]}): \033[m')
                                dia_fim, mes_fim, ano_fim = converter_data(novo_fim)
                                if dia_fim and mes_fim and ano_fim and data_valida(dia_fim, mes_fim, ano_fim) and data_no_prazo(dia_fim, mes_fim, ano_fim):
                                    if (ano_fim, mes_fim, dia_fim) >= (dia, mes, ano):  # Verifica se a data final não é anterior à inicial
                                        atividade["fim"] = novo_fim
                                        break
                                    else:
                                        print('\033[31mA data final não pode ser anterior à data inicial. Tente novamente.\033[m')
                                else:
                                    print('\033[31mData inválida. Tente novamente.\033[m')
                            except:
                                print('\033[31mErro ao editar o prazo final. Tente novamente.\033[m')

                        # Editar o horário
                        while True:
                            try:
                                # Verificar se o horário está em formato string e converter para minutos
                                if isinstance(atividade["horário"], str):
                                    horario_atual = converter_para_minutos(atividade["horário"])
                                else:
                                    horario_atual = atividade["horário"]  # Caso já esteja em minutos
                                
                                hora = horario_atual // 60  # Calcula as horas
                                minutos = horario_atual % 60  # Calcula os minutos restantes

                                # Exibir o horário no formato correto
                                novo_horario = input(f'\033[35mNova hora de início (atual: {hora:02}:{minutos:02}): \033[m')

                                # Usar a função de conversão para minutos
                                minutos_inicio = converter_para_minutos(novo_horario)

                                
                                if minutos_inicio is not None and 0 <= minutos_inicio <= 1440:  
                                    atividade['horário'] = novo_horario  
                                    break
                                else:
                                    print('\033[31mPor favor, insira um horário válido no formato HH:MM (entre 00:00 e 24:00).\033[m')

                            except ValueError:
                                print('\033[31mEntrada inválida. Tente novamente.\033[m')

                        # Editar o prazo de horas
                       
                        while True:
                            try:
                                hora_atual, minutos_atual = converter_string_hora_para_hora_minuto(atividade["horário"]) # 12:33
                                novo_prazo = input(f'\033[35mInforme o novo prazo de horas a partir das {hora_atual:02}:{minutos_atual:02} horas: \033[m')

                                prazo_minutos = converter_para_minutos(novo_prazo)
                                prazo_minutos_atividade = converter_para_minutos(atividade['horário'])

                                if prazo_minutos is not None and prazo_minutos > prazo_minutos_atividade:
                                    atividade['prazo'] = novo_prazo  
                                    break
                                else:
                                    print(f'\033[31mO prazo de horas deve ser maior que a hora inicial ({hora_atual:02}:{minutos_atual:02}) e entre 0 e 24 horas. Tente novamente.\033[m')

                            except ValueError:
                                print('\033[31mEntrada inválida. Por favor, insira um número válido.\033[m')

                        # Editar a prioridade
                        mostrar_painel_prioridade()
                        while True:
                            try:
                                nova_prioridade = int(input('\033[36mInforme a prioridade da atividade (1 - Alta, 2 - Média, 3 - Baixa): \033[m'))  
                                if nova_prioridade in (1, 2, 3):
                                    prioridade_texto = 'Alta' if nova_prioridade == 1 else 'Média' if nova_prioridade == 2 else 'Baixa'
                                    atividade['prioridade'] = prioridade_texto
                                    break
                                else:
                                    print('\033[31mPrioridade inválida. Insira um valor entre 1 e 3.\033[m')
                            except ValueError:
                                print('\033[31mPor favor, insira um número válido.\033[m')

                        print(f'\033[32mAtividade editada com sucesso!\033[m')
                        break
                    except ValueError:
                        print('\033[31mPor favor, insira um número válido.\033[m')
              
            elif pergunta == 'C':
                try:
                    while True:
                        atividade = input('\033[35mNome da atividade:\033[m ')
                        if atividade.strip() == "":  # Verifica se o nome da atividade está vazio
                            print('\033[31mO nome da atividade não pode ser vazio. Tente novamente.\033[m')
                            print(52 * '-=-')
                        else:
                            break

                    while True:
                        descreva = input('\033[35mDescreva sua atividade:\033[m ')
                        if descreva.strip() == "":  # Verifica se a descrição está vazia
                            print('\033[31mA descrição da atividade não pode ser vazia. Tente novamente.\033[m')
                            print(52 * '-=-')
                        else:
                            break

                except ValueError:
                    print('\033[31mPor favor, não deixe os dados vazios. Tente novamente.\033[m')

                while True:
                    inicial = input('\033[35mQual seu prazo inicial [dd/mm/aaaa]?\033[m ')
                    dia, mes, ano = converter_data(inicial)
                    if dia and mes and ano and data_valida(dia, mes, ano) and data_no_prazo(dia, mes, ano):
                        break
                    else:
                        print('\033[31mData inválida ou fora do prazo. Tente novamente.\033[m')

                while True:
                    final = input('\033[35mQual seu prazo final [dd/mm/aaaa]?\033[m ')
                    dia_fim, mes_fim, ano_fim = converter_data(final)
                    if dia_fim and mes_fim and ano_fim and data_valida(dia_fim, mes_fim, ano_fim) and data_no_prazo(dia_fim, mes_fim, ano_fim):
                        if (ano_fim, mes_fim, dia_fim) >= (ano, mes, dia):  # Verifica se a data final não é anterior à inicial
                            break
                        else:
                            print('\033[31mA data final não pode ser anterior à data inicial. Tente novamente.\033[m')
                    else:
                        print('\033[31mData inválida ou fora do prazo. Tente novamente.\033[m')

                # Função para converter horário
                def converter_para_minutos(hora_str):
                    try:
                        partes = hora_str.split(':')
                        if len(partes) == 1:
                            hora = int(partes[0])
                            minutos = 0
                        elif len(partes) == 2:
                            hora = int(partes[0])
                            minutos = int(partes[1])
                        else:
                            return None  

                        if 0 <= hora <= 24 and 0 <= minutos < 60:
                            return hora * 60 + minutos  
                        else:
                            return None  
                    except ValueError:
                        return None  

                while True:
                    try:
                        hora_inicial_str = input('\033[35mQual Período da Atividade(\033[33m0h\033[m \033[35ma\033[m \033[33m24h\033[m  \033[35m+\033[m \033[33minutos\033[m \033[35m)?\033[m ')
                        hora_inicial = converter_para_minutos(hora_inicial_str)
                        if hora_inicial is not None:
                            break
                        else:
                            print('\033[31mPor favor, insira um horário válido (formato HH ou HH:MM).\033[m')
                    except ValueError:
                        print('\033[31mPor favor, insira um número válido.\033[m')

                while True:
                    try:
                        prazo_str = input(f'\033[35mInforme o prazo de horas a partir de \033[33m{hora_inicial_str}\033[m:\033[m ')
                        prazo = converter_para_minutos(prazo_str)
                        if prazo is not None and prazo > hora_inicial:
                            break
                        else:
                            print(f'\033[31mO prazo de horas deve ser maior que a hora inicial ({hora_inicial_str}) e entre 0 e 24 horas. Tente novamente.\033[m')
                    except ValueError:
                        print('\033[31mEntrada inválida. Por favor, insira um número válido.\033[m')

                hora_inicial_display = f'{hora_inicial // 60:02}:{hora_inicial % 60:02}'
                prazo_display = f'{prazo // 60:02}:{prazo % 60:02}'

                mostrar_painel_prioridade()
                print(52 * '-=-')
                while True:
                    try:
                        prioridade = int(input('\033[36mInforme a prioridade da atividade: \033[m'))  
                        if prioridade in (1, 2, 3):
                            if prioridade == 1:
                                prioridade = 'Alta'
                                break
                            elif prioridade == 2:
                                prioridade = 'Média'
                                break
                            else:
                                prioridade = 'Baixa'
                                break
                        else:
                            print('\033[31mPrioridade inválida. Insira um valor entre 1 e 3.\033[m')
                    except ValueError:
                        print('\033[31mPor favor, insira um número válido.\033[m')
                    print(52 * '-=-')

                atividade_cadastro = {
                'nome': atividade,
                'descrição': descreva,
                'inicio': inicial,
                'fim': final,
                'horário': hora_inicial_str,
                'prazo': prazo_str,
                'prioridade': prioridade
                }
                atividades.append(atividade_cadastro)
                print(f'\033[32mAtividade {atividade} cadastrada, com início {inicial} das {hora_inicial_str} horas às {prazo_str} horas, e prazo final para {final}. Descrição: {descreva}. Prioridade: {prioridade}\n\033[m')
            
                atividades_ordenadas = sorted(atividades, key=lambda x: x['prioridade'])
                print(52 * '-=-')

main()
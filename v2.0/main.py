import os
from datetime import date

LIMITE_QTDE_SAQUE = 3
LIMITE_VALOR_SAQUE = 500
BANCO_VERSAO = "Banco v2.0"
AGENCIA = 1500


def obtem_opcao_menu(incial, final):
    try:
        valor_convertido = campo_numerico("Menu ")
        if valor_convertido == 0:
            return 0
        elif valor_convertido >= incial and valor_convertido <= final:
            return valor_convertido
        else:
            raise TypeError("Opção inválida.")
    except TypeError as e:
        print(f"Alerta: {e}")
        return obtem_opcao_menu(incial, final)


def campo_texto(label):
    valor = input(f"{label}")
    if valor.strip() == "":
        print(f"Alerta: Valor inválido.")
        return campo_texto(label)

    return valor


def campo_numerico(label):
    try:
        return int(input(f"{label}"))
    except ValueError:
        print(f"Alerta: Valor inválido.")
        return campo_numerico(label)


def campo_float(label):
    try:
        return float(input(f"{label}"))
    except ValueError:
        print(f"Alerta: Valor inválido.")
        return campo_float(label)


def deposito(saldo, transacoes):
    print('=' * 100)
    print(f"""
          {BANCO_VERSAO}
            -> Opção selecionada Depósito
            Saldo em conta R$ {saldo:.2f}.
        """)
    print('=' * 100)
    valor = campo_float('Informe o valor para depósito: ')
    if valor > 0:
        transacao = {'operacao': 'deposito',
                     'valor': valor, 'data': date.today()}
        transacoes.append(transacao)
        saldo += valor
        print(f"Depósito no valor de R$ {valor:.2f} efetuado com sucesso.")
    return saldo, transacoes


def saque(saldo, transacoes, contador_saque):
    print('=' * 100)
    print(f"""
          {BANCO_VERSAO}
            -> Opção selecionada Saque
            Saldo em conta R$ {saldo:.2f}.
            """)
    print('=' * 100)

    if contador_saque < LIMITE_QTDE_SAQUE:
        valor = campo_float('Informe o valor para saque: ')
        total_saque_diario = sum(x['valor']
                                 for x in transacoes if x['data'] == date.today()
                                 and x['operacao'].lower() == 'saque') + valor

        if total_saque_diario > LIMITE_VALOR_SAQUE:
            print(
                f'Limite diário do saque ultrapassou o valor de R$ {LIMITE_VALOR_SAQUE}')

        elif valor > saldo:
            print(
                f'Não é possível sacar o valor R$ {valor:.2f}, saldo insuficiente {saldo:.2f}.')

        elif valor > 0:
            transacao = {'operacao': 'saque',
                         'valor': valor, 'data': date.today()}
            transacoes.append(transacao)

            contador_saque = sum(1 for x in transacoes if x['data'] == date.today(
            ) and x['operacao'].lower() == 'saque')

            saldo -= valor
            print(f"Saque no valor de R$ {valor:.2f} efetuado com sucesso.")
    else:
        print(f"Limite de saque excedido {contador_saque}")

    return saldo, transacoes, contador_saque


def extrato(saldo, transacoes):
    print('=' * 100)
    print(f"""
          {BANCO_VERSAO}
            -> Opção selecionada Extrato
        """)
    print('=' * 100)

    if len(transacoes) == 0:
        print(f"Saldo em conta R$ 0.")
    else:
        for transacao in transacoes:
            cor = '\033[31m' if transacao['operacao'].lower(
            ) == 'saque' else '\033[32m'

            linha = f"""{cor}
                Operação: {transacao['operacao']}
                Valor: {transacao['valor']:.2f}
                Data: {transacao['data']}
                \033[0;0m"""
            print(linha)
            print('-' * 100)

    print(f"Saldo em conta R$ {saldo:.2f}.")


def gerar_numero_conta(contas):
    return len(contas) + 1


def nova_conta(clientes, contas):
    cpf = campo_texto('Informe o CPF: ')
    cliente = busca_cliente(cpf, clientes)

    numero_conta = gerar_numero_conta(contas)

    if cliente:
        print('Conta criada com sucesso!')
        return {'agencia': AGENCIA, 'numero_conta': numero_conta, 'cliente': cliente}

    print('Usuário não encontrado. Criação de conta encerrada!')


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência: {conta['agencia']}
            C/C: {conta['numero_conta']}
            Titular: {conta['cliente']['nome']}
         """

        print('-' * 100)
        print(linha)


def busca_cliente(cpf, clientes):
    busca = [cliente for cliente in clientes if cliente['cpf'] == cpf]

    return busca[0] if busca else None


def novo_cliente(clientes):

    cpf = campo_texto('Informe o CPF: ')

    valida = busca_cliente(cpf, clientes)

    if valida:
        print('CPF já cadastrado.')
        return

    nome = campo_texto('Informe o nome do cliente: ')
    data_nascimento = campo_texto(
        'Informe a data de nascimento (dd-mm-aaaa): ')

    print('Endereço')
    rua = campo_texto('Informe o nome da rua: ')
    numero = campo_texto('Informe o número da casa: ')
    bairro = campo_texto('Informe o nome do bairro: ')
    cidade = campo_texto('Informe o nome da cidade: ')
    estado = campo_texto('Informe o nome do estado: ')

    endereco = f"{rua} - {numero} - {bairro} - {cidade} - {estado}"

    cliente = {'nome': nome, 'data_nascimento': data_nascimento,
               'cpf': cpf, 'endereco': endereco}

    clientes.append(cliente)

    print(f'Cliente {nome} cadastrado com sucesso.')

    return clientes


def main():

    saldo = 0
    transacoes = []
    contador_saque = 0

    clientes = []
    contas = []

    while True:
        print('=' * 100)
        print(f"""
              {BANCO_VERSAO}
                1 - Depósito
                2 - Sacar
                3 - Extrato
                4 - Nova Conta
                5 - Listar Contas
                6 - Novo Usuário
                7 - Finalizar Operação
            """)
        print('=' * 100)

        menu = obtem_opcao_menu(1, 7)

        if menu == 1:
            saldo, transacoes = deposito(saldo, transacoes)
        elif menu == 2:
            saldo, transacoes, contador_saque = saque(
                saldo, transacoes, contador_saque)
        elif menu == 3:
            extrato(saldo, transacoes)
        elif menu == 4:
            conta = nova_conta(clientes, contas)
            if conta:
                contas.append(conta)
        elif menu == 5:
            listar_contas(contas)
        elif menu == 6:
            clientes = novo_cliente(clientes)
        elif menu == 7:
            print("Saindo do programa.")
            break


main()

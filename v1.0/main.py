from datetime import date

extratos = []
saldo = 0
contador_saque = 0

LIMITE_QTDE_SAQUE = 3
LIMITE_VALOR_SAQUE = 500

while True:
    print('=' * 100)
    print("""
          Banco v1.0
          1 - Depósito
          2 - Saque
          3 - Extrato
          4 - Finalizar Operação
          """)
    print('=' * 100)

    try:
        menu = int(input())
    except ValueError:
        print("Opção inválida.")

    if menu == 1:
        print('=' * 100)
        print(f"""
              Banco v1.0
                -> Opção selecionada Depósito
                Saldo em conta R$ {saldo:.2f}.
              """)
        print('=' * 100)

        try:
            valor = float(input('Informe o valor para depósito: '))
            if valor > 0:
                extrato = {'operacao': 'deposito',
                           'valor': valor, 'data': date.today()}
                extratos.append(extrato)
                saldo += valor
                print(
                    f"Depósito no valor de R$ {valor:.2f} efetuado com sucesso.")
        except ValueError:
            print("Informe apenas valores númericos.")

    elif menu == 2:
        print('=' * 100)
        print(f"""
              Banco v1.0
                -> Opção selecionada Saque
                Saldo em conta R$ {saldo:.2f}.
              """)
        print('=' * 100)

        if contador_saque < LIMITE_QTDE_SAQUE:
            try:
                valor = float(input('Informe o valor para saque: '))

                total_saque_diario = sum(
                    x['valor'] for x in extratos if x['data'] == date.today() and x['operacao'].lower() == 'saque') + valor

                if total_saque_diario > LIMITE_VALOR_SAQUE:
                    print(
                        f'Limite diário do saque ultrapassou o valor de R$ {LIMITE_VALOR_SAQUE}')
                elif valor > saldo:
                    print(
                        f'Não é possível sacar o valor R$ {valor:.2f}, saldo insuficiente {saldo:.2f}.')

                elif valor > 0:

                    extrato = {'operacao': 'saque',
                               'valor': valor, 'data': date.today()}
                    extratos.append(extrato)

                    contador_saque = sum(
                        1 for x in extratos if x['data'] == date.today() and x['operacao'].lower() == 'saque')

                    for extrato in extratos:

                        linha = f"""
                        Operação: {extrato['operacao']}
                        Valor: {extrato['valor']:.2f}
                        Data: {extrato['data']}
                        """
                        print('-' * 100)
                        print(linha)
                        print('-' * 100)

                    saldo -= valor
                    print(
                        f"Saque no valor de R$ {valor:.2f} efetuado com sucesso.")
            except ValueError:
                print("Informe apenas valores númericos.")
        else:
            print(
                f"Limite de saque excedido {contador_saque}")

    elif menu == 3:
        print('=' * 100)
        print("""
              Banco v1.0
                -> Opção selecionada Extrato
              """)
        print('=' * 100)

        if len(extratos) == 0:
            print(f"Saldo em conta R$ {saldo:.2f}.")
            break

        for extrato in extratos:

            linha = f"""
            Operação: {extrato['operacao']}
            Valor: {extrato['valor']:.2f}
            Data: {extrato['data']}
            """
            print('-' * 100)
            print(linha)
        print('-' * 100)
        print(f"Saldo em conta R$ {saldo:.2f}.")
    elif menu == 4:
        print("Saindo do programa.")
        break
    else:
        print("Opção inválida.")

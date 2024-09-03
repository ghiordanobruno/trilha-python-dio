import textwrap

def menu():
    return """
    [c] Cadastrar Usuário
    [a] Cadastrar Conta
    [l] Login
    [q] Sair
    => """

def menu_logado():
    return """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [l] Logout
    => """

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    cpf = input("CPF (somente números): ")
    endereco = input("Endereço (logradouro, número - bairro - cidade/sigla estado): ")

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Usuário já cadastrado!")
            return usuarios

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário cadastrado com sucesso!")
    return usuarios

def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        numero_conta += 1
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    else:
        print("Usuário não encontrado!")
        return None

def listar_contas(contas):
    for conta in contas:
        print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Usuário: {conta['usuario']['nome']}")

def main():
    usuarios = []
    contas = []
    saldo = 0
    limite = 500
    extrato_str = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuario_logado = None
    numero_conta = 0
    agencia = "0001"

    while True:
        if usuario_logado:
            opcao = input(menu_logado())
            if opcao == "d":
                valor = float(input("Informe o valor: "))
                saldo, extrato_str = depositar(saldo, valor, extrato_str)
            elif opcao == "s":
                valor = float(input("Informe o valor: "))
                saldo, extrato_str = sacar(saldo=saldo, valor=valor, extrato=extrato_str, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
            elif opcao == "e":
                exibir_extrato(saldo, extrato=extrato_str)
            elif opcao == "l":
                usuario_logado = None
                print("Logout realizado com sucesso!")
            else:
                print("Opção inválida!")
        else:
            opcao = input(menu())
            if opcao == "c":
                usuarios = criar_usuario(usuarios)
            elif opcao == "a":
                conta = criar_conta(agencia, numero_conta, usuarios)
                if conta:
                    contas.append(conta)
                    numero_conta += 1
                    print("Conta cadastrada com sucesso!")
            elif opcao == "l":
                cpf = input("Informe seu CPF (somente números): ")
                usuario_logado = filtrar_usuario(cpf, usuarios)
                if usuario_logado:
                    print(f"Bem-vindo(a), {usuario_logado['nome']}!")
                else:
                    print("Usuário não encontrado!")
            elif opcao == "q":
                break
            else:
                print("Opção inválida!")

main()

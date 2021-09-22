import mysql.connector
from random import randint, choice
from time import sleep

from mysql.connector.cursor import MySQLCursorDict
chave = ''
breakFlag = ''

meubd = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root000"
)
mycursor = meubd.cursor()

#? Criação do banco:
# mycursor.execute("CREATE DATABASE ecolaço DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;")
mycursor.execute("USE ecolaço")

print('\033[32m', end='')
print('-=' * 20)
print(f'{"ECOLAÇO":^40}')
print('-=' * 20)
print('\033[m', end='')

print(f'\033[33m{"Seja bem vindo ao Ecolaço!":^40}\033[m')

while True:
    print('-' * 40)
    sleep(1)
    print('''O que você deseja fazer?
[ 1 ] - Realizar Cadastro
[ 2 ] - Realizar Login
[ 0 ] - Finalizar Programa ''')
    while True:
        opção = int(input('Escolha: '))
        if opção in (1, 2, 0):
            break
    print('-' * 40)
    if opção == 0:
        break
    elif opção == 1:
        while True:
            sleep(1)
            print("""Você deseja se cadastrar como FORNECEDOR ou COLETOR?
[ 1 ] - Fornecedor
[ 2 ] - Coletor
[ 3 ] - Saiba mais
[ 4 ] - Voltar """)
            while True:
                opção = int(input("Escolha: "))
                if opção in (1, 2, 3, 4):
                    break

            if opção  == 3:
                print('-' * 40)
                print('''\033[32mFornecedor\033[m – Perfil destinado aos usuários que desejam contribuir com a atividade da coleta seletiva, 
reciclagem e reuso de resíduos.
\033[32mColetor\033[m – Perfil destinado aos usuários que tem a sua empresa/ cooperativas de coleta seletiva e desejam 
fazer parte de uma plataforma que facilite o contato com público.''')
                print('-' * 40)
            elif opção == 4:
                break
            else:
                print('-' * 40)
                print(f'\033[32m{"CADASTRO":^40}\033[m')
                print('-' * 40)
                nome = str(input('Nome: ')).strip().title()
                while True:
                    email = str(input('Email: ')).strip()
                    #? Verificando se já há um usuário cadastrado com esse email:
                    sql = "SELECT COUNT(*) FROM (SELECT email from fornecedor UNION SELECT email from coletor) as email WHERE email = %s"
                    adr = (email, )
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchall()
                    if 0 in myresult[0]:
                        break
                    else:
                        print('\033[33mEsse email já está em uso.\033[m Por favor, digite outro email:')
                telefone = str(input('Telefone (Exemplo: (00) 12345-6789): ')).strip()
                if opção == 1:
                    cpf = str(input('CPF: ')).strip()
                elif opção == 2:
                    cnpj = str(input('CNPJ: ')).strip()
                senha = str(input('Senha (Max: 20 caracteres): ')).strip()

                #? Geração de um ID de Login inédito:
                if opção == 2:
                    while True:
                        chave = ''
                        for c in range(0, 12):  #? Geração da chave com 12 dígitos
                            chave += str(randint(0, 9))
                            c += 1
                        mycursor = meubd.cursor()
                        #? Contagem de quantos registros em coletor possuem uma chave igual à gerada
                        sql = "SELECT COUNT(*) FROM coletor WHERE chave_login = %s"
                        adr = (chave, )
                        mycursor.execute(sql, adr)
                        myresult = mycursor.fetchall()
                        #? Caso o resultado seja igual a 0, o loop é finalizado. Senão, ele gera chaves até que uma delas seja válida.
                        if 0 in myresult[0]:
                            break
                
                #? Inserção dos dados nas tabelas
                if opção == 1:
                    sql = "INSERT INTO fornecedor (nome, email, telefone, cpf, senha) VALUES (%s, %s, %s, %s, %s)"
                    val = (nome, email, telefone, cpf, senha)
                if opção == 2:
                    sql = "INSERT INTO coletor (nome, email, telefone, cnpj, senha, chave_login) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (nome, email, telefone, cnpj, senha, chave)
                mycursor.execute(sql, val)
                meubd.commit()

                #? Cadastro de endereços dos coletores
                if opção == 2: 
                    #? Verificando qual o ID (pk) do coletor cadastrado
                    sql = "SELECT id_org FROM coletor where cnpj = %s"
                    adr = (cnpj, )
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchall()
                    id_coletor = myresult[0][0]

                    cont_endereço = 1
                    print('-' * 40)
                    print(f'\033[32m{"Cadastro de endereços":^40}\033[m')
                    while True:
                        print('-' * 40)
                        print(f'\033[32m{cont_endereço}° ENDEREÇO:\033[m')
                        rua = str(input('Rua: ')).strip().title()
                        numero = str(input('Número: ')).strip()
                        bairro = str(input('Bairro: ')).strip().title()
                        cidade = str(input('Cidade: ')).strip().title()
                        estado = str(input('Estado: ')).strip().upper()
                        cep = str(input('CEP: ')).strip()

                        #? Inserção dos dados na tabela endereço
                        sql = "INSERT INTO ENDEREÇO (rua, numero, bairro, cidade, estado, cep) VALUES (%s, %s, %s, %s, %s, %s)"
                        val = (rua, numero, bairro, cidade, estado, cep)
                        mycursor.execute(sql, val)
                        meubd.commit()

                        #? Adicionando o ID do coletor (id_org) ao endereço cadastrado por ele
                        sql = "UPDATE endereço SET id_coletor = %s WHERE cep = %s"
                        val = (id_coletor, cep, )
                        mycursor.execute(sql, val)
                        meubd.commit()

                        print(mycursor.rowcount, "endereço(s) adicionado!")

                        resposta = ''
                        while resposta not in 'SN' or resposta == '':
                            print('-' * 40)
                            resposta = str(input('Deseja cadastrar outro endereço? [S/N] ')).strip().upper()
                        if resposta == 'N':
                            break
                        cont_endereço += 1
                print('-' * 40)
                print('\033[32mCADASTRO REALIZADO COM SUCESSO!\033[m')
                if opção == 2:
                    print(f'Sua chave de login é \033[32m{chave}\033[m. Utilize-a para acessar a plataforma.')
                resposta = ''
                while resposta not in 'SN' or resposta == '':
                    resposta = str(input('Você deseja visualizar os seus dados cadastrados? [S/N] ')).upper().strip()
                if resposta == 'S':
                    if opção == 1:
                        sql = "SELECT * FROM fornecedor WHERE cpf = %s"
                        adr = (cpf, )
                    elif opção == 2:
                        sql = "SELECT * FROM coletor WHERE cnpj = %s"
                        adr = (cnpj, )
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchall()
                    print('-' * 52)
                    for x in myresult:
                        if opção == 1:
                            print(f'''Nome: {x[2]}
Email: {x[4]}
Telefone: {x[3]}
CPF: {x[1]}
Senha: {x[5]} ''')
                        elif opção == 2:
                            print(f'''Nome: {x[1]}
Email: {x[3]}
Telefone: {x[4]}
CPNJ: {x[2]}
Chave de Login: {x[5]}
Senha: {x[6]} ''')


    elif opção == 2:
        print(f'\033[32m{"Login":^40}\033[m')
        print('-' * 40)
        
        while True:
            sleep(1)
            print('''Você deseja realizar login como FORNECEDOR ou COLETOR?
[ 1 ] - FORNECEDOR
[ 2 ] - COLETOR
[ 3 ] - VOLTAR
[ 0 ] - SAIR DO PROGRAMA''')
            while True:
                opção = int(input('Escolha: '))
                if opção in (1, 2, 3, 0):
                    break
            if opção == 0:
                print('-' * 40)
                break
            elif opção == 1:
                print('-' * 40)
                sleep(1)
                email = str(input('Email: ')).strip()
                senha = str(input('Senha: ')).strip()
                sql = "SELECT COUNT(*) FROM fornecedor WHERE email = %s"
                adr = (email, )
                mycursor.execute(sql, adr)
                myresult = mycursor.fetchall()
                if 0 in myresult[0]:
                    sleep(1)
                    print('\033[31mEMAIL NÃO CADASTRADO!\033[m')
                    print('-' * 40)
                else:
                    sql = "SELECT nome, email, senha FROM fornecedor WHERE email = %s"
                    adr = (email, )
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchall()
                    if myresult[0][2] == senha:
                        break
                    else:
                        sleep(1)
                        print('\033[31mSENHA INCORRETA!\033[m')
                        print('-' * 40)

            elif opção == 2:
                print('-' * 40)
                sleep(1)
                login = str(input('Chave de Login: ')).strip()
                senha = str(input('Senha: ')).strip()
                #! Realize a contagem de registros cuja chave_login = chave. Se o resultado for 0, solicite outra chave ou o cadastro do usuário
                sql = "SELECT COUNT(*) FROM coletor WHERE chave_login = %s"
                adr = (login, )
                mycursor.execute(sql, adr)
                myresult = mycursor.fetchall()
                if 0 in myresult[0]:
                    sleep(1)
                    print('\033[31mCHAVE DE LOGIN NÃO CADASTRADA!\033[m')
                    print('-' * 40)
                else:
                    sql = "SELECT nome, chave_login, senha FROM coletor WHERE chave_login = %s"
                    adr = (login, )
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchall()
                    if myresult[0][2] == senha:
                        break
                    else:
                        sleep(1)
                        print('\033[31mSENHA INCORRETA!\033[m')
                        print('-' * 40)
            elif opção == 3:
                break
        if opção == 0:
            break

    #? Caso o login seja realizado:
        if opção == 1 or opção == 2:
            sleep(1)
            print(f'\033[32mLOGIN REALIZADO COM SUCESSO!\033[m Seja bem vindo(a), \033[32m{(myresult[0][0].split())[0]}!\033[m')
            print('-' * 40)
            if opção == 1:
                #? Buscando ID do fornecedor logado
                sql = "SELECT id_user FROM fornecedor WHERE email = %s"
                adr = (email, )
                mycursor.execute(sql, adr)
                myresult = mycursor.fetchall()
                id_fornecedor = myresult[0][0]

                while True:
                    sleep(1)
                    print('''O que você deseja fazer?
[ 1 ] - Visualizar minha pontuação
[ 2 ] - Resgatar código de pontos
[ 3 ] - Trocar pontos por recompensas
[ 4 ] - Visualizar meu histórico de trocas
[ 5 ] - Acessar relatório de atividades
[ 6 ] - Editar conta
[ 0 ] - Sair da conta''')
                    while True:
                        opção = int(input('Escolha: '))
                        if opção in (1, 2, 3, 4, 5, 6, 0):
                            break
                    if opção == 0:
                        break
                    elif opção == 1:
                        print('-' * 40)
                        print(f'\033[32m{"Pontuação":^40}\033[m')
                        print('-' * 40)
                        #? Buscando a pontuação do fornecedor:
                        sql = "SELECT pontuação FROM fornecedor WHERE email = %s"
                        adr = (email, )
                        mycursor.execute(sql, adr)
                        myresult = mycursor.fetchall()
                        pontuação = myresult[0][0]
                        sleep(1)
                        print(f'Sua pontuação atual é de \033[32m{pontuação} pontos\033[m!')
                        print('-' * 40)

                    elif opção == 2:
                        print('-' * 40)
                        print(f'\033[32m{"Resgate de pontos":^40}\033[m')
                        cont_codigos = 1
                        while True:
                            print('-' * 40)
                            sleep(1)
                            print(f'\033[32m{cont_codigos}º CÓDIGO\033[m')
                            codigo = str(input('Código de Resgate [0 para voltar]: ')).strip()
                            if codigo == '0':
                                print('-' * 40)
                                break
                            #? Verificando a validade do código (se o código existe na tabela entregas)
                            sql = "SELECT COUNT(*) FROM entregas WHERE codigo_resgate = %s"
                            adr = (codigo, )
                            mycursor.execute(sql, adr)
                            myresult = mycursor.fetchall()
                            if 0 in myresult[0]:
                                sleep(1)
                                print('\033[31mO código digitado é inválido.\033[m Tente novamente!')
                            else:
                                #? Verificando o status do código
                                sql = "SELECT status_codigo FROM entregas WHERE codigo_resgate = %s"
                                adr = (codigo, )
                                mycursor.execute(sql, adr)
                                myresult = mycursor.fetchall()
                                status = myresult[0][0]

                                #? Verificando se o usuário logado está resgatando um código seu
                                if status == 'INDISP':
                                    sleep(1)
                                    print('\033[33mEsse código já foi utilizado!\033[m')
                                
                                elif status == 'DISP':
                                    #? Verificando o id do fornecedor "dono" do código e a quantidade de pontos 'indexados' a esse código
                                    sql = "SELECT id_user, pontos FROM entregas WHERE codigo_resgate = %s"
                                    adr = (codigo, )
                                    mycursor.execute(sql, adr)
                                    myresult = mycursor.fetchall()
                                    id_dono = myresult[0][0]
                                    pontos = myresult[0][1]

                                    if id_dono != id_fornecedor:
                                        sleep(1)
                                        print('\033[33mEsse código de resgate pertence a outro usuário.\033[m')
                                    else:
                                        #? Adicionando pontuação ao fornecedor
                                        sql = "UPDATE fornecedor SET pontuação = (pontuação + %s) WHERE id_user = %s"
                                        val = (pontos, id_fornecedor)
                                        mycursor.execute(sql, val)
                                        meubd.commit()
                                        print(f'\033[32m{pontos} pontos adicionados!\033[m')

                                        #? Mudando o status do código de disponível para indisponível
                                        sql = "UPDATE entregas SET status_codigo = %s WHERE codigo_resgate = %s"
                                        val = ('INDISP', codigo)
                                        mycursor.execute(sql, val)
                                        meubd.commit()

                                        #? Verificando se o fornecedor deseja continuar a resgatar códigos
                                        resposta = ''
                                        while resposta not in 'SN' or resposta == '':
                                            resposta = str(input('Deseja resgatar outro código? [S/N] ')).strip().upper()
                                        if resposta == 'N':
                                            print('-' * 40)
                                            break
                                        cont_codigos += 1

                    elif opção == 3:
                        while True:
                            #? Buscando a pontuação do usuário
                            sql = "SELECT pontuação FROM fornecedor WHERE email = %s"
                            adr = (email, )
                            mycursor.execute(sql, adr)
                            myresult = mycursor.fetchall()
                            pontuação = myresult[0][0]

                            print('-' * 72)
                            print(f'\033[32m{"Loja de Recompensas"}{" " * 33}Sua pontuação: {pontuação:>4}\033[m')
                            print('-' * 72)
                            sleep(1)
                            print(f'''\033[32mID{' ' * 20}NOME DA RECOMPENSA{' ' * 27}CUSTO\033[m\n{'-' * 72}''')
                            #? Contando a quantidade de recompensas cadastradas
                            mycursor.execute("SELECT COUNT(*) FROM recompensas")
                            myresult = mycursor.fetchall()
                            cont_recompensas = myresult[0][0]

                            if cont_recompensas == 0:
                                print('Nenhuma recompensa cadastrada... ')
                            #? Buscando no banco de dados o id, nome e custo de cada recompensa
                            mycursor.execute("SELECT id_recompensa, nome, custo FROM recompensas ORDER BY custo DESC")
                            myresult = mycursor.fetchall()
                            for c in range(0, cont_recompensas):
                                id_recompensa = myresult[c][0]
                                nome = myresult[c][1]
                                custo = myresult[c][2]
                                d1 = len(str(id_recompensa))
                                d2 = len(str(nome))
                                d3 = len(str(custo))

                                #? Exibindo uma tabela com todas as recompensas disponíveis
                                print(f'''{id_recompensa}{' ' * (22 - d1)}{nome}{' ' * (45 - d2)}{custo:>4}''')
                                c += 1
                            print('-' * 72)
                            id_recompensa = int(input('Digite o ID da recompensa que você deseja [Digite 0 para voltar]: '))
                            if id_recompensa == 0:
                                print('-' * 40)
                                break
                            else:
                            #? Verificando se existe recompensa com o ID informado
                                sql = "SELECT COUNT(*) FROM recompensas WHERE id_recompensa = %s"
                                adr = (id_recompensa, )
                                mycursor.execute(sql, adr)
                                myresult = mycursor.fetchall()
                                if myresult[0][0] == 0:
                                    print('\033[31mNão existe nenhuma recompensa com esse ID!\033[m')
                                else:
                                    sql = "SELECT nome, custo FROM recompensas WHERE id_recompensa = %s"
                                    adr = (id_recompensa, )
                                    mycursor.execute(sql, adr)
                                    myresult = mycursor.fetchall()

                                    nome = myresult[0][0]
                                    custoUnitario = myresult[0][1]
                                    print('-' * 40)
                                    quantidadeRecompensa = int(input('Quantidade de unidades: '))
                                    print('-' * 72)
                                    custoTotal = custoUnitario * quantidadeRecompensa
                                    print('\033[32mCarrinho de compras\033[m')
                                    print(f'\033[33mItem:\033[m {nome}\t\t\033[33mQuantidade:\033[m {quantidadeRecompensa}\n\033[33mCusto total:\033[m {custoTotal}')
                                    print('-' * 72)
                                    if pontuação < custoTotal:
                                        print(f'Você não tem os \033[31m{custoTotal} pontos\033[m necessários para finalizar a compra. Continue reciclando!')
                                    else:
                                        resposta = ''
                                        while resposta not in 'SN' or resposta == '':
                                            resposta = str(input('Deseja finalizar a compra? [S/N] ')).strip().upper()
                                        if resposta == 'S':
                                            #? Buscando ID do coletor responsável pela recompensa
                                            sql = "SELECT id_coletor FROM recompensas WHERE id_recompensa = %s"
                                            adr = (id_recompensa, )
                                            mycursor.execute(sql, adr)
                                            myresult = mycursor.fetchall()
                                            id_coletor = myresult[0][0]

                                            #? Registrando troca na tabela trocas
                                            sql = '''INSERT INTO trocas (id_user, id_org, id_recompensa, quantidade, custototal) 
                                            VALUES (%s, %s, %s, %s, %s)'''
                                            val = (id_fornecedor, id_coletor, id_recompensa, quantidadeRecompensa, custoTotal)
                                            mycursor.execute(sql, val)
                                            meubd.commit()

                                            #? Corrigindo pontuação do fornecedor
                                            sql = "UPDATE fornecedor SET pontuação = pontuação - %s WHERE id_user = %s"
                                            val = (custoTotal, id_fornecedor)
                                            mycursor.execute(sql, val)
                                            meubd.commit()

                                            print(f'''\033[32mCompra finalizada com sucesso!\033[m {custoTotal} pontos foram descontados da sua pontuação.
\033[33mSua nova pontuação: \033[32m{pontuação - custoTotal} pontos\033[m''')

                    elif opção == 4:
                        print('-' * 85)
                        print(f'\033[32m{"Histórico de Trocas"}{" " * 57}Ano: 2021\033[m')
                        print('-' * 85)
                        sleep(1)

                        sql = "SELECT COUNT(*) FROM trocas WHERE id_user = %s"
                        adr = (id_fornecedor, )
                        mycursor.execute(sql, adr)
                        myresult = mycursor.fetchall()
                        quantidadeTrocas = myresult[0][0]

                        if quantidadeTrocas == 0:
                            print('Você ainda não realizou nenhuma troca...')
                            print('-' * 90)
                        else:
                            sql = '''SELECT recompensas.nome as nome_recompensa, coletor.nome as nome_coletor, trocas.quantidade, 
                            trocas.custototal FROM recompensas
                            JOIN trocas on recompensas.id_recompensa = trocas.id_recompensa
                            JOIN coletor on coletor.id_org = trocas.id_org
                            JOIN fornecedor on fornecedor.id_user = trocas.id_user WHERE trocas.id_user = %s'''
                            adr = (id_fornecedor, )
                            mycursor.execute(sql, adr)
                            myresult = mycursor.fetchall()

                            print(f'''\033[32mNOME DA RECOMPENSA{' ' * 22}NOME DO COLETOR{' ' * 10}QUANTIDADE{' ' * 5}CUSTO\033[m''')

                            for c in range(0, quantidadeTrocas):
                                nomeRecompensa = myresult[c][0]
                                nomeColetor = myresult[c][1]
                                quantidadeRecompensa = myresult[c][2]
                                custoTotal = myresult[c][3]

                                d1 = len(str(nomeRecompensa))
                                d2 = len(str(nomeColetor))
                                d3 = len(str(quantidadeRecompensa))
                                d4 = len(str(custoTotal))

                                print(f"""{nomeRecompensa}{' ' * (40 - d1)}{nomeColetor}{' ' * (25 - d2)}""", end='')
                                print(f"""{quantidadeRecompensa}{' ' * (15 - d3)}{custoTotal}""")
                            print('-' * 85)

                    elif opção == 5:
                        print('-' * 40)
                        print(f'\033[32m{"Relatório de Atividades":^40}\033[m')
                        print('-' * 40)

                        sql = "SELECT SUM(peso), COUNT(*) FROM entregas WHERE id_user = %s"
                        adr = (id_fornecedor, )
                        mycursor.execute(sql, adr)
                        myresult = mycursor.fetchall()
                        if myresult[0][0] is None:
                            pesoTotalReciclado = 0
                        else:
                            pesoTotalReciclado = myresult[0][0]
                        quantidadeEntregas = myresult[0][1]
                        sleep(1)
                        print(f'Ao todo você reciclou \033[32m{pesoTotalReciclado}kg\033[m!')

                        pesoPlastico = 0
                        pesoPapel = 0
                        pesoVidro = 0
                        pesoMetal = 0

                        sql = "SELECT peso, material FROM entregas WHERE id_user = %s"
                        adr = (id_fornecedor, )
                        mycursor.execute(sql, adr)
                        myresult = mycursor.fetchall()
                        for c in range(0, quantidadeEntregas):
                            if myresult[c][1] == 'P':
                                pesoPlastico += myresult[c][0]
                            elif myresult[c][1] == 'PP':
                                pesoPapel += myresult[c][0]
                            elif myresult[c][1] == 'V':
                                pesoVidro += myresult[c][0]
                            elif myresult[c][1] == 'M':
                                pesoMetal += myresult[c][0]
                            c += 1
                        sleep(1)
                        print('-' * 67)

                        #? Evitando erros: Denominador de uma divisão não pode ser 0
                        if pesoTotalReciclado == 0:
                            pesoTotalReciclado += 1
                        #? Calculando porcentagem relativa ao peso de cada material
                        porcentPlastico = int((100 * pesoPlastico / pesoTotalReciclado) / 2)
                        if porcentPlastico == 0:
                            porcentPlastico += 1
                        porcentPapel = int((100 * pesoPapel / pesoTotalReciclado) / 2)
                        if porcentPapel == 0:
                            porcentPapel += 1
                        porcentVidro = int((100 * pesoVidro / pesoTotalReciclado) / 2)
                        if porcentVidro == 0:
                            porcentVidro += 1
                        porcentMetal = int((100 * pesoMetal / pesoTotalReciclado) / 2)
                        if porcentMetal == 0:
                            porcentMetal += 1
                        
                        #? Exibição do gráfico (porcentagem convertida para int para evitar números decimais, o que pode ocasionar erros na impressão do gráfico)
                        print(f"\033[1;31m{'Plástico':<10}\033[;;41m{' ' * porcentPlastico}\033[m {pesoPlastico}kg\n")
                        print(f"\033[1;34m{'Papel':<10}\033[;;44m{' ' * porcentPapel}\033[m {pesoPapel}kg\n")
                        print(f"\033[1;32m{'Vidro':<10}\033[;;42m{' ' * porcentVidro}\033[m {pesoVidro}kg\n")
                        print(f"\033[1;33m{'Metal':<10}\033[;;43m{' ' * porcentMetal}\033[m {pesoMetal}kg")
                        print('-' * 67)

                    elif opção == 6:
                        while True:
                            print('-' * 40)
                            print(f'\033[32m{"Editar Conta":^40}\033[m')
                            print('-' * 40)
                            sleep(1)
                            print('''O que você deseja fazer?
[ 1 ] - Editar meus dados cadastrados
[ 2 ] - Excluir conta
[ 3 ] - Voltar''')
                            while True:
                                opção = int(input('Escolha: '))
                                if opção in (1, 2, 3):
                                    break
                            if opção == 1:
                                while True:
                                    print('-' * 40)
                                    sleep(1)
                                    print('\033[32mSeus dados de cadastro:\033[m')
                                    sql = "SELECT nome, cpf, telefone, email, senha FROM fornecedor WHERE id_user = %s"
                                    adr = (id_fornecedor, )
                                    mycursor.execute(sql, adr)
                                    myresult = mycursor.fetchall()
                                    print(f'''Nome: {myresult[0][0]}
CPF: {myresult[0][1]}
Telefone: {myresult[0][2]}
Email: {myresult[0][3]}
Senha: {myresult[0][4]}''')
                                    print('-' * 40)
                                    sleep(1)
                                    print('''Qual informação você deseja alterar?
[ 1 ] - Nome
[ 2 ] - Email
[ 3 ] - Telefone
[ 4 ] - Senha
[ 5 ] - Voltar''')
                                    while True:
                                        opção = int(input('Escolha: '))
                                        if opção in (1, 2, 3, 4, 5):
                                            break
                                    if opção != 5:
                                        print('-' * 40)
                                        sleep(1)
                                    if opção == 1:
                                        nome = str(input('Nome: ')).strip().title()
                                        sql = "UPDATE fornecedor SET nome = %s WHERE id_user = %s"
                                        val = (nome, id_fornecedor)
                                    elif opção == 2:
                                        email = str(input('Email: ')).strip()
                                        sql = "UPDATE fornecedor SET email = %s WHERE id_user = %s"
                                        val = (email, id_fornecedor)
                                    elif opção == 3:
                                        telefone = str(input('Telefone (Exemplo: (00) 12345-6789): ')).strip()
                                        sql = "UPDATE fornecedor SET telefone = %s WHERE id_user = %s"
                                        val = (telefone, id_fornecedor)
                                    elif opção == 4:
                                        novaSenha = str(input('Nova senha: ')).strip()
                                        sql = "UPDATE fornecedor SET senha = %s WHERE id_user = %s"
                                        val = (novaSenha, id_fornecedor)
                                    else:
                                        break
                                    mycursor.execute(sql, val)
                                    meubd.commit()
                            
                            elif opção == 3:
                                print('-' * 40)
                                break

                            elif opção == 2:
                                print('-' * 40)
                                sleep(1)
                                resposta = ''
                                while resposta not in 'SN' or resposta == '':
                                    resposta = str(input('Você tem CERTEZA que deseja \033[31mapagar a sua conta\033[m? [S/N] ')).strip().upper()
                                if resposta == 'S':
                                    #? Primeiro tenho que deletar os registros desse fornecedor de todas as outras tabelas onde ele é FK:
                                    #? Entregas
                                    sql = "DELETE FROM entregas WHERE id_user = %s"
                                    adr = (id_fornecedor, )
                                    mycursor.execute(sql, adr)
                                    meubd.commit()
                                    #? Trocas
                                    sql = "DELETE FROM trocas WHERE id_user = %s"
                                    adr = (id_fornecedor, )
                                    mycursor.execute(sql, adr)
                                    meubd.commit()
                                    #? Finalmente, deletamos o fornecedor
                                    sql = "DELETE FROM fornecedor WHERE id_user = %s"
                                    adr = (id_fornecedor, )
                                    mycursor.execute(sql, adr)
                                    meubd.commit()
                                    sleep(1)
                                    #? Criando flag de conta deletada que será identificada fora do loop
                                    breakFlag = 'conta fornecedor deletada'
                                    print('\033[32mSua conta foi deletada com sucesso!\033[m')
                                    break
                        #? Flag de conta deletada identificada, realizará outro break seguido para redirecionar à tela inicial do programa
                        if breakFlag == 'conta fornecedor deletada':
                            break

            #? Usuário coletor
            elif opção == 2:
                #? Buscando no banco de dados o ID do coletor
                sql = "SELECT id_org FROM coletor WHERE chave_login = %s"
                adr = (login, )
                mycursor.execute(sql, adr)
                myresult = mycursor.fetchall()
                id_coletor = myresult[0][0]
                #? Menu de opçãoes do coletor
                while True:
                    sleep(1)
                    print('''O que você deseja fazer?
[ 1 ] - Cadastrar recompensas para fornecedores
[ 2 ] - Confirmar recebimento de reciclável
[ 3 ] - Visualizar minhas recompensas cadastradas
[ 4 ] - Visualizar e/ou editar meus endereços cadastrados
[ 5 ] - Editar conta
[ 0 ] - Sair da Conta''')
                    while True:
                        opção = int(input('Escolha: '))
                        if opção in (1, 2, 3, 4, 5, 0):
                            break
                    if opção == 0:
                        break
                    elif opção == 1:
                        print('-' * 40)
                        print(f'\033[32m{"Cadastro de recompensas":^40}\033[m')
                        cont_recompensas = 1
                        while True:
                            print('-' * 40)
                            sleep(1)
                            print(f'\033[32m{cont_recompensas}ª RECOMPENSA:\033[m')
                            nome = str(input('Nome da recompensa: ')).strip().title()
                            custo = int(input('Valor em pontos: '))
                            #? Geração de um ID inédito
                            while True:
                                id_recompensa = ''
                                for c in range(0, 4):
                                    id_recompensa += str(randint(1, 9))
                                    c += 1
                                id_recompensa = int(id_recompensa)
                                sql = "SELECT COUNT(*) FROM recompensas WHERE id_recompensa = %s"
                                adr = (id_recompensa, )
                                mycursor.execute(sql, adr)
                                myresult = mycursor.fetchall()
                                if 0 in myresult[0]:
                                    break

                            #? Inserindo os dados na tabela recompensas
                            sql = "INSERT INTO recompensas (id_recompensa, nome, custo) VALUES (%s, %s, %s)"
                            val = (id_recompensa, nome, custo)
                            mycursor.execute(sql, val)
                            meubd.commit()

                            #? Adicionando o ID do coletor à recompensa cadastrada por ele
                            sql = "UPDATE recompensas SET id_coletor = %s WHERE id_recompensa = %s"
                            val = (id_coletor, id_recompensa)
                            mycursor.execute(sql, val)
                            meubd.commit()

                            #? Verificando se o coletor deseja continuar a cadastrar recompensas
                            print('-' * 40)
                            sleep(1)
                            resposta = ''
                            while resposta not in 'SN' or resposta == '':
                                resposta = str(input('Deseja cadastrar outra recompensa? [S/N] ')).strip().upper()
                            if resposta == 'N':
                                print('-' * 40)
                                break
                            cont_recompensas += 1

                    elif opção == 2:
                        print('-' * 40)
                        print(f'\033[32m{"Recebimento de Recicláveis":^40}\033[m')
                        print('-' * 40)
                        cont_entregas = 1
                        while True:
                            sleep(1)
                            print(f'\033[32m{cont_entregas}ª ENTREGA:\033[m')
                            nome_fornecedor = str(input('Nome do Fornecedor: ')).strip().title()
                            email_fornecedor = str(input('Email do Fornecedor: ')).strip()

                            #? Verificando se existe um fornecedor com o nome e email informado:
                            sql = "SELECT COUNT(*) FROM fornecedor WHERE nome = %s and email = %s"
                            adr = (nome_fornecedor, email_fornecedor, )
                            mycursor.execute(sql, adr)
                            myresult = mycursor.fetchall()
                            if myresult[0][0] == 0:
                                sleep(1)
                                print('\033[31mNome e/ou email incorretos!\033[m Verifique-os e tente novamente.')
                            else:
                                while True:
                                    material = str(input('Material [P/PP/V/M]: ')).strip().upper()
                                    if material in 'PPVM':
                                        break
                                    else:
                                        sleep(1)
                                        print('\033[33mOpções válidas: P = Plástico, PP = Papel, V = Vidro, M = Metal.\033[m Tente novamente:')
                                peso = int(input('Peso recebido: '))
                                pontos = 15 * peso

                                #? Gerando código de resgate inédito com 15 caracteres
                                caracteres = 'ABCD12EFGH34IJK56LMNO78RSTU9VWYXZ'
                                while True:
                                    codigo_resgate = ''
                                    for c in range (0, 15):
                                        codigo_resgate += str(choice(caracteres))
                                        c += 1
                                    mycursor = meubd.cursor()
                                    sql = "SELECT COUNT(*) FROM entregas WHERE codigo_resgate = %s"
                                    adr = (codigo_resgate, )
                                    mycursor.execute(sql, adr)
                                    myresult = mycursor.fetchall()
                                    if 0 in myresult[0]:
                                        print('-' * 40)
                                        sleep(1)
                                        print(f'O código de resgate de \033[32m{pontos} pontos\033[m do fornecedor é: \033[32m{codigo_resgate}\033[m!')
                                        break
                                sql = """INSERT INTO entregas (codigo_resgate, material, peso, pontos)
                                VALUES (%s, %s, %s, %s)"""
                                val = (codigo_resgate, material, peso, pontos)
                                mycursor.execute(sql, val)
                                meubd.commit()

                                #? Adicionando o ID do coletor ao reciclável recebido por ele
                                sql = "UPDATE entregas SET id_coletor = %s WHERE codigo_resgate = %s"
                                val = (id_coletor, codigo_resgate)
                                mycursor.execute(sql, val)
                                meubd.commit()
                                
                                #? Buscando no banco de dados o ID do fornecedor
                                sql = "SELECT id_user FROM fornecedor WHERE nome = %s and email = %s"
                                adr = (nome_fornecedor, email_fornecedor, )
                                mycursor.execute(sql, adr)
                                myresult = mycursor.fetchall()
                                id_fornecedor = myresult[0][0]

                                #? Adicionando o ID do fornecedor ao reciclável entregue por ele
                                sql = "UPDATE entregas SET id_user = %s WHERE codigo_resgate = %s"
                                val = (id_fornecedor, codigo_resgate)
                                mycursor.execute(sql, val)
                                meubd.commit()

                                print('-' * 40)
                                sleep(1)
                                resposta = ''
                                while resposta not in 'SN' or resposta == '':
                                    resposta = str(input('Deseja cadastrar outro recebimento de recicláveis? [S/N] ')).strip().upper()
                                if resposta == 'N':
                                    print('-' * 40)
                                    break
                                cont_entregas += 1
                            print('-' * 40)

                    elif opção == 3:
                        print('-' * 71)
                        print(f'''\033[32mID{' ' * 20}NOME DA RECOMPENSA{' ' * 26}CUSTO\033[m\n{'-' * 71}''')
                        sleep(1)

                        sql = "SELECT COUNT(*) FROM recompensas WHERE id_coletor = %s"
                        adr = (id_coletor, )
                        mycursor.execute(sql, adr)
                        myresult = mycursor.fetchall()
                        cont_recompensas = myresult[0][0]

                        if cont_recompensas == 0:
                            print('Nenhuma recompensa cadastrada...')
                        sql = "SELECT id_recompensa, nome, custo FROM recompensas WHERE id_coletor = %s ORDER BY custo desc"
                        adr = (id_coletor, )
                        mycursor.execute(sql, adr)
                        myresult = mycursor.fetchall()

                        for c in range(0, cont_recompensas):
                            id_recompensa = myresult[c][0]
                            nome = myresult[c][1]
                            custo = myresult[c][2]
                            d1 = len(str(myresult[c][0]))
                            d2 = len(str(myresult[c][1]))
                            d3 = len(str(myresult[c][2]))
                            print(f'''{id_recompensa}{' ' * (22 - d1)}{nome}{' ' * (45 - d2)}{custo:>4}''') 
                            c += 1
                        print('-' * 71)

                    elif opção == 4:
                        while True:
                            print('-' * 40)
                            print(f'\033[32m{"Endereços Cadastrados":^40}\033[m')
                            print('-' * 40)
                            sql = "SELECT COUNT(*) FROM endereço WHERE id_coletor = %s"
                            adr = (id_coletor, )
                            mycursor.execute(sql, adr)
                            myresult = mycursor.fetchall()
                            cont_endereço = myresult[0][0]

                            sql = "SELECT rua, numero, bairro, cidade, estado, cep FROM endereço WHERE id_coletor = %s"
                            adr = (id_coletor, )
                            mycursor.execute(sql, adr)
                            myresult = mycursor.fetchall()

                            ordemEndereço = 1
                            opçõesEndereço = ''
                            listaOpções = []
                            for c in range(0, cont_endereço):
                                sleep(1)
                                print(f'\033[32m{ordemEndereço}º ENDEREÇO\033[m')
                                listaOpções.append(ordemEndereço)
                                opçõesEndereço += '\n[ ' + str(ordemEndereço) + ' ] - ' + str(ordemEndereço) + 'º ENDEREÇO'
                                print(f'Rua: {myresult[c][0]}')
                                print(f'Número: {myresult[c][1]}')
                                print(f'Bairro: {myresult[c][2]}')
                                print(f'Cidade: {myresult[c][3]}')
                                print(f'Estado: {myresult[c][4]}')
                                print(f'CEP: {myresult[c][5]}')
                                c += 1
                                ordemEndereço += 1
                                print('-' * 40)
                            sleep(1)
                            print('''O que você deseja fazer?
[ 1 ] - Adicionar endereço
[ 2 ] - Editar endereço
[ 3 ] - Excluir endereço
[ 4 ] - Voltar''')
                            while True:
                                opção = int(input('Escolha: '))
                                if opção in (1, 2, 3, 4):
                                    break
                            if opção == 1:
                                print('-' * 40)
                                print(f'\033[32m{"Cadastro de endereços":^40}\033[m')
                                print('-' * 40)
                                sleep(1)
                                rua = str(input('Rua: ')).strip().title()
                                numero = str(input('Número: ')).strip()
                                bairro = str(input('Bairro: ')).strip().title()
                                cidade = str(input('Cidade: ')).strip().title()
                                estado = str(input('Estado: ')).strip().upper()
                                cep = str(input('CEP: ')).strip()
                                sql = "INSERT INTO endereço (id_coletor, rua, numero, bairro, cidade, estado, cep) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                val = (id_coletor, rua, numero, bairro, cidade, estado, cep)
                                mycursor.execute(sql, val)
                                meubd.commit()
                                sleep(1)
                                print('\033[32mEndereço adicionado com sucesso!\033[m')

                            elif opção == 2:
                                print('-' * 40)
                                sleep(1)
                                print(f'Qual desses endereços você deseja alterar?{opçõesEndereço}')
                                while True:
                                    opção = int(input('Escolha: '))
                                    if opção in listaOpções:
                                        break
                                print('-' * 40)
                                sleep(1)
                                rua = str(input('Rua: ')).strip().title()
                                numero = str(input('Número: ')).strip()
                                bairro = str(input('Bairro: ')).strip().title()
                                cidade = str(input('Cidade: ')).strip().title()
                                estado = str(input('Estado: ')).strip().upper()
                                cep = str(input('CEP: ')).strip()

                                sql = "UPDATE endereço SET rua = %s, numero = %s, bairro = %s, cidade = %s, estado = %s, cep = %s WHERE cep = %s"
                                val = (rua, numero, bairro, cidade, estado, cep, myresult[opção - 1][5])
                                mycursor.execute(sql, val)
                                meubd.commit()
                                sleep(1)
                                print('\033[32mEndereço alterado com sucesso!\033[m')

                            elif opção == 3:
                                print('-' * 40)
                                sleep(1)
                                print(f'Qual desses endereços você deseja excluir?{opçõesEndereço}')
                                while True:
                                    opção = int(input('Escolha: '))
                                    if opção in listaOpções:
                                        break
                                sql = "DELETE FROM endereço WHERE cep = %s"
                                adr = (myresult[opção - 1][5], )
                                mycursor.execute(sql, adr)
                                meubd.commit()
                                sleep(1)
                                print('\033[32mEndereço excluído com sucesso!\033[m')
                            elif opção == 4:
                                print('-' * 40)
                                break
                        
                    elif opção == 5:
                        while True:
                            print('-' * 40)
                            print(f'\033[32m{"Editar dados":^40}\033[m')
                            print('-' * 40)
                            sleep(1)
                            print('''O que você deseja fazer?
[ 1 ] - Editar dados cadastrados
[ 2 ] - Excluir conta
[ 3 ] - Voltar''')
                            while True:
                                opção = int(input('Escolha: '))
                                if opção in (1, 2, 3):
                                    break
                            if opção == 1:
                                while True:
                                    print('-' * 40)
                                    sleep(1)
                                    print('\033[32mSeus dados de cadastro:\033[m')
                                    sql = "SELECT nome, cnpj, telefone, email, chave_login, senha FROM coletor WHERE id_org = %s"
                                    adr = (id_coletor, )
                                    mycursor.execute(sql, adr)
                                    myresult = mycursor.fetchall()
                                    print(f'''Nome: {myresult[0][0]}
CNPJ: {myresult[0][1]}
Telefone: {myresult[0][2]}
Email: {myresult[0][3]}
Login: {myresult[0][4]}
Senha: {myresult[0][5]}''')
                                    print('-' * 40)
                                    sleep(1)
                                    print('''Qual informação você deseja alterar?:
[ 1 ] - Nome
[ 2 ] - Email
[ 3 ] - Telefone
[ 4 ] - Senha
[ 5 ] - Voltar''')
                                    while True:
                                        opção = int(input('Escolha: '))
                                        if opção in (1, 2, 3, 4, 5):
                                            break
                                    if opção != 5:
                                        print('-' * 40)
                                        sleep(1)
                                    if opção == 1:
                                        nome = str(input('Nome: ')).strip().title()
                                        sql = "UPDATE coletor SET nome = %s WHERE id_org = %s"
                                        val = (nome, id_coletor)
                                    elif opção == 2:
                                        email = str(input('Email: ')).strip()
                                        sql = "UPDATE coletor SET email = %s WHERE id_org = %s"
                                        val = (email, id_coletor)
                                    elif opção == 3:
                                        telefone = str(input('Telefone: ')).strip()
                                        sql = "UPDATE coletor SET telefone = %s WHERE id_org = %s"
                                        val = (telefone, id_coletor)
                                    elif opção == 4:
                                        senha = str(input('Senha: ')).strip()
                                        sql = "UPDATE coletor SET senha = %s WHERE id_org = %s"
                                        val = (senha, id_coletor)
                                    else:
                                        break
                                    mycursor.execute(sql, val)
                                    meubd.commit()
                            
                            elif opção == 3:
                                print('-' * 40)
                                break

                            elif opção == 2:
                                print('-' * 40)
                                sleep(1)
                                resposta = ''
                                while resposta not in 'SN' or resposta == '':
                                    resposta = str(input('Você tem CERTEZA que deseja \033[31mapagar a sua conta\033[m? [S/N] ')).strip().upper()
                                if resposta == 'S':
                                    #? Primeiro tenho que deletar os registros desse coletor de todas as outras tabelas onde ele é FK:
                                    #? Entregas
                                    sql = "DELETE FROM entregas WHERE id_coletor = %s"
                                    adr = (id_coletor, )
                                    mycursor.execute(sql, adr)
                                    meubd.commit()
                                    #? Trocas
                                    sql = "DELETE FROM trocas WHERE id_org = %s"
                                    adr = (id_coletor, )
                                    mycursor.execute(sql, adr)
                                    meubd.commit()
                                    #? Endereço
                                    sql = "DELETE FROM endereço WHERE id_coletor = %s"
                                    adr = (id_coletor, )
                                    mycursor.execute(sql, adr)
                                    meubd.commit()
                                    #? Recompensas
                                    sql = "DELETE FROM recompensas WHERE id_coletor = %s"
                                    adr = (id_coletor, )
                                    mycursor.execute(sql, adr)
                                    meubd.commit()
                                    #? Finalmente, deletamos o coletor
                                    sql = "DELETE FROM coletor WHERE id_org = %s"
                                    adr = (id_coletor, )
                                    mycursor.execute(sql, adr)
                                    meubd.commit()
                                    sleep(1)
                                    #? Criando flag de conta deletada que será identificada fora do loop
                                    breakFlag = 'conta coletor deletada'
                                    print('\033[32mSua conta foi deletada com sucesso!\033[m')
                                    break
                        #? Flag de conta deletada identificada, realizará outro break seguido para redirecionar à tela inicial do programa
                        if breakFlag == 'conta coletor deletada':
                            break
sleep(1)
print('\033[32mPROGRAMA FINALIZADO COM SUCESSO!\033[m')
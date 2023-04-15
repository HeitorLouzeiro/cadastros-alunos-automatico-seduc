import docx

# Abrir o arquivo docx
doc = docx.Document(
    'E:/pythonProject/personalProjects/seleniumAutoCadAluno/alunos.docx')

# Criar uma lista vazia para armazenar as strings a serem ignoradas
ignore_list = []

# Adicionar as strings à lista usando um for loop
for i in range(1, 10):
    ignore_list.append("TURMA " + str(i))

# Definir os CPFs selecionados
cpf_selecionados = ['999.999.999-99']

# Acessar as tabelas do documento
alunos = []
for table in doc.tables:
    for row in table.rows:
        # Verificar se a primeira célula contém o cabeçalho da tabela
        if row.cells[0].text.strip() != "QTD":
            '''
                Verificar se a primeira célula
                contém uma string da lista de ignore_list
            '''
            ignore_row = False
            for ignore_str in ignore_list:
                if ignore_str in row.cells[0].text.strip():
                    ignore_row = True
                    break
            if ignore_row:
                '''
                Pular a linha se ela contém uma string da lista de ignore_list
                '''
                continue
            # Criar um novo dicionário para armazenar as informações do aluno
            aluno = {}
            for i, cell in enumerate(row.cells):
                # Ignorar as células que contêm o cabeçalho
                if i > 0:
                    # Adicionar o conteúdo da célula ao dicionário
                    if i == 3 and not cell.text.strip():
                        aluno["coluna_" + str(i)] = "Rua Projetada"
                    else:
                        aluno["coluna_" + str(i)] = cell.text.strip()
            # Adicionar o sexo ao dicionário do aluno
            if aluno["coluna_1"] in cpf_selecionados:
                aluno["sexo"] = "Feminino"
            else:
                aluno["sexo"] = "Masculino"
            # Adicionar o dicionário à lista de alunos
            alunos.append(aluno)

# Exibir a lista de alunos
for aluno in alunos:
    print("CPF:", aluno["coluna_1"])
    print("Aluno:", aluno["coluna_2"])
    print("Endereço do aluno:", aluno["coluna_3"])
    print("Bairro do aluno:", aluno["coluna_4"])
    print("Data de nascimento:", aluno["coluna_5"])
    print("Sexo:", aluno["sexo"])
    print("-" * 30)

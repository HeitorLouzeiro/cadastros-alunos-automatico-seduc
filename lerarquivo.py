import docx


def extrairDados():
    # Abrir o arquivo docx
    doc = docx.Document(
        'E:/pythonProject/personalProjects/seleniumAutoCadAluno/alunos5Pessoas.docx')  # noqa

    # Criar uma lista vazia para armazenar as strings a serem ignoradas
    ignore_list = []

    # Adicionar as strings à lista usando um for loop
    for i in range(1, 10):
        ignore_list.append("TURMA " + str(i))

    # Definir os CPFs selecionados
    cpf_selecionados = ['064.864.333-61', '810.948.843-91', '032.343.253-08',
                        '023.175.543-03', '875.597.301-91', '018.897.993-00',
                        '520.524.003-20', '728.701.093-34', '789.608.003-68',
                        '040.876.003-60', '015.393.973-78', '011.254.951-97',
                        '984.656.603-44', '007.984.573-84', '995.828.303-44',
                        '856.839.493-00', '021.091.703-28', '019.399.953-61',
                        '510.167.533-49', '964.677.463-68', '699.221.953-72',
                        '322.492.763-15', '001.871.593-19', '068.983.113-79',
                        '833.726.013-00', '111.864.787-48', '017.176.083-29',
                        '392.960.911-87', '827.148.193-20', '034.274.253-12',
                        '007.392.383-45', '008.910.203-73', '021.103.943-82',
                        '001.244.933-43', '045.771.003-98', '005.544.443-13',
                        '399.370.201-82', '002.917.893-23', '035.811.673-28',
                        '577.882.863-20', '600.364.213-08', '071.614.623-12',
                        '025.761.151-79', '044.223.693-00', '725.026.141-04',
                        '021.671.683-73', '882.143.703-53', '055.004.371-35',
                        '493.099.601-59', '008.800.713-89', '076.330.131-09',
                        '399.771.451-72', '584.315.431-91', '044.223.693-00',
                        '725.026.141-04', '021.671.683-73', '882.143.703-53',
                        '055.004.371-35', '493.099.601-59', '008.800.713-89',
                        '076.330.131-09', '399.771.451-72', '584.315.431-91',
                        '067.613.743-16', '659.014.441-91', '694.824.893-49',
                        '939.516.983-49', '020.337.813-05', '216.772.803-44',
                        '909.786.413-53', '361.970.413-91', '002.608.023-01']

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
                    Pular a linha se ela contém uma string da
                    lista de ignore_list
                    '''
                    continue
                '''
                Criar um novo dicionário para armazenar
                as informações do aluno
                '''
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
    return alunos

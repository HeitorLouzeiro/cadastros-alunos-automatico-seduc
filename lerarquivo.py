import tkinter as tk
from tkinter import filedialog

import docx


def extrairDados():
    # Abrir o arquivo docx

    root = tk.Tk()
    root.withdraw()
    # Pede ao usuário para selecionar um arquivo
    file_path = filedialog.askopenfilename()

    # Abre o arquivo selecionado com o docx.Document
    doc = docx.Document(file_path)

    # Criar uma lista vazia para armazenar as strings a serem ignoradas
    ignore_list = []

    # Adicionar as strings à lista usando um for loop
    for i in range(1, 10):
        ignore_list.append("TURMA " + str(i))

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

                        if i == 6 and not cell.text.strip():
                            aluno["coluna_" + str(i)] = "Masculino"
                        else:
                            aluno["coluna_" + str(i)] = cell.text.strip()

                # Adicionar o dicionário à lista de alunos
                alunos.append(aluno)
    return alunos

from lerarquivo import extrairDados

print("Executando extrairDados()...")
informacoes = extrairDados()


def preencher_formulario(informacoes):
    # Exibir a lista de alunos

    for aluno in informacoes:
        print("CPF:", aluno["coluna_1"])
        print("Aluno:", aluno["coluna_2"])
        print("Endereço do aluno:", aluno["coluna_3"])
        print("Bairro do aluno:", aluno["coluna_4"])
        print("Data de nascimento:", aluno["coluna_5"])
        print("Sexo:", aluno["sexo"])
        print("-" * 30)


print("Executando preencher_formulario()...")
preencher_formulario(informacoes)

from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from lerarquivo import extrairDados

espaco = "-" * 50

# importando dados do arquivo leraquivo.py

# Chrome Options
# https://peter.sh/experiments/chromium-command-line-switches/


# Caminho para a raiz do projeto
ROOT_FOLDER = Path(__file__).parent
# Caminho para a pasta onde o chromedriver está
CHROME_DRIVER_PATH = ROOT_FOLDER / 'drivers' / 'chromedriver'


def make_chrome_browser(*options: str) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()

    # chrome_options.add_argument('--headless')
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)  # type: ignore

    chrome_service = Service(
        executable_path=str(CHROME_DRIVER_PATH),
    )

    browser = webdriver.Chrome(
        service=chrome_service,
        options=chrome_options
    )

    return browser

# Importe a função extrairDados() aqui, se necessário


def preencher_formulario(pessoas):
    # Exibir a lista de alunos
    for pessoa in pessoas:
        print("Nome:", pessoa["nome"])
        print("CPF:", pessoa["cpf"])
        print("Data de nascimento:", pessoa["data_nascimento"])
        print("Sexo:", pessoa["sexo"])
        print("Endereço:", pessoa["endereco"])
        print("Bairro:", pessoa["bairro"])
        print("-" * 30)


cpf_especifico = input("Digite o CPF do aluno de onde quer fazer a busca: ")

pessoas = []

deve_adicionar = False

print("Executando extrairDados()...")
informacoes = extrairDados()


for aluno in informacoes:
    pessoa = {
        "nome": aluno["coluna_2"],
        "cpf": aluno["coluna_1"],
        "data_nascimento": aluno["coluna_5"],
        "sexo": aluno["coluna_6"],
        "endereco": aluno["coluna_3"],
        "bairro": aluno["coluna_4"]
    }
    if cpf_especifico == aluno["coluna_1"]:
        deve_adicionar = True
    if deve_adicionar:
        pessoas.append(pessoa)


print("Executando preencher_formulario()...")
preencher_formulario(pessoas)


def url(url):
    browser.get(url)
    print(espaco)


def encontrarElemento(browser, tempo_de_espera, tipo_de_seletor, valor_do_seletor):  # noqa
    elemento = WebDriverWait(browser, tempo_de_espera).until(
        EC.presence_of_element_located(
            (tipo_de_seletor, valor_do_seletor)
        )
    )
    return elemento


def Login():
    print('Fazendo login.')
    print(espaco)

    UserName = input('Digite seu Usuario: ')
    Senha = input('Digite sua senha: ')
    print(espaco)

    inputUsuario = encontrarElemento(
        browser, TIME_TO_SLEEP_MEDIAN, By.ID, 'username')
    inputUsuario.send_keys(UserName)

    inputSenha = encontrarElemento(
        browser, TIME_TO_SLEEP_MEDIAN, By.ID, 'password')
    inputSenha.send_keys(Senha)
    inputSenha.send_keys(Keys.ENTER)
    print('Login feito com sucesso.')
    print(espaco)


def selecionandoOpcaoDiretor():
    print('Selecionando Opção diretor.')
    print(espaco)
    selecOptionDiretor = encontrarElemento(
        browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '//*[@id="login-page"]/div/div/div/div[2]/div/div/a[2]')  # noqa
    selecOptionDiretor.click()
    print('Opção selecionada com sucesso.')
    print(espaco)


def popUpSenha():
    selecDialogSenha = encontrarElemento(
        browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[8]')  # noqa
    selecDialogSenha.send_keys(Keys.ESCAPE)
    print('Pop up da senha fechado com sucesso.')
    print(espaco)


def selecionaEscola():
    print('Selecionando escola.')
    print(espaco)
    selecButtonAbrir = encontrarElemento(
        browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[3]/button')  # noqa
    selecButtonAbrir.click()
    print('Escola Selecionada com sucesso.')
    print(espaco)


def cadastroAluno():
    for pessoa in pessoas:
        print(f'Cadastrando pessoa {pessoa["nome"]} do CPF {pessoa["cpf"]}')
        print(espaco)
        # Preechendo o campo nome
        print('Preenchendo o nome do aluno.')
        print(espaco)
        inputName = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[1]/div[1]/md-input-container/input')  # noqa
        inputName.send_keys(pessoa["nome"])

        print('Nome preenchido com sucesso.')
        print(espaco)

        print('Preenchendo o CPF do aluno.')
        print(espaco)
        inputCPF = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[1]/div[2]/md-input-container/input')  # noqa
        inputCPF.send_keys(pessoa["cpf"])
        inputCPF.send_keys(Keys.TAB)
        print('CPF preenchido com sucesso.')
        print(espaco)

        try:
            inputExistente = encontrarElemento(browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[8]/md-dialog')  # noqa

            print('CPF já cadastrado no sistema')
            print(espaco)
            inputExistente.send_keys(Keys.ESCAPE)
            inputName.clear()
            inputCPF.clear()
            print(f'Pulando pessoa {pessoa["nome"]}')
            print(espaco)

            sleep(TIME_TO_SLEEP_SHORT)
        except TimeoutException:
            print('CPF não cadastrado no sistema')
            print(espaco)
            # preecheno campo data nascimento

            sleep(TIME_TO_SLEEP_SHORT)
            print('Preechendo Data de nascimento.')
            inputDataNasc = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[2]/div[2]/md-input-container/input')  # noqa
            inputDataNasc.send_keys(pessoa["data_nascimento"])
            print(espaco)

            print('Data de nascimento preenchida com sucesso.')
            print(espaco)

            sleep(TIME_TO_SLEEP_SHORT)

            # Selecionando o campo Cor/Raça
            inputCor = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[3]/div[1]/md-select')  # noqa

            inputCor.click()
            sleep(TIME_TO_SLEEP_SHORT)

            print('Selecionando a cor do aluno.')
            print(espaco)
            inputNaoDecla = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[8]/md-select-menu/md-content/md-option[1]')  # noqa
            inputNaoDecla.send_keys(Keys.ENTER)
            print('Selecionada Cor não declarada com sucesso.')
            print(espaco)

            # Selecionado option sexo do aluno
            print('Selecionando o sexo do aluno.')
            print(espaco)
            inputSexo = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[3]/div[2]/md-select')
            inputSexo.click()
            print(inputSexo.text)

            valorSexo = pessoa["sexo"].lower()
            if valorSexo == 'masculino':
                # selecionando Sexo Masculino
                Sexo = encontrarElemento(
                    browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[9]/md-select-menu/md-content/md-option[1]')  # noqa
                print('Selecionado sexo masculino com sucesso.')
            else:
                # selecionando Sexo Feminino
                Sexo = encontrarElemento(
                    browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[9]/md-select-menu/md-content/md-option[2]')
                print('Selecionado sexo feminino com sucesso.')

            sleep(TIME_TO_SLEEP_SHORT)
            Sexo.send_keys(Keys.ENTER)
            sleep(TIME_TO_SLEEP_SHORT)
            print(espaco)

            # selecionando Option o Nacionalidade
            inputNacionalidade = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[5]/div[1]/md-select')
            inputNacionalidade.click()

            print('Selecionando a nacionalidade do aluno.')
            print(espaco)

            # selecionando a nacionalidade brasileira
            inputNaturalidadeBrasileira = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[10]/md-select-menu/md-content/md-option[1]')

            print('Selecionada nacionalidade brasileira com sucesso.')
            sleep(TIME_TO_SLEEP_SHORT)
            inputNaturalidadeBrasileira.send_keys(Keys.ENTER)
            print(espaco)

            # selecionando option UF
            # selecionando o Naturalidade
            print('Selecionando o Estado do aluno.')
            inputNaturalidade = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[5]/div[2]/md-select')  # noqa

            inputNaturalidade.click()
            print(espaco)

            #  selecionando a nacionalidade piauiense
            inputNacionalidadePiaui = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[11]/md-select-menu/md-content/md-option[19]')
            print('Selecionada nacionalidade piauiense com sucesso.')
            sleep(TIME_TO_SLEEP_SHORT)

            inputNacionalidadePiaui.send_keys(Keys.ENTER)
            print(espaco)

            # selecionando Opcao da Cidade
            print('Selecionando a cidade do aluno.')
            inputCidade = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[5]/div[3]/md-select')  # noqa
            inputCidade.click()
            print(espaco)

            # selecionando a cidade de Corrente
            inputCidadeCorrente = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[12]/md-select-menu/md-content/md-option[65]')
            sleep(TIME_TO_SLEEP_SHORT)
            inputCidadeCorrente.send_keys(Keys.ENTER)
            print('Selecionada cidade de Corrente com sucesso.')
            print(espaco)

            # Preecnendo o campo Lagadouro
            print('Preenchendo o campo Lagadouro.')
            print(espaco)
            inputLagadouro = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[7]/div[2]/md-input-container/input')  # noqa
            inputLagadouro.send_keys(pessoa["endereco"])
            print('Lagadouro preenchido com sucesso.')
            print(espaco)

            # preenchendo o campo Bairro
            print('Preenchendo o campo Bairro.')
            print(espaco)

            inputBairro = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[8]/div[2]/md-input-container/input')  # noqa
            inputBairro.send_keys(pessoa["bairro"])
            sleep(TIME_TO_SLEEP_SHORT)
            print('Bairro preenchido com sucesso.')
            print(espaco)

            # selecionando o Opção Piaui
            print('Selecionando o estado do aluno.')
            inputEstado = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[1]/md-select')  # noqa
            inputEstado.click()
            print(espaco)

            # selecionando o estado Piaui
            inputEstadoPiaui = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[13]/md-select-menu/md-content/md-option[19]')
            inputEstadoPiaui.send_keys(Keys.ENTER)
            print('Selecionado o estado Piaui do aluno.')
            print(espaco)

            # Selecionando o Opção Cidade
            print('Selecionando a cidade do aluno.')
            inputCidade = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[2]/md-input-container/md-select')  # noqa
            inputCidade.click()
            print(espaco)

            # selecionando a cidade de Corrente
            inputCidadeCorrente = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[14]/md-select-menu/md-content/md-option[65]')
            inputCidadeCorrente.send_keys(Keys.ENTER)
            print('Selecionada cidade de Corrente com sucesso.')
            print(espaco)

            # Selecionando a Opção Zona
            print('Selecionando a zona do aluno.')
            inputZona = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[3]/md-input-container/md-select')
            inputZona.click()
            print(espaco)

            # Selecionando a zona urbana
            inputZonaUrbana = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[15]/md-select-menu/md-content/md-option[1]')
            inputZonaUrbana.send_keys(Keys.ENTER)
            print('Selecionada a zona urbana com sucesso.')
            print(espaco)

            # Selecionando a Opção Tipo de Residencia
            print('Selecionando o tipo de residencia do aluno.')
            inputLoc = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[4]/md-input-container/md-select')  # noqa
            inputLoc.click()

            # Selecionando não esta em area diferente
            inputNaoLoc = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[16]/md-select-menu/md-content/md-option[1]')
            inputNaoLoc.send_keys(Keys.ENTER)

            # Clicando no Botão Avançar
            print('Clicando no botão avançar.')
            print(espaco)
            inputAvancar = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[13]/div[2]/a')
            sleep(TIME_TO_SLEEP_SHORT)
            inputAvancar.click()

            # Clicando no Botão Cadastrar Aluno
            print('Clicando no botão cadastrar aluno.')
            print(espaco)
            inputCadastrarAluno = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/div/div/div/div/div/div/div[4]/div/div[4]/a')

            # inputCadastrarAluno.click()
            print('Aluno cadastrado com sucesso.')
            print(espaco)

            sleep(TIME_TO_SLEEP_SHORT)

            # Cadastrando Proximo aluno
            print('Cadastrando proximo aluno.')
            print(espaco)
            print('Direcionando para a pagina de Cadastro do aluno.')
            url('https://portal.seduc.pi.gov.br/#!/aluno/cadastro')

            sleep(TIME_TO_SLEEP_MEDIAN)

    print('Ultima pessoa cadastrada!')
    print('Fim!')
    browser.close()
    browser.quit()


if __name__ == '__main__':
    TIME_TO_SLEEP_SHORT = 2
    TIME_TO_SLEEP_MEDIAN = 5
    TIME_TO_SLEEP_LONG = 10
    # Example
    # options = '--headless', '--disable-gpu',
    options = ()
    browser = make_chrome_browser(*options)

    # Como antes
    print('Abrindo o site Seduc.')
    url('https://portal.seduc.pi.gov.br/#!/login')

    sleep(TIME_TO_SLEEP_SHORT)

    Login()

    sleep(TIME_TO_SLEEP_SHORT)

    # Selecionando opção diretor

    selecionandoOpcaoDiretor()

    sleep(TIME_TO_SLEEP_SHORT)

    # pop up da senha
    popUpSenha()

    sleep(TIME_TO_SLEEP_SHORT)

    # Clica no botão abrir
    selecionaEscola()

    sleep(TIME_TO_SLEEP_SHORT)

    print('Direcionando para a pagina de Cadastro do aluno.')
    url('https://portal.seduc.pi.gov.br/#!/aluno/cadastro')

    sleep(TIME_TO_SLEEP_SHORT)

    cadastroAluno()

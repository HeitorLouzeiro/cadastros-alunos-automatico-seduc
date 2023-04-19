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


cpf_especifico = "064.864.333-61"

pessoas = []

deve_adicionar = False

print("Executando extrairDados()...")
informacoes = extrairDados()


for aluno in informacoes:
    pessoa = {
        "nome": aluno["coluna_2"],
        "cpf": aluno["coluna_1"],
        "data_nascimento": aluno["coluna_5"],
        "sexo": aluno["sexo"],
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
    # UserName = input('Digite seu Usuario: ')
    UserName = '72776382120'
    Senha = '72776382120'
    # Senha = input('Digite sua senha: ')

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
            inputExistente.send_keys(Keys.ESCAPE)
            inputName.clear()
            inputCPF.clear()

            print(f'Pulando pessoa {pessoa["nome"]}')

            sleep(TIME_TO_SLEEP_SHORT)
        except TimeoutException:
            print('CPF não cadastrado no sistema')
            print(espaco)
            # preecheno campo data nascimento

            sleep(TIME_TO_SLEEP_MEDIAN)
            print('Preechendo Data de nascimento.')
            inputDataNasc = encontrarElemento(
                browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[2]/div[2]/md-input-container/input')  # noqa
            inputDataNasc.send_keys(pessoa["data_nascimento"])
            print(espaco)

            print('Data de nascimento preenchida com sucesso.')
            sleep(TIME_TO_SLEEP_SHORT)

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

    # for pessoa in pessoas:
    #     print(f'Cadastrando pessoa {pessoa["nome"]} do CPF {pessoa["cpf"]}')
    #     # Coloca valor na compo Nome
    #     inputName = encontrarElemento(
    #         browser, TIME_TO_SLEEP_MEDIAN, By.XPATH, '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[1]/div[1]/md-input-container/input')  # noqa
    #     inputName.send_keys(pessoa["nome"])

    #     sleep(TIME_TO_SLEEP_SHORT)

    #     # Coloca valor na compo CPF
    #     inputCPF = WebDriverWait(
    #         browser, TIME_TO_SLEEP_MEDIAN
    #     ).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH,
    #              '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[1]/div[2]/md-input-container/input')  # noqa
    #         )
    #     )
    #     inputCPF.send_keys(pessoa["cpf"])

    #     inputCPF.send_keys(Keys.TAB)

    #     sleep(TIME_TO_SLEEP_SHORT)

    #     # Verifca se o CPF já esta cadastrado no sistema
    #     # Coloca valor na compo CPF
    #     try:
    #         inputExistente = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[8]/md-dialog')
    #             )
    #         )
    #         print('CPF já cadastrado no sistema')
    #         inputExistente.send_keys(Keys.ESCAPE)
    #         inputName.clear()
    #         inputCPF.clear()

    #         print(f'Pulando pessoa {pessoa["nome"]}')

    #         sleep(TIME_TO_SLEEP_SHORT)
    #     except TimeoutException:
    #         print('CPF não cadastrado no sistema')

    #         inputDataNasc = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[2]/div[2]/md-input-container/input')  # noqa
    #             )
    #         )
    #         inputDataNasc.send_keys(pessoa["data_nascimento"])
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         # selecionando o Cor
    #         inputCor = WebDriverWait(
    #             browser, 3600
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[3]/div[1]/md-select')  # noqa
    #             )
    #         )
    #         inputCor.click()
    #         # selecionando Não declarado
    #         inputNaoDecla = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[8]/md-select-menu/md-content/md-option[1]')
    #             )
    #         )
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         inputNaoDecla.send_keys(Keys.ENTER)
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         # selecionando o Sexo
    #         inputSexo = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[3]/div[2]/md-select')  # noqa
    #             )
    #         )
    #         inputSexo.click()
    #         print(inputSexo.text)
    #         valorSexo = pessoa["sexo"].lower()
    #         if valorSexo == 'masculino':
    #             # selecionando Sexo Masculino
    #             inputSexo = WebDriverWait(
    #                 browser, TIME_TO_SLEEP_MEDIAN
    #             ).until(
    #                 EC.presence_of_element_located(
    #                     (By.XPATH,
    #                      '/html/body/div[9]/md-select-menu/md-content/md-option[1]')
    #                 )
    #             )
    #         else:
    #             # selecionando Sexo Feminino
    #             inputSexo = WebDriverWait(
    #                 browser, TIME_TO_SLEEP_MEDIAN
    #             ).until(
    #                 EC.presence_of_element_located(
    #                     (By.XPATH,
    #                      '/html/body/div[9]/md-select-menu/md-content/md-option[2]')
    #                 )
    #             )
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         inputSexo.send_keys(Keys.ENTER)
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         # selecionando o Nacionalidade
    #         inputNacionalidade = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[5]/div[1]/md-select')  # noqa
    #             )
    #         )
    #         inputNacionalidade.click()
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         # selecionando a nacionalidade brasileira
    #         inputNaturalidadeBrasileira = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[10]/md-select-menu/md-content/md-option[1]')
    #             )
    #         )
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         inputNaturalidadeBrasileira.send_keys(Keys.ENTER)
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         # selecionando o Naturalidade
    #         inputNacionalidade = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[5]/div[2]/md-select')  # noqa
    #             )
    #         )
    #         inputNacionalidade.click()
    #         # selecionando a nacionalidade piauiense
    #         inputNacionalidadePiaui = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[11]/md-select-menu/md-content/md-option[19]')
    #             )
    #         )
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         inputNacionalidadePiaui.send_keys(Keys.ENTER)
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         # selecionando o Naturalidade Cidade
    #         inputNaturalidadeCidade = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[5]/div[3]/md-select')  # noqa
    #             )
    #         )
    #         inputNaturalidadeCidade.click()
    #         # selecionando a nacionalidade piauiense
    #         # TODO: verificar se a cidade existe
    #         inputNacionalidadeCorrente = WebDriverWait(
    #             browser, 3600
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[12]/md-select-menu/md-content/md-option[65]')
    #             )
    #         )
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         inputNacionalidadeCorrente.send_keys(Keys.ENTER)
    #         print('Cidade selecionada')
    #         print(inputNacionalidadeCorrente.text)
    #         selecionacorrente = inputNacionalidadeCorrente.text

    #         if (selecionacorrente == 'CORRENTE'):
    #             print('Cidade encontrada de primeira')

    #         else:
    #             print('Cidade não encontrada, selecionando outra')
    #             idcidade = 187
    #             while (selecionacorrente != 'CORRENTE'):
    #                 inputNaturalidadeCidade = WebDriverWait(
    #                     browser, TIME_TO_SLEEP_MEDIAN
    #                 ).until(
    #                     EC.presence_of_element_located(
    #                         (By.XPATH,
    #                         '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[5]/div[3]/md-select')  # noqa
    #                     )
    #                 )
    #                 inputNaturalidadeCidade.click()
    #                 idcidade = idcidade + 1
    #                 inputNacionalidadeCorrente = WebDriverWait(
    #                     browser, TIME_TO_SLEEP_MEDIAN
    #                 ).until(
    #                     EC.presence_of_element_located(
    #                         (By.ID, 'select_option_' + str(idcidade))
    #                     )
    #                 )
    #                 sleep(TIME_TO_SLEEP_MEDIAN)
    #                 inputNacionalidadeCorrente.send_keys(Keys.ENTER)
    #                 selecionacorrente = inputNacionalidadeCorrente.text
    #                 print('Cidade selecionada')
    #                 print(inputNacionalidadeCorrente.text)

    #         inputLagradouro = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[7]/div[2]/md-input-container/input')  # noqa
    #             )
    #         )
    #         inputLagradouro.send_keys(pessoa["endereco"])
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         inputBairro = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[8]/div[2]/md-input-container/input')  # noqa
    #             )
    #         )
    #         inputBairro.send_keys(pessoa["bairro"])
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         # selecionando o estado
    #         inputEstado = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[1]/md-select')  # noqa
    #             )
    #         )
    #         inputEstado.click()
    #         # selecionando o estado PI
    #         inputEstadoPiuai = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[13]/md-select-menu/md-content/md-option[19]')
    #             )
    #         )
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         inputEstadoPiuai.send_keys(Keys.ENTER)
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         # selecionando o Municipio
    #         inputMunicipio = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[2]/md-input-container/md-select')  # noqa
    #             )
    #         )
    #         inputMunicipio.click()
    #         # selecionando Corrente
    #         # TODO VERIFICANDO SE O MUNICIPIO É CORRENTE
    #         inputCorrente = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[14]/md-select-menu/md-content/md-option[65]')
    #             )
    #         )
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         inputCorrente.send_keys(Keys.ENTER)
    #         print('Cidade selecionada')
    #         print(inputCorrente.text)
    #         selecionacorrente = inputCorrente.text

    #         if (selecionacorrente == 'CORRENTE'):
    #             print('Cidade encontrada de primeira')

    #         else:
    #             print('Cidade não encontrada, selecionando outra')
    #             idcidade = 411
    #             while (selecionacorrente != 'CORRENTE'):
    #                 inputCorrente = WebDriverWait(
    #                     browser, TIME_TO_SLEEP_MEDIAN
    #                 ).until(
    #                     EC.presence_of_element_located(
    #                         (By.XPATH,
    #                         '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[2]/md-input-container/md-select')  # noqa
    #                     )
    #                 )
    #                 inputCorrente.click()
    #                 idcidade = idcidade + 1
    #                 inputCorrente = WebDriverWait(
    #                     browser, TIME_TO_SLEEP_MEDIAN
    #                 ).until(
    #                     EC.presence_of_element_located(
    #                         (By.ID, 'select_option_' + str(idcidade))
    #                     )
    #                 )
    #                 sleep(TIME_TO_SLEEP_MEDIAN)
    #                 inputCorrente.send_keys(Keys.ENTER)
    #                 selecionacorrente = inputCorrente.text
    #                 print('Cidade selecionada')
    #                 print(inputCorrente.text)

    #         sleep(TIME_TO_SLEEP_SHORT)
    #         # selecionando o Zona
    #         inputZona = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[3]/md-input-container/md-select')  # noqa
    #             )
    #         )
    #         inputZona.click()
    #         # selecionando Corrente
    #         inputZonaUrbana = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[15]/md-select-menu/md-content/md-option[1]')
    #             )
    #         )
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         inputZonaUrbana.send_keys(Keys.ENTER)
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         # selecionando o Localização diferente
    #         inputLoc = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[4]/md-input-container/md-select')  # noqa
    #             )
    #         )
    #         inputLoc.click()
    #         # selecionando não esta em area diferente
    #         inputNaoLoc = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[16]/md-select-menu/md-content/md-option[1]')
    #             )
    #         )
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         inputNaoLoc.send_keys(Keys.ENTER)
    #         sleep(TIME_TO_SLEEP_SHORT)

    #         # Clica no botão de avançar
    #         selecButtonAvancaAluno = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[13]/div[2]/a')  # noqa
    #             )
    #         )
    #         selecButtonAvancaAluno.click()
    #         sleep(TIME_TO_SLEEP_SHORT)

    #         # clicando no botão de casdastrar
    #         selecButtonAvancaAluno = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH,
    #                  '/html/body/div[2]/div/section/div/div[2]/div/div/div/div/div/div/div[4]/div/div[4]/a')  # noqa
    #             )
    #         )
    #         selecButtonAvancaAluno.click()
    #         sleep(TIME_TO_SLEEP_SHORT)
    #         print('Indo para o Proximo cadastro')
    #         sleep(TIME_TO_SLEEP_MEDIAN)
    #         browser.get(
    #             'https://portal.seduc.pi.gov.br/#!/escola/dashboard')

    #         sleep(TIME_TO_SLEEP_SHORT)

    #         # Clicar no botão de cadastro Aluno
    #         selecButtonCadastroAluno = WebDriverWait(
    #             browser, TIME_TO_SLEEP_MEDIAN
    #         ).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH, '//*[@id="slide-out"]/li[11]/a')
    #             )
    #         )

    #         selecButtonCadastroAluno.click()
    #         print('Cadastrando o proximo aluno')

    # print('Ultima pessoa cadastrada!')
    # print('Fim!')
    # browser.quit()

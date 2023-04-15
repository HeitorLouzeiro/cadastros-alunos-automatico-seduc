import os
from pathlib import Path
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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


if __name__ == '__main__':
    TIME_TO_SLEEP_SHORT = 3
    TIME_TO_SLEEP_MEDIAN = 10
    TIME_TO_SLEEP_LONG = 20
    # Example
    # options = '--headless', '--disable-gpu',
    options = ()
    browser = make_chrome_browser(*options)

    pessoas = [
        {
            "nome": "NILVA GUEDES DE SOUZA",
            "cpf": "",
            "data_nascimento": "24/07/1992",
            "sexo": "FEMININO",
            "endereco": "RUA BUQUEIRĂO",
            "bairro": "VERMELHÃO",

            # adicione mais informações que você precise
        },
        {
            "nome": "ISAQUE DIAS DO NASCIMENTO",
            "cpf": "",
            "sexo": "MASCULINO",
            "data_nascimento": "15/05/1983",
            "endereco": "RUA PROJETADA 06",
            "bairro": "VERMELHÃO",
            # adicione mais informações que você precise
        },
        {
            "nome": "LUZIA MARIA VIEIRA DE SOUZA",
            "cpf": "",
            "sexo": "Feminino",
            "data_nascimento": "13/12/1954",
            "endereco": "RUA SĂO JOSÉ",
            "bairro": "VERMELHÃO",
            # adicione mais informações que você precise
        },

    ]

    # Como antes
    browser.get('https://portal.seduc.pi.gov.br/#!/aluno/cadastro-finalizar')
    sleep(TIME_TO_SLEEP_SHORT)

    # Aguarda o elemento aparecer
    # https://selenium-python.readthedocs.io/waits.html
    load_dotenv()
    loginSenha = os.environ.get('loginSenha')

    inputUsuario = WebDriverWait(browser, TIME_TO_SLEEP_MEDIAN).until(
        EC.presence_of_element_located(
            (By.ID, 'username')
        )
    )
    inputUsuario.send_keys(loginSenha)

    inputSenha = WebDriverWait(browser, TIME_TO_SLEEP_MEDIAN).until(
        EC.presence_of_element_located(
            (By.ID, 'password')
        )
    )
    inputSenha.send_keys(loginSenha)

    sleep(TIME_TO_SLEEP_SHORT)

    # Clica no botão para entrar
    inputSenha.send_keys(Keys.ENTER)

    sleep(TIME_TO_SLEEP_SHORT)

    selecOptionDiretor = WebDriverWait(browser, TIME_TO_SLEEP_MEDIAN).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="login-page"]/div/div/div/div[2]/div/div/a[2]')
        )
    )
    selecOptionDiretor.click()

    sleep(TIME_TO_SLEEP_SHORT)

    # pop up da senha
    selecDialogSenha = WebDriverWait(browser, TIME_TO_SLEEP_MEDIAN).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[8]')
        )
    )
    selecDialogSenha.send_keys(Keys.ESCAPE)

    sleep(TIME_TO_SLEEP_SHORT)

    # Clica no botão abrir
    selecButtonAbrir = WebDriverWait(browser, TIME_TO_SLEEP_MEDIAN).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[3]/button')
        )
    )
    selecButtonAbrir.click()

    sleep(TIME_TO_SLEEP_SHORT)

    # Clicar no botão de cadastro Aluno
    selecButtonCadastroAluno = WebDriverWait(
        browser, TIME_TO_SLEEP_MEDIAN
    ).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="slide-out"]/li[11]/a')
        )
    )

    selecButtonCadastroAluno.click()
    sleep(TIME_TO_SLEEP_SHORT)
    for pessoa in pessoas:
        print(f'Cadastrando pessoa {pessoa["nome"]}')
        # Coloca valor na compo nome
        inputName = WebDriverWait(
            browser, TIME_TO_SLEEP_MEDIAN
        ).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[1]/div[1]/md-input-container/input')  # noqa
            )
        )
        inputName.send_keys(pessoa["nome"])

        sleep(TIME_TO_SLEEP_SHORT)

        # Coloca valor na compo CPF
        inputCPF = WebDriverWait(
            browser, TIME_TO_SLEEP_MEDIAN
        ).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[1]/div[2]/md-input-container/input')  # noqa
            )
        )
        inputCPF.send_keys(pessoa["cpf"])

        sleep(TIME_TO_SLEEP_SHORT)

        inputCPF.send_keys(Keys.TAB)

        sleep(TIME_TO_SLEEP_SHORT)

        # Verifca se o CPF já esta cadastrado no sistema
        # Coloca valor na compo CPF
        try:
            inputExistente = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[8]/md-dialog')
                )
            )
            print('CPF já cadastrado no sistema')
            inputExistente.send_keys(Keys.ESCAPE)
            inputName.clear()
            inputCPF.clear()
        except TimeoutException:
            print('CPF não cadastrado no sistema')

            inputDataNasc = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[2]/div[2]/md-input-container/input')  # noqa
                )
            )
            inputDataNasc.send_keys(pessoa["data_nascimento"])
            sleep(TIME_TO_SLEEP_SHORT)
            # selecionando o Cor
            inputCor = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[3]/div[1]/md-select')  # noqa
                )
            )
            inputCor.click()
            # selecionando Não declarado
            inputNaoDecla = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.ID,
                     'select_option_49')
                )
            )
            sleep(TIME_TO_SLEEP_SHORT)
            inputNaoDecla.send_keys(Keys.ENTER)
            sleep(TIME_TO_SLEEP_SHORT)
            # selecionando o Sexo
            inputSexo = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[3]/div[2]/md-select')  # noqa
                )
            )
            inputSexo.click()
            valorSexo = pessoa["sexo"].lower()
            if valorSexo == 'masculino':
                # selecionando Sexo Masculino
                inputSexo = WebDriverWait(
                    browser, TIME_TO_SLEEP_MEDIAN
                ).until(
                    EC.presence_of_element_located(
                        (By.ID,
                         'select_option_47')
                    )
                )
            else:
                # selecionando Sexo Feminino
                inputSexo = WebDriverWait(
                    browser, TIME_TO_SLEEP_MEDIAN
                ).until(
                    EC.presence_of_element_located(
                        (By.ID,
                         'select_option_48')
                    )
                )
            sleep(TIME_TO_SLEEP_SHORT)
            inputSexo.send_keys(Keys.ENTER)
            sleep(TIME_TO_SLEEP_SHORT)
            # selecionando o Nacionalidade
            inputNacionalidade = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[5]/div[1]/md-select')  # noqa
                )
            )
            inputNacionalidade.click()
            sleep(TIME_TO_SLEEP_SHORT)
            # selecionando a nacionalidade brasileira
            inputNaturalidadeBrasileira = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.ID,
                     'select_option_117')
                )
            )
            sleep(TIME_TO_SLEEP_SHORT)
            inputNaturalidadeBrasileira.send_keys(Keys.ENTER)
            sleep(TIME_TO_SLEEP_SHORT)
            # selecionando o Naturalidade
            inputNacionalidade = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[5]/div[2]/md-select')  # noqa
                )
            )
            inputNacionalidade.click()
            # selecionando a nacionalidade piauiense
            inputNacionalidadePiaui = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.ID,
                     'select_option_75')
                )
            )
            sleep(TIME_TO_SLEEP_SHORT)
            inputNacionalidadePiaui.send_keys(Keys.ENTER)
            sleep(TIME_TO_SLEEP_SHORT)
            # selecionando o Naturalidade Cidade
            inputNaturalidadeCidade = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[5]/div[3]/md-select')  # noqa
                )
            )
            inputNaturalidadeCidade.click()
            # selecionando a nacionalidade piauiense
            inputNacionalidadeCorrente = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.ID,
                     'select_option_189')
                )
            )
            sleep(TIME_TO_SLEEP_SHORT)
            inputNacionalidadeCorrente.send_keys(Keys.ENTER)
            sleep(TIME_TO_SLEEP_SHORT)
            inputLagradouro = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[7]/div[2]/md-input-container/input')  # noqa
                )
            )
            inputLagradouro.send_keys(pessoa["endereco"])
            sleep(TIME_TO_SLEEP_SHORT)
            inputBairro = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[8]/div[2]/md-input-container/input')  # noqa
                )
            )
            inputBairro.send_keys(pessoa["bairro"])
            sleep(TIME_TO_SLEEP_SHORT)
            # selecionando o estado
            inputEstado = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[1]/md-select')  # noqa
                )
            )
            inputEstado.click()
            # selecionando o estado PI
            inputEstadoPiuai = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.ID,
                     'select_option_103')
                )
            )
            sleep(TIME_TO_SLEEP_SHORT)
            inputEstadoPiuai.send_keys(Keys.ENTER)
            sleep(TIME_TO_SLEEP_SHORT)
            # selecionando o Municipio
            inputMunicipio = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[2]/md-input-container/md-select')  # noqa
                )
            )
            inputMunicipio.click()
            # selecionando Corrente
            inputCorrente = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.ID,
                     'select_option_413')
                )
            )
            sleep(TIME_TO_SLEEP_SHORT)
            inputCorrente.send_keys(Keys.ENTER)
            sleep(TIME_TO_SLEEP_SHORT)
            # selecionando o Zona
            inputZona = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[3]/md-input-container/md-select')  # noqa
                )
            )
            inputZona.click()
            # selecionando Corrente
            inputZonaUrbana = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.ID,
                     'select_option_55')
                )
            )
            sleep(TIME_TO_SLEEP_SHORT)
            inputZonaUrbana.send_keys(Keys.ENTER)
            sleep(TIME_TO_SLEEP_SHORT)
            # selecionando o Localização diferente
            inputLoc = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[9]/div[4]/md-input-container/md-select')  # noqa
                )
            )
            inputLoc.click()
            # selecionando não esta em area diferente
            inputNaoLoc = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.ID,
                     'select_option_120')
                )
            )
            sleep(TIME_TO_SLEEP_SHORT)
            inputNaoLoc.send_keys(Keys.ENTER)
            sleep(TIME_TO_SLEEP_SHORT)
            selecButtonAvancaAluno = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/form/div/div/div/div/div/div[13]/div[2]/a')  # noqa
                )
            )
            selecButtonAvancaAluno.click()
            sleep(TIME_TO_SLEEP_SHORT)

            # clicando no botão de casdastrar
            selecButtonAvancaAluno = WebDriverWait(
                browser, TIME_TO_SLEEP_MEDIAN
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div[2]/div/section/div/div[2]/div/div/div/div/div/div/div[4]/div/div[4]/a')  # noqa
                )
            )
            # selecButtonAvancaAluno.click()
            sleep(TIME_TO_SLEEP_SHORT)

            browser.get(
                'https://portal.seduc.pi.gov.br/#!/aluno/cadastro')

            sleep(TIME_TO_SLEEP_SHORT)
            print('Indo para o Proximo cadastro')

    print('Ultima pessoa cadastrada!')
    print('Fim!')
    browser.quit()

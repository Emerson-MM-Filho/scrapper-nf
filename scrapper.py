import argparse
from typing import Dict, List
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from operations import CliOperation, CliOperationsEnum

parser = argparse.ArgumentParser(
    prog="scrapper.py",
    epilog="See repo: https://github.com/Emerson-MM-Filho/scrapper-nf-sc",
    description="Scrapper Nota Fiscal Eletrônica Florianópolis.",
    fromfile_prefix_chars="@"
)

parser.add_argument(
    "-cmc",
    "--codigomunicipal",
    type=int,
    help="Código municipal",
    dest="cmc",
    required=True,
)
parser.add_argument(
    "-e",
    "--email",
    type=str,
    help="Email",
    dest="email",
    required=True,
)
parser.add_argument(
    "-p",
    "--password",
    type=str,
    help="Senha",
    dest="password",
    required=True,
)

args = parser.parse_args()

url = "https://nfps-e.pmf.sc.gov.br/frontend/#!/login"

driver = webdriver.Chrome()

driver.get(url)
login_buttons = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_elements(By.CLASS_NAME, "label-recarrega")
)

login_button_list = list(
    filter(
        lambda elem: "Realizar login sem certificado digital" in elem.text,
        login_buttons
    )
)

login_button = None
if login_button_list:
    login_button = login_button_list[0]

if not login_button:
    raise Exception("Login button not founded")

login_button.click()

login_field_settings = {
    "usuario": args.cmc,
    "email": args.email,
    "senha": args.password,
}

for field_name, value in login_field_settings.items():
    element = WebDriverWait(driver, timeout=10).until(
        lambda driver: driver.find_element(By.NAME, field_name)
    )
    if not element:
        raise Exception(f"{field_name.title()} button not founded")
    element.send_keys(value)

submit_button = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.ID, "entrar")
)

if not submit_button:
    raise Exception("Submit button not founded")
submit_button.click()

consult_button = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.XPATH, '//*[@id="transmitidas"]/form/div/div[5]/button')
)

if not consult_button:
    raise Exception("Consultar button not founded")

consult_button.click()

options_button = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.XPATH, '//*[@id="transmitidas"]/table/tbody/tr[1]/td[11]/div/button')
)

if not options_button:
    raise Exception("Consultar button not founded")

options_button.click()

clone_button = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.XPATH, '//*[@id="transmitidas"]/table/tbody/tr[1]/td[11]/div/ul/li[2]/a')
)

if not clone_button:
    raise Exception("Consultar button not founded")

clone_button.click()

tipo_nota_select = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.ID, "inputAedf")
)

if not tipo_nota_select:
    raise Exception("Tipo nota select not founded")

tipo_nota_select.click()

tipo_nota_options = tipo_nota_select.find_elements(By.TAG_NAME, "option")

correct_option_list = list(
    filter(
        lambda option: option.get_attribute('value') == "0676722",
        tipo_nota_options
    )
)

correct_option = None
if correct_option_list:
    correct_option = correct_option_list[0]

if not correct_option:
    raise Exception("Login button not founded")

correct_option.click()

emissao_input = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.ID, "inputDataEmissao")
)
if not emissao_input:
    raise Exception(f"Data Emissão input not founded")

date = datetime.now()
date_str = date.strftime("%d/%m/%Y")
emissao_input.send_keys(date_str)

confirm_button = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[2]/button[2]')
)

if not confirm_button:
    raise Exception("Confirmar button not founded")

confirm_button.click()

continue_button_1 = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.XPATH, '//*[@id="content-new-register"]/div/div[6]/div/div[3]/div[1]/form/div[6]/button[2]')
)

if not continue_button_1:
    raise Exception("Continuar button 1 not founded")

continue_button_1.click()

confirm_cfps_button = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[2]/button[2]')
)

if not confirm_cfps_button:
    raise Exception("Confirma CFPS button not founded")

confirm_cfps_button.click()

continue_button_2 = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.XPATH, '//*[@id="content-new-register"]/div/div[6]/div/div[2]/form/div[2]/button[3]')
)

if not continue_button_2:
    raise Exception("Continuar button 2 button not founded")

continue_button_2.click()

transmit_button = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.ID, 'transmitir')
)

if not transmit_button:
    raise Exception("Transmitir button not founded")

transmit_button.click()

submit_message = WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(By.XPATH, '//*[@id="transmitidas"]/form/div[1]')
)

if not submit_message:
    raise Exception("Submit message not founded")

if "Nota fiscal transmitida com sucesso. E-mail enviado com sucesso." not in submit_message.text:
    raise Exception(f"Falha na submissão da Nota Fiscal ({submit_message.text})")

while(True):
    pass
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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
    "usuario": "usuario",
    "email": "email",
    "senha": "senha",
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


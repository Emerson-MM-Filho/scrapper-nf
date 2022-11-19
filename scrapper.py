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


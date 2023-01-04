import os
import exceptions as scrapper_exceptions
from datetime import datetime
from typing import Dict, List, Union
from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CancelAction(Exception):
    pass

class Scrapper(object):
    DOWNLOAD_DIRECTORY = F"{BASE_DIR}\\downloads"
    DEFAULT_FIND_ELEMENT_TIME_OUT = 15
    URL: str = "https://nfps-e.pmf.sc.gov.br/frontend/#!/login"

    def __init__(self, cmc: str, email: str, password: str):
        options = Options()
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self.DOWNLOAD_DIRECTORY,
            },
        )
        self.driver: WebDriver = webdriver.Chrome(options=options)
        self.login_field_settings: Dict = {
            "usuario": cmc,
            "email": email,
            "senha": password,
        }

    def login(self):
        """
            Make login at fiscal note platform
            Raise ElementNotFounded if any element not founded
        """
        self.driver.get(self.URL)
        login_button = self.find_element(By.XPATH, "/html/body/div[2]/div/div/form/div[10]/div", "Login button")
        login_button.click()

        for field_name, value in self.login_field_settings.items():
            element = WebDriverWait(self.driver, timeout=10).until(
                lambda driver: driver.find_element(By.NAME, field_name)
            )
            if not element: raise scrapper_exceptions.ElementNotFoundedException(f"{field_name} input")
            element.send_keys(value)

        submit_login_button = self.find_element(By.ID, "entrar", "Submit login button")
        submit_login_button.click()

    def run_consult(
        self,
        taker_document: Union[str, None] = None,
        taker_name: Union[str, None] = None,
        start_date: Union[str, None] = None,
        end_date: Union[str, None] = None
    ):
        """
            Consult fiscal notes
            Param taker_document recieve only numbers.
                Ex.:
                    CNPJ -> 53445313000110
                    CPF -> 90038336057
            Accepted format for start_date, end_date params -> "%d/%m/Y"
        """
        if taker_document is not None: 
            taker_document_input = self.find_element(By.ID, "inputSearchDocTomador", "Taker document input")
            taker_document_input.send_keys(taker_document)
        if taker_name is not None:
            taker_name_input = self.find_element(By.ID, "inputSearchNomeTomador", "Taker name input")
            taker_name_input.send_keys(taker_name)
        if start_date is not None:
            start_date_input = self.find_element(By.ID, "inputSearchIniEmissao", "Start date input")
            start_date_input.send_keys(start_date)
        if end_date is not None:
            end_date_input = self.find_element(By.ID, "inputSearchFimEmissao", "End date input")
            end_date_input.send_keys(end_date)

        consult_button = self.find_element(By.XPATH, '//*[@id="transmitidas"]/form/div/div[5]/button', "Consult button")
        consult_button.click()

    def find_element(self, by: str, value: str, name: str) -> WebElement:
        """
            Return an element
            Raise ElementNotFoundedException if not founded
        """
        try:
            element = WebDriverWait(self.driver, timeout=self.DEFAULT_FIND_ELEMENT_TIME_OUT).until(
                lambda driver: driver.find_element(by, value)
            )
        except selenium_exceptions.TimeoutException:
            raise scrapper_exceptions.ElementNotFoundedException(name)

        if not element: raise scrapper_exceptions.ElementNotFoundedException(name)
        return element

    def find_elements(self, by: str, value: str, name: str) -> List[WebElement]:
        """
            Return a list of elements
            Raise ElementNotFoundedException if not founded
        """
        try:
            element = WebDriverWait(self.driver, timeout=self.DEFAULT_FIND_ELEMENT_TIME_OUT).until(
                lambda driver: driver.find_elements(by, value)
            )
        except selenium_exceptions.TimeoutException:
            raise scrapper_exceptions.ElementNotFoundedException(name)

        if not element: raise scrapper_exceptions.ElementNotFoundedException(name)
        return element

    def get_consult_result(self) -> List[WebElement]:
        """
            Return a list containing the fiscal notes foundeds on the consult
            Raise ElementNotFoundedException if not founded
        """
        return self.find_elements(By.XPATH, '//*[@id="transmitidas"]/table/tbody/tr', "Consult result rows")

    def get_last_consult_result(self) -> WebElement:
        """
            Return the last fiscal note founded at result
            Raise ElementNotFoundedException if not founded
        """
        return self.get_consult_result()[0]

    def download_last_consult_result(self) -> None:
        """
            Download the last fiscal note to DOWNLOAD_DIRECTORY
            Raise ElementNotFoundedException if last fical note not founded
        """
        self.run_consult()
        last_result = self.get_last_consult_result()
        download_button = last_result.find_element(By.XPATH, "//*/td/a")
        download_button.click()

    def clone_last_consult_result(self, request_confirmation: bool) -> None:
        """
            Clone the last fiscal note founded at consult
            Raise ElementNotFoundedException if any element not founded
            Raise FiscalNoteException if any element not founded
        """
        self.run_consult()
        options_button = self.get_last_consult_result().find_element(By.XPATH, "//*/td/div/button")
        options_button.click()

        clone_button = self.get_last_consult_result().find_element(By.XPATH, '//*/td/div/ul/li[2]/a')
        clone_button.click()

        tipo_nota_select = self.find_element(By.ID, "inputAedf", "AEDF input")
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

        if not correct_option: raise scrapper_exceptions.ElementNotFoundedException("AEDF option 0676722")
        correct_option.click()

        emissao_input = self.find_element(By.ID, "inputDataEmissao", "Emission date input")
        date = datetime.now()
        date_str = date.strftime("%d/%m/%Y")
        emissao_input.send_keys(date_str)

        confirm_button = self.find_element(By.XPATH, "//*/form/div/button[2]", "Confirm duplication button")
        confirm_button.click()

        taker_data_continue_button = self.find_element(By.XPATH, "//*/div[1]/form/div[6]/button[2]", "Taker data continue button")
        taker_data_continue_button.click()

        confirm_cfps_button = self.find_element(By.XPATH, "//*/div/form/div[2]/button[2]", "Confirm CFPS button")
        confirm_cfps_button.click()

        service_data_continue_button = self.find_element(By.XPATH, "//*/div[2]/form/div[2]/button[3]", "Service data continue button")
        service_data_continue_button.click()

        if request_confirmation:
            confirmation = input("Type 'Y' to continue or 'N' to cancel: ")
            if confirmation.upper() != "Y":
                raise CancelAction("Confirmation refused")

        transmit_button = self.find_element(By.ID, "transmitir", "Transmit button")
        transmit_button.click()

        submit_message = self.find_element(By.XPATH, '//*[@id="transmitidas"]/form/div[1]', "Submit message")
        if "Nota fiscal transmitida com sucesso. E-mail enviado com sucesso." not in submit_message.text:
            raise scrapper_exceptions.FiscalNoteException("Clone", f"Falha na submissão da Nota Fiscal ({submit_message.text})")

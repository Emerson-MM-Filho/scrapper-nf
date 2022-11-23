class ElementNotFoundedException(Exception):
    def __init__(self, element_name: str):
        self.element_name: str = element_name

    @property
    def error_message(self) -> str:
        return f"Element not founded: {self.element_name.title()}"

class FiscalNoteException(Exception):
    def __init__(self, action: str, error: str):
        self.action: str = action
        self.error: str = error

    @property
    def error_message(self) -> str:
        return f"{self.action} - {self.error_message}"
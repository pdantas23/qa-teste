from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from core.web.base_page import PaginaBase


class PaginaLogin(PaginaBase):
    _CAMPO_USUARIO = (By.ID, "user-name")
    _CAMPO_SENHA = (By.ID, "password")
    _BOTAO_LOGIN = (By.ID, "login-button")
    _MENSAGEM_ERRO = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        driver.get("https://www.saucedemo.com")

    def fazer_login(self, usuario: str, senha: str) -> "PaginaInventario":
        from pages.inventory_page import PaginaInventario
        self._digitar(self._CAMPO_USUARIO, usuario)
        self._digitar(self._CAMPO_SENHA, senha)
        self._clicar(self._BOTAO_LOGIN)
        self._aguardar_url_conter("inventory")
        return PaginaInventario(self._driver)

    def tentar_login(self, usuario: str, senha: str) -> "PaginaLogin":
        self._digitar(self._CAMPO_USUARIO, usuario)
        self._digitar(self._CAMPO_SENHA, senha)
        self._clicar(self._BOTAO_LOGIN)
        return self

    def obter_mensagem_erro(self) -> str:
        return self._obter_texto(self._MENSAGEM_ERRO)

    def tem_mensagem_erro(self) -> bool:
        return self._esta_visivel(self._MENSAGEM_ERRO)

from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from loguru import logger
from config.configuracoes import configuracoes

Localizador = Tuple[By, str]


class PaginaBase:
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._espera = WebDriverWait(driver, timeout=configuracoes.TIMEOUT_PADRAO)

    def _encontrar(self, localizador: Localizador) -> WebElement:
        return self._espera.until(EC.presence_of_element_located(localizador))

    def _encontrar_clicavel(self, localizador: Localizador) -> WebElement:
        return self._espera.until(EC.element_to_be_clickable(localizador))

    def _clicar(self, localizador: Localizador) -> None:
        elemento = self._encontrar_clicavel(localizador)
        self._driver.execute_script("arguments[0].click();", elemento)

    def _clicar_js(self, localizador: Localizador) -> None:
        self._clicar(localizador)

    def _digitar(self, localizador: Localizador, texto: str) -> None:
        elemento = self._encontrar_clicavel(localizador)
        self._driver.execute_script(
            "var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
            "s.call(arguments[0],arguments[1]);"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
            elemento,
            texto,
        )

    def _obter_texto(self, localizador: Localizador) -> str:
        return self._encontrar(localizador).text

    def _esta_visivel(self, localizador: Localizador) -> bool:
        try:
            self._espera.until(EC.visibility_of_element_located(localizador))
            return True
        except Exception:
            return False

    def _aguardar_url_conter(self, fragmento: str) -> None:
        self._espera.until(EC.url_contains(fragmento))

    def tirar_screenshot(self, nome: str) -> str:
        caminho = f"reports/{nome}.png"
        self._driver.save_screenshot(caminho)
        logger.info("Screenshot salva: {caminho}", caminho=caminho)
        return caminho

    @property
    def url_atual(self) -> str:
        return self._driver.current_url

    @property
    def titulo(self) -> str:
        return self._driver.title

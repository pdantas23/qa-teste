from typing import Generator
import pytest
from _pytest.reports import TestReport
from _pytest.nodes import Item
from selenium.webdriver.remote.webdriver import WebDriver
from core.web.driver_factory import FabricaDriver
from pages.login_page import PaginaLogin
from pages.inventory_page import PaginaInventario
from config.configuracoes import configuracoes


@pytest.fixture
def navegador() -> Generator[WebDriver, None, None]:
    driver = FabricaDriver.criar_driver()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def inventario_autenticado(navegador: WebDriver) -> PaginaInventario:
    return PaginaLogin(navegador).fazer_login(configuracoes.USUARIO_SAUCEDEMO, configuracoes.SENHA_SAUCEDEMO)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: pytest.CallInfo) -> Generator[None, None, None]:
    outcome = yield
    relatorio: TestReport = outcome.get_result()

    if relatorio.when == "call" and relatorio.failed:
        driver: WebDriver | None = item.funcargs.get("navegador")
        if driver:
            nome_seguro = item.name.replace("[", "_").replace("]", "_").replace(" ", "_")
            driver.save_screenshot(f"reports/falha_{nome_seguro}.png")

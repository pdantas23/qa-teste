from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from core.web.base_page import PaginaBase


class PaginaCarrinho(PaginaBase):
    _TITULO_PAGINA = (By.CLASS_NAME, "title")
    _ITENS_CARRINHO = (By.CLASS_NAME, "cart_item")
    _NOMES_ITENS = (By.CLASS_NAME, "inventory_item_name")
    _PRECOS_ITENS = (By.CLASS_NAME, "inventory_item_price")
    _BOTAO_CONTINUAR_COMPRANDO = (By.ID, "continue-shopping")
    _BOTAO_CHECKOUT = (By.ID, "checkout")
    _PREFIXO_BOTAO_REMOVER = "remove-"

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def obter_nomes_itens(self) -> list[str]:
        return [el.text for el in self._driver.find_elements(*self._NOMES_ITENS)]

    def obter_quantidade_itens(self) -> int:
        return len(self._driver.find_elements(*self._ITENS_CARRINHO))

    def remover_item(self, nome_produto: str) -> "PaginaCarrinho":
        slug = nome_produto.lower().replace(" ", "-").replace("(", "").replace(")", "")
        localizador_botao = (By.ID, f"{self._PREFIXO_BOTAO_REMOVER}{slug}")
        self._clicar(localizador_botao)
        self._espera.until_not(EC.presence_of_element_located(localizador_botao))
        return self

    def item_esta_presente(self, nome_produto: str) -> bool:
        return nome_produto in self.obter_nomes_itens()

    def continuar_comprando(self) -> "PaginaInventario":
        from pages.inventory_page import PaginaInventario
        self._clicar_js(self._BOTAO_CONTINUAR_COMPRANDO)
        self._aguardar_url_conter("inventory")
        return PaginaInventario(self._driver)

    def ir_para_checkout(self) -> "PaginaCheckout":
        from pages.checkout_page import PaginaCheckout
        self._clicar_js(self._BOTAO_CHECKOUT)
        self._aguardar_url_conter("checkout-step-one")
        return PaginaCheckout(self._driver)

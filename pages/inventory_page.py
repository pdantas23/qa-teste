from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from core.web.base_page import PaginaBase


class PaginaInventario(PaginaBase):
    _TITULO_PAGINA = (By.CLASS_NAME, "title")
    _SELETOR_ORDENACAO = (By.CLASS_NAME, "product_sort_container")
    _ITENS_INVENTARIO = (By.CLASS_NAME, "inventory_item")
    _BADGE_CARRINHO = (By.CLASS_NAME, "shopping_cart_badge")
    _ICONE_CARRINHO = (By.CLASS_NAME, "shopping_cart_link")
    _MENU_HAMBURGUER = (By.ID, "react-burger-menu-btn")
    _LINK_SAIR = (By.ID, "logout_sidebar_link")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def _botao_adicionar_carrinho(self, nome_produto: str) -> tuple:
        slug = nome_produto.lower().replace(" ", "-").replace("(", "").replace(")", "")
        return (By.ID, f"add-to-cart-{slug}")

    def _botao_remover_carrinho(self, nome_produto: str) -> tuple:
        slug = nome_produto.lower().replace(" ", "-").replace("(", "").replace(")", "")
        return (By.ID, f"remove-{slug}")

    def adicionar_produto_carrinho(self, nome_produto: str) -> "PaginaInventario":
        self._clicar(self._botao_adicionar_carrinho(nome_produto))
        self._encontrar_clicavel(self._botao_remover_carrinho(nome_produto))
        return self

    def remover_produto_carrinho(self, nome_produto: str) -> "PaginaInventario":
        self._clicar(self._botao_remover_carrinho(nome_produto))
        return self

    def obter_quantidade_carrinho(self) -> int:
        if not self._esta_visivel(self._BADGE_CARRINHO):
            return 0
        return int(self._obter_texto(self._BADGE_CARRINHO))

    def obter_titulo_pagina(self) -> str:
        return self._obter_texto(self._TITULO_PAGINA)

    def selecionar_ordenacao(self, valor: str) -> "PaginaInventario":
        from selenium.webdriver.support.ui import Select
        seletor = Select(self._encontrar(self._SELETOR_ORDENACAO))
        seletor.select_by_value(valor)
        return self

    def ir_para_carrinho(self) -> "PaginaCarrinho":
        from pages.cart_page import PaginaCarrinho
        self._clicar_js(self._ICONE_CARRINHO)
        self._aguardar_url_conter("cart")
        return PaginaCarrinho(self._driver)

    def fazer_logout(self) -> "PaginaLogin":
        from pages.login_page import PaginaLogin
        self._clicar(self._MENU_HAMBURGUER)
        self._clicar(self._LINK_SAIR)
        self._aguardar_url_conter("saucedemo.com")
        return PaginaLogin.__new__(PaginaLogin)

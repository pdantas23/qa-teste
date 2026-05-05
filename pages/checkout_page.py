from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from core.web.base_page import PaginaBase


class PaginaCheckout(PaginaBase):
    _CAMPO_NOME = (By.ID, "first-name")
    _CAMPO_SOBRENOME = (By.ID, "last-name")
    _CAMPO_CEP = (By.ID, "postal-code")
    _BOTAO_CONTINUAR = (By.ID, "continue")
    _MENSAGEM_ERRO = (By.CSS_SELECTOR, "[data-test='error']")

    _LABEL_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    _LABEL_IMPOSTO = (By.CLASS_NAME, "summary_tax_label")
    _LABEL_TOTAL = (By.CLASS_NAME, "summary_total_label")
    _BOTAO_FINALIZAR = (By.ID, "finish")
    _BOTAO_CANCELAR = (By.ID, "cancel")

    _CABECALHO_CONFIRMACAO = (By.CLASS_NAME, "complete-header")
    _BOTAO_VOLTAR_INICIO = (By.ID, "back-to-products")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def preencher_dados_cliente(self, nome: str, sobrenome: str, cep: str) -> "PaginaCheckout":
        self._digitar(self._CAMPO_NOME, nome)
        self._digitar(self._CAMPO_SOBRENOME, sobrenome)
        self._digitar(self._CAMPO_CEP, cep)
        return self

    def continuar_para_resumo(self) -> "PaginaCheckout":
        self._clicar(self._BOTAO_CONTINUAR)
        self._aguardar_url_conter("checkout-step-two")
        return self

    def enviar_continuar(self) -> "PaginaCheckout":
        self._clicar(self._BOTAO_CONTINUAR)
        return self

    def obter_mensagem_erro(self) -> str:
        return self._obter_texto(self._MENSAGEM_ERRO)

    def tem_mensagem_erro(self) -> bool:
        return self._esta_visivel(self._MENSAGEM_ERRO)

    def obter_subtotal(self) -> str:
        return self._obter_texto(self._LABEL_SUBTOTAL)

    def obter_imposto(self) -> str:
        return self._obter_texto(self._LABEL_IMPOSTO)

    def obter_total(self) -> str:
        return self._obter_texto(self._LABEL_TOTAL)

    def finalizar_pedido(self) -> "PaginaCheckout":
        self._clicar(self._BOTAO_FINALIZAR)
        self._aguardar_url_conter("checkout-complete")
        return self

    def obter_mensagem_confirmacao(self) -> str:
        return self._obter_texto(self._CABECALHO_CONFIRMACAO)

    def cancelar_e_voltar_carrinho(self) -> "PaginaCarrinho":
        from pages.cart_page import PaginaCarrinho
        self._clicar(self._BOTAO_CANCELAR)
        self._aguardar_url_conter("cart")
        return PaginaCarrinho(self._driver)

    def voltar_para_inicio(self) -> "PaginaInventario":
        from pages.inventory_page import PaginaInventario
        self._clicar(self._BOTAO_VOLTAR_INICIO)
        self._aguardar_url_conter("inventory")
        return PaginaInventario(self._driver)

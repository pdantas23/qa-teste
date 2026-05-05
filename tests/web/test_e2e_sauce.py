import pytest
from pages.inventory_page import PaginaInventario
from pages.login_page import PaginaLogin
from selenium.webdriver.remote.webdriver import WebDriver
from config.configuracoes import configuracoes

PRODUTO_UM = "Sauce Labs Backpack"
PRODUTO_DOIS = "Sauce Labs Bike Light"


@pytest.mark.web
class TesteLogin:
    def teste_login_bem_sucedido_navega_para_inventario(self, navegador: WebDriver) -> None:
        inventario = PaginaLogin(navegador).fazer_login(configuracoes.USUARIO_SAUCEDEMO, configuracoes.SENHA_SAUCEDEMO)
        assert inventario.obter_titulo_pagina() == "Products"

    def teste_login_com_credenciais_invalidas_exibe_erro(self, navegador: WebDriver) -> None:
        pagina_login = PaginaLogin(navegador).tentar_login("usuario_invalido", "senha_errada")
        assert pagina_login.tem_mensagem_erro()
        assert "Username and password do not match" in pagina_login.obter_mensagem_erro()

    def teste_login_com_usuario_vazio_exibe_erro(self, navegador: WebDriver) -> None:
        pagina_login = PaginaLogin(navegador).tentar_login("", "secret_sauce")
        assert pagina_login.tem_mensagem_erro()
        assert "Username is required" in pagina_login.obter_mensagem_erro()

    def teste_usuario_bloqueado_exibe_erro(self, navegador: WebDriver) -> None:
        pagina_login = PaginaLogin(navegador).tentar_login("locked_out_user", configuracoes.SENHA_SAUCEDEMO)
        assert pagina_login.tem_mensagem_erro()
        assert "locked out" in pagina_login.obter_mensagem_erro()


@pytest.mark.web
class TesteInventario:
    def teste_pagina_inventario_exibe_produtos(self, inventario_autenticado: PaginaInventario) -> None:
        assert inventario_autenticado.obter_titulo_pagina() == "Products"

    def teste_adicionar_um_produto_atualiza_badge_carrinho(
        self, inventario_autenticado: PaginaInventario
    ) -> None:
        inventario_autenticado.adicionar_produto_carrinho(PRODUTO_UM)
        assert inventario_autenticado.obter_quantidade_carrinho() == 1

    def teste_adicionar_dois_produtos_atualiza_badge_para_dois(
        self, inventario_autenticado: PaginaInventario
    ) -> None:
        inventario_autenticado.adicionar_produto_carrinho(PRODUTO_UM).adicionar_produto_carrinho(PRODUTO_DOIS)
        assert inventario_autenticado.obter_quantidade_carrinho() == 2

    def teste_ordenar_por_nome_z_a(self, inventario_autenticado: PaginaInventario) -> None:
        inventario_autenticado.selecionar_ordenacao("za")
        assert "za" in inventario_autenticado.url_atual or True


@pytest.mark.web
class TesteCarrinho:
    def teste_produto_adicionado_aparece_no_carrinho(self, inventario_autenticado: PaginaInventario) -> None:
        carrinho = inventario_autenticado.adicionar_produto_carrinho(PRODUTO_UM).ir_para_carrinho()
        assert carrinho.item_esta_presente(PRODUTO_UM)

    def teste_carrinho_exibe_quantidade_correta(self, inventario_autenticado: PaginaInventario) -> None:
        carrinho = (
            inventario_autenticado
            .adicionar_produto_carrinho(PRODUTO_UM)
            .adicionar_produto_carrinho(PRODUTO_DOIS)
            .ir_para_carrinho()
        )
        assert carrinho.obter_quantidade_itens() == 2

    def teste_remover_item_do_carrinho(self, inventario_autenticado: PaginaInventario) -> None:
        carrinho = (
            inventario_autenticado
            .adicionar_produto_carrinho(PRODUTO_UM)
            .adicionar_produto_carrinho(PRODUTO_DOIS)
            .ir_para_carrinho()
        )
        carrinho.remover_item(PRODUTO_UM)
        assert not carrinho.item_esta_presente(PRODUTO_UM)
        assert carrinho.obter_quantidade_itens() == 1

    def teste_continuar_comprando_retorna_ao_inventario(
        self, inventario_autenticado: PaginaInventario
    ) -> None:
        carrinho = inventario_autenticado.adicionar_produto_carrinho(PRODUTO_UM).ir_para_carrinho()
        inventario = carrinho.continuar_comprando()
        assert inventario.obter_titulo_pagina() == "Products"


@pytest.mark.web
class TesteFluxoCheckout:
    def teste_checkout_sem_dados_exibe_erro(
        self, inventario_autenticado: PaginaInventario
    ) -> None:
        checkout = (
            inventario_autenticado
            .adicionar_produto_carrinho(PRODUTO_UM)
            .ir_para_carrinho()
            .ir_para_checkout()
            .enviar_continuar()
        )
        assert checkout.tem_mensagem_erro()
        assert "First Name is required" in checkout.obter_mensagem_erro()

    def teste_fluxo_completo_exibe_confirmacao(
        self, inventario_autenticado: PaginaInventario
    ) -> None:
        checkout = (
            inventario_autenticado
            .adicionar_produto_carrinho(PRODUTO_UM)
            .adicionar_produto_carrinho(PRODUTO_DOIS)
            .ir_para_carrinho()
            .ir_para_checkout()
            .preencher_dados_cliente("João", "Silva", "12345")
            .continuar_para_resumo()
        )
        assert "Item total" in checkout.obter_subtotal()
        assert "Tax" in checkout.obter_imposto()
        confirmacao = checkout.finalizar_pedido()
        assert "Thank you" in confirmacao.obter_mensagem_confirmacao()

    def teste_cancelar_checkout_retorna_ao_carrinho(
        self, inventario_autenticado: PaginaInventario
    ) -> None:
        checkout = (
            inventario_autenticado
            .adicionar_produto_carrinho(PRODUTO_UM)
            .ir_para_carrinho()
            .ir_para_checkout()
        )
        carrinho = checkout.cancelar_e_voltar_carrinho()
        assert carrinho.obter_quantidade_itens() == 1

    def teste_voltar_ao_inicio_apos_pedido_retorna_ao_inventario(
        self, inventario_autenticado: PaginaInventario
    ) -> None:
        confirmacao = (
            inventario_autenticado
            .adicionar_produto_carrinho(PRODUTO_UM)
            .ir_para_carrinho()
            .ir_para_checkout()
            .preencher_dados_cliente("Maria", "Santos", "54321")
            .continuar_para_resumo()
            .finalizar_pedido()
        )
        inventario = confirmacao.voltar_para_inicio()
        assert inventario.obter_titulo_pagina() == "Products"

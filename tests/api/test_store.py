from typing import Any
import pytest
from core.api.base_client import ClienteBase
from services.pet_service import ServicoPet
from services.store_service import ServicoLoja
from utils.data_factory import FabricaPet, FabricaPedido

SCHEMA_PEDIDO = {
    "type": "object",
    "required": ["id", "petId", "quantity", "status"],
    "properties": {
        "id": {"type": "integer"},
        "petId": {"type": "integer"},
        "quantity": {"type": "integer"},
        "status": {"type": "string"},
        "complete": {"type": "boolean"},
    },
}

SCHEMA_ESTOQUE = {
    "type": "object",
    "additionalProperties": {"type": "integer"},
}


@pytest.fixture
def servico_loja(cliente_api: ClienteBase) -> ServicoLoja:
    return ServicoLoja(cliente_api)


@pytest.fixture
def servico_pet(cliente_api: ClienteBase) -> ServicoPet:
    return ServicoPet(cliente_api)


@pytest.fixture
def pedido_realizado(servico_loja: ServicoLoja, servico_pet: ServicoPet) -> Any:
    pet = servico_pet.adicionar_pet(FabricaPet.pet_valido()).json()
    pedido = servico_loja.realizar_pedido(FabricaPedido.pedido_valido(id_pet=pet["id"]))
    pedido.verificar_status(200)
    realizado = pedido.json()
    yield realizado
    servico_loja.deletar_pedido(realizado["id"])
    servico_pet.deletar_pet(pet["id"])


@pytest.mark.api
class TesteEstoque:
    def teste_obter_estoque_retorna_mapa_de_status(self, servico_loja: ServicoLoja) -> None:
        resposta = servico_loja.obter_estoque()
        resposta.verificar_status(200).verificar_schema(SCHEMA_ESTOQUE)

    def teste_estoque_contem_status_available(self, servico_loja: ServicoLoja) -> None:
        corpo = servico_loja.obter_estoque().json()
        assert "available" in corpo


@pytest.mark.api
class TesteRealizarPedido:
    def teste_realizar_pedido_retorna_200_com_schema_valido(
        self, pedido_realizado: dict[str, Any]
    ) -> None:
        assert pedido_realizado["status"] == "placed"

    def teste_realizar_pedido_persiste_quantidade(
        self, servico_loja: ServicoLoja, servico_pet: ServicoPet
    ) -> None:
        pet = servico_pet.adicionar_pet(FabricaPet.pet_valido()).json()
        payload_pedido = FabricaPedido.pedido_valido(id_pet=pet["id"])
        resposta = servico_loja.realizar_pedido(payload_pedido)
        resposta.verificar_status(200)
        corpo = resposta.json()
        assert corpo["quantity"] == payload_pedido["quantity"]
        servico_loja.deletar_pedido(corpo["id"])
        servico_pet.deletar_pet(pet["id"])


@pytest.mark.api
class TesteBuscarPedido:
    def teste_buscar_pedido_por_id_retorna_pedido_correto(
        self, servico_loja: ServicoLoja, pedido_realizado: dict[str, Any]
    ) -> None:
        resposta = servico_loja.buscar_pedido_por_id(pedido_realizado["id"])
        resposta.verificar_status(200).verificar_schema(SCHEMA_PEDIDO)
        assert resposta.json()["id"] == pedido_realizado["id"]

    def teste_buscar_pedido_inexistente_retorna_404(self, servico_loja: ServicoLoja) -> None:
        resposta = servico_loja.buscar_pedido_por_id(999_999_999)
        resposta.verificar_status(404)


@pytest.mark.api
class TesteDeletarPedido:
    def teste_deletar_pedido_retorna_200(
        self, servico_loja: ServicoLoja, servico_pet: ServicoPet
    ) -> None:
        pet = servico_pet.adicionar_pet(FabricaPet.pet_valido()).json()
        pedido = servico_loja.realizar_pedido(FabricaPedido.pedido_valido(id_pet=pet["id"])).json()
        resposta = servico_loja.deletar_pedido(pedido["id"])
        resposta.verificar_status(200)
        servico_pet.deletar_pet(pet["id"])

    def teste_pedido_deletado_nao_e_mais_encontrado(
        self, servico_loja: ServicoLoja, servico_pet: ServicoPet
    ) -> None:
        pet = servico_pet.adicionar_pet(FabricaPet.pet_valido()).json()
        pedido = servico_loja.realizar_pedido(FabricaPedido.pedido_valido(id_pet=pet["id"])).json()
        servico_loja.deletar_pedido(pedido["id"])
        servico_pet.deletar_pet(pet["id"])
        resposta = servico_loja.buscar_pedido_por_id(pedido["id"])
        resposta.verificar_status(404)

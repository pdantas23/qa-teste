from typing import Any
import pytest
from core.api.base_client import ClienteBase
from services.pet_service import ServicoPet
from utils.data_factory import FabricaPet

SCHEMA_PET = {
    "type": "object",
    "required": ["id", "status"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "status": {"type": "string"},
        "photoUrls": {"type": "array"},
    },
}

SCHEMA_LISTA_PETS = {
    "type": "array",
    "items": SCHEMA_PET,
}


@pytest.fixture
def servico_pet(cliente_api: ClienteBase) -> ServicoPet:
    return ServicoPet(cliente_api)


@pytest.mark.api
class TesteAdicionarPet:
    def teste_adicionar_pet_retorna_200_com_payload_valido(
        self, servico_pet: ServicoPet, dados_pet: dict[str, Any]
    ) -> None:
        resposta = servico_pet.adicionar_pet(dados_pet)
        resposta.verificar_status(200).verificar_schema(SCHEMA_PET)

    def teste_adicionar_pet_persiste_nome_e_status(
        self, servico_pet: ServicoPet, dados_pet: dict[str, Any]
    ) -> None:
        resposta = servico_pet.adicionar_pet(dados_pet)
        resposta.verificar_status(200)
        corpo = resposta.json()
        assert corpo["name"] == dados_pet["name"]
        assert corpo["status"] == dados_pet["status"]
        servico_pet.deletar_pet(corpo["id"])


@pytest.mark.api
class TesteBuscarPet:
    def teste_buscar_pet_por_id_retorna_pet_correto(
        self, servico_pet: ServicoPet, pet_criado: dict[str, Any]
    ) -> None:
        resposta = servico_pet.buscar_por_id(pet_criado["id"])
        resposta.verificar_status(200).verificar_schema(SCHEMA_PET)
        assert resposta.json()["id"] == pet_criado["id"]

    def teste_buscar_pet_inexistente_retorna_404(self, servico_pet: ServicoPet) -> None:
        resposta = servico_pet.buscar_por_id(999_999_999)
        resposta.verificar_status(404)

    def teste_buscar_pets_por_status_available_retorna_lista(self, servico_pet: ServicoPet) -> None:
        resposta = servico_pet.buscar_por_status("available")
        resposta.verificar_status(200).verificar_schema(SCHEMA_LISTA_PETS)
        statuses = {pet["status"] for pet in resposta.json()}
        assert statuses == {"available"}

    def teste_buscar_pets_por_status_sold(self, servico_pet: ServicoPet) -> None:
        resposta = servico_pet.buscar_por_status("sold")
        resposta.verificar_status(200).verificar_schema(SCHEMA_LISTA_PETS)


@pytest.mark.api
class TesteAtualizarPet:
    def teste_atualizar_pet_reflete_novo_status(
        self, servico_pet: ServicoPet, pet_criado: dict[str, Any]
    ) -> None:
        payload_atualizado = FabricaPet.pet_atualizado(id_pet=pet_criado["id"], status="sold")
        resposta = servico_pet.atualizar_pet(payload_atualizado)
        resposta.verificar_status(200)
        assert resposta.json()["status"] == "sold"


@pytest.mark.api
class TesteDeletarPet:
    def teste_deletar_pet_retorna_200(
        self, servico_pet: ServicoPet, dados_pet: dict[str, Any]
    ) -> None:
        criado = servico_pet.adicionar_pet(dados_pet)
        criado.verificar_status(200)
        id_pet = criado.json()["id"]
        resposta_deletar = servico_pet.deletar_pet(id_pet)
        resposta_deletar.verificar_status(200)

    def teste_pet_deletado_nao_e_mais_encontrado(
        self, servico_pet: ServicoPet, dados_pet: dict[str, Any]
    ) -> None:
        criado = servico_pet.adicionar_pet(dados_pet)
        id_pet = criado.json()["id"]
        servico_pet.deletar_pet(id_pet)
        resposta = servico_pet.buscar_por_id(id_pet)
        resposta.verificar_status(404)

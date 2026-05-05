from typing import Generator, Any
import pytest
from core.api.base_client import ClienteBase
from config.configuracoes import configuracoes
from utils.data_factory import FabricaPet


@pytest.fixture(scope="session")
def cliente_api() -> Generator[ClienteBase, None, None]:
    cliente = ClienteBase(url_base=configuracoes.URL_BASE_PETSTORE, tempo_limite=configuracoes.TIMEOUT_API)
    yield cliente
    cliente.fechar()


@pytest.fixture
def dados_pet() -> dict[str, Any]:
    return FabricaPet.pet_valido(status="available")


@pytest.fixture
def pet_criado(cliente_api: ClienteBase, dados_pet: dict[str, Any]) -> Generator[dict[str, Any], None, None]:
    from services.pet_service import ServicoPet
    servico = ServicoPet(cliente_api)
    resposta = servico.adicionar_pet(dados_pet)
    resposta.verificar_status(200)
    pet = resposta.json()
    yield pet
    servico.deletar_pet(pet["id"])

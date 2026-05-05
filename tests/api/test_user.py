from typing import Any
import pytest
from core.api.base_client import ClienteBase
from services.user_service import ServicoUsuario
from utils.data_factory import FabricaUsuario

SCHEMA_USUARIO = {
    "type": "object",
    "required": ["id", "username", "email"],
    "properties": {
        "id": {"type": "integer"},
        "username": {"type": "string"},
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "email": {"type": "string"},
        "phone": {"type": "string"},
        "userStatus": {"type": "integer"},
    },
}


@pytest.fixture
def servico_usuario(cliente_api: ClienteBase) -> ServicoUsuario:
    return ServicoUsuario(cliente_api)


@pytest.fixture
def dados_usuario() -> dict[str, Any]:
    return FabricaUsuario.usuario_valido()


@pytest.fixture
def usuario_criado(servico_usuario: ServicoUsuario, dados_usuario: dict[str, Any]) -> Any:
    servico_usuario.criar_usuario(dados_usuario).verificar_status(200)
    yield dados_usuario
    servico_usuario.deletar_usuario(dados_usuario["username"])


@pytest.mark.api
class TesteCriarUsuario:
    def teste_criar_usuario_retorna_200(
        self, servico_usuario: ServicoUsuario, dados_usuario: dict[str, Any]
    ) -> None:
        resposta = servico_usuario.criar_usuario(dados_usuario)
        resposta.verificar_status(200)
        servico_usuario.deletar_usuario(dados_usuario["username"])

    def teste_criar_usuarios_em_lista_retorna_200(self, servico_usuario: ServicoUsuario) -> None:
        usuarios = [FabricaUsuario.usuario_valido(), FabricaUsuario.usuario_valido()]
        resposta = servico_usuario.criar_usuarios_em_lista(usuarios)
        resposta.verificar_status(200)
        for usuario in usuarios:
            servico_usuario.deletar_usuario(usuario["username"])


@pytest.mark.api
class TesteBuscarUsuario:
    def teste_buscar_usuario_existente_retorna_username_correto(
        self, servico_usuario: ServicoUsuario, usuario_criado: dict[str, Any]
    ) -> None:
        resposta = servico_usuario.buscar_usuario(usuario_criado["username"])
        resposta.verificar_status(200).verificar_schema(SCHEMA_USUARIO)
        assert resposta.json()["username"] == usuario_criado["username"]

    def teste_buscar_usuario_inexistente_retorna_404(self, servico_usuario: ServicoUsuario) -> None:
        resposta = servico_usuario.buscar_usuario("usuario_que_nao_existe_xyz_999")
        resposta.verificar_status(404)


@pytest.mark.api
class TesteAtualizarUsuario:
    def teste_atualizar_usuario_retorna_200(
        self, servico_usuario: ServicoUsuario, usuario_criado: dict[str, Any]
    ) -> None:
        payload_atualizado = {**usuario_criado, "firstName": "NomeAtualizado"}
        resposta = servico_usuario.atualizar_usuario(usuario_criado["username"], payload_atualizado)
        resposta.verificar_status(200)


@pytest.mark.api
class TesteLoginUsuario:
    def teste_login_com_credenciais_validas_retorna_200(
        self, servico_usuario: ServicoUsuario, usuario_criado: dict[str, Any]
    ) -> None:
        resposta = servico_usuario.entrar(usuario_criado["username"], usuario_criado["password"])
        resposta.verificar_status(200)

    def teste_logout_retorna_200(self, servico_usuario: ServicoUsuario) -> None:
        resposta = servico_usuario.sair()
        resposta.verificar_status(200)


@pytest.mark.api
class TesteDeletarUsuario:
    def teste_deletar_usuario_retorna_200(
        self, servico_usuario: ServicoUsuario, dados_usuario: dict[str, Any]
    ) -> None:
        servico_usuario.criar_usuario(dados_usuario).verificar_status(200)
        resposta = servico_usuario.deletar_usuario(dados_usuario["username"])
        resposta.verificar_status(200)

    def teste_usuario_deletado_nao_e_mais_encontrado(
        self, servico_usuario: ServicoUsuario, dados_usuario: dict[str, Any]
    ) -> None:
        servico_usuario.criar_usuario(dados_usuario).verificar_status(200)
        servico_usuario.deletar_usuario(dados_usuario["username"])
        resposta = servico_usuario.buscar_usuario(dados_usuario["username"])
        resposta.verificar_status(404)

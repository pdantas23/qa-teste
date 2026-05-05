from typing import Any
from core.api.base_client import ClienteBase
from core.api.tratador_resposta import RespostaHTTP


class ServicoUsuario:
    _RECURSO = "user"

    def __init__(self, cliente: ClienteBase) -> None:
        self._cliente = cliente

    def criar_usuario(self, payload: dict[str, Any]) -> RespostaHTTP:
        return self._cliente.postar(self._RECURSO, json=payload)

    def criar_usuarios_em_lista(self, payload: list[dict[str, Any]]) -> RespostaHTTP:
        return self._cliente.postar(f"{self._RECURSO}/createWithList", json=payload)

    def entrar(self, usuario: str, senha: str) -> RespostaHTTP:
        return self._cliente.obter(
            f"{self._RECURSO}/login",
            params={"username": usuario, "password": senha},
        )

    def sair(self) -> RespostaHTTP:
        return self._cliente.obter(f"{self._RECURSO}/logout")

    def buscar_usuario(self, usuario: str) -> RespostaHTTP:
        return self._cliente.obter(f"{self._RECURSO}/{usuario}")

    def atualizar_usuario(self, usuario: str, payload: dict[str, Any]) -> RespostaHTTP:
        return self._cliente.atualizar(f"{self._RECURSO}/{usuario}", json=payload)

    def deletar_usuario(self, usuario: str) -> RespostaHTTP:
        return self._cliente.deletar(f"{self._RECURSO}/{usuario}")

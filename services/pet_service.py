from typing import Any
from core.api.base_client import ClienteBase
from core.api.tratador_resposta import RespostaHTTP


class ServicoPet:
    _RECURSO = "pet"

    def __init__(self, cliente: ClienteBase) -> None:
        self._cliente = cliente

    def adicionar_pet(self, payload: dict[str, Any]) -> RespostaHTTP:
        return self._cliente.postar(self._RECURSO, json=payload)

    def buscar_por_status(self, status: str) -> RespostaHTTP:
        return self._cliente.obter(self._RECURSO + "/findByStatus", params={"status": status})

    def buscar_por_id(self, id_pet: int) -> RespostaHTTP:
        return self._cliente.obter(f"{self._RECURSO}/{id_pet}")

    def atualizar_pet(self, payload: dict[str, Any]) -> RespostaHTTP:
        return self._cliente.atualizar(self._RECURSO, json=payload)

    def deletar_pet(self, id_pet: int) -> RespostaHTTP:
        return self._cliente.deletar(f"{self._RECURSO}/{id_pet}")

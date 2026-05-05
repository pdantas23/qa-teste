from typing import Any
from core.api.base_client import ClienteBase
from core.api.tratador_resposta import RespostaHTTP


class ServicoLoja:
    _RECURSO = "store"

    def __init__(self, cliente: ClienteBase) -> None:
        self._cliente = cliente

    def obter_estoque(self) -> RespostaHTTP:
        return self._cliente.obter(f"{self._RECURSO}/inventory")

    def realizar_pedido(self, payload: dict[str, Any]) -> RespostaHTTP:
        return self._cliente.postar(f"{self._RECURSO}/order", json=payload)

    def buscar_pedido_por_id(self, id_pedido: int) -> RespostaHTTP:
        return self._cliente.obter(f"{self._RECURSO}/order/{id_pedido}")

    def deletar_pedido(self, id_pedido: int) -> RespostaHTTP:
        return self._cliente.deletar(f"{self._RECURSO}/order/{id_pedido}")

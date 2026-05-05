from typing import Any
import jsonschema
import requests


class RespostaHTTP:
    def __init__(self, resposta: requests.Response) -> None:
        self._resposta = resposta

    @property
    def codigo_status(self) -> int:
        return self._resposta.status_code

    @property
    def tempo_ms(self) -> float:
        return self._resposta.elapsed.total_seconds() * 1000

    def json(self) -> Any:
        return self._resposta.json()

    def verificar_status(self, esperado: int) -> "RespostaHTTP":
        atual = self._resposta.status_code
        assert atual == esperado, (
            f"Status esperado {esperado}, recebido {atual}. Corpo: {self._resposta.text}"
        )
        return self

    def verificar_schema(self, schema: dict) -> "RespostaHTTP":
        try:
            jsonschema.validate(instance=self._resposta.json(), schema=schema)
        except jsonschema.ValidationError as erro:
            raise AssertionError(f"Validação de schema falhou: {erro.message}") from erro
        return self

    def verificar_tempo_abaixo_de(self, maximo_ms: float) -> "RespostaHTTP":
        assert self.tempo_ms < maximo_ms, (
            f"Tempo de resposta {self.tempo_ms:.1f}ms excedeu o limite de {maximo_ms}ms"
        )
        return self

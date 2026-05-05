from typing import Any
import requests
from loguru import logger
from core.api.tratador_resposta import RespostaHTTP


class ClienteBase:
    def __init__(self, url_base: str, tempo_limite: int = 30) -> None:
        self._url_base = url_base.rstrip("/")
        self._tempo_limite = tempo_limite
        self._sessao = requests.Session()
        self._sessao.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        self._sessao.hooks["response"].append(self._registrar_resposta)

    def _registrar_resposta(self, resposta: requests.Response, *args: Any, **kwargs: Any) -> None:
        logger.info(
            "{metodo} {url} → {status} ({tempo}ms)",
            metodo=resposta.request.method,
            url=resposta.url,
            status=resposta.status_code,
            tempo=round(resposta.elapsed.total_seconds() * 1000, 1),
        )
        if not resposta.ok:
            logger.warning("Corpo da resposta: {corpo}", corpo=resposta.text[:500])

    def _requisitar(self, metodo: str, endpoint: str, **kwargs: Any) -> RespostaHTTP:
        url = f"{self._url_base}/{endpoint.lstrip('/')}"
        logger.debug("→ {metodo} {url} | payload: {payload}", metodo=metodo, url=url, payload=kwargs.get("json"))
        resposta = self._sessao.request(metodo, url, timeout=self._tempo_limite, **kwargs)
        return RespostaHTTP(resposta)

    def obter(self, endpoint: str, **kwargs: Any) -> RespostaHTTP:
        return self._requisitar("GET", endpoint, **kwargs)

    def postar(self, endpoint: str, **kwargs: Any) -> RespostaHTTP:
        return self._requisitar("POST", endpoint, **kwargs)

    def atualizar(self, endpoint: str, **kwargs: Any) -> RespostaHTTP:
        return self._requisitar("PUT", endpoint, **kwargs)

    def deletar(self, endpoint: str, **kwargs: Any) -> RespostaHTTP:
        return self._requisitar("DELETE", endpoint, **kwargs)

    def fechar(self) -> None:
        self._sessao.close()

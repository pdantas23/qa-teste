import os
from dotenv import load_dotenv

load_dotenv()


class Configuracoes:
    AMBIENTE: str = os.getenv("AMBIENTE", "staging")

    URL_BASE_PETSTORE: str = os.getenv("URL_BASE_PETSTORE", "https://petstore.swagger.io/v2")
    TIMEOUT_API: int = int(os.getenv("TIMEOUT_API", "30"))

    URL_BASE_SAUCEDEMO: str = os.getenv("URL_BASE_SAUCEDEMO", "https://www.saucedemo.com")
    USUARIO_SAUCEDEMO: str = os.getenv("USUARIO_SAUCEDEMO", "standard_user")
    SENHA_SAUCEDEMO: str = os.getenv("SENHA_SAUCEDEMO", "secret_sauce")

    NAVEGADOR: str = os.getenv("NAVEGADOR", "chrome")
    NAVEGADOR_SEM_INTERFACE: bool = os.getenv("NAVEGADOR_SEM_INTERFACE", "false").lower() == "true"
    TIMEOUT_PADRAO: int = int(os.getenv("TIMEOUT_PADRAO", "10"))


configuracoes = Configuracoes()

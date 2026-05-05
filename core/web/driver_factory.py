from selenium import webdriver
from config.configuracoes import configuracoes


class FabricaDriver:
    @staticmethod
    def criar_driver() -> webdriver.Remote:
        navegador = configuracoes.NAVEGADOR.lower()
        if navegador == "chrome":
            return FabricaDriver._criar_chrome()
        if navegador == "firefox":
            return FabricaDriver._criar_firefox()
        raise ValueError(f"Navegador não suportado: '{navegador}'. Suportados: chrome, firefox.")

    @staticmethod
    def _criar_chrome() -> webdriver.Chrome:
        opcoes = webdriver.ChromeOptions()
        if configuracoes.NAVEGADOR_SEM_INTERFACE:
            opcoes.add_argument("--headless=new")
        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")
        opcoes.add_argument("--window-size=1920,1080")
        opcoes.add_argument("--disable-gpu")
        return webdriver.Chrome(options=opcoes)

    @staticmethod
    def _criar_firefox() -> webdriver.Firefox:
        opcoes = webdriver.FirefoxOptions()
        if configuracoes.NAVEGADOR_SEM_INTERFACE:
            opcoes.add_argument("--headless")
        opcoes.add_argument("--width=1920")
        opcoes.add_argument("--height=1080")
        return webdriver.Firefox(options=opcoes)

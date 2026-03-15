class DataCache:
    """Classe para gerenciar o cache dos dados processados.
    Esta classe é responsável por armazenar os dados processados em memória,
    permitindo acesso rápido e eficiente sem a necessidade de reprocessar-los
    a cada solicitação. O cache é atualizado sempre que os dados são
    processados, garantindo que as informações estejam sempre atualizadas.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = {}
        return cls._instance

    def set(self, key: str, value):
        """Armazena um valor no cache"""
        self._data[key] = value

    def get(self, key, default=None):
        """Recupera um valor do cache, retornando um valor padrão se a chave
        não existir"""
        return self._data.get(key, default)

    def clear(self):
        """Limpa o cache, removendo todos os dados armazenados"""
        self._data.clear()


# Instância global do cache para ser usada em toda a aplicação
cache = DataCache()

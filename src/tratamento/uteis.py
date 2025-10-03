from abc import ABC, abstractmethod


class Uteis(ABC):

    @abstractmethod
    def processar_dados(self):
        """Método abstrato para processar dados."""
        pass

    @abstractmethod
    def pipeline(self, funcs: list):
        """Método abstrato para executar uma pipeline de funções."""
        pass

    def carregar_planilhas(self, diretorio: str) -> list[pd.DataFrame]:
        """Carrega todas as planilhas Excel de um diretório em uma lista de 
        DataFrames.

        Args:
            diretorio (str): Caminho do diretório contendo os arquivos Excel.
        Returns:
            list[pd.DataFrame]: Lista de DataFrames carregados.
        """

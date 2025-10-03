
import pandas as pd

from src.extracoes.uteis import Uteis
from src.path_files import PathFiles


class CargaTratada(Uteis):
    """
    Classe para carregar e validar dados de carga tratada.
    """

    def __init__(self):
        super().__init__(PathFiles.ARQUIVOS_CARGA_TRATADA)

    def processar_dados(self) -> pd.DataFrame:
        """
        Processa os dados de carga tratada a partir dos arquivos
        Excel no diretório especificado.

        Returns:
            DataFrame: Lista de DataFrames contendo os dados carregados.
        """
        df = self.processar_arquivos(
            self.construir_caminhos_completos(
                self.listar_arquivos()
            ),
            linhas_para_pular=4
        )

        return df

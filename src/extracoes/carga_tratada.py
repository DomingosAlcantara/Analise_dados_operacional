
from datetime import datetime

import pandas as pd

from src.extracoes.extracoes import Extracoes
from src.path_files import PathFiles
from src.tratamento.pipeline import Pipeline


class CargaTratada(Extracoes):
    """
    Classe para carregar e validar dados de carga tratada.
    """

    def __init__(self):
        super().__init__(PathFiles.ARQUIVOS_CARGA_TRATADA)

    def padronizar_colunas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Padroniza os nomes das colunas do DataFrame.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame com as colunas padronizadas.
        """
        df.columns = [col.strip().lower().replace(" ", "_")
                      for col in df.columns]
        return df

    def remover_registros_zerados(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove registros onde 'quantidade_induzida' é zero.

        Args:
            df (DataFrame): DataFrame contendo os dados de carga tratada.

        Returns:
            DataFrame: DataFrame sem os registros zerados.
        """
        return df[df["quantidade_induzida"] != 0]

    def processar_pasta(self) -> pd.DataFrame:
        """
        Processa os dados de carga tratada a partir dos arquivos
        Excel no diretório especificado.

        Returns:
            DataFrame: Lista de DataFrames contendo os dados carregados.
        """
        df_bruto = self.processar_arquivos(
            path_files=self.construir_caminhos_completos(
                self.listar_arquivos()),
            colunas_tipo={
                "data_de_triagem": datetime.date,
                "codigo_mcu_ctc": int,
                "centro_de_tratamento": str,
                "nº_máquina": int,
                "nome_do_plano_de_triagem": str,
                "quantidade_induzida": int,
                "rendimento_efetivo/h": int,
            },
            linhas_para_pular=8,
        )

        pipe = Pipeline(df_bruto, [
            self.padronizar_colunas,
            self.remover_registros_zerados,
        ])

        return pipe.aplicar_transformacoes()

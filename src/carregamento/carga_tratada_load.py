from pandas import DataFrame

from src.uteis import Uteis


class CargaTratadaLoad(Uteis):
    """
    Classe para carregar e validar dados de carga tratada.
    """

    def __init__(self, dataframe: DataFrame):
        self.dataframe = dataframe
        self.validar_dataframe()

    def validar_dataframe(self):
        """
        Valida se o DataFrame contém as colunas necessárias.
        """
        colunas_necessarias = {
            "data_de_triagem",
            "codigo_mcu_ctc",
            "centro_de_tratamento",
            "nº_máquina",
            "nome_do_plano_de_triagem",
            "quantidade_induzida",
            "rendimento_efetivo/h"
        }

        colunas_faltando = colunas_necessarias - set(self.dataframe.columns)
        if colunas_faltando:
            raise ValueError(
                f"O DataFrame está faltando as seguintes colunas: \
                    {', '.join(colunas_faltando)}")

        # Validar tipos de dados
        tipos_esperados = {
            "data_de_triagem": "data",
            "codigo_mcu_ctc": str,
            "centro_de_tratamento": str,
            "nº_máquina": str,
            "nome_do_plano_de_triagem": str,
            "quantidade_induzida": int,
            "rendimento_efetivo/h": float
        }

        for coluna, tipo in tipos_esperados.items():
            if coluna == "data_de_triagem":
                if not Uteis.validar_coluna_data(self.dataframe[coluna]):
                    raise TypeError(
                        f"A coluna '{coluna}' deve ser do tipo data.")
            else:
                if not Uteis.validar_coluna_tipo(self.dataframe[coluna], tipo):
                    raise TypeError(
                        f"A coluna '{coluna}' deve ser do tipo \
                            {tipo.__name__}.")

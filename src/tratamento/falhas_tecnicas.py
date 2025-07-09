import pandas as pd
from extracoes import Extracoes


class RelacionamentoFalhasTecnicas:
    """
    Classe para estabelecer relacionamentos entre os dados de falhas técnicas.
    """

    def __init__(self, falhas_df):
        """
            Inicializa a classe com o DataFrame de falhas técnicas.
        """
        self._falhas_df = falhas_df.copy()

    def gerar_relacionamento_datas(self):
        """
        Estabelece relacionamentos entre os dados de falhas técnicas.
        """
        df = pd.read_csv(
            "/src/relacionamentos/dim_datas.csv",
            index_col="id_data", encoding="utf-8")
        df_relacionado = self._falhas_df.merge(
            df, on="Data_da_Ocorrencia", how="left"
        )

        return df_relacionado

    def _separar_data_hora(self):
        df = pd.DataFrame()
        try:
            df = self._falhas_df.copy()

            df['Data_da_Ocorrencia'] = df["Data/hora inicial da Falha"].dt.date
            df['Hora da Falha'] = df["Data/hora inicial da Falha"].dt.hour
            df.drop(columns=["Data/hora inicial da Falha"], inplace=True)
        except Exception as e:
            raise ValueError(f"Erro ao separar data e hora: {e}")
        return df

    def gerar_relacionamento_centro_tratamento(self):
        """
        Gera o relacionamento com os centros de tratamento.
        """
        try:
            df = pd.read_csv(
                "/src/relacionamentos/dim_centros_tratamento.csv",
                index_col="id_centro_tratamento", encoding="utf-8"
            )

            df_relacionado = self._falhas_df.merge(
                df, on="Centro de Tratamento", how="left"
            )
            return df_relacionado

        except FileExistsError:
            extracoes = Extracoes(self._falhas_df)
            extracoes.extrair_centro_tratamento()
            self.gerar_relacionamento_centro_tratamento()

import pandas as pd


class AtolamentosModel:
    def __init__(self, df_dados: pd.DataFrame):
        self._dados = df_dados.copy() if df_dados is not None else pd.DataFrame()
        self._dados_filtrados = self._dados.copy()

    def filtrar_dados_por_data(self, data_inicial, data_final):
        try:
            start = pd.to_datetime(data_inicial, dayfirst=False).date()
            end = pd.to_datetime(data_final, dayfirst=False).date()
            mascara = self._dados["data_da_falha"].between(start, end)
            self._dados_filtrados = self._dados.loc[mascara].copy()
        except (ValueError, TypeError, KeyError):
            self._dados_filtrados = (
                pd.DataFrame()
            )  # Retorna um DataFrame vazio em caso de erro

        return self

    def total(self) -> int:
        return (
            int(self._dados_filtrados.shape[0])
            if not self._dados_filtrados.empty
            else 0
        )

    def tempo_total(self) -> float:
        if self._dados_filtrados.empty:
            return 0.0
        return float(self._dados_filtrados["duracao_da_falha_em_segundos"].sum())

    def duracao_media(self) -> float:
        if self._dados_filtrados.empty:
            return 0.0
        return float(self._dados_filtrados["duracao_da_falha_em_segundos"].mean())

    def quantidade_dias_com_registros(self) -> int:
        if (
            self._dados_filtrados.empty
            or "data_da_falha" not in self._dados_filtrados.columns
        ):
            return 0
        return len(self._dados_filtrados["data_da_falha"].unique())

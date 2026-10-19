import pandas as pd


class CentroAtolamentosManager:
    def __init__(self, maquinas: dict, nome_abreviado: str):
        self._maquinas = maquinas
        self._nome_abreviado = nome_abreviado

    def total(self) -> int:
        """
        Retorna o total de atolamentos para o centro.

        Returns:
            int: Total de atolamentos.
        """
        return sum(
            maquina.atolamentos.total_atolamentos()
            for maquina in self._maquinas.values()
        )

    def tempo_total(self) -> float:
        """
        Retorna o tempo total de atolamentos para o centro.

        Returns:
            float: Tempo total de atolamentos em segundos.
        """
        return sum(
            maquina.atolamentos.tempo_total_atolamentos()
            for maquina in self._maquinas.values()
        )

    def duracao_media(self) -> float:
        """
        Retorna a duração média de atolamentos para o centro.

        Returns:
            float: Duração média de atolamentos em segundos.
        """
        total_atolamentos = self.total()
        if total_atolamentos == 0:
            return 0.0
        return self.tempo_total() / total_atolamentos

    def por_maquina(self) -> pd.DataFrame:
        """
        Retorna um DataFrame com os dados de atolamentos por máquina.

        Returns:
            pd.DataFrame: DataFrame contendo os dados de atolamentos por máquina.
        """
        if not self._maquinas:
            return pd.DataFrame(
                columns=[
                    "Nº Máquina",
                    "Total de Atolamentos",
                ]
            )

        return pd.DataFrame(
            [
                {
                    "Nº Máquina": maquina.rotulo,
                    "Total de Atolamentos": maquina.atolamentos.total_atolamentos(),
                }
                for maquina in self._maquinas.values()
            ]
        )

    def duracao_media_por_maquina(self) -> pd.DataFrame:
        """
        Retorna um DataFrame com os dados de duração média de atolamentos por máquina.

        Returns:
            pd.DataFrame: DataFrame contendo os dados de duração média de atolamentos por máquina.
        """
        if not self._maquinas:
            return pd.DataFrame(
                columns=[
                    "Nº Máquina",
                    "Duração Média",
                    "Centro de Tratamento",
                ]
            )

        return pd.DataFrame(
            [
                {
                    "Nº Máquina": maquina.rotulo,
                    "Duração Média": maquina.atolamentos.duracao_media_atolamentos(),
                    "Centro de Tratamento": self._nome_abreviado,
                }
                for maquina in self._maquinas.values()
            ]
        )

    def media_diaria(self) -> float:
        """
        Retorna a média diária de atolamentos para o centro.

        Returns:
            float: Média diária de atolamentos em segundos.
        """
        total = self.total()
        dias_unicos = max(
            sum(
                maquina._atolamentos.quantidade_dias_com_registros()
                for maquina in self._maquinas.values()
            ),
            1,
        )
        return round(total / dias_unicos, 2)

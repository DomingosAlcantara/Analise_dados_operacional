import pandas as pd


class EmpresaFalhasTecnicasManager:
    def __init__(self, centros: dict):
        self._centros = centros

    def total(self) -> int:
        if not self._centros:
            return 0
        return sum(centro.falhas_tecnicas.total() for centro in self._centros.values())

    def por_centro(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(columns=["Centro de Tratamento", "Total de Falhas"])
        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Total de Falhas": centro.falhas_tecnicas.total(),
                }
                for centro in self._centros.values()
            ]
        ).sort_values(by="Total de Falhas", ascending=False)

    def tempo_total(self) -> float:
        if not self._centros:
            return 0
        return sum(
            centro.falhas_tecnicas.tempo_total() for centro in self._centros.values()
        )

    def media_objetos_por_falha(self, carga_tratada) -> float:
        if not self._centros or not carga_tratada:
            return 0
        return carga_tratada / self.total()

    def duracao_media(self) -> float:
        if not self._centros or not self.total():
            return 0
        return self.tempo_total() / self.total()

    def retornar_resumo_tempo_por_centro(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Centro de Tratamento",
                    "Tempo Total",
                    "Tempo Médio",
                ]
            )
        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Tempo Total": centro.falhas_tecnicas.tempo_total(),
                    "Tempo Médio": centro.falhas_tecnicas.duracao_media(),
                }
                for centro in self._centros.values()
            ]
        ).sort_values(by="Tempo Total", ascending=False)

    def retornar_resumo_tempo_por_maquina(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Máquina",
                    "Tempo Total",
                    "Tempo Médio",
                ]
            )
        return pd.DataFrame(
            [
                {
                    "Máquina": maquina.rotulo,
                    "Tempo Total": maquina.falhas_tecnicas.tempo_total(),
                    "Tempo Médio": maquina.falhas_tecnicas.duracao_media(),
                }
                for centro in self._centros.values()
                for maquina in centro.maquinas.values()
            ]
        ).sort_values(by="Tempo Total", ascending=False)

    # def total_por_centro(self) -> pd.DataFrame:
    #     if not self._centros:
    #         return pd.DataFrame(
    #             columns=[
    #                 "Centro de Tratamento",
    #                 "Total de Falhas",
    #             ]
    #         )
    #     return pd.DataFrame(
    #         [
    #             {
    #                 "Centro de Tratamento": centro.nome_abreviado,
    #                 "Total de Falhas": centro.falhas_tecnicas.total(),
    #             }
    #             for centro in self._centros.values()
    #         ]
    #     ).sort_values(by="Total de Falhas", ascending=False)

    def por_maquina(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Máquina",
                    "Total de Falhas",
                    "Centro de Tratamento",
                ]
            )

        dfs = [
            centro.falhas_tecnicas.por_maquina().assign(
                **{"Centro de Tratamento": centro.nome_abreviado}
            )
            for centro in self._centros.values()
        ]

        df_concat = (
            pd.concat(dfs, ignore_index=True)
            if dfs
            else pd.DataFrame(
                columns=[
                    "Máquina",
                    "Total de Falhas",
                    "Centro de Tratamento",
                ]
            )
        )
        return df_concat.sort_values(by="Total de Falhas", ascending=False)

    def duracao_media_por_centro(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Centro de Tratamento",
                    "Duração Média",
                ]
            )
        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Duração Média": centro.falhas_tecnicas.duracao_media_por_centro(),
                }
                for centro in self._centros.values()
            ]
        ).sort_values(by="Duração Média", ascending=False)

    def duracao_media_por_maquina(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Máquina",
                    "Duração Média",
                    "Centro de Tratamento",
                ]
            )

        dfs = [
            centro.falhas_tecnicas.duracao_media_por_maquina().assign(
                **{"Centro de Tratamento": centro.nome_abreviado}
            )
            for centro in self._centros.values()
        ]

        df_concat = (
            pd.concat(dfs, ignore_index=True)
            if dfs
            else pd.DataFrame(
                columns=[
                    "Máquina",
                    "Duração Média",
                    "Centro de Tratamento",
                ]
            )
        )
        return df_concat.sort_values(
            by=[
                "Duração Média",
                "Centro de Tratamento",
            ],
            ascending=[False, True],
        )

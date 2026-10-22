import pandas as pd


class EmpresaAtolamentosManager:
    def __init__(self, centros: dict):
        self._centros = centros

    def total(self) -> int:
        if not self._centros:
            return 0
        return sum(centro.atolamentos.total() for centro in self._centros.values())

    def tempo_total(self) -> float:
        if not self._centros:
            return 0
        return sum(
            centro.atolamentos.tempo_total() for centro in self._centros.values()
        )

    def duracao_media(self) -> float:
        total = self.total()
        if total == 0:
            return 0.0
        return self.tempo_total() / total

    def media_diaria(self) -> float:
        if not self._centros:
            return 0
        total_atolamentos = self.total()

        # Soma os dias únicos considerados em cada centro
        dias_totais = sum(
            m._atolamentos.quantidade_dias_com_registros()
            for c in self._centros.values()
            for m in c.maquinas.values()
        )

        if dias_totais == 0:
            return 0.0
        return round(total_atolamentos / dias_totais)

    def media_objetos_por_atolamento(self, carga_total: int) -> float:
        total_atolamentos = self.total()
        if total_atolamentos == 0:
            return 0.0
        return round(carga_total / total_atolamentos, 2)

    def media_objetos_induzidos_por_atolamentos_nos_centros(
        self, carga_total: int
    ) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Centro de Tratamento",
                    "Objetos por Atolamento",
                ]
            )
        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Objetos Induzidos": (
                        carga_total / centro.atolamentos.total()
                        if carga_total > 0
                        else 0
                    ),
                }
                for centro in self._centros.values()
            ]
        ).sort_values(by="Objetos Induzidos", ascending=False)

    def media_objetos_induzidos_por_atolamentos_por_maquina(
        self, carga_total: int
    ) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Nº Máquina",
                    "Objetos por Atolamento",
                ]
            )
        return pd.DataFrame(
            [
                {
                    "Nº Máquina": maquina.rotulo,
                    "Objetos por Atolamento": (
                        carga_total / maquina.atolamentos.total_atolamentos()
                        if carga_total > 0
                        else 0
                    ),
                    "Centro de Tratamento": centro.nome_abreviado,
                }
                for centro in self._centros.values()
                for maquina in centro.maquinas.values()
            ]
        ).sort_values(
            by=[
                "Objetos por Atolamento",
            ],
            ascending=[False],
        )

    def por_centro(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=["Centro de Tratamento", "Total de Atolamentos"]
            )
        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Total de Atolamentos": centro.atolamentos.total(),
                }
                for centro in self._centros.values()
            ]
        ).sort_values(by="Total de Atolamentos", ascending=False)

    def duracao_media_por_centro(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Centro de Tratamento",
                    "Tempo Médio",
                ]
            )
        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Tempo Médio": centro.atolamentos.duracao_media(),
                }
                for centro in self._centros.values()
            ]
        ).sort_values(by="Tempo Médio", ascending=False)

    def por_maquina(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Nº Máquina",
                    "Total de Atolamentos",
                    "Centro de Tratamento",
                ]
            )
        dfs = [
            centro.atolamentos.por_maquina().assign(
                **{"Centro de Tratamento": centro.nome_abreviado}
            )
            for centro in self._centros.values()
        ]
        df_concat = (
            pd.concat(dfs, ignore_index=True)
            if dfs
            else pd.DataFrame(
                columns=[
                    "Nº Máquina",
                    "Total de Atolamentos",
                    "Centro de Tratamento",
                ]
            )
        )
        return df_concat.sort_values(
            by=[
                "Total de Atolamentos",
            ],
            ascending=[False],
        )

    def duracao_media_por_maquina(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=["Nº Máquina", "Tempo Médio", "Centro de Tratamento"]
            )
        dfs = [
            centro.atolamentos.duracao_media_por_maquina().assign(
                **{"Centro de Tratamento": centro.nome_abreviado}
            )
            for centro in self._centros.values()
        ]
        df_concat = (
            pd.concat(dfs, ignore_index=True)
            if dfs
            else pd.DataFrame(
                columns=["Nº Máquina", "Duração Média", "Centro de Tratamento"]
            )
        )
        return df_concat.sort_values(
            by=[
                "Duração Média",
                "Centro de Tratamento",
            ],
            ascending=[False, True],
        )

    def resumo_tempo_por_centro(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Centro de Tratamento",
                    "Tempo Total",
                ]
            )
        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Tempo Total": centro.atolamentos.tempo_total(),
                }
                for centro in self._centros.values()
            ]
        ).sort_values(by="Tempo Total", ascending=False)

    def resumo_tempo_por_maquina(self) -> pd.DataFrame:
        if not self._centros:
            return pd.DataFrame(
                columns=[
                    "Nº Máquina",
                    "Tempo Total",
                ]
            )
        dados = []
        for centro in self._centros.values():
            for maquina in centro.maquinas.values():
                dados.append(
                    {
                        "Nº Máquina": maquina.rotulo,
                        "Tempo Total": maquina.atolamentos.tempo_total_atolamentos(),
                    }
                )

        df = pd.DataFrame(dados)

        if df.empty:
            return pd.DataFrame(
                columns=[
                    "Nº Máquina",
                    "Tempo Total",
                ]
            )
        return df.sort_values(by="Tempo Total", ascending=False)

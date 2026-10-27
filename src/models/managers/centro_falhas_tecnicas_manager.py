import pandas as pd


class CentroFalhasTecnicasManager:
    def __init__(self, maquinas, nome_abreviado):
        self.maquinas = maquinas
        self._nome_abreviado = nome_abreviado

    def total(self):
        return sum(
            maquina.falhas_tecnicas.total() for maquina in self.maquinas.values()
        )

    def tempo_total(self):
        return sum(
            maquina.falhas_tecnicas.tempo_total() for maquina in self.maquinas.values()
        )

    def media_objetos_por_falha(self, carga_tratada):
        return carga_tratada / self.total()

    def duracao_media(self):
        if not self.total():
            return 0
        return self.tempo_total() / self.total()

    def duracao_media_por_centro(self):
        if not self.total():
            return 0
        return self.tempo_total() / self.total()

    def por_maquina(self) -> pd.DataFrame:
        if not self.maquinas:
            return pd.DataFrame(
                columns=[
                    "Nº Máquina",
                    "Total de Falhas",
                ]
            )

        return pd.DataFrame(
            [
                {
                    "Nº Máquina": maquina.rotulo,
                    "Total de Falhas": maquina.falhas_tecnicas.total(),
                }
                for maquina in self.maquinas.values()
            ]
        )

    def duracao_media_por_maquina(self) -> pd.DataFrame:
        if not self.maquinas:
            return pd.DataFrame(
                columns=[
                    "Nº Máquina",
                    "Duração Média",
                ]
            )

        return pd.DataFrame(
            [
                {
                    "Nº Máquina": maquina.rotulo,
                    "Duração Média": maquina.falhas_tecnicas.duracao_media(),
                }
                for maquina in self.maquinas.values()
            ]
        )

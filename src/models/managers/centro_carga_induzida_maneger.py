class CentroCargaInduzidaManager:
    def __init__(self, maquinas: dict, nome_abreviado: str):
        self._maquinas = maquinas
        self._nome_abreviado = nome_abreviado

    def total(self):
        return sum(
            maquina.carga_induzida.total() for maquina in self._maquinas.values()
        )

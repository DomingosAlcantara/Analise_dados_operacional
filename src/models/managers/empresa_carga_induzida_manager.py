class EmpresaCargaInduzidaManager:
    def __init__(self, centros: dict):
        self._centros = centros

    def total(self):
        if not self._centros:
            return 0
        return sum(centro.total_carga_induzida() for centro in self._centros.values())

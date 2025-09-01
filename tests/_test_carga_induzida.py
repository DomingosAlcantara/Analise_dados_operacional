import pytest

from src.models.carga_induzida_model import CargaInduzidaModel
from src.path_files import PathFiles as pf


@pytest.fixture(autouse=True, scope="module")
def model():
    """
    Configuração inicial para os testes.
    """
    return CargaInduzidaModel(pf.ARQUIVOS_CARGA_TRATADA)


class TestCargaInduzidaModel:
    def test_total_de_carga_induzida(self, model):
        """
        Testa o método total_de_carga_induzida.
        """
        total = model.total_de_carga_induzida()
        assert isinstance(
            total, int), "O total de carga induzida deve ser um inteiro."
        assert total >= 0, "O total de carga induzida não pode ser negativo."

    def test_media_carga_induzida(self, model):
        """
        Testa o método media_carga_induzida.
        """
        media = model.media_carga_induzida()
        assert isinstance(
            media, float), "A média de carga induzida deve ser um float."
        assert media >= 0, "A média de carga induzida não pode ser negativa."

    def test_rendimento_efetivo_hora(self, model):
        """
        Testa o método rendimento_efetivo_hora.
        """
        rendimento = model.rendimento_efetivo_hora()
        assert isinstance(
            rendimento, float), "O rendimento efetivo por hora deve ser um float."
        assert rendimento >= 0, "O rendimento efetivo por hora não pode ser negativo."

    def test_carga_induzida_por_centro(self, model):
        """
        Testa o método carga_induzida_por_centro.
        """
        pass

    def test_rendimento_efetivo_por_centro(self, model):
        """
        Testa o método rendimento_efetivo_por_centro.
        """
        pass

    def test_carga_induzida_por_maquina(self, model):
        """
        Testa o método carga_induzida_por_maquina.
        """
        pass

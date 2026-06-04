import pytest

from src.models.base.centro_tratamento_model import CentroTratamentoModel


@pytest.fixture
def model(mock_carga_tratada):
    return CentroTratamentoModel(id_centro=431115).configurar(mock_carga_tratada)


class TestCentroTratamentoModel:
    def test_total_carga_induzida(self, model):
        total_carga = model.total_carga_induzida()
        assert total_carga == 29612  # Valor esperado para o teste

    def test_media_carga_induzida(self, model):
        media_carga = model.media_carga_induzida()
        assert media_carga == 29612  # Valor esperado para o teste

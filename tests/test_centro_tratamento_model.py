import pytest

from src.models.base.centro_tratamento_model import CentroTratamentoModel


@pytest.fixture
def model(mock_carga_tratada):
    mock_ct = mock_carga_tratada[mock_carga_tratada["código_mcu_ctc"] == 431115]
    return (
        CentroTratamentoModel(id_centro=431115)
        .configurar({"carga tratada": mock_ct})
        .filtrar_dados_por_data("2023-01-01", "2023-12-31")
    )


class TestCentroTratamentoModel:
    def test_total_carga_induzida(self, model):
        total_carga = model.total_carga_induzida()
        assert total_carga == 51255, "Valor esperado 51255"

    def _test_media_carga_induzida(self, model):
        media_carga = model.media_carga_induzida()
        assert media_carga == 25627, "Valor esperado 25627"

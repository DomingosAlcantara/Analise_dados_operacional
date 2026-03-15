import pytest

from src.models.base.centro_tratamento_model import CentroTratamentoModel


@pytest.fixture
def model(mock_dataframe):

    return CentroTratamentoModel(id_centro=431115, df=mock_dataframe)


class TestCentroTratamentoModel:

    def test_retorna_nome_centro(self, model):
        nome_centro = model.retornar_nome_centro()
        assert nome_centro == "CTC1"

    def test_retorna_maquinas(self, model):
        maquinas = model.retornar_maquinas()
        print(f"Máquinas retornadas: {len(maquinas)}")
        assert len(maquinas) >= 1
        assert maquinas[0]._id_maquina == "M001"

    def test_total_carga_induzida(self, model):
        total_carga = model.total_carga_induzida()
        assert total_carga == 94832  # Valor esperado para o teste

    def test_media_carga_induzida(self, model):
        media_carga = model.media_carga_induzida()
        assert media_carga == 500  # Valor esperado para o teste

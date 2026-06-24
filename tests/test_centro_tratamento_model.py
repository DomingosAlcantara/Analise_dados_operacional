import pandas as pd
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

    def test_media_carga_induzida(self, model):
        media_carga = model.media_carga_induzida()
        assert media_carga == 25628, "Valor esperado 25628"

    def test_retornar_rendimento_efetivo_medio(self, model):
        rendimento_medio = model.retornar_rendimento_efetivo_medio()
        assert rendimento_medio >= 0, "O rendimento efetivo médio deve ser não negativo"

    def test_obter_media_diaria(self, model):
        media_diaria = model.obter_media_diaria()
        assert (
            media_diaria >= 0
        ), "A média diária de carga induzida deve ser não negativa"

    def test_retornar_carga_induzida_por_maquina(self, model):
        carga_por_maquina = model.retornar_carga_induzida_por_maquina()
        assert isinstance(carga_por_maquina, pd.DataFrame), "Deve retornar um DataFrame"
        assert not carga_por_maquina.empty, "O DataFrame não deve estar vazio"

    def test_retornar_rendimento_efetivo_por_maquina(self, model):
        rendimento_por_maquina = model.retornar_rendimento_efetivo_por_maquina()
        assert isinstance(
            rendimento_por_maquina, pd.DataFrame
        ), "Deve retornar um DataFrame"
        assert not rendimento_por_maquina.empty, "O DataFrame não deve estar vazio"

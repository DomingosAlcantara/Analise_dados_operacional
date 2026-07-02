import pandas as pd
import pytest

from src.models.base.centro_tratamento_model import CentroTratamentoModel


@pytest.fixture(scope="module")
def model(mock_dados_globais):
    id_alvo = 431115
    return (
        CentroTratamentoModel(id_centro=id_alvo)
        .configurar(
            {
                chave: df[df["codigo_mcu_ctc"] == id_alvo]
                for chave, df in mock_dados_globais.items()
            }
        )
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

    def test_retornar_total_de_falhas(self, model):
        total_falhas = model.retornar_total_de_falhas()
        assert isinstance(total_falhas, int), "Deve retornar um inteiro"
        assert total_falhas == 4, "O total de falhas deve ser 4"

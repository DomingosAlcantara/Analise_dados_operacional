import pytest
from pandas import DataFrame

from src.models.base.maquina_model import MaquinaModel


@pytest.fixture
def model(mock_carga_tratada: DataFrame):
    """
    Configuração inicial para os testes.
    """
    mock_maquina = mock_carga_tratada[mock_carga_tratada["nº_máquina"] == 138]
    return MaquinaModel(138, {"carga_tratada": mock_maquina}).filtrar_dados_por_data(
        "2023-01-01", "2023-12-31"
    )


class Test_MaquinaModel:

    def test_total_carga_induzida(self, model):
        """
        Testa o método total_carga_induzida.
        """
        total_carga = model.total_carga_induzida()
        print(f"Total de carga induzida: {total_carga}")

        assert isinstance(total_carga, int), "Deve retornar um inteiro"
        assert total_carga == 29612, "O total de carga deve ser 29612"

    def _test_media_carga_induzida(self, model):
        """
        Testa o método media_carga_induzida.
        """
        media_carga = model.media_carga_induzida()

        print(f"Média de carga induzida: {media_carga}")

        assert isinstance(media_carga, float), "Deve retornar um float"
        assert media_carga == pytest.approx(
            14806, 0.01
        ), "A média de carga induzida deve ser aproximadamente 14806"

    def _test_retornar_rendimento_efetivo_medio(self, model):
        """
        Testa o método retornar_rendimento_efetivo_medio.
        """
        rendimento = model.retornar_rendimento_efetivo_medio()

        assert isinstance(rendimento, float), "Deve retornar um float"
        assert rendimento == pytest.approx(
            16714, 0.01
        ), "O rendimento deve ser aproximadamente 16714"

    def _test_tempo_plano_carregado(self, model):
        """
        Testa o método tempo_plano_carregado.
        """
        tempo_plano = model.tempo_plano_carregado()

        assert isinstance(tempo_plano, float), "Deve retornar um float"
        assert tempo_plano == pytest.approx(
            5.883333, rel=1e-3
        ), "O tempo de plano carregado deve ser aproximadamente 5.88"

    def _test_planos_carregados(self, model):
        """
        Testa o método que lista os planos que foram carregados na máquina.
        """
        planos = model.listagem_planos_carregados()
        assert isinstance(planos, list), "Deve retornar uma lista"
        assert len(planos) == 4, "Deve conter 4 planos carregados"

import pytest
from pandas import DataFrame

from src.models.base.maquina_model import MaquinaModel


@pytest.fixture
def model(mock_dataframe: DataFrame):
    """
    Configuração inicial para os testes.
    """

    return MaquinaModel("M001", mock_dataframe)


class Test_MaquinaModel:

    def test_total_carga_induzida(self, model):
        """
        Testa o método total_carga_induzida.
        """
        total_carga = model.total_carga_induzida()

        assert isinstance(total_carga, int), "Deve retornar um inteiro"
        assert total_carga == 29612, "O total de carga deve ser 29612"

    def test_media_carga_induzida(self, model):
        """
        Testa o método media_carga_induzida.
        """
        media_carga = model.media_carga_induzida()

        print(f"Média de carga induzida: {media_carga}")

        assert isinstance(media_carga, float), "Deve retornar um float"
        assert media_carga == pytest.approx(
            14806, 0.01
        ), "A média de carga induzida deve ser aproximadamente 14806"

    def test_media_rendimento_efetivo(self, model):
        """
        Testa o método media_rendimento_efetivo.
        """
        rendimento = model.media_rendimento_efetivo()

        assert isinstance(rendimento, float), "Deve retornar um float"
        assert rendimento == pytest.approx(
            16714, 0.01
        ), "O rendimento deve ser aproximadamente 16714"

    def test_tempo_plano_carregado(self, model):
        """
        Testa o método tempo_plano_carregado.
        """
        tempo_plano = model.tempo_plano_carregado()

        assert isinstance(tempo_plano, float), "Deve retornar um float"
        assert tempo_plano == pytest.approx(
            5.883333, rel=1e-3
        ), "O tempo de plano carregado deve ser aproximadamente 5.88"

    def test_planos_carregados(self, model):
        """
        Testa o método que lista os planos que foram carregados na máquina.
        """
        planos = model.listagem_planos_carregados()
        assert isinstance(planos, list), "Deve retornar uma lista"
        assert len(planos) == 4, "Deve conter 4 planos carregados"

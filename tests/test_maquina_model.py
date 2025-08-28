import pytest
from pandas import DataFrame

from src.models.base.maquina_model import MaquinaModel


@pytest.fixture(scope="module")
def model():
    """
    Configuração inicial para os testes.
    """
    data = {
        "quantidade_induzida": [20847, 19298, 20792, 6985],
        "nome_do_plano_de_triagem":
        ["PLANO A", "PLANO B", "PLANO C", "PLANO D"],
        "tempo_total_do_plano": ["02:17", "02:14", "01:03", "00:19"]
    }
    df = DataFrame(data)
    return MaquinaModel("M001", df)


class Test_MaquinaModel:

    def test_retornar_total_carga(self, model):
        """
        Testa o método retornar_total_carga.
        """
        total_carga = model.retornar_total_carga()

        assert isinstance(total_carga, int), "Deve retornar um inteiro"
        assert total_carga == 67922, "O total de carga deve ser 750"

    def test_media_rendimento_efetivo(self, model):
        """
        Testa o método media_rendimento_efetivo.
        """
        rendimento = model.media_rendimento_efetivo()

        assert isinstance(rendimento, float), "Deve retornar um float"
        assert rendimento == pytest.approx(16980.5, 0.01), \
            "O rendimento deve ser aproximadamente 16980.5"

    def test_tempo_plano_carregado(self, model):
        """
        Testa o método tempo_plano_carregado.
        """
        tempo_plano = model.tempo_plano_carregado()

        assert isinstance(tempo_plano, float), "Deve retornar um float"
        assert tempo_plano == pytest.approx(5.883333, rel=1e-3), \
            "O tempo de plano carregado deve ser aproximadamente 5.88"

    def test_planos_carregados(self, model):
        """
        Testa o método que lista os planos que foram carregados na máquina.
        """
        planos = model.listagem_planos_carregados()
        assert isinstance(planos, list), "Deve retornar uma lista"
        assert len(planos) == 4, "Deve conter 4 planos carregados"

import pytest

from src.models.base.maquina_model import MaquinaModel


@pytest.fixture
def model(mock_dados_globais: dict):
    """
    Configuração inicial para os testes.
    """
    id_alvo = 138
    return MaquinaModel(
        id_alvo,
        {
            chave: df[df["no_maquina"] == id_alvo]
            for chave, df in mock_dados_globais.items()
        },
    ).filtrar_dados_por_data("2023-01-01", "2023-12-31")


class Test_MaquinaModel:

    def test_total_carga_induzida(self, model):
        """
        Testa o método total_carga_induzida.
        """
        total_carga = model.total_carga_induzida()

        assert isinstance(total_carga, int), "Deve retornar um inteiro"
        assert total_carga == 29612, "O total de carga deve ser 29612"

    def test_media_diaria_de_carga_induzida(self, model):
        """
        Testa o método media_carga_induzida.
        """
        media_carga = model.obter_media_diaria()

        assert isinstance(media_carga, float), "Deve retornar um float"
        assert media_carga == pytest.approx(
            14806, 0.01
        ), "A média de carga induzida deve ser aproximadamente 14806"

    def test_retornar_rendimento_efetivo_medio(self, model):
        """
        Testa o método retornar_rendimento_efetivo_medio.
        """
        rendimento = model.retornar_rendimento_efetivo_medio()

        assert isinstance(rendimento, float), "Deve retornar um float"
        assert rendimento == pytest.approx(
            16714, 0.01
        ), "O rendimento deve ser aproximadamente 16714"

    def test_retornar_total_de_falhas(self, model):
        """
        Testa o método retornar_total_de_falhas.
        """
        total_falhas = model.retornar_total_de_falhas()

        assert isinstance(total_falhas, int), "Deve retornar um inteiro"
        assert total_falhas == 2, "O total de falhas deve ser 2"

    def test_retornar_media_de_objetos_por_falha(self, model):
        """
        Testa o método retornar_media_de_objetos_por_falha.
        """
        media_objetos = model.retornar_media_de_objetos_por_falha()

        assert isinstance(media_objetos, float), "Deve retornar um float"
        assert media_objetos == pytest.approx(
            14806.0, 0.01
        ), "A média de objetos por falha deve ser aproximadamente 14806.0"

    def test_retornar_tempo_total_de_ocorrencias(self, model):
        """
        Testa o método retornar_tempo_total_de_ocorrencias.
        """
        tempo_total = model.retornar_tempo_total_de_ocorrencias()

        assert isinstance(tempo_total, (float, int)), "Deve retornar um número"
        # assert tempo_total == pytest.approx(
        #     0.5, 0.01
        # ), "O tempo total de ocorrências deve ser aproximadamente 0.5"

    def test_retornar_duracao_media_das_falhas(self, model):
        """
        Testa o método retornar_duracao_media_das_falhas.
        """
        duracao_media = model.retornar_duracao_media_das_falhas()

        assert isinstance(duracao_media, (float, int)), "Deve retornar um número"
        # assert duracao_media == pytest.approx(
        #     0.25, 0.01
        # ), "A duração média das falhas deve ser aproximadamente 0.25"

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

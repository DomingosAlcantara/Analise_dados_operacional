import pandas as pd
import pytest

from src.models.falhas_tecnicas_model import FalhasTecnicasModel


@pytest.fixture(scope="module")
def model(mock_falhas_tecnicas: pd.DataFrame):
    """
    Configuração inicial para os testes.
    """
    return FalhasTecnicasModel(mock_falhas_tecnicas).filtrar_dados_por_data(
        "2023-01-01", "2023-12-31"
    )


class Test_FalhasTecnicasModel:
    """Classe de testes relacionados às Falhas técnicas"""

    def test_total_falhas_tecnicas(self, model):
        """
        Testa a obtenção do total de falhas técnicas.
        """
        total_falhas = model.total_falhas_tecnicas()

        assert isinstance(total_falhas, int), "Deve retornar um inteiro"
        assert total_falhas >= 0, "O total de falhas não deve ser negativo"

    def test_falhas_tecnicas_por_centro(self, model):
        """
        Testa a obtenção do total de falhas técnicas por centro de tratamento.
        """
        falhas_por_centro = model.falhas_tecnicas_por_centro()

        assert isinstance(falhas_por_centro, pd.DataFrame), "Deve retornar um DataFrame"
        for centro, total in falhas_por_centro.items():
            assert isinstance(
                centro, str
            ), "As chaves devem ser strings (nomes dos centros)"
            assert isinstance(
                total, int
            ), "Os valores devem ser inteiros (total de falhas)"
            assert total >= 0, "O total de falhas por centro não deve ser negativo"

    def test_retornar_metricas_falhas_tecnicas(self, model):
        """
        Testa a obtenção das métricas de falhas técnicas.
        """
        start_date = pd.to_datetime("14/08/2023", dayfirst=True).date()
        end_date = pd.to_datetime("18/08/2023", dayfirst=True).date()
        metricas = model.retornar_metricas_falhas_tecnicas(start_date, end_date)

        assert isinstance(metricas, dict), "Deve retornar um dicionário"
        assert "total_de_falhas" in metricas, "Deve conter a chave 'total_falhas'"
        assert (
            "media_objetos_falha" in metricas
        ), "Deve conter a chave 'media_objetos_falha'"

        total_falhas = metricas.get("total_de_falhas", 0)
        media_objetos_falha = metricas.get("media_objetos_falha", 0)
        tempo_total_ocorrencias = metricas.get("tempo_total_ocorrencias", 0)
        duracao_media_falhas = metricas.get("duracao_media_falha", 0)

        assert isinstance(total_falhas, int), "'total_falhas' deve ser um inteiro"
        assert total_falhas >= 0, "'total_falhas' não deve ser negativo"
        assert isinstance(
            media_objetos_falha, (int, float)
        ), "'media_objetos_falha' deve ser um número (inteiro ou float)"
        assert media_objetos_falha >= 0, "'media_objetos_falha' não deve ser negativa"
        assert isinstance(
            tempo_total_ocorrencias, (int, float)
        ), "'tempo_total_ocorrencias' deve ser um número (inteiro ou float)"
        assert (
            tempo_total_ocorrencias >= 0
        ), "'tempo_total_ocorrencias' não deve ser negativa"
        assert isinstance(
            duracao_media_falhas, (int, float)
        ), "'duracao_media_falhas' deve ser um número (inteiro ou float)"
        assert duracao_media_falhas >= 0, "'duracao_media_falhas' não deve ser negativa"

    # def test_falhas_kpi_e_graficos(self, model):
    #     """
    #     Testa a obtenção dos dados para os KPIs e gráficos relacionados às falhas técnicas.
    #     """
    #     start_date = pd.to_datetime("14/08/2023", dayfirst=True).date()
    #     end_date = pd.to_datetime("18/08/2023", dayfirst=True).date()

    #     dados_kpi = model.falhas_kpi_e_graficos(start_date, end_date)

    #     assert isinstance(dados_kpi, dict), "Deve retornar um dicionário"
    #     assert (
    #         "falhas_por_centro" in dados_kpi
    #     ), "Deve conter a chave 'falhas_por_centro'"
    #     assert "falhas_por_tipo" in dados_kpi, "Deve conter a chave 'falhas_por_tipo'"

    #     falhas_por_centro = dados_kpi.get("falhas_por_centro", {})
    #     falhas_por_tipo = dados_kpi.get("falhas_por_tipo", {})

    #     assert isinstance(
    #         falhas_por_centro, dict
    #     ), "'falhas_por_centro' deve ser um dicionário"
    #     for centro, total in falhas_por_centro.items():
    #         assert isinstance(
    #             centro, str
    #         ), "As chaves de 'falhas_por_centro' devem ser strings (nomes dos centros)"
    #         assert isinstance(
    #             total, int
    #         ), "Os valores de 'falhas_por_centro' devem ser inteiros (total de falhas)"
    #         assert total >= 0, "O total de falhas por centro não deve ser negativo"

    #     assert isinstance(
    #         falhas_por_tipo, dict
    #     ), "'falhas_por_tipo' deve ser um dicionário"
    #     for tipo, total in falhas_por_tipo.items():
    #         assert isinstance(
    #             tipo, str
    #         ), "As chaves de 'falhas_por_tipo' devem ser strings (descrição das falhas)"
    #         assert isinstance(
    #             total, int
    #         ), "Os valores de 'falhas_por_tipo' devem ser inteiros (total de falhas)"
    #         assert total >= 0, "O total de falhas por tipo não deve ser negativo"

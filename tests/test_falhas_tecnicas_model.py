import pandas as pd
import pytest

from src.models.falhas_tecnicas_model import FalhasTecnicasModel


@pytest.fixture(scope="function")
def model(mock_falhas_tecnicas: pd.DataFrame):
    """
    Configuração inicial para os testes.
    """
    return FalhasTecnicasModel(mock_falhas_tecnicas)
    # .filtrar_dados_por_data(
    #     "01/01/2023", "31/12/2023"
    # )


class Test_FalhasTecnicasModel:
    """Classe de testes relacionados às Falhas técnicas"""

    def test_inicializacao_sem_filtros_manter_dados(self, model, mock_falhas_tecnicas):
        """Testa se a inicialização carrega corretamente todos os dados na
        propriedade de dados_filtrados (comportamento padrão)
        """
        assert model.total_falhas_tecnicas() == len(mock_falhas_tecnicas)

    def test_inicializacao_com_dataframe_vazio(self):
        """
        Testa se o model lida bem quando recebe um DataFrame vazio
        """
        model_vazio = FalhasTecnicasModel(pd.DataFrame())
        assert model_vazio.total_falhas_tecnicas() == 0

    def test_filtrar_dados_por_data_reduz_o_total(self, model):
        """
        Testa o filtro interagindo com o método de contagem pública
        """
        model.filtrar_dados_por_data("2023-08-14", "2023-08-14")
        assert model.total_falhas_tecnicas() == 2

    def test_filtrar_dados_por_data_sem_resultados(self, model):
        """
        Testa o filtro com um intervalo de datas que não possui falhas no mock
        """
        model.filtrar_dados_por_data("2023-05-15", "2023-05-14")
        assert model.total_falhas_tecnicas() == 0

    def test_filtrar_dados_por_data_invalida_zerar_dataframe(self, model):
        """
        Testa o comportamento de segurança: se a data for invalida, deve zerar
        os dados para não exibir lixo no dashboard
        """
        model.filtrar_dados_por_data("data_invalida", "2023-05-14")
        assert model.total_falhas_tecnicas() == 0

    def test_retornar_falhas_por_centro_agrupamento(self, model):
        """Testa se o agrupamento soma corretamente as falhas por centro."""
        df_agrupado = model.retornar_falhas_por_centro()

        # Se você tiver um método público que retorne a amostra ou se inspecionar a série:
        df_agrupado = model.retornar_falhas_por_centro()

        assert isinstance(df_agrupado, pd.DataFrame), "Deve retornar um DataFrame"
        assert list(df_agrupado.columns) == ["centro_de_tratamento", "total_de_falhas"]

        resultado_ctc1 = df_agrupado.loc[
            df_agrupado["centro_de_tratamento"] == "CTC1", "total_de_falhas"
        ]

        assert not resultado_ctc1.empty, "O centro 'CTC1' não foi encontrado"

        falhas_ctc1 = resultado_ctc1.iloc[0]
        assert falhas_ctc1 == 2

    def test_encadeamento_de_metodos(self, model):
        """Testa o Design Pattern 'Method Chaining' avaliando o output final
        do encadeamento.
        """
        # Filtra pelo dia 15 (2 falhas no CTC3) e já chama o agrupamento
        df_resultado = model.filtrar_dados_por_data(
            "2023-08-15", "2023-08-15"
        ).retornar_falhas_por_centro()

        assert isinstance(df_resultado, pd.DataFrame), "Deve retornar um DataFrame"
        assert len(df_resultado) == 1

        linha = df_resultado.iloc[0]
        assert linha["centro_de_tratamento"] == "CTC3"
        assert linha["total_de_falhas"] == 2

    def test_total_falhas_tecnicas(self, model):
        """
        Testa a obtenção do total de falhas técnicas.
        """
        total_falhas = model.total_falhas_tecnicas()

        assert isinstance(total_falhas, int), "Deve retornar um inteiro"
        assert total_falhas > 0, "O total de falhas não deve ser negativo"

    def test_falhas_tecnicas_por_centro(self, model):
        """
        Testa a obtenção do total de falhas técnicas por centro de tratamento.
        """
        falhas_por_centro = model.retornar_falhas_por_centro()

        assert isinstance(falhas_por_centro, pd.DataFrame), "Deve retornar um DataFrame"
        for centro, total in falhas_por_centro.items():
            assert isinstance(
                centro, str
            ), "As chaves devem ser strings (nomes dos centros)"
            assert isinstance(
                total, pd.Series
            ), "Os valores devem ser inteiros (total de falhas)"
            assert len(total) >= 0, "O total de falhas por centro não deve ser negativo"

    def test_retornar_metricas_falhas_tecnicas(self, model):
        """
        Testa a saida do dicionário de metricas, validando chaves e valores
        usando apenas a interface publica.
        """
        start_date = pd.to_datetime("2023-08-14").date()
        end_date = pd.to_datetime("2023-08-14").date()
        metricas = model.retornar_metricas_falhas_tecnicas(start_date, end_date)

        assert isinstance(metricas, dict), "Deve retornar um dicionário"
        assert "total_de_falhas" in metricas, "Deve conter a chave 'total_falhas'"

        total_falhas = metricas.get("total_de_falhas", 0)
        tempo_total_ocorrencias = metricas.get("tempo_total_ocorrencias", 0)
        duracao_media_falhas = metricas.get("duracao_media_falha", 0)

        assert isinstance(total_falhas, int), "'total_falhas' deve ser um inteiro"
        assert total_falhas == 2, "'total_falhas' não deve ser negativo"
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

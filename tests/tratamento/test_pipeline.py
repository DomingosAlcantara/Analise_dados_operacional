import pytest
from pandas import DataFrame

from src.tratamento.pipeline_comum import Pipeline_Comum

# @pytest.fixture
# def mock_transformacoes(monkeypatch, mock_carga_tratada):
#     def mock_method(*args, **kwargs):
#         return mock_carga_tratada

#     monkeypatch.setattr(Pipeline_Comum, "aplicar_transformacoes", mock_method)


# @pytest.fixture
# def model():
#     return Pipeline_Comum()


class TestPipeline:

    def test_normalizar_colunas(self):
        df_mock = DataFrame(
            columns=["Nome da Coluna", "Outra Coluna", "Ação", "Tensão Máxima"]
        )
        df_normalizado = Pipeline_Comum.normalizar_colunas(df_mock)
        print(df_normalizado.columns)
        assert list(df_normalizado.columns) == [
            "nome_da_coluna",
            "outra_coluna",
            "acao",
            "tensao_maxima",
        ]

    def test_normalizar_colunas_vazio(self):
        df_mock = DataFrame()
        df_normalizado = Pipeline_Comum.normalizar_colunas(df_mock)
        assert df_normalizado.empty

    def test_normalizar_colunas_com_none_levanta_erro(self):
        with pytest.raises(AttributeError):
            Pipeline_Comum.normalizar_colunas(None)

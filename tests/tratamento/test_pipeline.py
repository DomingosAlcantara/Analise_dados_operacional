import pytest

from src.tratamento.pipeline import Pipeline


@pytest.fixture
def mock_transformacoes(monkeypatch, mock_dataframe):
    def mock_method(*args, **kwargs):
        return mock_dataframe

    monkeypatch.setattr(Pipeline, "aplicar_transformacoes", mock_method)


@pytest.fixture
def model(mock_dataframe, mock_transformacoes):
    return Pipeline(mock_dataframe, transformacoes=mock_transformacoes)


class TestPipeline:

    def test_inicializacao(self, model):
        assert isinstance(model, Pipeline)

    def test_executar_sem_dataframe(self):
        pipeline = Pipeline(dataframe=None, transformacoes=[])
        with pytest.raises(ValueError, match="DataFrame não fornecido"):
            pipeline.aplicar_transformacoes()

    def test_executar_sem_transformacoes(self, mock_dataframe):
        pipeline = Pipeline(mock_dataframe, transformacoes=[])
        with pytest.raises(ValueError, match="Transformações não fornecidas"):
            pipeline.aplicar_transformacoes()

    def test_executar_com_dataframe_valido(self, model):
        df_tratado = model.aplicar_transformacoes()
        assert not df_tratado.empty

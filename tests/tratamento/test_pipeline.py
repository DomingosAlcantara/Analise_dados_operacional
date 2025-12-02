import pandas as pd
import pytest

from src.tratamento.pipeline import Pipeline


@pytest.fixture
def mock_dataframe():
    dados = {
        "data_de_triagem": [
            "14/08/2023",
            "14/08/2023",
            "14/08/2023",
            "14/08/2023",
            "15/08/2023",
            "15/08/2023",
            "15/08/2023",
            "15/08/2023",
            "15/08/2023",
            "15/08/2023",
        ],
        "codigo_mcu_ctc": [
            "00431115",
            "00431083",
            "00437023",
            "00437023",
            "00437023",
            "00437023",
            "00431115",
            "00431083",
            "00437023",
            "00437023",
        ],
        "centro_de_tratamento": [
            "CTC1",
            "CTC2",
            "CTC3",
            "CTC3",
            "CTC3",
            "CTC3",
            "CTC1",
            "CTC2",
            "CTC3",
            "CTC3",
        ],
        "nº_máquina": [
            "M001",
            "M002",
            "M003",
            "M003",
            "M003",
            "M003",
            "M001",
            "M002",
            "M003",
            "M003",
        ],
        "nome_do_plano_de_triagem": [
            "PLANO A",
            "PLANO B",
            "PLANO C",
            "PLANO C",
            "PLANO D",
            "PLANO E",
            "PLANO A",
            "PLANO B",
            "PLANO C",
            "PLANO D",
        ],
        "quantidade_induzida": [
            20847,
            19298,
            20792,
            6985,
            1234,
            4321,
            8765,
            2345,
            6789,
            3456,
        ],
        "rendimento_efetivo/h": [
            19997,
            18470,
            24960,
            27561,
            12237,
            17701,
            13431,
            19920,
            12631,
            5251,
        ],
    }

    df = pd.DataFrame(dados, index=dados["codigo_mcu_ctc"])
    return df


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

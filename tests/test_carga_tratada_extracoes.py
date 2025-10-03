"""TDD sobre os dados de carga trada para persistência no banco de dados.
    """

import os

import pytest
from pandas import DataFrame

from src.extracoes.carga_tratada import CargaTratada


@pytest.fixture
def mock_diretorio_existe(monkeypatch):
    # Mock para simular que o diretório existe
    monkeypatch.setattr(os.path, "exists", lambda _: True)


@pytest.fixture
def mock_listagem_arquivos(monkeypatch):
    # Mock para simular a listagem de arquivos no diretório
    mock_files = ["file1.xls", "file2.xls"]
    monkeypatch.setattr(os, "listdir", lambda _: mock_files)
    return mock_files


@pytest.fixture
def model(mock_diretorio_existe):
    return CargaTratada()


@pytest.fixture
def dados_mock():
    dados = {
        "data_de_triagem": ["14/08/2023", "14/08/2023", "14/08/2023",
                            "14/08/2023", "15/08/2023", "15/08/2023",
                            "15/08/2023", "15/08/2023", "15/08/2023",
                            "15/08/2023"],
        "codigo_mcu_ctc": ["00431115", "00431083", "00437023", "00437023",
                           "00437023", "00437023", "00431115", "00431083",
                           "00437023", "00437023"],
        "centro_de_tratamento": ["CTC1", "CTC2", "CTC3", "CTC3", "CTC3",
                                 "CTC3", "CTC1", "CTC2", "CTC3", "CTC3"],
        "nº_máquina": ["M001", "M002", "M003", "M003", "M003",
                       "M003", "M001", "M002", "M003", "M003"],
        "nome_do_plano_de_triagem": ["PLANO A", "PLANO B", "PLANO C",
                                     "PLANO C", "PLANO D", "PLANO E",
                                     "PLANO A", "PLANO B", "PLANO C",
                                     "PLANO D"],
        "quantidade_induzida": [20847, 19298, 20792, 6985, 1234,
                                4321, 8765, 2345, 6789, 3456],
        "rendimento_efetivo/h": [19997, 18470, 24960, 27561, 12237,
                                 17701, 13431, 19920, 12631, 5251],
    }

    df = DataFrame(dados, index=dados["codigo_mcu_ctc"])
    return df


class Test_CargaTratadaExtracoes:

    def test_listar_arquivos(self, model, mock_listagem_arquivos):
        """
        Testa se esta sendo retornado uma lista de arquivos.
        """
        arquivos = model.listar_arquivos()
        assert arquivos == mock_listagem_arquivos, \
            f"Esperado: {mock_listagem_arquivos}, Obtido: {arquivos}"

    def test_colunas_necessarias(self, dados_mock):
        """
        Testa se o DataFrame contém as colunas necessárias.
        """
        colunas_necessarias = {
            "data_de_triagem",
            "codigo_mcu_ctc",
            "centro_de_tratamento",
            "nº_máquina",
            "nome_do_plano_de_triagem",
            "quantidade_induzida",
            "rendimento_efetivo/h"
        }
        colunas_df = set(dados_mock.columns)

        assert colunas_necessarias.issubset(colunas_df), \
            f"O DataFrame deve conter as colunas: {colunas_necessarias}. " \
            f"Colunas presentes: {colunas_df}"

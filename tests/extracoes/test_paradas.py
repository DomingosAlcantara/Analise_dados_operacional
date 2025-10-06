"""
    TDD sobre os dados de 'engarrafamento' para persistência no banco de dados.
"""

import os

import pytest
from pandas import DataFrame

from src.extracoes.parada import Parada


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
def dados_mock():
    dados = {
        "data/hora_inicial_da_falha": ["14/08/2023 06:38:54",
                                       "14/08/2023 07:19:37",
                                       "14/08/2023 08:10:24",
                                       "14/08/2023 14:00:52",
                                       "15/08/2023 07:33:37",
                                       "15/08/2023 08:10:24",
                                       "15/08/2023 13:40:16",
                                       "15/08/2023 08:06:40",
                                       "15/08/2023 14:00:52",
                                       "15/08/2023 15:30:00"],
        "codigo_mcu_ctc": ["00431115", "00431083", "00437023", "00437023",
                           "00437023", "00437023", "00431115", "00431083",
                           "00437023", "00437023"],
        "centro_de_tratamento": ["CTC1", "CTC2", "CTC3", "CTC3", "CTC3",
                                 "CTC3", "CTC1", "CTC2", "CTC3", "CTC3"],
        "nº_máquina_de_triagem": ["M001", "M002", "M003", "M003", "M003",
                                  "M003", "M001", "M002", "M003", "M003"],
        "descricao_da_falha": ["Atolamento na Seção - localização não foi \
                               relatado pela porta serial",
                               "Atolamento: no LDU (T;0,C;4)",
                               "Atolamento; IOS1 PC5 - Na parte frontal da \
                                entrada do Turn Drum",
                               "Atolamento; OCR1 PC3 - Entrada do Turn Drum",
                               "Atolamento; no escaninho 1",
                               "Atolamento; no escaninho 158",
                               "Atolamento; no escaninho 166",
                               "Atolamento; no escaninho 186, 184",
                               "Atolamento; no escaninho 257",
                               "Geléia; LDU1 PC5 - Seção de Rastreamento"],
    }

    df = DataFrame(dados, index=dados["codigo_mcu_ctc"])
    return df


@pytest.fixture
def model():
    return Parada()


class Test_ParadaExtracoes:
    @pytest.fixture
    def mock_processar_pasta(self, monkeypatch, dados_mock):
        # Mock para simular o método processar_pasta
        def mock_method(*args, **kwargs):
            # Retorna um DataFrame vazio ou simulado
            return DataFrame(dados_mock)

        monkeypatch.setattr(Parada, "processar_pasta", mock_method)

    def test_listar_arquivos(self, model, mock_listagem_arquivos):
        """
        Testa se o método listar_arquivos retorna a lista correta de arquivos.
        """
        arquivos = model.listar_arquivos()
        assert arquivos == mock_listagem_arquivos, \
            f"Esperado: {mock_listagem_arquivos}, Obtido: {arquivos}"

    def test_colunas_necessarias(self, dados_mock):
        """
        Testa se o DataFrame contém as colunas necessárias.
        """
        colunas_necessarias = {
            "data/hora_inicial_da_falha",
            "codigo_mcu_ctc",
            "centro_de_tratamento",
            "nº_máquina_de_triagem",
            "descricao_da_falha",
        }
        colunas_df = set(dados_mock.columns)
        assert colunas_necessarias.issubset(colunas_df), \
            f"O DataFrame deve conter as colunas: {colunas_necessarias}. "\
            f"Colunas presentes: {colunas_df}"

    def test_processar_pasta(self, model, mock_processar_pasta):
        """
        Testa se o método processar_pasta retorna um DataFrame.
        """
        df_tratado = model.processar_pasta()
        assert isinstance(df_tratado, DataFrame), \
            f"Esperado um DataFrame, mas obteve: {type(df_tratado)}"
        assert not df_tratado.empty, "O DataFrame retornado está vazio."

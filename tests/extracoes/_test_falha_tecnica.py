"""TDD sobre os dados de Falhas Técnicas para persistência no banco de dados."""

import os

import pytest
from pandas import DataFrame

from src.extracoes.falha_tecnica import FalhaTecnica


class Test_FalhaTecnica:
    """Testa a extração e transformação dos dados de Falhas Técnicas."""

    @pytest.fixture
    def mock_diretorio_existe(self, monkeypatch):
        # Mock para simular que o diretório existe
        monkeypatch.setattr(os.path, "exists", lambda _: True)

    @pytest.fixture
    def mock_listagem_arquivos(self, monkeypatch):
        # Mock para simular a listagem de arquivos no diretório
        mock_files = ["file1.xls", "file2.xls"]
        monkeypatch.setattr(os, "listdir", lambda _: mock_files)
        return mock_files

    @pytest.fixture
    def falha_tecnica(self, mock_diretorio_existe) -> FalhaTecnica:
        """Instancia a classe FalhaTecnica para os testes."""
        return FalhaTecnica(mock_diretorio_existe)

    def mock_dados_falha_tecnica(self, monkeypatch):
        # Mock para simular os dados de Falha Técnica
        dados = {
            "codigo_mcu_ctc": ["00431115", "00431083", "00431083", "00437023"],
            "centro_de_tratamento": ["CTC1", "CTC2", "CTC2", "CTC3"],
            "nº_máquina": [1, 2, 2, 3],
            "descrição_da_falha": ["Falha A", "Falha B", "Falha B", "Falha C"],
            "data/hora_inicial_da_falha": [
                "14/08/2023 10:00",
                "14/08/2023 11:00",
                "14/08/2023 11:00",
                "15/08/2023 09:30",
            ],
        }
        df_mock = DataFrame(dados)
        monkeypatch.setattr(
            FalhaTecnica,
            "extrair_dados",
            lambda self: df_mock,
        )

    def test_extrair_dados(self, falha_tecnica: FalhaTecnica) -> None:
        """Testa a extração dos dados de Falhas Técnicas."""
        df: DataFrame = falha_tecnica.extrair_dados()
        assert not df.empty, "O DataFrame extraído está vazio."
        assert list(df.columns) == [
            "codigo_mcu_ctc",
            "centro_de_tratamento",
            "nº_máquina",
        ], "As colunas do DataFrame não correspondem ao esperado."

    def test_transformar_dados(self, falha_tecnica: FalhaTecnica) -> None:
        """Testa a transformação dos dados de Falhas Técnicas."""
        df_extraido: DataFrame = falha_tecnica.extrair_dados()
        df_transformado: DataFrame = falha_tecnica.transformar_dados(df_extraido)
        assert not df_transformado.empty, "O DataFrame transformado está vazio."
        assert all(
            col in df_transformado.columns
            for col in [
                "id_falha_tecnica",
                "descricao",
                "data_ocorrencia",
                "status",
                "ano_ocorrencia",
            ]
        ), "As colunas transformadas não correspondem ao esperado."
        assert (
            df_transformado["ano_ocorrencia"].dtype == int
        ), "A coluna 'ano_ocorrencia' não é do tipo inteiro."

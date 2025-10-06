import os

import pandas as pd
import pytest

from src.extracoes.extracoes import Extracoes


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
    return Extracoes(path="mock_path")


class Test_Extracoes:
    """Classe de teste para a classe Extracoes.
    """

    def test_listar_arquivos(self, model, mock_listagem_arquivos):
        arquivos = model.listar_arquivos()
        assert arquivos == mock_listagem_arquivos

    def test_construir_caminhos_completos(self, model, mock_listagem_arquivos):
        caminhos = model.construir_caminhos_completos(mock_listagem_arquivos)
        caminhos_esperados = [os.path.join(
            model._path, f) for f in mock_listagem_arquivos]
        assert caminhos == caminhos_esperados

    def test_listar_arquivos_diretorio_inexistente(self, monkeypatch):
        # Mock para simular que o diretório não existe
        monkeypatch.setattr(os.path, "exists", lambda _: False)
        model = Extracoes(path="non_existent_path")
        arquivos = model.listar_arquivos()
        assert arquivos == []

    def test_construir_caminhos_completos_lista_vazia(self, model):
        caminhos = model.construir_caminhos_completos([])
        assert caminhos == []

    def test_processar_arquivos_lista_vazia(self, model):
        df = model.processar_arquivos([], colunas_tipo={}, linhas_para_pular=0)
        assert df.empty

    def test_processar_arquivos_colunas_invalidas(self, model, tmp_path):
        # Cria um arquivo Excel temporário com colunas inválidas
        arquivo_excel = tmp_path / "test_invalid_columns.xls"
        df_invalido = pd.DataFrame({
            "Coluna1": [1, 2],
            "Coluna2": [3, 4]
        })
        df_invalido.to_excel(arquivo_excel, index=False)

        caminhos = [str(arquivo_excel)]
        colunas_tipo = {"ColunaInexistente": str}
        df_resultado = model.processar_arquivos(
            caminhos, colunas_tipo=colunas_tipo, linhas_para_pular=0)
        assert df_resultado.empty

    def test_processar_arquivos_linhas_para_pular_invalidas(self, model,
                                                            tmp_path):
        # Cria um arquivo Excel temporário
        arquivo_excel = tmp_path / "test_skip_rows.xls"
        df_valido = pd.DataFrame({
            "Coluna1": [1, 2, 3],
            "Coluna2": [4, 5, 6]
        })
        df_valido.to_excel(arquivo_excel, index=False)
        caminhos = [str(arquivo_excel)]
        colunas_tipo = {"Coluna1": int, "Coluna2": int}  # Tipos corretos
        df_resultado = model.processar_arquivos(
            caminhos, colunas_tipo=colunas_tipo, linhas_para_pular=5)
        assert df_resultado.empty

    def test_processar_arquivos_sucesso(self, model, tmp_path):
        # Cria dois arquivos Excel temporários
        arquivo_excel1 = tmp_path / "test1.xls"
        df1 = pd.DataFrame({
            "Coluna1": [1, 2],
            "Coluna2": [3, 4]
        })
        df1.to_excel(arquivo_excel1, index=False)

        arquivo_excel2 = tmp_path / "test2.xls"
        df2 = pd.DataFrame({
            "Coluna1": [5, 6],
            "Coluna2": [7, 8]
        })
        df2.to_excel(arquivo_excel2, index=False)

        caminhos = [str(arquivo_excel1), str(arquivo_excel2)]
        colunas_tipo = {"Coluna1": int, "Coluna2": int}
        df_resultado = model.processar_arquivos(
            caminhos, colunas_tipo=colunas_tipo, linhas_para_pular=0)

        df_esperado = pd.DataFrame({
            "Coluna1": [1, 2, 5, 6],
            "Coluna2": [3, 4, 7, 8]
        })

        pd.testing.assert_frame_equal(df_resultado.reset_index(drop=True),
                                      df_esperado)

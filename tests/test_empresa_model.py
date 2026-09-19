"""Classe que conterá os testes para a classe que representa os Correios"""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from src.carregamento.data_loader import DataLoader
from src.models.base.empresa_model import EmpresaModel


@pytest.fixture
def model(mock_dados_globais: dict):
    mock_loader = MagicMock(spec=DataLoader)
    mock_loader.carregar_tudo.return_value = mock_dados_globais
    # empresa = EmpresaModel()
    # empresa.configurar(loader=mock_loader)
    return (
        EmpresaModel()
        .configurar(loader=mock_loader)
        .definir_intervalo_de_pesquisa("2023-01-01", "2023-12-31")
    )


class TestEmpresaModel:
    def test_retornar_carga_induzida_total(self, model):
        assert (
            model.retornar_carga_induzida_total() >= 0
        ), "A carga total deve ser um valor não negativo"

        assert (
            model.retornar_carga_induzida_total() == 94832
        ), "A carga total deve ser 94832"

    def _test_retornar_carga_induzida_total_com_dataframe_vazio(self, model):
        empty_model = EmpresaModel()
        empty_model._carregar_carga_induzida(df=pd.DataFrame())
        assert (
            empty_model.retornar_carga_induzida_total() == 0
        ), "A carga total deve ser 0 para um DataFrame vazio"

        assert (
            len(empty_model.retornar_centros_de_tratamento()) == 0
        ), "Deve retornar uma lista vazia para um DataFrame vazio"

    def test_retornar_rendimento_efetivo_medio(self, model):
        assert (
            model.retornar_rendimento_efetivo_medio() >= 0
        ), "O rendimento efetivo médio deve ser não negativo"

    def test_retornar_media_diaria_de_carga_induzida(self, model):
        assert (
            model.retornar_media_diaria() >= 0
        ), "A média diária de carga induzida deve ser não negativa"

    def test_retornar_quantidade_de_carga_induzida_por_centro(self, model):
        carga_por_centro = model.retornar_carga_induzida_por_centro()
        assert isinstance(carga_por_centro, pd.DataFrame), "Deve retornar um DataFrame"
        assert not carga_por_centro.empty, "O DataFrame não deve estar vazio"

    def test_retornar_rendimento_efetivo_por_centro(self, model):
        rendimento_por_centro = model.retornar_rendimento_efetivo_por_centro()
        assert isinstance(
            rendimento_por_centro, pd.DataFrame
        ), "Deve retornar um DataFrame"
        assert not rendimento_por_centro.empty, "O DataFrame não deve estar vazio"

    def test_retornar_carga_induzida_por_maquina(self, model):
        carga_por_maquina = model.retornar_carga_induzida_por_maquina()
        assert isinstance(carga_por_maquina, pd.DataFrame), "Deve retornar um DataFrame"
        assert not carga_por_maquina.empty, "O DataFrame não deve estar vazio"

    def test_retornar_rendimento_efetivo_por_maquina(self, model):
        rendimento_por_maquina = model.retornar_rendimento_efetivo_por_maquina()
        assert isinstance(
            rendimento_por_maquina, pd.DataFrame
        ), "Deve retornar um DataFrame"
        assert not rendimento_por_maquina.empty, "O DataFrame não deve estar vazio"

    def test_retornar_total_de_falhas(self, model):
        total_falhas = model.retornar_total_de_falhas()
        assert isinstance(total_falhas, int), "Deve retornar um inteiro"
        assert total_falhas == 4, "O total de falhas deve ser 4"

    def test_retornar_media_de_objetos_por_falha(self, model):
        media_objetos = model.retornar_media_de_objetos_por_falha()
        assert isinstance(media_objetos, (float, int)), "A média deve ser um número"

        # 94832 (Carga Total) / 4 (Falhas) = 23708
        assert media_objetos == pytest.approx(
            23708, 0.01
        ), "A média de objetos por falha deve ser aproximadamente 23708"

    def test_retornar_tempo_total_de_ocorrencias(self, model):
        tempo_total = model.retornar_tempo_total_de_ocorrencias()
        assert isinstance(tempo_total, (float, int)), "O tempo total deve ser um número"
        assert tempo_total >= 0, "O tempo total deve ser positivo"

    def test_retornar_duracao_media_das_falhas(self, model):
        duracao_media = model.retornar_duracao_media_das_falhas()
        assert isinstance(
            duracao_media, (float, int)
        ), "A duração média deve ser um número"
        assert duracao_media >= 0, "A duração média deve ser positiva"

    def test_retornar_total_falhas_por_centro(self, model):
        total_falhas_por_centro = model.retornar_total_falhas_por_centro()
        assert isinstance(
            total_falhas_por_centro, pd.DataFrame
        ), "Deve retornar um DataFrame"
        assert not total_falhas_por_centro.empty, "O DataFrame nao deve estar vazio"
        assert list(total_falhas_por_centro.columns) == [
            "Centro de Tratamento",
            "Total de Falhas",
        ]
        assert len(total_falhas_por_centro) == 2

        # Valida valores (CTC1 tem 2 falhas, CTC3 tem 2 falhas)
        assert total_falhas_por_centro["Total de Falhas"].sum() == 4
        assert total_falhas_por_centro.iloc[0]["Total de Falhas"] == 2

    def test_retornar_total_falhas_por_maquina(self, model):
        """
        Verifica se a EmpresaModel consegue consolidar o total de falhas
        de todas as máquinas, adicionando a qual centro elas pertencem,
        e retornando um DataFrame ordenado do maior para o menor.
        """
        df_resultado = model.retornar_total_falhas_por_maquina()
        assert isinstance(df_resultado, pd.DataFrame), "Deve retornar um DataFrame"
        assert not df_resultado.empty, "O DataFrame nao deve estar vazio"
        assert "Nº Máquina" in df_resultado.columns
        assert "Total de Falhas" in df_resultado.columns
        assert "Centro de Tratamento" in df_resultado.columns
        assert len(df_resultado) == 4

        # Como o retorno deve ser ordenado decrescente pelo total de falhas,
        # o primeiro registro (iloc[0]) tem que ser a Máquina com 2 falhas
        assert df_resultado.iloc[0]["Total de Falhas"] == 2

    def test_retornar_resumo_tempo_por_centro(self, model):
        """
        Verifica se a EmpresaModel consegue gerar um DataFrame com
        Centro de Tratamento, Tempo Total e Tempo Média.
        """
        df_resultado = model.retornar_resumo_tempo_por_centro()
        assert isinstance(df_resultado, pd.DataFrame), "Deve retornar um DataFrame"
        assert list(df_resultado.columns) == [
            "Centro de Tratamento",
            "Tempo Total",
            "Tempo Médio",
        ]
        assert len(df_resultado) == 2

    def test_retornar_duracao_media_falhas_por_centro(self, model):
        """
        Verifica se a EmpresaModel consegue consolidar a duração média das falhas
        por centro de tratamento em um DataFrame.
        """
        df_resultado = model.retornar_duracao_media_falhas_por_centro()

        assert isinstance(df_resultado, pd.DataFrame), "Deve retornar um DataFrame"
        assert "Centro de Tratamento" in df_resultado.columns
        assert "Duração Média" in df_resultado.columns
        assert len(df_resultado) == 2

    def test_retornar_duracao_media_falhas_por_maquina(self, model):
        """
        Verifica se a EmpresaModel consegue consolidar a duração média das falhas
        por maquina em um DataFrame.
        """
        df_resultado = model.retornar_duracao_media_falhas_por_maquina()

        assert isinstance(df_resultado, pd.DataFrame), "Deve retornar um DataFrame"
        assert "Nº Máquina" in df_resultado.columns
        assert "Duração Média" in df_resultado.columns
        assert "Centro de Tratamento" in df_resultado.columns
        assert len(df_resultado) == 4

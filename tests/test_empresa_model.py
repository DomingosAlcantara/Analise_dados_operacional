"""Classe que conterá os testes para a classe que representa os Correios"""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from src.carregamento.data_loader import DataLoader
from src.models.base.empresa_model import EmpresaModel


@pytest.fixture
def model(mock_carga_tratada):
    mock_loader = MagicMock(spec=DataLoader)
    mock_loader.carregar_tudo.return_value = {"carga tratada": mock_carga_tratada}
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

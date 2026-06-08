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

    def _test_retornar_rendimento_efetivo_medio(self, model):
        # centros = model.retornar_centros_de_tratamento()
        # rendimentos = [
        #     centro.retornar_maquinas()[0].media_rendimento_efetivo()
        #     for centro in centros
        # ]
        # assert all(
        #     rendimento >= 0 for rendimento in rendimentos
        # ), "O rendimento efetivo médio deve ser não negativo"
        assert (
            model.retornar_rendimento_efetivo_medio() >= 0
        ), "O rendimento efetivo médio deve ser não negativo"

    def _test_retornar_media_diaria_de_carga_induzida(self, model):
        assert (
            model.retornar_media_diaria_de_carga_induzida() >= 0
        ), "A média diária de carga induzida deve ser não negativa"

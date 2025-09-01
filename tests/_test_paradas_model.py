import pytest
from pandas import DataFrame

from src.models.paradas_model import ParadasModel


@pytest.fixture(scope="module")
def model():
    """
    Configuração inicial para os testes.
    """
    return ParadasModel("/home/domingos/Documentos/Dados/Engarrafamento/")


class Test_ParadasModel:

    def test_get_maiores_paradas(self, model):
        """
        Testa a obtenção dos maiores atolamentos.
        """
        maiores_paradas = model.get_maiores_paradas(3)

        assert isinstance(
            maiores_paradas, DataFrame), "Deve retornar um DataFrame"
        assert not maiores_paradas.empty, "O DataFrame não deve estar vazio"
        assert "descrição_da_falha" in maiores_paradas.columns, \
            "Deve conter a coluna descrição_da_falha"
        assert "quantidade" in maiores_paradas.columns, \
            "Deve conter a coluna quantidade"

    def test_get_soma_geral_paradas(self, model):
        """
        Testa a soma geral dos atolamentos.
        """
        soma_geral = model.get_soma_total_paradas()

        assert isinstance(soma_geral, int), "Deve retornar um inteiro"
        assert soma_geral >= 0, "A soma geral não deve ser negativa"

    def test_get_paradas_em_percentual(self, model):
        """
        Testa o cálculo do percentual de atolamentos.
        """
        percentual_paradas = model.get_paradas_em_percentual(3)

        assert isinstance(
            percentual_paradas, DataFrame), "Deve retornar um DataFrame"
        assert not percentual_paradas.empty, "O DataFrame não deve estar vazio"
        assert "descrição_da_falha" in percentual_paradas.columns, \
            "Deve conter a coluna descrição_da_falha"
        assert "quantidade" in percentual_paradas.columns, \
            "Deve conter a coluna quantidade"
        assert "percentual" in percentual_paradas.columns, \
            "Deve conter a coluna percentual"

    def test_mostrar_maquinas(self, model):
        """
        Testa a exibição das máquinas existentes.
        """
        maquinas = model.mostrar_maquinas()

        assert isinstance(maquinas, DataFrame), "Deve retornar um DataFrame"
        assert not maquinas.empty, "O DataFrame não deve estar vazio"
        assert "nº_máquina_de_triagem" in maquinas.columns, \
            "Deve conter a coluna nº_máquina_de_triagem"

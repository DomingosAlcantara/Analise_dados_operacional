import numpy as np
import pytest

from src.models.carga_induzida_model import CargaInduzidaModel
from src.path_files import PathFiles as pf


@pytest.fixture(autouse=True, scope="module")
def model():
    """
    Configuração inicial para os testes.
    """
    return CargaInduzidaModel(pf.ARQUIVOS_CARGA_TRATADA)


class TestCargaInduzidaModel:

    def test_filtrar_dados_por_data(self, model):
        """
        Testa o método filtrar_dados_por_data.
        """
        data_inicial = "2023-01-01"
        data_final = "2023-12-31"
        model.filtrar_dados_por_data(data_inicial, data_final)
        dados_filtrados = model._dados_filtrados

        print(f"Dados filtrados: {dados_filtrados.shape}")

        assert not dados_filtrados.empty, "Os dados filtrados não devem estar vazios."
        assert all(
            (dados_filtrados["Data de triagem"] >= np.datetime64(data_inicial))
            & (dados_filtrados["Data de triagem"] <= np.datetime64(data_final))
        ), "Os dados filtrados devem estar dentro do intervalo de datas especificado."
        assert (
            dados_filtrados.shape[0] > 0
        ), "Os dados filtrados devem conter registros."

    def test_total_de_carga_induzida(self, model):
        """
        Testa o método total_de_carga_induzida.
        """
        total = model.total_de_carga_induzida()
        print(f"Total de Carga Induzida: {total}")
        assert isinstance(
            total, np.int64
        ), "O total de carga induzida deve ser um inteiro."
        assert total >= 0, "O total de carga induzida não pode ser negativo."

    def test_media_carga_induzida(self, model):
        """
        Testa o método media_carga_induzida.
        """
        media = model.media_carga_induzida()
        assert isinstance(media, float), "A média de carga induzida deve ser um float."
        assert media >= 0, "A média de carga induzida não pode ser negativa."

    def test_rendimento_efetivo_hora(self, model):
        """
        Testa o método rendimento_efetivo_hora.
        """
        rendimento = model.rendimento_efetivo_hora()
        assert isinstance(
            rendimento, float
        ), "O rendimento efetivo por hora deve ser um float."
        assert rendimento >= 0, "O rendimento efetivo por hora não pode ser negativo."

    def test_carga_induzida_por_centro(self, model):
        """
        Testa o método carga_induzida_por_centro.
        """
        pass

    def test_rendimento_efetivo_por_centro(self, model):
        """
        Testa o método rendimento_efetivo_por_centro.
        """
        pass

    def test_carga_induzida_por_maquina(self, model):
        """
        Testa o método carga_induzida_por_maquina.
        """
        pass

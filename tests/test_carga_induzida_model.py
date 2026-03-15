import math
from datetime import date

import pandas as pd

from src.models.base.auxiliares import Auxiliares
from src.models.carga_induzida_model import CargaInduzidaModel


def sample_df():
    return pd.DataFrame(
        {
            "Data de triagem": ["01/08/2023", "15/08/2023", "19/08/2023", "10/09/2023"],
            "Código MCU CTC": [1, 2, 2, 3],
            "Centro de Tratamento": [
                "CTCE INDAIATUBA",
                "CTCE INDAIATUBA",
                "CTCE JABOATAO DOS GUARARAPES",
                "CTCE JABOATAO DOS GUARARAPES",
            ],
            "Nº Máquina": [1, 1, 2, 3],
            "Nome do Plano de Triagem": ["P1", "P1", "P2", "P3"],
            "Quantidade Induzida": [100, 150, 200, 50],
            "Rendimento Efetivo/h": [10, 15, 20, 15],
        }
    )


def test_filtrar_e_aggregados(monkeypatch):
    # Substitui processar_dados para controlar o DataFrame de entrada
    monkeypatch.setattr(Auxiliares, "processar_dados", lambda self: sample_df())

    model = CargaInduzidaModel(path="dummy")

    # Filtra agosto de 2023
    model.filtrar_dados_por_data(date(2023, 8, 1), date(2023, 8, 31))
    assert model._dados_filtrados.shape[0] == 3
    total = model.total_de_carga_induzida()
    media = model.media_carga_induzida()
    rendimento = model.rendimento_efetivo_hora()

    assert total == 450
    assert math.isclose(media, 150.0)
    assert math.isclose(rendimento, 15.0)


def test_filtrar_sem_resultados(monkeypatch):
    monkeypatch.setattr(Auxiliares, "processar_dados", lambda self: sample_df())

    model = CargaInduzidaModel(path="dummy")

    # Intervalo sem correspondência
    model.filtrar_dados_por_data(date(2022, 1, 1), date(2022, 1, 31))
    print(f"shape: {model._dados_filtrados.shape}")
    assert model._dados_filtrados.shape[0] == 0
    assert model.total_de_carga_induzida() == 0
    assert model.media_carga_induzida() == 0
    assert model.rendimento_efetivo_hora() == 0
    assert pd.isna(model.media_carga_induzida())
    assert pd.isna(model.rendimento_efetivo_hora())

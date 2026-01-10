from datetime import date

import pandas as pd

from src.models.base.auxiliares import Auxiliares
from src.models.carga_induzida_model import CargaInduzidaModel
from src.models.resumo_model import ResumoModel


def sample_df():
    return pd.DataFrame(
        {
            "Data de triagem": ["01/08/2023", "15/08/2023", "10/09/2023"],
            "Código MCU CTC": [1, 2, 3],
            "Centro de Tratamento": ["A", "B", "B"],
            "Nº Máquina": [1, 2, 3],
            "Nome do Plano de Triagem": ["P1", "P2", "P3"],
            "Quantidade Induzida": [100, 200, 50],
            "Rendimento Efetivo/h": [10, 20, 15],
        }
    )


def test_get_performance_metrics_com_dados(monkeypatch):
    monkeypatch.setattr(Auxiliares, "processar_dados", lambda self: sample_df())
    model = CargaInduzidaModel(path="dummy")
    resumo = ResumoModel(model)

    metrics = resumo.get_performance_metrics(date(2023, 8, 1), date(2023, 8, 31))

    assert metrics["carga_induzida"] == "300"
    assert metrics["media_carga"] == "150"
    assert metrics["eficiencia"] == "15"


def test_get_performance_metrics_sem_dados(monkeypatch):
    monkeypatch.setattr(Auxiliares, "processar_dados", lambda self: sample_df())
    model = CargaInduzidaModel(path="dummy")
    resumo = ResumoModel(model)

    metrics = resumo.get_performance_metrics(date(2022, 1, 1), date(2022, 1, 31))

    # Total 0, médias vazias retornam '—'
    assert metrics["carga_induzida"] == "0"
    assert metrics["media_carga"] == "—"
    assert metrics["eficiencia"] == "—"

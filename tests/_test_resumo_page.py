from src.models.base.auxiliares import Auxiliares
from src.views.resumo import ResumoPage


def sample_df():
    import pandas as pd

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


def test_compute_kpis_returns_expected(monkeypatch):
    monkeypatch.setattr(Auxiliares, "processar_dados", lambda self: sample_df())

    # Instanciamos a página sem registrar callbacks
    page = ResumoPage(app_instance=None, register_callbacks=False)

    result = page.compute_kpis("2023-08-01", "2023-08-31")

    assert result == ("300", "150", "15")


def test_compute_kpis_empty_range(monkeypatch):
    monkeypatch.setattr(Auxiliares, "processar_dados", lambda self: sample_df())
    page = ResumoPage(app_instance=None, register_callbacks=False)

    result = page.compute_kpis("2022-01-01", "2022-01-31")
    assert result == ("0", "—", "—")

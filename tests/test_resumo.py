
from unittest.mock import MagicMock, patch

from src.pages.resumo import Resumo


class test_resumo:
    def test_definir_area_resumo_calls_metric_three_times(self):
        data = [
            4086,
            4087,
            4088,
        ]

        resumo = Resumo(data)
        with patch("streamlit.columns") as mock_columns, \
                patch("streamlit.metric") as mock_metric:
            # Mock das colunas retornando três mocks
            mock_col1 = MagicMock()
            mock_col2 = MagicMock()
            mock_col3 = MagicMock()
            mock_columns.return_value = (mock_col1, mock_col2, mock_col3)

            resumo.definir_area_resumo()

            # Verifica se metric foi chamado em cada coluna
            assert mock_col1.metric.called
            assert mock_col2.metric.called
            assert mock_col3.metric.called
            # Verifica se cada coluna chamou metric exatamente uma vez
            assert mock_col1.metric.call_count == 1
            assert mock_col2.metric.call_count == 1
            assert mock_col3.metric.call_count == 1

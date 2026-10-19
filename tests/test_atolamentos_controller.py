from unittest.mock import Mock

import pandas as pd

from src.controllers.resumos.atolamentos import AtolamentosController


class TestAtolamentosController:

    def test_processar_atualizacao_do_dashboard_deve_retornar_payload_completo(self):
        # Arrange
        mock_model = Mock()
        mock_model.definir_intervalo_de_pesquisa.return_value = mock_model
        mock_model.retornar_carga_induzida_total.return_value = 1050

        # Mocks para KPIs alinhados exatamente com os métodos chamados pela controller
        mock_atolamentos_mgr = Mock()
        mock_atolamentos_mgr.total.return_value = 100
        mock_atolamentos_mgr.media_diaria.return_value = 5.0
        mock_atolamentos_mgr.tempo_total.return_value = "02:15:00"
        # mock_atolamentos_mgr.retornar_media_diaria_objetos_por_atolamentos.return_value = 2.5
        mock_atolamentos_mgr.media_objetos_por_atolamento.return_value = 10.5

        # Mocks para DataFrames (Centro e Máquina)
        df_qtd_centro = pd.DataFrame(
            [{"Centro de Tratamento": "CTC A", "Total de Atolamentos": 60}]
        )
        df_media_centro = pd.DataFrame(
            [{"Centro de Tratamento": "CTC A", "Duração Média": "00:02:10"}]
        )
        df_tempo_centro = pd.DataFrame(
            [
                {
                    "Centro de Tratamento": "CTC A",
                    "Tempo Total": "01:30:00",
                    "Tempo Médio": "00:02:10",
                }
            ]
        )

        df_qtd_maquina = pd.DataFrame(
            [
                {
                    "Nº Máquina": "M1",
                    "Total de Falhas": 30,
                    "Centro de Tratamento": "CTC A",
                }
            ]
        )
        df_media_maquina = pd.DataFrame(
            [
                {
                    "Nº Máquina": "M1",
                    "Duração Média": "00:01:15",
                    "Centro de Tratamento": "CTC A",
                }
            ]
        )
        df_tempo_maquina = pd.DataFrame(
            [{"Nº Máquina": "M1", "Tempo Total": "00:45:00", "Tempo Médio": "00:01:15"}]
        )

        mock_atolamentos_mgr.por_centro.return_value = df_qtd_centro
        mock_atolamentos_mgr.duracao_media_por_centro.return_value = df_media_centro
        mock_atolamentos_mgr.por_maquina.return_value = df_qtd_maquina
        mock_atolamentos_mgr.duracao_media_por_maquina.return_value = df_media_maquina
        mock_atolamentos_mgr.resumo_tempo_por_centro.return_value = df_tempo_centro
        mock_atolamentos_mgr.resumo_tempo_por_maquina.return_value = df_tempo_maquina

        # Associa o gerenciador mockado à propriedade .atolamentos da empresa
        mock_model.atolamentos = mock_atolamentos_mgr

        controller = AtolamentosController(empresa_instancia=mock_model)

        # Act
        payload = controller.processar_atualizacao_do_dashboard(
            "2026-01-01", "2026-01-31"
        )

        # Assert
        assert isinstance(payload, dict)
        assert "kpis" in payload
        assert "graficos" in payload
        assert "tabelas" in payload

        assert payload["kpis"]["total_atolamentos"] == 100
        assert payload["kpis"]["media_atolamentos"] == 5.0
        assert payload["graficos"]["qtd_centro"] == df_qtd_centro.to_dict("records")
        assert payload["tabelas"]["tempo_centro"] == df_tempo_centro.to_dict("records")

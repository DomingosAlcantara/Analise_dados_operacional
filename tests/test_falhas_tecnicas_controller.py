from src.controllers.resumos.falhas_tecnicas import FalhasTecnicasController


class TestFalhasTecnicasController:
    def test_processar_atualizacao_retorna_kpi_total_correto(
        self, mock_empresa_model, mocker
    ):
        mocker.patch.object(
            mock_empresa_model,
            "definir_intervalo_de_pesquisa",
            return_value=mock_empresa_model,
        )

        mocker.patch.object(
            mock_empresa_model,
            "retornar_total_de_falhas",
            return_value=4,
        )

        mocker.patch.object(
            mock_empresa_model,
            "retornar_media_de_objetos_por_falha",
            return_value=2,
        )

        controller = FalhasTecnicasController(mock_empresa_model)
        start_date_str = "2023-08-14"
        end_date_str = "2023-08-15"
        resultado = controller.processar_atualizacao_do_dashboard(
            start_date_str, end_date_str
        )

        assert isinstance(resultado, tuple), "O retorno deve ser uma tupla"
        assert len(resultado) == 4, "O controller deve retornar 4 Valores"
        assert (
            resultado[0] == "4"
        ), f"O KPI total deveria ser '4', mas veio {resultado[0]}"
        assert (
            resultado[1] == "2"
        ), f"O KPI Média deveria ser '2', mas veio {resultado[1]}"
        assert (
            resultado[2] == "00:00:00"
        ), f"O KPI Tempo Total deveria ser '00:00:00', mas veio {resultado[2]}"
        assert (
            resultado[3] == "00:00:00"
        ), f"O KPI Duração Média deveria ser '00:00:00', mas veio {resultado[3]}"

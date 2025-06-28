
from datetime import datetime
from unittest.mock import patch

from src.data_processing import DataProcessing


class Test_Data_Process():
    # def test_data_process(self):
    #     mock_log_data = """\
    #         2023-10-01 12:00:00,000: Stacker Diag: Belt Speed ips; section 1; T1:100.0 T2:200.0
    #         2023-10-01 12:00:00,000: Stacker Diag: Belt Speed ips; section 2; T1:150.0 T2:250.0
    #         2023-10-01 12:00:00,000: Stacker Diag: Slowest Speed in section 1 is at Port=1 and is: 300 mm/sec
    #         2023-10-01 12:00:00,000: Stacker Diag: Temperature Celsius; section 1 at Port=1 is: 75
    #         2023-10-01 12:00:00,000: Stacker Diag: Temperature Celsius; section 2 at Port=2 is: 80
    #         2023-10-01 12:00:00,000: Stacker Diag: Belt Speed ips; section 1; T1:Unable to decode! Response=A123 * OK
    #         2023-10-01 12:00:00,000: Stacker Diag: Belt Speed ips; the LDU; T1:Unable to decode! Response=A456 * OK
    #         """

    # with patch("builtins.open", mock_open(read_data=mock_log_data)):
    #     file_path = "mocked_file.log"
    #     data_processor = DataProcessing(file_path)
    #     data = data_processor.process_data()

    def test_get_listagem_data_arquivos(self):
        mock_file_names = [
            "4086 09072024.log",
            "4086 09082024.log",
            "4086 09092024.log"
        ]

        expected_machines = [
            "4086",
            "4086",
            "4086"
        ]

        expected_dates = [
            datetime.strptime("09072024", "%m%d%Y").date(),
            datetime.strptime("09082024", "%m%d%Y").date(),
            datetime.strptime("09092024", "%m%d%Y").date()
        ]

        with patch("os.listdir", return_value=mock_file_names):
            data_processor = DataProcessing(mock_file_names)
            result_machines, result_dates = data_processor.get_listagem_data_arquivos()

        assert result_machines == expected_machines, f"Expected \
            {expected_machines}, but got {result_machines}"
        assert result_dates == expected_dates, f"Expected \
                {expected_dates}, but got {result_dates}"

    def test_carregar_media_obj_falhas_tecnicas(self):
        '''
            Testa o carregamento da média de objetos alimentados por falhas técnicas.
        '''
        data_informada = "21092023"

        data_processing = DataProcessing(None)
        resultado = data_processing.get_soma_carga_induzida_por_centro(
            data_informada)

        assert isinstance(
            resultado, float), f"Expected a float, but got {type(resultado)}"

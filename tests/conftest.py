import pandas as pd
import pytest

from src.tratamento.carga_tratada_pipeline import CargaTratadaPipeline
from src.tratamento.falhas_tecnicas_pipeline import FalhasTecnicasPipeline


@pytest.fixture(scope="module")
def mock_carga_tratada():
    dados = {
        "data_de_triagem": [
            "14/08/2023",
            "14/08/2023",
            "14/08/2023",
            "14/08/2023",
            "15/08/2023",
            "15/08/2023",
            "15/08/2023",
            "15/08/2023",
            "15/08/2023",
            "15/08/2023",
        ],
        "código_mcu_ctc": [
            431115,
            431115,
            437023,
            437023,
            437023,
            437023,
            431115,
            431115,
            437023,
            437023,
        ],
        "centro_de_tratamento": [
            "CTC1",
            "CTC1",
            "CTC3",
            "CTC3",
            "CTC3",
            "CTC3",
            "CTC1",
            "CTC1",
            "CTC3",
            "CTC3",
        ],
        "nº_máquina": [
            138,
            139,
            140,
            140,
            140,
            140,
            138,
            139,
            140,
            140,
        ],
        "nome_do_plano_de_triagem": [
            "PLANO A",
            "PLANO B",
            "PLANO C",
            "PLANO C",
            "PLANO D",
            "PLANO E",
            "PLANO A",
            "PLANO B",
            "PLANO C",
            "PLANO D",
        ],
        "quantidade_induzida": [
            20847,
            19298,
            20792,
            6985,
            1234,
            4321,
            8765,
            2345,
            6789,
            3456,
        ],
        "rendimento_efetivo/h": [
            19997,
            18470,
            24960,
            27561,
            12237,
            17701,
            13431,
            19920,
            12631,
            5251,
        ],
    }

    df = pd.DataFrame(dados, index=dados["código_mcu_ctc"])
    df["data_de_triagem"] = pd.to_datetime(df["data_de_triagem"], format="%d/%m/%Y")
    return CargaTratadaPipeline().processar(df)


@pytest.fixture(scope="module")
def mock_falhas_tecnicas():
    dados = {
        "Código MCU CTC": [431115, 431115, 437023, 437023],
        "Centro de Tratamento": ["CTC1", "CTC1", "CTC3", "CTC3"],
        "Nº Máquina de triagem": [138, 139, 140, 141],
        "Descrição da Falha": [
            "Falha A",
            "Falha B",
            "Falha C",
            "Falha D",
        ],
        "Data/hora inicial da Falha": [
            "14/08/2023 10:00:00",
            "14/08/2023 11:30:00",
            "15/08/2023 09:15:00",
            "15/08/2023 14:45:00",
        ],
        "Data/hora final da Falha": [
            "14/08/2023 11:00:00",
            "14/08/2023 12:30:00",
            "15/08/2023 10:15:00",
            "15/08/2023 15:45:00",
        ],
    }

    return FalhasTecnicasPipeline().processar(pd.DataFrame(dados))


@pytest.fixture(scope="module")
def mock_dados_globais(mock_carga_tratada, mock_falhas_tecnicas):
    """
    Retorna um dicionário com dados globais simulados para os testes.
    """
    return {
        "carga tratada": mock_carga_tratada,
        "tecnicas": mock_falhas_tecnicas,
    }

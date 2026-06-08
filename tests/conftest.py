import pandas as pd
import pytest


@pytest.fixture
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
    return df

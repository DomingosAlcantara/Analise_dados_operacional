import pytest
from pandas import DataFrame

from src.models.base.turno_model import TurnoModel


@pytest.fixture(scope="module")
def model():
    """
    Configuração inicial para os testes.
    """
    horarios = {
        "id": ["T001", "T002", "T003"],
        "horario_inicio": ["06:15", "13:00", "22:00"],
        "horario_final": ["13:00", "22:00", "06:15"]
    }

    data = {
        "hora_inicial_de_triagem": ["06:23", "13:20", "15:03", "18:16",
                                    "19:16", "13:19", "06:18", "13:23",
                                    "14:26", "15:17"],
        "nº_máquina": ["M001", "M001", "M001", "M001", "M001", "M002",
                       "M003", "M003", "M003", "M003"],
        "hora_final_de_triagem": ["09:16", "14:47", "16:53", "18:49",
                                  "20:15", "15:24", "07:23", "14:26",
                                  "15:17", "16:16"],
        "nome_do_plano_de_triagem": ["PLANO A", "PLANO B", "PLANO C",
                                     "PLANO D", "PLANO E", "PLANO E",
                                     "PLANO G", "PLANO H", "PLANO I",
                                     "PLANO J"],
        "quantidade_induzida": [20847, 19298, 20792, 6985, 1234, 4321, 8765,
                                2345, 6789, 3456],
        "tempo_total_do_plano": ["02:17", "02:14", "01:03", "00:19",
                                 "00:45", "01:05", "00:50", "00:30",
                                 "01:15", "00:40"],
        "rendimento_efetivo/h": [19997, 18470, 24960, 27561, 12237, 17701,
                                 13431, 19920, 12631, 5251],
    }
    df_horarios_turnos = DataFrame(horarios, index=horarios["id"])
    df = DataFrame(data)
    return TurnoModel(df_horarios_turnos, df)


class Test_TurnoModel:

    def test_total_carga_induzida_maquina(self, model):
        """
        Testa o método que retorna o total de carga induzida pela máquina
        durante o turno.
        """
        total_carga = model.total_carga_induzida_maquina()

        assert isinstance(total_carga, dict), "Deve retornar um dicionário"
        assert "T001" in total_carga, "Deve conter a chave 'T001'. Chaves presentes: " \
            + ", ".join(total_carga.keys())
        assert isinstance(total_carga["T001"], dict), \
            "O valor associado a 'T001' deve ser um dicionário"
        assert total_carga["T001"]["M001"] == 20847, \
            "O total de carga para a máquina M001 no turno T001 deve ser 20847"
        assert total_carga["T001"]["M003"] == 8765, \
            "O total de carga para a máquina M003 no turno T001 deve ser 8765"

    def test_media_rendimento_efetivo_maquina(self, model):
        """
        Testa o método que retorna o rendimento efetivo da máquina
        durante o turno.
        """
        media_rendimento = model.media_rendimento_efetivo_maquina()

        assert isinstance(media_rendimento, dict), "Deve retornar um dicionário"
        assert "T001" in media_rendimento, "Deve conter a chave 'T001'"
        assert isinstance(media_rendimento["T001"], dict), \
            "O valor associado a 'T001' deve ser um dicionário"
        assert "M001" in media_rendimento["T001"], \
            "Deve conter a chave 'M001' no dicionário de 'T001'"
        # Verifica se a média do rendimento da M001 noT001 está correta
        assert media_rendimento["T001"]["M001"] == pytest.approx(
            19997.0, rel=1e-3), \
            "O rendimento da M001 no turno T001 deve ser aproximadamente 19997.0"
        # Verifica se a média do rendimento da M003 no T001 está correta
        assert media_rendimento["T001"]["M003"] == pytest.approx(
            13431.0, rel=1e-3), \
            "O rendimento da M003 no turno T001 deve ser aproximadamente 13431.0"

    def test_total_paradas(self, model):
        """
        Testa o método que retorna o total de paradas da máquina
        durante o turno.
        """
        total_paradas = model.total_paradas()

        assert isinstance(total_paradas, int), "Deve retornar um inteiro"
        assert total_paradas == 0, "O total de paradas deve ser 0"

    def test_media_objetos_induzidos_por_parada(self, model):
        """
        Testa o método que retorna a média de objetos induzidos por parada
        da máquina durante o turno.
        """
        media_induzidos = model.media_objetos_induzidos_por_parada()

        assert isinstance(media_induzidos, float), "Deve retornar um float"
        assert media_induzidos == 0.0, \
            "A média de objetos induzidos por parada deve ser 0.0"

    def test_total_paradas_maquina(self, model):
        """
        Testa o método que retorna o total de paradas da máquina
        durante o turno.
        """
        total_paradas = model.total_paradas_maquina()

        assert isinstance(total_paradas, int), "Deve retornar um inteiro"
        assert total_paradas == 0, "O total de paradas deve ser 0"

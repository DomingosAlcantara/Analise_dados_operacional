"""Classe para modelagem dos Centros de Tratamento de Cargas e
Encomendas dos Correios.
"""

from pandas import DataFrame

from src.models.base.maquina_model import MaquinaModel


class CentroTratamentoModel:
    """
    Classe base para modelagem dos Centros de Tratamento.
    Esta classe pode ser estendida para incluir atributos e métodos específicos
    relacionados aos centros de tratamento de cargas e encomendas.
    """

    def __init__(self, id_centro: int, df: DataFrame):
        """Inicializa a classe com os dados pertinentes, bem como suas
            maquinas associadas.

        Args:
            id_centro (int): Código identificador do centro de tratamento.
            df (DataFrame): DataFrame contendo os dados dos centros de
            tratamento.
        """
        self._id_centro = id_centro
        self._df = df[df["codigo_mcu_ctc"] == self._id_centro]

    def retornar_nome_centro(self) -> str:
        """Retorna o nome do centro de tratamento com base no código
        identificador.

        Returns:
            str: Nome do centro de tratamento.
        """
        return self._df[self._df["codigo_mcu_ctc"] == self._id_centro][
            "centro_de_tratamento"
        ].iloc[0]

    def retornar_maquinas(self) -> list[MaquinaModel]:
        """Retorna uma lista de objetos MaquinaModel contendo as máquinas
        associadas a um centro de tratamento específico.

        Args:
            centro (int): Código identificador do centro de tratamento.

        Returns:
            list[MaquinaModel]: Lista de objetos contendo as máquinas
            associadas ao centro.
        """
        return [
            MaquinaModel(maquina, self._df)
            for maquina in self._df[self._df["codigo_mcu_ctc"] == self._id_centro][
                "nº_máquina"
            ]
            .unique()
            .tolist()
        ]

    def total_carga_induzida(self) -> int:
        """Calcula o total de carga induzida para o centro de tratamento.

        Returns:
            int: Total de carga induzida.
        """
        maquinas = self.retornar_maquinas()
        total_carga = sum(maquina.total_carga_induzida() for maquina in maquinas)
        return total_carga

    def media_carga_induzida(self) -> int:
        """Calcula a média de carga induzida para o centro de tratamento.

        Returns:
            int: Média de carga induzida.
        """
        print(f"Total de carga induzida: {self.total_carga_induzida()}")
        print(f"Total de maquinas: {len(self.retornar_maquinas())}")
        return round(self.total_carga_induzida() / len(self.retornar_maquinas()))

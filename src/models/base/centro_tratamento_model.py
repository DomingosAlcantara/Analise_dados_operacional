"""Classe para modelagem dos Centros de Tratamento de Cargas e
Encomendas dos Correios.
"""

from statistics import mean

from pandas import DataFrame

from src.models.base.maquina_model import MaquinaModel


class CentroTratamentoModel:
    """
    Classe base para modelagem dos Centros de Tratamento.
    Esta classe pode ser estendida para incluir atributos e métodos específicos
    relacionados aos centros de tratamento de cargas e encomendas.
    """

    def __init__(self, id_centro: int):
        """Inicializa a classe com os dados pertinentes, bem como suas
            maquinas associadas.

        Args:
            id_centro (int): Código identificador do centro de tratamento.
            dict_dfs_centro (dict): Dicionário contendo os DataFrames dos centros.
        """
        self._id_centro = id_centro
        self.maquinas = {}

    def configurar(self, dict_dfs_centro: dict):
        """Configura a classe com os dados pertinentes, bem como suas
            maquinas associadas.

        Args:
            dict_dfs_centro (dict): Dicionário contendo os DataFrames dos centros.
        """
        df_produtividade = dict_dfs_centro.get("carga tratada", DataFrame()).set_index(
            "nº_máquina"
        )
        codigos_maquinas = sorted(df_produtividade.index.unique())

        print(f"Maquinas: {codigos_maquinas}")

        mapeamento = (
            df_produtividade[["centro_de_tratamento"]]
            .drop_duplicates()
            .to_dict()["centro_de_tratamento"]
        )

        # for categoria, df in dict_dfs_centro.items():
        #     if "nº_máquina" in df.columns:
        #         for maquina in df["nº_máquina"].unique():
        #             self.maquinas[maquina] = MaquinaModel(maquina, df)
        for codigo_maquina in codigos_maquinas:
            df_maquina = df_produtividade[df_produtividade.index == codigo_maquina]
            self.maquinas[codigo_maquina] = MaquinaModel(
                codigo_maquina, {"carga_tratada": df_maquina}
            )

        return self

    def filtrar_dados_por_data(self, data_inicial: str, data_final: str):
        """Filtra os dados do centro de tratamento com base em um intervalo de
            datas.

        Args:
            data_inicial (str): Data inicial no formato 'YYYY-MM-DD'.
            data_final (str): Data final no formato 'YYYY-MM-DD'.

        Returns:
            CentroTratamentoModel: A própria instância da classe, permitindo
            encadeamento de métodos.
        """
        for maquina in self.maquinas.values():
            maquina.filtrar_dados_por_data(data_inicial, data_final)
        return self

    def _extrair_maquinas(self, df: DataFrame) -> list:
        """Extrai os códigos das máquinas de um DataFrame.

        Args:
            df (DataFrame): DataFrame contendo a coluna 'nº_máquina'.

        Returns:
            list: Lista de códigos de máquinas.
        """
        if "nº_máquina" not in df.columns:
            return []

        return sorted(df["nº_máquina"].dropna().unique().tolist())

    def total_carga_induzida(self) -> int:
        """Calcula o total de carga induzida para o centro de tratamento.

        Returns:
            int: Total de carga induzida.
        """
        if len(self.maquinas) == 1:
            return self.maquinas[list(self.maquinas.keys())[0]].total_carga_induzida()
        return sum(maquina.total_carga_induzida() for maquina in self.maquinas.values())

    def obter_media_diaria(self) -> float:
        """Calcula a média diária de carga induzida para o centro de tratamento.

        Returns:
            float: Média diária de carga induzida.
        """
        # maquinas = self.retornar_maquinas()
        return round(
            sum(maquina.obter_media_diaria() for maquina in self.maquinas.values()), 2
        )

    def media_carga_induzida(self) -> int:
        """Calcula a média de carga induzida para o centro de tratamento.

        Returns:
            int: Média de carga induzida.
        """
        print(f"Total de carga induzida: {self.total_carga_induzida()}")
        # print(f"Total de maquinas: {len(self.retornar_maquinas())}")
        return round(self.total_carga_induzida() / len(self.maquinas))

    def retornar_rendimento_efetivo_medio(self) -> float:
        """Calcula o rendimento efetivo médio para o centro de tratamento.

        Returns:
            float: Rendimento efetivo médio.
        """
        return mean(
            maquina.retornar_rendimento_efetivo_medio()
            for maquina in self.maquinas.values()
        )

    def retornar_carga_induzida_por_maquina(self) -> DataFrame:
        """Retorna a carga induzida por máquina para o centro de tratamento.

        Returns:
            DataFrame: DataFrame contendo a carga induzida por máquina.
        """
        return DataFrame(
            [
                {
                    "Nº Máquina": maquina._id_maquina,
                    "Quantidade Induzida": maquina.total_carga_induzida(),
                }
                for maquina in self.maquinas.values()
            ]
        )

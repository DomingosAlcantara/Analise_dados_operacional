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

        # Inicialização defensiva dos atributos de nomeclatura
        self._nome_centro = f"Centro {self._id_centro}"
        self._nome_abreviado = f"Centro {self._id_centro}"
        self._sigla = "N/A"

    def configurar(self, dict_dfs_centro: dict):
        """Configura a classe com os dados pertinentes, bem como suas
            maquinas associadas.

        Args:
            dict_dfs_centro (dict): Dicionário contendo os DataFrames dos centros.
        """
        df_produtividade = dict_dfs_centro.get("carga tratada", DataFrame()).set_index(
            "no_maquina"
        )

        df_falhas_tecnicas = dict_dfs_centro.get("tecnicas", DataFrame()).set_index(
            "no_maquina"
        )

        if not df_produtividade.empty:
            if "centro_de_tratamento" in df_produtividade.columns:
                self._nome_centro = str(
                    df_produtividade["centro_de_tratamento"].iloc[0]
                )

            if "centro_abrev_19" in df_produtividade.columns:
                self._nome_abreviado = str(df_produtividade["centro_abrev_19"].iloc[0])

            if "centro_abrev_3" in df_produtividade.columns:
                self._sigla = str(df_produtividade["centro_abrev_3"].iloc[0])

        maquinas_prod = (
            set(df_produtividade.index.unique())
            if not df_produtividade.empty
            else set()
        )
        maquinas_falhas = (
            set(df_falhas_tecnicas.index.unique())
            if not df_falhas_tecnicas.empty
            else set()
        )

        codigos_maquinas = sorted(maquinas_prod.union(maquinas_falhas))

        for ordem, codigo_maquina in enumerate(codigos_maquinas, start=1):
            df_carga_maquina = df_produtividade[
                df_produtividade.index == codigo_maquina
            ]
            df_falhas_maquina = df_falhas_tecnicas[
                df_falhas_tecnicas.index == codigo_maquina
            ]
            rotulo_maquina = f"{codigo_maquina}<br>{self._sigla}\xa0-\xa0PBVS{ordem}"
            self.maquinas[codigo_maquina] = MaquinaModel(
                codigo_maquina,
                {"carga tratada": df_carga_maquina, "tecnicas": df_falhas_maquina},
                rotulo=rotulo_maquina,
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
            df (DataFrame): DataFrame contendo a coluna 'nº_maquina'.

        Returns:
            list: Lista de códigos de máquinas.
        """
        if "no_maquina" not in df.columns:
            return []

        return sorted(df["no_maquina"].dropna().unique().tolist())

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
                    "Nº Máquina": maquina.rotulo,
                    "Quantidade Induzida": maquina.total_carga_induzida(),
                }
                for maquina in self.maquinas.values()
            ]
        )

    def retornar_rendimento_efetivo_por_maquina(self) -> DataFrame:
        """Retorna o rendimento efetivo por máquina para o centro de tratamento.

        Returns:
            DataFrame: DataFrame contendo o rendimento efetivo por máquina.
        """
        return DataFrame(
            [
                {
                    "Nº Máquina": maquina.rotulo,
                    "Rendimento Efetivo Médio": maquina.retornar_rendimento_efetivo_medio(),
                }
                for maquina in self.maquinas.values()
            ]
        )

    def retornar_total_de_falhas(self) -> int:
        """Retorna o total de falhas para o centro de tratamento.

        Returns:
            int: Total de falhas.
        """
        return sum(
            maquina.retornar_total_de_falhas() for maquina in self.maquinas.values()
        )

    @property
    def nome_centro(self) -> str:
        """Retorna o nome do centro de tratamento.

        Returns:
            str: Nome do centro de tratamento.
        """
        return self._nome_centro

    @property
    def nome_abreviado(self) -> str:
        """Retorna o nome abreviado do centro de tratamento.

        Returns:
            str: Nome abreviado do centro de tratamento.
        """
        return self._nome_abreviado

    @property
    def sigla(self) -> str:
        """Retorna a sigla do centro de tratamento.

        Returns:
            str: Sigla do centro de tratamento.
        """
        return self._sigla

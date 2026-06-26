"""
Classe que consolidará as informações dos Centros de Tratamento
Automatizados
"""

from statistics import mean

import pandas as pd

from src.carregamento.data_loader import DataLoader
from src.models.base.centro_tratamento_model import CentroTratamentoModel


class EmpresaModel:

    def __init__(self, nome_empresa="Correios"):
        self._nome_empresa = nome_empresa
        self.centros = {}

    def configurar(self, loader: DataLoader):
        """
        Configura a empresa com os dados carregados pelo DataLoader.
        """
        dados_globais = loader.carregar_tudo()
        df_prod = dados_globais["carga tratada"].set_index("código_mcu_ctc")
        codigos_centros = df_prod.index.unique()

        mapeamento = (
            df_prod[["centro_de_tratamento"]]
            .drop_duplicates()
            .to_dict()["centro_de_tratamento"]
        )

        for id_centro in codigos_centros:
            dados_centro = {}
            for categoria, df in dados_globais.items():
                if id_centro in df["código_mcu_ctc"].values:
                    dados_centro[categoria] = df[df["código_mcu_ctc"] == id_centro]
                else:
                    dados_centro[categoria] = df[df.index == id_centro]

            nome_centro = mapeamento.get(id_centro, "Desconhecido")
            self.centros[nome_centro] = CentroTratamentoModel(id_centro).configurar(
                dados_centro
            )

        return self

    def definir_intervalo_de_pesquisa(self, data_inicio: str, data_fim: str):
        """
        Define o intervalo de pesquisa para os dados de carga induzida.
        """
        for centro in self.centros.values():
            centro.filtrar_dados_por_data(data_inicio, data_fim)

        return self

    def retornar_centros_de_tratamento(self):
        """
        Retorna a lista de centros de tratamento automatizados presentes no
        DataFrame.
        """
        if not self.centros:
            return []

        return self.centros

    def retornar_carga_induzida_total(self):
        """
        Calcula a carga total induzida somando a carga induzida de todos
        os centros de tratamento.
        """
        if not self.centros:
            return 0

        return sum(centro.total_carga_induzida() for centro in self.centros.values())

    def retornar_media_diaria(self):
        """
        Calcula a média diária de carga induzida somando a carga induzida de
        todos os centros de tratamento.
        """
        if not self.centros:
            return 0

        return sum(centro.obter_media_diaria() for centro in self.centros.values())

    def retornar_rendimento_efetivo_medio(self):
        """
        Calcula o rendimento efetivo médio somando o rendimento efetivo de
        todos os centros de tratamento.
        """
        if not self.centros:
            return 0

        return mean(
            centro.retornar_rendimento_efetivo_medio()
            for centro in self.centros.values()
        )

    def retornar_carga_induzida_por_centro(self):
        """
        Retorna a carga induzida por centro de tratamento.
        """
        if not self.centros:
            return pd.DataFrame(columns=["Centro de Tratamento", "Quantidade Induzida"])

        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": nome_centro,
                    "Quantidade Induzida": centro.total_carga_induzida(),
                }
                for nome_centro, centro in self.centros.items()
            ]
        )

    def _concatenar_dataframes(self, dataframes, nome_coluna):
        """
        Concatena uma lista de DataFrames, adicionando uma coluna com o nome
        do centro de tratamento.
        """
        if not self.centros or not dataframes:
            return pd.DataFrame(
                columns=["Nº Máquina", nome_coluna, "Centro de Tratamento"]
            )

        df_concatenado = pd.concat(
            [
                df.assign(**{"Centro de Tratamento": nome_centro})
                for nome_centro, df in dataframes.items()
            ],
            ignore_index=True,
        )

        return df_concatenado

    def retornar_rendimento_efetivo_por_centro(self):
        """
        Retorna o rendimento efetivo por centro de tratamento.
        """
        if not self.centros:
            return pd.DataFrame(
                columns=["Centro de Tratamento", "Rendimento Efetivo Médio"]
            )

        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": nome_centro,
                    "Rendimento Efetivo Médio": centro.retornar_rendimento_efetivo_medio(),
                }
                for nome_centro, centro in self.centros.items()
            ]
        )

    def retornar_carga_induzida_por_maquina(self):
        """
        Retorna a carga induzida por máquina.
         - Se não houver centros, retorna um DataFrame vazio.
         - Se houver centros, concatena os DataFrames de carga por máquina de
           cada centro, adicionando uma coluna para o nome do centro.
         - O resultado é um DataFrame com as colunas 'Nº Máquina',
           'Quantidade Induzida', 'Centro de Tratamento' e 'Nome do Centro'.
         - O DataFrame resultante é ordenado por 'Quantidade Induzida' em
           ordem decrescente.
         - Se o DataFrame resultante estiver vazio, retorna um DataFrame vazio
           com as colunas esperadas.
         - Caso contrário, retorna o DataFrame concatenado e ordenado.
         - O método é projetado para lidar com a ausência de dados e garantir
           que a estrutura do DataFrame seja consistente, mesmo quando não há
           dados disponíveis.
        """
        return self._concatenar_dataframes(
            {
                nome_centro: centro.retornar_carga_induzida_por_maquina()
                for nome_centro, centro in self.centros.items()
            },
            "Quantidade Induzida",
        ).sort_values(by="Quantidade Induzida", ascending=False)

    def retornar_rendimento_efetivo_por_maquina(self):
        """
        Retorna o rendimento efetivo por máquina.
         - Se não houver centros, retorna um DataFrame vazio.
         - Se houver centros, concatena os DataFrames de rendimento por máquina
           de cada centro, adicionando uma coluna para o nome do centro.
         - O resultado é um DataFrame com as colunas 'Nº Máquina',
           'Rendimento Efetivo', 'Centro de Tratamento' e 'Nome do Centro'.
         - O DataFrame resultante é ordenado por 'Rendimento Efetivo' em ordem
           decrescente.
         - Se o DataFrame resultante estiver vazio, retorna um DataFrame vazio
           com as colunas esperadas.
         - Caso contrário, retorna o DataFrame concatenado e ordenado.
         - O método é projetado para lidar com a ausência de dados e garantir
           que a estrutura do DataFrame seja consistente, mesmo quando não há
           dados disponíveis.
        """
        return self._concatenar_dataframes(
            {
                nome_centro: centro.retornar_rendimento_efetivo_por_maquina()
                for nome_centro, centro in self.centros.items()
            },
            "Rendimento Efetivo Médio",
        ).sort_values(by="Rendimento Efetivo Médio", ascending=False)

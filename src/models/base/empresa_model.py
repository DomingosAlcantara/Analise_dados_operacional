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
        df_prod = dados_globais["carga tratada"].set_index("codigo_mcu_ctc")
        codigos_centros = df_prod.index.unique()

        mapeamento = (
            df_prod[["centro_de_tratamento"]]
            .drop_duplicates()
            .to_dict()["centro_de_tratamento"]
        )

        for id_centro in codigos_centros:
            dados_centro = {}
            for categoria, df in dados_globais.items():
                if id_centro in df["codigo_mcu_ctc"].values:
                    dados_centro[categoria] = df[df["codigo_mcu_ctc"] == id_centro]
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
        if self.centros:
            for centro in self.centros.values():
                centro.filtrar_dados_por_data(data_inicio, data_fim)

        return self

    @property
    def retornar_centros_de_tratamento(self):
        """
        Retorna a lista de centros de tratamento automatizados presentes no
        DataFrame.
        """
        if not self.centros:
            return []

        return [centro.nome_abreviado for centro in self.centros.values()]

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
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Quantidade Induzida": centro.total_carga_induzida(),
                }
                for centro in self.centros.values()
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
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Rendimento Efetivo Médio": centro.retornar_rendimento_efetivo_medio(),
                }
                for centro in self.centros.values()
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
                centro.nome_abreviado: centro.retornar_carga_induzida_por_maquina()
                for centro in self.centros.values()
            },
            "Quantidade Induzida",
        ).sort_values(
            by=["Centro de Tratamento", "Quantidade Induzida"],
            ascending=[True, False],
        )

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
                centro.nome_abreviado: centro.retornar_rendimento_efetivo_por_maquina()
                for centro in self.centros.values()
            },
            "Rendimento Efetivo Médio",
        ).sort_values(by="Rendimento Efetivo Médio", ascending=False)

    def retornar_total_de_falhas(self):
        """
        Retorna o total de falhas em todos os centros de tratamento.
         - Se não houver centros, retorna 0.
         - Caso contrário, soma o total de falhas de cada centro e retorna o
           valor total.
        """
        if not self.centros:
            return 0

        return sum(
            centro.retornar_total_de_falhas() for centro in self.centros.values()
        )

    def retornar_media_de_objetos_por_falha(self):
        """
        Retorna a média de falhas em todos os centros de tratamento.
         - Se não houver centros, retorna 0.
         - Caso contrário, calcula a média de falhas de cada centro e retorna a
           média geral.
        """
        if not self.centros or self.retornar_total_de_falhas() == 0:
            return 0

        return self.retornar_carga_induzida_total() / self.retornar_total_de_falhas()

    def retornar_tempo_total_de_ocorrencias(self):
        """
        Retorna o tempo total de ocorrências em todos os centros de tratamento.
         - Se não houver centros, retorna 0.
         - Caso contrário, soma o tempo total de ocorrências de cada centro e
           retorna o valor total.
        """
        if not self.centros:
            return 0

        return sum(
            centro.retornar_tempo_total_de_ocorrencias()
            for centro in self.centros.values()
        )

    def retornar_duracao_media_das_falhas(self):
        """
        Retorna a duração média das falhas em todos os centros de tratamento.
         - Se não houver centros, retorna 0.
         - Caso contrário, calcula a duração média das falhas de cada centro e
           retorna a média geral.
        """
        if self.retornar_total_de_falhas() == 0:
            return "00:00:00"

        return (
            self.retornar_tempo_total_de_ocorrencias() / self.retornar_total_de_falhas()
        )

    def retornar_total_falhas_por_centro(self):
        """
        Retorna o total de falhas agrupado por centro de tratamento.
         - Se não houver centro, retorna um DataFrame vazio com as colunas
            esperadas.
         - Caso contrário, itera sobre os centros, captura o nome e o total de
            falhas, e retorna um DataFrame ordenado do maior para o menor
        """
        if not self.centros:
            return pd.DataFrame(columns=["Centro de Tratamento", "Total de Falhas"])

        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Total de Falhas": centro.retornar_total_de_falhas(),
                }
                for centro in self.centros.values()
            ]
        ).sort_values(by="Total de Falhas", ascending=False)

    def retornar_total_falhas_por_maquina(self):
        """
        Retorna o total de falhas agrupado por maquina.
         - Se houver centros, concatena os DataFrames de falhas por máquina
           de cada centro, adicionando uma coluna para o nome do centro.
         - O DataFrame resultante é ordenado por 'Total de Falhas' em ordem
           decrescente.
        """
        return self._concatenar_dataframes(
            {
                centro.nome_abreviado: centro.retornar_total_falhas_por_maquina()
                for centro in self.centros.values()
            },
            "Total de Falhas",
        ).sort_values(
            by=["Total de Falhas", "Centro de Tratamento"], ascending=[False, True]
        )

    def retornar_resumo_tempo_por_centro(self):
        """
        Retorna um DataFrame resumindo o tempo total e médio de falhas
        agrupado por Centro de Tratamento
        """
        if not self.centros:
            return pd.DataFrame(
                columns=["Centro de Tratamento", "Tempo Total", "Tempo Médio"]
            )

        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Tempo Total": centro.retornar_tempo_total_de_ocorrencias(),
                    "Tempo Médio": centro.retornar_duracao_media_das_falhas(),
                }
                for centro in self.centros.values()
            ]
        ).sort_values(by="Tempo Total", ascending=False)

    def retornar_duracao_media_falhas_por_centro(self):
        """
        Retorna a duração média de falhas agrupada por centro de tratamento.
        """
        if not self.centros:
            return pd.DataFrame(columns=["Centro de Tratamento", "Duração Média"])

        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": centro.nome_abreviado,
                    "Duração Média": centro.retornar_duracao_media_das_falhas(),
                }
                for centro in self.centros.values()
            ]
        ).sort_values(by="Duração Média", ascending=False)

    def retornar_duracao_media_falhas_por_maquina(self):
        """
        Retorna a duração média de falhas agrupada por máquina
        de todos os centros de tratamento.
        """
        if not self.centros:
            return pd.DataFrame(
                columns=["Nº Máquina", "Duração Média", "Centro de Tratamento"]
            )

        dados = []
        for centro in self.centros.values():
            for maquina in centro.maquinas.values():
                dados.append(
                    {
                        "Nº Máquina": maquina.rotulo,
                        "Duração Média": maquina.retornar_duracao_media_das_falhas(),
                        "Centro de Tratamento": centro.nome_abreviado,
                    }
                )

        df = pd.DataFrame(dados)

        if df.empty:
            return pd.DataFrame(
                columns=["Nº Máquina", "Duração Média", "Centro de Tratamento"]
            )

        return df.sort_values(by="Duração Média", ascending=False)

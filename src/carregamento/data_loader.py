"""
Esta classe contém as funções que auxiliaram o tratamento dos dados
"""

import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd


class DataLoader:
    """
    Classe auxiliar para tratamento de dados.
    """

    def __init__(self, configuracoes: dict) -> None:
        """
        Args:
            configuracoes (dict): Dicionário contendo os parâmetros de cada métrica.
            Exemplo:
            {
                'produtividade': {'path': 'dados/prod', 'skip': 2, 'cols': {...}},
                'paradas': {'path': 'dados/paradas', 'skip': 1, 'cols': {...}}
            }
        """
        self._configs = configuracoes

    def _carregar_planilha(
        self,
        caminho_do_arquivo: str,
        num_linhas_desconsiderar: int,
        utilizar_colunas: dict,
    ) -> pd.DataFrame:
        """
        Carrega uma planilha Excel com configurações específicas.

        Returns:
            DataFrame: Dados carregados da planilha.
        """
        try:
            return pd.read_excel(
                caminho_do_arquivo,
                skiprows=num_linhas_desconsiderar,
                usecols=list(utilizar_colunas.keys()),
                dtype=utilizar_colunas,
            )
        except ValueError as e:
            raise ValueError(
                f"Erro ao carregar a planilha: {caminho_do_arquivo}"
            ) from e

    def _listar_caminhos_arquivos(self, diretorio: str) -> list:
        """
        Método para listar os caminhos completos dos arquivos no diretório.
        """
        if not os.path.exists(diretorio):
            return []
        return [
            os.path.join(diretorio, f)
            for f in os.listdir(diretorio)
            if f.endswith((".xlsx", ".xls"))
        ]

    def processar_categoria(self, nome_categoria: str, conf: dict) -> pd.DataFrame:
        """
        Método placeholder para processamento de dados.
        """

        caminhos = self._listar_caminhos_arquivos(conf["path"])

        if not caminhos:
            # Retorna um DataFrame vazio com as colunas esperadas se não houver arquivos
            return pd.DataFrame(columns=list(conf["cols"].keys()))

        # Usando o seu modelo com ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            # Passamos os argumentos especificos de cada categoria para a função de carga
            dataframes = list(
                executor.map(
                    lambda caminho: self._carregar_planilha(
                        caminho, conf["skip"], conf["cols"]
                    ),
                    caminhos,
                )
            )
        return pd.concat(dataframes, ignore_index=True)

    def carregar_tudo(self) -> dict:
        """
        Método para carregar todas as categorias de dados.

        Returns:
            dict: Dicionário contendo os DataFrames de cada categoria.
        """

        dados_carregados = {}

        for categoria, conf in self._configs.items():
            df_bruto = self.processar_categoria(categoria, conf)

            pipeline = conf.get("pipeline")

            if pipeline and not df_bruto.empty:
                df_limpo = pipeline.processar(df_bruto)
            else:
                df_limpo = df_bruto

            dados_carregados[categoria] = df_limpo
        return dados_carregados

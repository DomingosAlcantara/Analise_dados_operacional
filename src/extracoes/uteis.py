import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd


class Uteis:
    """Classe utilitária para operações comuns de carregamento de dados."""

    def __init__(self, path: str):
        self._path = path

    def listar_arquivos(self) -> list[str]:
        """
        Lista todos os arquivos em um diretório específico.

        Returns:
            list[str]: Lista de nomes de arquivos no diretório.
        """
        try:
            arquivos = [f for f in os.listdir(self._path)
                        if f.endswith('.xls')]
            return arquivos
        except FileNotFoundError:
            print(f"O diretório {self._path} não foi encontrado.")
            return []
        except Exception as e:
            print(f"Ocorreu um erro ao listar os arquivos: {e}")
            return []

    def construir_caminhos_completos(self, arquivos: list[str]) -> list[str]:
        """
        Constrói caminhos completos para uma lista de arquivos em um diretório
        específico.

        Args:
            arquivos (list[str]): Lista de nomes de arquivos.

        Returns:
            list[str]: Lista de caminhos completos dos arquivos.
        """
        return [os.path.join(self._path, arquivo)
                for arquivo in arquivos]

    def processar_arquivos(self, path_files: list[str], colunas_tipo: dict,
                           linhas_para_pular: int) -> pd.DataFrame:
        """
        Processa os dados carregando múltiplas planilhas em paralelo e
        concatenando os resultados.

        Args:
            path (str): Caminho para o diretório contendo os arquivos Excel.
            linhas_para_pular (int): Quant. de linha a desconsiderar.

        Returns:
            pd.DataFrame: DataFrame consolidado com os dados de todas as
            planilhas.
        """

        def carregar_planilha(self, path: str, colunas_tipo: dict,
                              linhas_para_pular: int) -> pd.DataFrame:
            """Carrega uma planilha Excel em um DataFrame do pandas, conforme os
            parâmetros especificados.

            Args:
                path (str): Caminho para o arquivo Excel.
                linhas_para_pular (int): Quant. de linha a desconsiderar.

            Returns:
                pd.DataFrame: Dados da planilha carregados em um DataFrame.
            """
            try:
                df = pd.read_excel(path, usecols=list(colunas_tipo.keys()),
                                   skiprows=linhas_para_pular, dtype=colunas_tipo)
                return df
            except FileNotFoundError:
                print(f"O arquivo {path} não foi encontrado.")
                return pd.DataFrame()
            except Exception as e:
                print(f"Ocorreu um erro ao carregar a planilha: {e}")
                return pd.DataFrame()

        with ThreadPoolExecutor() as executor:
            resultados = list(executor.map(
                lambda p: self.carregar_planilha(p, linhas_para_pular),
                path_files
            ))

        df_consolidado = pd.concat(resultados, ignore_index=True)
        return df_consolidado

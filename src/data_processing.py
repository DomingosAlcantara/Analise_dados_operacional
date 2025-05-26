"""Classe para processamento dos dados.
"""
import os
from datetime import datetime

import pandas as pd

from padroes import Padroes as Regex


class DataProcessing:
    """Classe para processamento dos dados.
    """

    def __init__(self, file_path):
        self._file_path = file_path
        self._data = None
        # self._set_dados(self, data)

        self._padroes = Regex()

    def _set_dados(self, data):
        """Define os dados a serem processados."""
        if data is not None:
            df = data.copy()
            self._data = df[df["Quantidade Induzida"] > 0]
        else:
            self._data = pd.DataFrame()

    def get_dados(self):
        """Retorna os dados processados."""
        if self._data is not None:
            return self._data
        else:
            raise ValueError("Dados não carregados.")

    def _formatar_datas(self, data):
        """Formata a data no formato desejado."""
        # Formato desejado: "09072024" -> "2024-09-07"
        return datetime.strptime(data, "%m%d%Y").date()

    def _is_single_date(self, value, date_format="%d/%m/%Y"):
        """Verifica se o valor é uma data única."""
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            return False

    def _is_date_range(self, value, date_format="%d/%m/%Y"):
        """Verifica se o valor é um intervalo de datas."""
        try:
            start_date, end_date = value.split(" - ")
            return self._is_single_date(start_date, date_format) and \
                self._is_single_date(end_date, date_format)
        except ValueError:
            return False

    def carregar_planilha(self, path):
        """Carrega a planilha de dados."""
        # Implementar o carregamento da planilha
        df = pd.read_excel(path, skiprows=8)

        return df

    def processar_dados(self):
        """Processa os dados do arquivo."""
        # Implementar o processamento dos dados
        if self._file_path:
            # Carregar os dados do arquivo
            planilhas = os.listdir(self._file_path)
            caminhos = [os.path.join(self._file_path, nome)
                        for nome in planilhas]
            dfs = list(map(self.carregar_planilha, caminhos))
            if dfs:
                df_final = pd.concat(dfs, ignore_index=False)
                df_final.set_index("Data de triagem", inplace=True)
                self._set_dados(df_final)
            else:
                df = self.carregar_planilha(self._file_path)
                df.set_index("Data de triagem", inplace=True)
                self._set_dados(df)
            # Processar os dados
            # ...
            # return self._data
        else:
            raise ValueError("Caminho do arquivo não fornecido.")

    def recuperar_dados_pelo_centro(self, centro: str):
        """
        Recupera os dados filtrados pelo centro de triagem.
        """
        df = self.get_dados()
        if df is not None:
            return df[df["Centro de Tratamento"] == centro.upper()]
        else:
            raise ValueError("Dados não carregados.")

    def recuperar_soma_quantidade_induzida(self, data_informada,
                                           centro: pd.DataFrame
                                           ) -> int:
        """
        Carrega a média de objetos alimentados por falhas técnicas.
        """
        df = centro["Quantidade Induzida"].copy()
        if self._is_single_date(data_informada):
            data = datetime.strptime(data_informada, "%d/%m/%Y").date()
            df = df[df["Data de triagem"] == data]
            return df.sum()

        elif self._is_date_range(data_informada):
            start_date, end_date = data_informada.split(" - ")
            start_date = datetime.strptime(start_date, "%d/%m/%Y").date()
            end_date = datetime.strptime(end_date, "%d/%m/%Y").date()
            df = df[(df["Data de triagem"] >= start_date) &
                    (df["Data de triagem"] <= end_date)]
            return df.sum()

        else:
            raise ValueError("Formato de data inválido.")

    def _extrair_informacoes(self, arquivo):
        """Lista os arquivos no diretório."""
        padrao = self._padroes.NOME_DO_ARQUIVO
        match = padrao.match(arquivo)
        if match:
            # Extrai as informações do arquivo
            maquina, data = match.groups()
            return maquina, data

        return None, None

    def get_listagem_data_arquivos(self):
        """Retorna uma lista de datas extraídas dos nomes dos arquivos 
            no diretório.
        """
        # file_names = os.listdir(self._file_path)
        maquinas, dates = zip(*map(
            self._extrair_informacoes,
            os.listdir(self._file_path)
        ))

        datas_formatadas = list(map(
            self._formatar_datas,
            dates
        ))

        print(maquinas, datas_formatadas)

        return list(maquinas), datas_formatadas


if __name__ == "__main__":
    # Exemplo de uso
    # Obter os dados
    file_path_carga_tratada = "C:/Users/80891950/Downloads/Relatório Pitney \
        Bower/Dados/Carga Tratada/"
    file_path_falhas_tecnicas = "C:/Users/80891950/Downloads/Relatório Pitney \
        Bower/Dados/Falhas Técnicas/"

    carga_tratada = DataProcessing(file_path_carga_tratada)
    carga_tratada.processar_dados()
    dados_df = carga_tratada.recuperar_dados_pelo_centro("CTCE Salvador")

    falhas_tecnicas = DataProcessing(file_path_falhas_tecnicas)
    falhas_tecnicas.processar_dados()
    # dados_df
    print(f"Teste: {dados_df}")

"""Classe para processamento dos dados.
"""

import pandas as pd

from padroes import Padroes as Regex
from uteis import Uteis


class DataProcessing(Uteis):
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
            self._data = data.copy()
        else:
            self._data = pd.DataFrame()

    def get_dados(self):
        """Retorna os dados processados."""
        if self._data is not None:
            return self._data
        else:
            raise ValueError("Dados não carregados.")

    def carregar_planilha(self, path):
        """Carrega a planilha de dados."""
        try:
            df = pd.read_excel(path, skiprows=8)
            return df
        except ValueError:
            ValueError(f"Erro ao carregar a planilha: {path}")

    # def padronizar_colunas(self, df):

    def processar_carga_tratada(self):
        """Processa os dados do arquivo."""
        import os
        from concurrent.futures import ThreadPoolExecutor

        # Implementar o processamento dos dados
        if self._file_path:
            # Carregar os dados do arquivo
            planilhas = os.listdir(self._file_path)
            caminhos = [os.path.join(self._file_path, nome)
                        for nome in planilhas]
            with ThreadPoolExecutor() as executor:
                dfs = list(executor.map(self.carregar_planilha, caminhos))
                if dfs:
                    df_final = pd.concat(dfs, ignore_index=False)
                    df_final.set_index("Data de triagem", inplace=True)
                    df_final.index = pd.to_datetime(
                        df_final.index, dayfirst=True).date
                    df_final = df_final[df_final["Quantidade Induzida"] > 0]
                    self._set_dados(df_final)
                else:
                    df = self.carregar_planilha(self._file_path)
                    df.set_index("Data de triagem", inplace=True)
                    df.index = pd.to_datetime(df.index, dayfirst=True).date
                    self._set_dados(df)
                # return self._data
        else:
            raise ValueError("Caminho do arquivo não fornecido.")

    def get_soma_carga_induzida_por_centro(self, data_informada,
                                           centro="CTCE Salvador"
                                           ) -> int:
        """
        Carrega a média de objetos alimentados por falhas técnicas.
        """
        df = self.recuperar_dados_pelo_centro(centro)

        if isinstance(data_informada, (list, tuple)):
            data_inicial, data_final = data_informada
        else:
            data_inicial = data_final = data_informada

        if data_final is not None:
            df = df[(df.index >= data_inicial) &
                    (df.index <= data_final)]
        else:
            df = df[df.index == data_inicial]

        return df["Quantidade Induzida"].sum()

    def get_soma_geral_de_carga_induzida(self, data_informada) -> int:
        """
        Retorna a soma geral da carga induzida.
        """

        df = self.get_dados() if self.get_dados() is not None \
            else pd.DataFrame()

        if isinstance(data_informada, (list, tuple)):
            data_inicial, data_final = data_informada
        else:
            data_inicial = data_final = data_informada

        if data_final is not None:
            df = df[(df.index >= data_inicial) &
                    (df.index <= data_final)]
        else:
            df = df[df.index == data_inicial]

        return df["Quantidade Induzida"].sum()

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
    file_path_carga_tratada = "C:/Users/80891950/Downloads/Relatório Pitney Bower/Dados/Carga Tratada/"
    file_path_falhas_tecnicas = "C:/Users/80891950/Downloads/Relatório Pitney Bower/Dados/Técnica/"

    carga_tratada = DataProcessing(file_path_carga_tratada)
    carga_tratada.processar_carga_tratada()
    # carga_tratada_df = carga_tratada.recuperar_dados_pelo_centro(
    #     "CTCE Salvador")
    # print(f"Teste: {carga_tratada_df.head(5)}")
    print(
        f"Carga tratada: {carga_tratada.get_soma_carga_induzida_por_centro(
            '14/08/2023 - 17/08/2023', "CTCE Salvador")}"
    )
    # print(f"Colunas existentes: {carga_tratada.get_dados().columns.tolist()}")

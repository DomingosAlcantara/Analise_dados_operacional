import pandas as pd


class Extracoes:
    """
        Classe para gerar um arquivo CSV com datas de 01/01/2023 a 31/12/2023.
    """

    def __init__(self, dados=None):
        """
        Inicializa a classe Extracoes.
        """
        self._dados = dados.copy() if dados is not None else pd.DataFrame()

    def extrair_centro_tratamento(self):
        """
        Método para extrair dados de centros de tratamento.
        """
        df = self._dados["Centro de Tratamento"].copy()
        df = df.drop_duplicates().reset_index(drop=True)
        df["id_centro_tratamento"] = range(1, len(df) + 1)
        df.set_index("id_centro_tratamento", inplace=True)

        df.to_csv("/src/relacionamentos/dim_centros_tratamento.csv",
                  index=True, encoding="utf-8")

    def extrair_descricao_falha(self):
        """
        Método para extrair descrições de falhas.
        """
        df = self._dados["Descrição da Falha"].copy()
        df = df.drop_duplicates().reset_index(drop=True)
        df["id_descricao_falha"] = range(1, len(df) + 1)
        df.set_index("id_descricao_falha", inplace=True)

        df.to_csv("/src/relacionamentos/dim_descricoes_falhas.csv",
                  index=True, encoding="utf-8")

    def extrair_codigos_mcu_ctc(self):
        """
        Método para extrair códigos MCU CTC.
        """
        df = self._dados["Código MCU CTC"].copy()
        df = df.drop_duplicates().reset_index(drop=True)
        df["id_codigo_mcu_ctc"] = range(1, len(df) + 1)
        df.set_index("id_codigo_mcu_ctc", inplace=True)

        df.to_csv("/src/relacionamentos/dim_codigos_mcu_ctc.csv",
                  index=True, encoding="utf-8")

    @staticmethod
    def gerar_arquivo_datas():
        """
        Gera um DataFrame com datas de 01/01/2020 a 31/12/2023.
        """
        datas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        df = pd.DataFrame(datas, columns=['Data_da_Ocorrencia'])

        df["id_data"] = range(1, len(df) + 1)
        df.set_index("id_data", inplace=True)

        df.to_csv("/src/relacionamentos/dim_datas.csv",
                  index=True, encoding="utf-8")


if __name__ == "__main__":
    Extracoes.gerar_arquivo_datas()
    print("Arquivo 'dim_datas.csv' gerado com sucesso.")

"""
    Classe para processar as falhas técnicas dos sistemas de triagem de cartas do CTCE.
"""

import pandas as pd

from uteis import Uteis


class FalhasTecnicas(Uteis):
    """Classe para processar as falhas técnicas dos sistemas de triagem de
        cartas do CTCE.
    Args:
        Uteis (_type_): Classe com métodos comuns a diversas outras classes.
    """

    def __init__(self, file_path=None):
        """
        Inicializa a classe FalhasTecnicas com o caminho do arquivo.
        """
        self._file_path = file_path
        self._data = None

    def estabelecer_relacionamentos(self):
        """
        Estabelece o relacionamento entre os dados do DataFrame principal
        e seus auxiliares.
        """
        pass

    def processar_dados(self):
        """
        Processa os arquivos de falhas técnicas e retorna um DataFrame 
        consolidado.
        """
        import os
        from concurrent.futures import ThreadPoolExecutor

        def carregar_planilha(path):
            """
            Carrega uma planilha do Excel e retorna um DataFrame.
            """
            # colunas = [
            #     "Código MCU CTC", "Centro de Tratamento",
            #     "Nº Máquina de triagem", "Descrição da Falha",
            #     "Data/hora Inicial da Falha"
            # ]
            dtypes = {
                "Código MCU CTC": str,
                "Centro de Tratamento": str,
                "Nº Máquina de triagem": int,
                "Descrição da Falha": str,
                # "Data/hora Inicial da Falha": datetime
            }
            try:
                # [0, 1, 2, 5, 6])
                df = pd.read_excel(path, skiprows=7, usecols=[
                    0, 1, 2, 5, 6], dtype=dtypes,
                )
                # print(df.columns)
                return df
            except ValueError:
                ValueError(f"Erro ao carregar a planilha: {path}")

        if self._file_path:
            planilhas = os.listdir(self._file_path)
            caminhos = [os.path.join(self._file_path, nome)
                        for nome in planilhas]
            with ThreadPoolExecutor() as executor:
                # Carregar os dados do arquivo
                dfs = list(executor.map(carregar_planilha, caminhos))

                if dfs:
                    df_final = pd.concat(dfs, ignore_index=True)
                    df_final.set_index("Código MCU CTC", inplace=True)
                    df_final = df_final[(df_final["Descrição da Falha"] !=
                                        "Máquina desabilitada - pressione e \
                                        mantenha o botão de habilitar por \
                                        1 segundo p")]

                    df_final["Data/hora inicial da Falha"] = pd.to_datetime(
                        df_final["Data/hora inicial da Falha"],
                        format="%d/%m/%Y %H:%M:%S",)
                    df_final["Data da Falha"] = df_final["Data/hora inicial da Falha"].dt.date
                    df_final["Hora da Falha"] = df_final["Data/hora inicial da Falha"].dt.time
                    self._set_dados(df_final)
                else:
                    raise ValueError("Nenhum arquivo válido encontrado.")
        else:
            raise ValueError("Caminho do arquivo não fornecido.")

    def get_soma_geral_de_falhas(self, data_informada) -> int:
        """
        Retorna a soma geral das falhas técnicas.
        """
        df = self.get_dados() if self.get_dados() is not None \
            else pd.DataFrame()

        if isinstance(data_informada, (list, tuple)):
            data_inicial, data_final = data_informada
        else:
            data_inicial = data_final = data_informada

        if data_final is not None:
            df = df[(df["Data da Falha"] >= data_inicial) &
                    (df["Data da Falha"] <= data_final)]
        else:
            df = df[df["Data da Falha"] == data_inicial]

        return df["Descrição da Falha"].count() if not df.empty else 0

    # Retornar nesta função para corrigir o campo de pesquisa

    def get_soma_falhas_tecnicas(self, centro="CTCE Salvador") -> int:
        """
        Recupera a soma de falhas técnicas para um centro específico.
        """
        df = self.recuperar_dados_pelo_centro(centro)

        def get_falhas_por_data(data_informada):

            if isinstance(data_informada, (list, tuple)):
                data_inicial, data_final = data_informada
            else:
                data_inicial = data_final = data_informada

            if data_final is not None:
                df_ = df[(df["Data da Falha"] >= data_inicial) &
                         (df["Data da Falha"] <= data_final)]
            else:
                df_ = df[df["Data da Falha"] == data_inicial]

            return df_["Descrição da Falha"].count()  # if not df_.empty else 0

        return get_falhas_por_data


if __name__ == "__main__":
    # Exemplo de uso
    # Obter os dados
    file_path_falhas_tecnicas = "C:/Users/80891950/Downloads/Relatório Pitney Bower/Dados/Técnica/"

    falhas_tecnicas = FalhasTecnicas(file_path_falhas_tecnicas)
    falhas_tecnicas.processar_dados()
    # falhas_tecnicas_df = falhas_tecnicas.recuperar_dados_pelo_centro(
    # "CTCE Salvador")
    # print(f"Teste: {falhas_tecnicas_df.head(5)}")
    print(
        f"Total de falhas técnicas: {falhas_tecnicas.get_soma_geral_de_falhas()}")

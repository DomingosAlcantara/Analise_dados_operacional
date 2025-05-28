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

    def _set_dados(self, dados):
        """
        Define os dados a serem processados.
        """
        if dados is not None:
            self._data = dados.copy()
        else:
            self._data = pd.DataFrame()

    def get_dados(self):
        """
        Retorna os dados processados.
        """
        return self._data

    def carregar_planilha(self, path):
        """
        Carrega uma planilha do Excel e retorna um DataFrame.
        """

        # COLUNA_CHAVE = "Código MCU CTC"
        # MAX_LINHAS = 10

        # def tentar_ler(linha):
        #     try:
        #         df = pd.read_excel(path, sheet_name=linha)
        #     except Exception as e:
        #         print(f"Erro ao ler a linha {linha}: {e}")
        #         return None

        #     if COLUNA_CHAVE in df.columns:
        #         return df

        #     return None

        # with ThreadPoolExecutor() as executor:
        #     resultados = list(executor.map(tentar_ler, range(MAX_LINHAS)))

        # for resultado in resultados:
        #     if resultado is not None:
        #         return resultado

        # raise ValueError(f"Coluna '{COLUNA_CHAVE}' não encontrada no arquivo: {path}")
        try:
            df = pd.read_excel(path, skiprows=7)
            return df
        except ValueError:
            ValueError(f"Erro ao carregar a planilha: {path}")

    def processar_dados(self):
        """
        Processa os arquivos de falhas técnicas e retorna um DataFrame consolidado.
        """
        import os
        from concurrent.futures import ThreadPoolExecutor

        if self._file_path:
            planilhas = os.listdir(self._file_path)
            caminhos = [os.path.join(self._file_path, nome)
                        for nome in planilhas]
            with ThreadPoolExecutor() as executor:
                # Carregar os dados do arquivo
                dfs = list(executor.map(self.carregar_planilha, caminhos))

                if dfs:
                    df_final = pd.concat(dfs, ignore_index=True)
                    df_final.set_index("Código MCU CTC", inplace=True)
                    self._set_dados(df_final)
                else:
                    raise ValueError("Nenhum arquivo válido encontrado.")
        else:
            raise ValueError("Caminho do arquivo não fornecido.")

    def get_soma_geral_de_falhas(self):
        """
        Retorna a soma geral das falhas técnicas.
        """
        df = self.get_dados() if self.get_dados() is not None \
            else pd.DataFrame()

        df = df[df["Descrição da Falha"] !=
                "Máquina desabilitada - pressione e mantenha o botão de \
                    habilitar por 1 segundo p"]
        soma_df = df["Descrição da Falha"].count() if not df.empty else 0
        return soma_df

    def get_soma_falhas_tecnicas(self, data_informada, centro: str) -> int:
        """
        Recupera a soma de falhas técnicas para um centro específico.
        """
        df = self.recuperar_dados_pelo_centro(centro)
        return self.get_soma_quantidade_induzida(data_informada, df)


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

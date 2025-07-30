from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import src.uteis as Uteis


class CargaInduzidaModel(Uteis):
    """Classe para modelagem dos dados de carga induzida."""

    def __init__(self, files_path):
        """Inicializa a classe com o caminho dos arquivos."""
        self._files_path = files_path
        self._dados_periodo_selecionado = None
        self.processar_dados()
        self.set_dados_periodo_selecionado()

    def _carregar_planilha(self, path):
        """Carrega uma planilha do Excel e retorna um DataFrame."""
        dtypes = {
            # "Data de triagem": str,
            "Código MCU CTC": str,
            "Centro de Tratamento": str,
            "Nº Máquina de triagem": int,
            "Nome do Plano de Triagem": str,
            "Quantidade Induzida": int,
            "Rendimento Efetivo/h": int,
        }
        try:
            df = pd.read_excel(
                path, skiprows=8, usecols=[0, 1, 2, 3, 5, 6, 13],
                dtype=dtypes
            )
            return df
        except ValueError as e:
            raise ValueError(f"Erro ao carregar a planilha: {path}") from e

    def _formatar_coluna_de_data(self, df):
        """Formata a coluna de data para o formato desejado."""
        df["Data de triagem"] = pd.to_datetime(
            df["Data de triagem"], format="%d/%m/%Y")
        return df

    def _normalizar_nome_colunas(self, df):
        """Normaliza os nomes das colunas do DataFrame."""
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df

    def _definir_indice(self, df):
        """Define o índice do DataFrame."""
        df.set_index("código_mcu_ctc", inplace=True)
        return df

    def processar_dados(self):
        """Processa os dados carregando e formatando as planilhas."""
       dfs = []

        def pipeline(df):
            df = self._carregar_planilha(path)
            df = self._formatar_coluna_de_data(df)
            df = self._normalizar_nome_colunas(df)
            df = self._definir_indice(df)
            return df
    
        with ThreadPoolExecutor() as executor:
            dfs = list(executor.map(
                self._carregar_planilha, 
                self._recuperar_caminhos_planilhas(self._files_path)
            ))
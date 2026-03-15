import pandas as pd

from src.models.paradas_model import ParadasModel
from src.utils.cache import cache


class FalhasTecnicasModel:
    """
    Classe para gerenciar os dados de falhas técnicas.
    """

    def __init__(self, path="/home/domingos/Documentos/Dados/Técnica/"):
        self._paradas_model = ParadasModel(path)
        self._dados_tratados = self.aplicar_tratamento_dados()
        self._dados_filtrados = pd.DataFrame()

    def aplicar_tratamento_dados(self):
        """
        Aplica o tratamento necessário aos dados de falhas técnicas.
        """

        return self._paradas_model._pipeline(
            self._paradas_model.get_dados(),
            [
                self._paradas_model.remover_desabilitacoes,
                self._paradas_model.converter_para_datetime,
                self._paradas_model.extrair_data,
                self._paradas_model.extrair_hora,
                self._paradas_model.remover_coluna_de_data,
                self._paradas_model.padronizar_colunas,
            ],
        )

    def filtrar_dados_por_data(self, data_inicial, data_final):
        """
        Filtra os dados de falhas técnicas por um intervalo de datas.

        Args:
            data_inicial (str): Data inicial no formato 'YYYY-MM-DD'.
            data_final (str): Data final no formato 'YYYY-MM-DD'.

        Returns:
            DataFrame: Dados filtrados pelo intervalo de datas.
        """
        try:
            start = pd.to_datetime(data_inicial).date()
            end = pd.to_datetime(data_final).date()
        except Exception:
            self._dados_filtrados = pd.DataFrame()
            return

        self._dados_filtrados = self._dados_tratados.loc[
            self._dados_tratados["data_da_falha"].between(start, end)
        ]

    def total_falhas_tecnicas(self) -> int:
        """
        Retorna o total de falhas técnicas.

        Returns:
            int: Total de falhas técnicas.
        """
        return int(self._dados_filtrados.shape[0])  # ["descrição_da_falha"].count()

    def media_objetos_por_falhas(self) -> float:
        """
        Retorna a média de objetos por falha técnica.

        Returns:
            float: Média de objetos por falha técnica.
        """
        total_carga = cache.get("total_carga_induzida", 0)  # Recuperar do cache
        print(f"Total de carga induzida recuperada do cache: {total_carga}")
        total_falhas = self.total_falhas_tecnicas()
        if total_falhas == 0:
            return 0
        return total_carga / total_falhas

    def retornar_metricas_falhas_tecnicas(self, data_inicial, data_final):
        """
        Retorna as métricas relacionadas às falhas técnicas.

        Returns:
            dict: Dicionário contendo as métricas calculadas.
        """
        self.filtrar_dados_por_data(data_inicial, data_final)
        print(f"Média de objetos por falha técnica: {self.media_objetos_por_falhas()}")

        return {
            "total_de_falhas": self.total_falhas_tecnicas(),
            "media_objetos_por_falha": round(self.media_objetos_por_falhas(), 2),
            "tempo_total_ocorrencias": 0,
            "duracao_media_falha": 0,
        }

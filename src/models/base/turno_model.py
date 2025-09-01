""" Classe para modelagem dos turnos de trabalho das máquinas de triagem
    automatizadas nos Centros de Tratamento.
"""


import pandas as pd
from pandas import DataFrame


class TurnoModel():
    """
        Classe base para modelagem dos turnos de trabalho.
        Esta classe pode ser estendida para incluir atributos e métodos
        específicos relacionados aos turnos de trabalho das máquinas de triagem
        automatizadas.
    """

    def __init__(self, horarios, df):
        self._horarios = self._definir_formato_hora(horarios,
                                                    ["horario_inicio",
                                                     "horario_final"])
        self._dados = self._definir_formato_hora(
            df, ["hora_inicial_de_triagem",
                 "hora_final_de_triagem"]
        )

    def _definir_formato_hora(self, df: DataFrame,
                              colunas: list = None) -> DataFrame:
        """
        Converte colunas de horário para datetime.time usando transformações
        funcionais.

        Args:
            df (DataFrame): DataFrame com as colunas de horário
            colunas (list, optional): Lista de colunas para converter

        Returns:
            DataFrame: Novo DataFrame com as colunas convertidas
        """
        def converter_para_time(coluna: str) -> pd.Series:
            return pd.to_datetime(df[coluna], format="%H:%M").dt.time

        # Usa colunas padrão se nenhuma for especificada
        colunas_para_converter = colunas or ["horario_inicio", "horario_final"]

        # Filtra apenas colunas que existem no DataFrame
        colunas_validas = filter(
            lambda col: col in df.columns, colunas_para_converter)

        # Cria novo DataFrame com as conversões
        return df.assign(**{
            coluna: converter_para_time(coluna)
            for coluna in colunas_validas
        })

    def _mesclar_dados(self):
        """
        Mescla os dados de horários com os dados de turnos.
        """
        return pd.merge(
            self._dados,
            self._horarios.reset_index(),
            how='cross'
        )

    def _limpar_informacoes_turno(self):
        """
        Limpa os dados para incluir apenas os registros dentro do turno.
        """
        df_merged = self._mesclar_dados()
        return df_merged[
            (df_merged['hora_inicial_de_triagem'] >=
             df_merged['horario_inicio']) &
            (df_merged['hora_final_de_triagem'] <= df_merged['horario_final'])
        ]

    def total_carga_induzida_maquina(self) -> dict:
        """
        Retorna o total de carga induzida pela máquina durante o turno usando
        operações vetorizadas.

        Returns:
            dict: Total de carga induzida por turno e máquina.
        """

        df_filtrado = self._limpar_informacoes_turno()

        # Agrupa por turno e máquina, somando a carga induzida
        resultado = (df_filtrado
                     .groupby(['id', 'nº_máquina'])['quantidade_induzida']
                     .sum()
                     .unstack(fill_value=0)
                     .to_dict('index'))

        return resultado

    def media_rendimento_efetivo_maquina(self) -> dict:
        """
        Retorna o rendimento efetivo da máquina durante o turno.

        Returns:
            float: Rendimento efetivo (carga/hora).
        """
        df_filtrado = self._limpar_informacoes_turno()

        # Calcula a média do rendimento por máquina e turno
        return (df_filtrado
                .groupby(['id', 'nº_máquina'])['rendimento_efetivo/h']
                .mean()
                .reset_index()
                .pivot(index='id', columns='nº_máquina',
                       values='rendimento_efetivo/h')
                .to_dict('index'))

from concurrent.futures import ThreadPoolExecutor as _ThreadPoolExecutor

import pandas as pd
import streamlit as st

from src.uteis import Uteis


class OperacionalModel(Uteis):
    """Classe para modelagem dos dados operacionais."""

    def __init__(self, files_path):
        """Inicializa a classe com o caminho dos arquivos."""
        self._files_path = files_path
        self._dados_periodo_selecionado = None
        self.processar_dados()
        self.set_dados_perido_selecionado()

    def _carregar_planilha(self, path):
        """Carrega uma planilha do Excel e retorna um DataFrame."""
        dtypes = {
            "Código MCU CTC": str,
            "Centro de Tratamento": str,
            "Nº Máquina de triagem": int,
            "Quantidade de Objetos Alimentados": int,
            # "Data/hora inicial da Falha": pd.to_datetime,
            "Descrição da Falha": str,
        }
        try:
            df = pd.read_excel(
                path, skiprows=7, usecols=[0, 1, 2, 3, 5, 6],
                dtype=dtypes
            )
            return df
        except ValueError as e:
            raise ValueError(f"Erro ao carregar a planilha: {path}") from e

    def _formatar_coluna_de_data(self, df):
        """Formata a coluna de data para o formato desejado."""
        df["Data/hora inicial da Falha"] = pd.to_datetime(
            df["Data/hora inicial da Falha"], format="%d/%m/%Y %H:%M:%S")
        return df

    def _extrair_data(self, df):
        """Extrai a data e hora da coluna de data/hora inicial da Falha."""
        df["Data da Falha"] = df["Data/hora inicial da Falha"].dt.date
        return df

    def _extrair_hora(self, df):
        """Extrai a hora da coluna de data/hora inicial da Falha."""
        df["Hora da Falha"] = df["Data/hora inicial da Falha"].dt.time
        return df

    def _normalizar_nome_colunas(self, df):
        """Normaliza os nomes das colunas do DataFrame."""
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df

    def _apagar_coluna_desnecessaria(self, df):
        """Remove colunas desnecessárias do DataFrame."""
        df = df.drop(columns=["Data/hora inicial da Falha"], errors='ignore')
        return df

    def _definir_indice(self, df):
        """Define o índice do DataFrame."""
        df.set_index("Código MCU CTC", inplace=True)
        return df

    def processar_dados(self):
        """Processa os arquivos operacionais e retorna um
            DataFrame consolidado.
        """
        dfs = []

        def pipeline(df):
            """Aplica o pipeline de formatação e extração de dados."""
            df = self._definir_indice(df)
            df = self._formatar_coluna_de_data(df)
            df = self._extrair_data(df)
            df = self._extrair_hora(df)
            df = self._normalizar_nome_colunas(df)
            df = self._apagar_coluna_desnecessaria(df)
            return df

        with _ThreadPoolExecutor() as executor:
            dfs = list(executor.map(
                self._carregar_planilha,
                self._recuperar_caminho_das_planilhas(self._files_path)
            ))
            if dfs:
                df_final = pd.concat(dfs, ignore_index=True)
                self._set_dados(pipeline(df_final))
            else:
                raise ValueError("Nenhum dado encontrado nos arquivos.")

    def set_dados_perido_selecionado(self):
        """Define os dados do período selecionado com base na
            data ou intervalo de datas escolhidas pelo usuário.
        """
        is_interval = st.session_state["modo_data"]
        df = self.get_dados()

        if is_interval:
            data_inicial, data_final = st.session_state["periodos"]
        else:
            data_inicial = st.session_state["periodos"]

        if is_interval:
            self._dados_periodo_selecionado = df[
                (df["data_da_falha"] >= data_inicial) & (
                    df["data_da_falha"] <= data_final)
            ]
        else:
            self._dados_periodo_selecionado = df[
                (df["data_da_falha"] >= data_inicial)
            ]

    def get_centro_de_tratamento(self):
        """Retorna os centros de tratamento únicos do DataFrame."""

        return sorted(self._dados_periodo_selecionado[
            "centro_de_tratamento"].unique().tolist()) \
            if self._dados_periodo_selecionado is not None \
            else pd.DataFrame()

    def get_maquinas(self):
        """Retorna as máquinas de triagem únicas do DataFrame."""
        centros_selecionados = st.session_state["centros_selecionados"]

        df_filtrado = self._dados_periodo_selecionado[
            self._dados_periodo_selecionado["centro_de_tratamento"].
            isin(centros_selecionados)
        ]

        return sorted(df_filtrado["nº_máquina_de_triagem"].unique().tolist()) \
            if self._dados_periodo_selecionado is not None \
            else pd.DataFrame()

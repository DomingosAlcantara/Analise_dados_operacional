"""
Classe que consolidará as informações dos Centros de Tratamento
Automatizados
"""

from statistics import mean

import pandas as pd

from src.carregamento.data_loader import DataLoader
from src.models.base.centro_tratamento_model import CentroTratamentoModel


class EmpresaModel:

    def __init__(self, nome_empresa="Correios"):
        self._nome_empresa = nome_empresa
        self.centros = {}

    def configurar(self, loader: DataLoader):
        """
        Configura a empresa com os dados carregados pelo DataLoader.
        """
        dados_globais = loader.carregar_tudo()
        df_prod = dados_globais["carga tratada"].set_index("código_mcu_ctc")
        codigos_centros = df_prod.index.unique()

        mapeamento = (
            df_prod[["centro_de_tratamento"]]
            .drop_duplicates()
            .to_dict()["centro_de_tratamento"]
        )

        for id_centro in codigos_centros:
            dados_centro = {}
            for categoria, df in dados_globais.items():
                if id_centro in df["código_mcu_ctc"].values:
                    dados_centro[categoria] = df[df["código_mcu_ctc"] == id_centro]
                else:
                    dados_centro[categoria] = df[df.index == id_centro]
                    print(
                        f"Dados para o centro {id_centro} na categoria '{categoria}' estão vazios."
                    )

            nome_centro = mapeamento.get(id_centro, "Desconhecido")
            self.centros[nome_centro] = CentroTratamentoModel(id_centro).configurar(
                dados_centro
            )

        return self

    def definir_intervalo_de_pesquisa(self, data_inicio: str, data_fim: str):
        """
        Define o intervalo de pesquisa para os dados de carga induzida.
        """
        for centro in self.centros.values():
            centro.filtrar_dados_por_data(data_inicio, data_fim)

        return self

    def retornar_centros_de_tratamento(self):
        """
        Retorna a lista de centros de tratamento automatizados presentes no
        DataFrame.
        """
        if not self.centros:
            return []

        return self.centros

    def retornar_carga_induzida_total(self):
        """
        Calcula a carga total induzida somando a carga induzida de todos
        os centros de tratamento.
        """
        if not self.centros:
            return 0

        return sum(centro.total_carga_induzida() for centro in self.centros.values())

    def retornar_media_diaria(self):
        """
        Calcula a média diária de carga induzida somando a carga induzida de
        todos os centros de tratamento.
        """
        if not self.centros:
            return 0

        return sum(centro.obter_media_diaria() for centro in self.centros.values())

    def retornar_rendimento_efetivo_medio(self):
        """
        Calcula o rendimento efetivo médio somando o rendimento efetivo de
        todos os centros de tratamento.
        """
        if not self.centros:
            return 0

        return mean(
            centro.retornar_rendimento_efetivo_medio()
            for centro in self.centros.values()
        )

    def retornar_carga_induzida_por_centro(self):
        """
        Retorna a carga induzida por centro de tratamento.
        """
        if not self.centros:
            return pd.DataFrame(columns=["Centro de Tratamento", "Quantidade Induzida"])

        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": nome_centro,
                    "Quantidade Induzida": centro.total_carga_induzida(),
                }
                for nome_centro, centro in self.centros.items()
            ]
        )

    def retornar_rendimento_efetivo_por_centro(self):
        """
        Retorna o rendimento efetivo por centro de tratamento.
        """
        if not self.centros:
            return pd.DataFrame(
                columns=["Centro de Tratamento", "Rendimento Efetivo Médio"]
            )

        return pd.DataFrame(
            [
                {
                    "Centro de Tratamento": nome_centro,
                    "Rendimento Efetivo Médio": centro.retornar_rendimento_efetivo_medio(),
                }
                for nome_centro, centro in self.centros.items()
            ]
        )

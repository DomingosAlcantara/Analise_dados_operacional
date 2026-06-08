"""
Classe que consolidará as informações dos Centros de Tratamento
Automatizados
"""

from statistics import mean

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

        print(f"Centros de Tratamento: {codigos_centros}")

        for id_centro in codigos_centros:
            dados_centro = {}
            for categoria, df in dados_globais.items():
                if "código_mcu_ctc" in df.columns:
                    dados_centro[categoria] = df.loc[[id_centro]]
                else:
                    dados_centro[categoria] = df[df["código_mcu_ctc"] == id_centro]

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

    def retornar_media_diaria_de_carga_induzida(self):
        """
        Calcula a média diária de carga induzida dividindo a carga total
        induzida pelo número de dias presentes no DataFrame.
        """
        # É necessaŕio definir melhor o calculo da média diária
        if not self._df_carga_induzida.empty:
            dias = self._df_carga_induzida["data"].nunique()
            if dias > 0:
                return self.retornar_carga_induzida_total() / dias
        return 0

from src.carregamento.data_loader import DataLoader
from src.models.base.empresa_model import EmpresaModel
from src.path_files import PathFiles
from src.tratamento.carga_tratada_pipeline import CargaTratadaPipeline

# Definindo as configurações para cada tipo de planilha
configuracoes_dashboard = {
    "carga tratada": {
        "path": PathFiles.ARQUIVOS_CARGA_TRATADA,
        "skip": 8,
        "cols": {
            "Data de triagem": str,
            "Código MCU CTC": int,
            "Centro de Tratamento": str,
            "Nº Máquina": int,
            "Nome do Plano de Triagem": str,
            "Quantidade Induzida": int,
            "Rendimento Efetivo/h": int,
        },
        "pipeline": CargaTratadaPipeline(),
    },
    # "desempenho": {
    #     "path": PathFiles.ARQUIVOS_DISPONIBILIDADE,
    #     "skip": 8,
    #     "cols": {
    #         "Data de triagem": str,
    #         "MCU do centro de tratamento": int,
    #         "Centro de Tratamento": str,
    #         "Nº Máquina de triagem": int,
    #         "Nome do Plano de Triagem": str,
    #         "Quantidade Induzida": int,
    #         "Rendimento Efetivo/h": int,
    #     },
    # },
    # "engarrafamento": {
    #     "path": PathFiles.ARQUIVOS_ATOLAMENTOS,
    #     "skip": 7,
    #     "cols": {
    #         "Código MCU CTC": int,
    #         "Centro de Tratamento": str,
    #         "Nº Máquina de triagem": int,
    #         "Descrição da Falha": str,
    #         "Data/hora inicial da Falha": str,
    #         "Data/hora final da Falha": str,
    #     },
    # },
    # "operacional": {
    #     "path": PathFiles.ARQUIVOS_OPERACIONAL,
    #     "skip": 7,
    #     "cols": {
    #         "Código MCU CTC": int,
    #         "Centro de Tratamento": str,
    #         "Nº Máquina de triagem": int,
    #         "Descrição da Falha": str,
    #         "Data/hora inicial da Falha": str,
    #         "Data/hora final da Falha": str,
    #     },
    # },
    # "tecnicas": {
    #     "path": PathFiles.ARQUIVOS_FALHAS_TECNICAS,
    #     "skip": 7,
    #     "cols": {
    #         "Código MCU CTC": int,
    #         "Centro de Tratamento": str,
    #         "Nº Máquina de triagem": int,
    #         "Descrição da Falha": str,
    #         "Data/hora inicial da Falha": str,
    #         "Data/hora final da Falha": str,
    #     },
    # },
    # "planos de triagem": {
    #     "path": PathFiles.ARQUIVOS_PLANOS_TRAIGEM,
    #     "skip": 8,
    #     "cols": {
    #         "Data Inicial de triagem": str,
    #         "Hora Inicial de triagem": str,
    #         "Código MCU CTC": int,
    #         "Centro de Tratamento": str,
    #         "Nº Máquina de triagem": int,
    #         "Nome do Plano de Triagem": str,
    #         "Data Final de triagem": str,
    #         "Hora Final de triagem": str,
    #         "Tempo de indução": str,
    #         "Tempo de mau funcionamento": str,
    #         "Tempo de setup": str,
    #     },
    # },
}

loader = DataLoader(configuracoes_dashboard)
empresa = EmpresaModel()

empresa.configurar(loader)

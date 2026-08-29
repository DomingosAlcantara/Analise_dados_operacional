from src.controllers.detalhamento import Detalhamento as DetalhamentoController
from src.controllers.index import Index_Controller
from src.controllers.resumos.carga_induzida import CargaInduzida as CargaInduzida_Resumo


def registrar_todos_callbacks():
    """Registra todos os callbacks dos controladores de resumo"""
    Index_Controller().register_callbacks()
    CargaInduzida_Resumo().registrar_callbacks()
    DetalhamentoController().registrar_callbacks()

from src.models.paradas_model import ParadasModel
from src.views.paradas_view import ParadasView


class ParadasController:
    def __init__(self,
                 files_path="/home/domingos/Documentos/Dados/Engarrafamento/"):
        self.modelo = ParadasModel(files_path)
        self.view = ParadasView()

    def exibir_maquinas(self):
        """
        Exibe as máquinas existentes no Centro de Tratamento.
        """
        maquinas = self.modelo.mostrar_maquinas()
        self.view.mostrar_maquinas(maquinas)

    def exibir_grafico_percentual_atolamentos(self):
        """
        Exibe os dados de atolamento de cartas do CTCE.
        """
        atolamentos = self.modelo.get_atolamentos_em_percentual()
        self.view.mostrar_atolamentos(atolamentos if atolamentos is not None
                                      else ("Nenhum atolamento registrado.", 0
                                            )
                                      )

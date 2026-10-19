from dash import dcc

from src.views.resumos.atolamentos import AtolamentosView


class TestAtolamentosView:

    def test_obter_layout_deve_conter_dcc_store_para_dados(self):
        # Arrange
        view = AtolamentosView()

        # Act
        layout = view.obter_layout()

        # Assert - O dcc.Store é o primeiro filho do Div raiz da view
        store_component = layout.children[0]

        assert isinstance(store_component, dcc.Store)
        assert store_component.id == view.ID_STORE_ATOLAMENTOS

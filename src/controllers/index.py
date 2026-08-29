from dash import Input, Output, callback

from src.components.back_button import BackButton
from src.components.sidebar import sidebar_component as Sidebar
from src.views.index_view import IndexApp


class Index_Controller:
    def __init__(self):
        self._view = IndexApp
        self.back_button = BackButton()

    def register_callbacks(self):
        @callback(
            Output(self._view.ID_SIDEBAR_CONTAINER, "children"),
            Input(self._view.ID_URL_LOCATION, "pathname"),
            allow_duplicate=True,
            prevent_initial_call=True,
        )
        def update_sidebar(pathname):
            return Sidebar.layout(current_path=pathname)

        @callback(
            Output(self.back_button.container_id, "style"),
            Input(self._view.ID_URL_LOCATION, "pathname"),
        )
        def toggle_back_button(pathname):
            if pathname and pathname.startswith("/resumos/") and pathname != "/resumos":
                return {"display": "flex", "alignItems": "center"}
            else:
                return {"display": "none"}

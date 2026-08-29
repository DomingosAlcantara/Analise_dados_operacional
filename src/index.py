from src.app import app
from src.controllers import registrar_todos_callbacks
from src.views.index_view import IndexApp

index_app = IndexApp(app)

try:
    registrar_todos_callbacks()
except Exception as e:
    # Silencioso no startup — isso só tenta garantir registro de callbacks
    print(f"Erro ao registrar callbacks da página de Carga Induzida: {e}")

# 3.2. Criamos a instância da classe principal
# Isso define app.layout e registra o callback de roteamento da sidebar
# main_app_instance = IndexApp(app)
if __name__ == "__main__":
    app.run(debug=True)

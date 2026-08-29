import plotly.express as px

from src.engine import empresa

TODOS_OS_CENTROS = empresa.retornar_centros_de_tratamento

_palette = px.colors.qualitative.Plotly
MAPA_CORES_CENTROS = {
    centro: _palette[i % len(_palette)]
    for i, centro in enumerate(sorted(TODOS_OS_CENTROS))
}


def get_color_palette(nome_centro):
    """
    Função para obter uma paleta de cores do Plotly.

    Args:
        nome_centro (str): Nome do centro de tratamento.

    Returns:
        str: Cor associada ao centro de tratamento.
    """
    # print(f"Obtendo cor para o centro: {nome_centro}")
    # print(f"Mapa de cores atual: {MAPA_CORES_CENTROS}")
    return MAPA_CORES_CENTROS.get(
        nome_centro, "#A9A9A9"
    )  # Retorna cinza se o centro não estiver mapeado
    # palette_name = px.colors.qualitative.Plotly

    # return {
    #     name: palette_name[i % len(palette_name)] for i, name in enumerate(unique_names)
    # }

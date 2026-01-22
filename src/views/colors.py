import plotly.express as px


def get_color_palette(names_list):
    """
    Função para obter uma paleta de cores do Plotly.

    Args:
        names_list (DataFrame): Centros de Tratamento.

    Returns:
        list: Lista de cores na paleta especificada.
    """
    unique_names = sorted(list(set(names_list)))
    palette_name = px.colors.qualitative.Plotly

    return {
        name: palette_name[i % len(palette_name)] for i, name in enumerate(unique_names)
    }

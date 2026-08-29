import pandas as pd
import plotly.graph_objects as go

# from src.utils.colors import get_color_palette


class Graficos:
    """Classe utilitário para padronização e geração de gráficos em todo o
    sistema.
    """

    @staticmethod
    def gerar_grafico_barras(df, coluna_x, coluna_y, titulo, texts, cores=None):
        """
        Gera um gráfico de barras com base padronizado.
        Espera receber o DataFrame já ordenado e os textos já formatados

        Args:
            df (pd.DataFrame): DataFrame contendo os dados.
            coluna_x (str): Nome da coluna para o eixo X.
            coluna_y (str): Nome da coluna para o eixo Y.
            titulo (str): Título do gráfico.
            texts (list): Lista de textos para o gráfico.
            cores (list): Lista de cores para as barras.

        Returns:
            plotly.graph_objs._figure.Figure: Gráfico de barras gerado.
        """
        if df is None or df.empty:
            # Retorna um gráfico vazio com uma mensagem
            fig = go.Figure()
            fig.add_annotation(
                text="Sem dados para exibir",
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=20),
            )
            fig.update_layout(
                title=titulo,
                xaxis_title=coluna_x,
                yaxis_title=coluna_y,
                template="plotly_white",
            )
            return fig

        # Evita modificar o DataFrame original
        df = df.copy() if isinstance(df, pd.DataFrame) else df.reset_index()

        figura = go.Figure(
            data=go.Bar(
                x=df[coluna_x],
                y=df[coluna_y],
                text=texts,
                textposition="outside",
                marker_color=cores,
                textfont={"size": 18},
            )
        )

        figura.update_traces(texttemplate="%{text}")

        ticktext = [str(x).replace(" ", "<br>").title() for x in df[coluna_x]]

        figura.update_layout(
            title={
                "text": titulo,
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
                "font": {"size": 25, "color": "black"},
            },
            xaxis=dict(type="category", tickvals=df[coluna_x], ticktext=ticktext),
        )
        figura.update_yaxes(
            range=[0, df[coluna_y].max() * 1.2]
        )  # Ajusta o limite superior do eixo Y
        return figura

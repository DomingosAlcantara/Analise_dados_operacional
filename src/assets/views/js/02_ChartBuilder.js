window.ChartBuilder = class ChartBuilder {
    // Agora não engessamos mais um único formatter no construtor.
    // Injetaremos a função de formatação diretamente no método de construção.
    
    /**
     * Constrói a estrutura de dados e layout para gráficos de barras Plotly
     */
    builderBarChart(
        {
            dados, 
            eixo_x, 
            eixo_y, 
            titulo, 
            orientacao ='v', 
            funcaoFormatacao = null,
            corPadrao = '#3182CE'
        }
    ) {
        if (!dados || dados.length === 0) {
            return {data: [], layout: {}};
        }

        // Se uma função de formatação foi fornecida, a usaremos
        const aplicarFormatacao = (valor) => {
            if (valor === null || valor === undefined) return '';
            return funcaoFormatacao ? funcaoFormatacao(valor) : valor;
        };

        const trace = {
            x: dados.map(d => d[eixo_x]),
            y: dados.map(d => d[eixo_y]),
            text: orientacao === 'v'
                ? dados.map(d => aplicarFormatacao(d[eixo_y]))
                : dados.map(d => aplicarFormatacao(d[eixo_x])),
            textposition: "inside",
            type: "bar",
            orientation: orientacao,
            marker: {
                color: dados.map(d => d["cor"] || corPadrao),
            }
        };

        const layout = {
            title: {
                text: titulo,
                x: 0.5,
                font: {
                    size: 18,
                    color: "#2C3E50",
                    family: "Arial, sans-serif",
                    weight: "bold"
                }
            },
            margin: { t: 50, l: orientacao === 'h' ? 100 : 50, r: 20, b: 30},
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            xaxis: {
                visible:true,
                automargin: true,
            },
            yaxis: {
                visible: orientacao === 'h',
                automargin: true
            },
        };

        // Ordenação do eixo para gráficos horizontais ficarem com o maior em cima
        if (orientacao === 'h') {
            layout.yaxis.categoryorder = 'total ascending'; 
        }

        return {
            data: [trace],
            layout: layout
        };
    }
}
window.AtolamentosPresenter = class AtolamentosPresenter {
    constructor(ChartBuilder, timeFormatter, numberFormatter, tableFormatter) {
        this.ChartBuilder = ChartBuilder;
        this.timeFormatter = timeFormatter;
        this.numberFormatter = numberFormatter;
        this.tableFormatter = tableFormatter;
    }

    render(payload) {
        if (!payload || Object.keys(payload).length === 0) {
            return Array(11).fill(window.dash_clientside.no_update);
        }
        const { kpis, graficos, tabelas } = payload;

        console.log("Payload recebido do Python:", payload);

        return [
            // KPIs Superiores
            this.numberFormatter.formatarCompacto(kpis.total_atolamentos),
            this.numberFormatter.formatarCompacto(kpis.media_atolamentos),
            this.timeFormatter.formatarHHMMSS(kpis.tempo_total_atolamentos || "00:00:00"),
            this.numberFormatter.formatarCompacto(kpis.media_obj_atolamentos),
            this.numberFormatter.formatarCompacto(kpis.media_diaria_objetos_atolamentos),

            //Aba Quantidade (Gráficos e Tabela)
            this.ChartBuilder.builderBarChart({
                dados: graficos.qtd_centro,
                eixo_x: "Total de Atolamentos",
                eixo_y: "Centro de Tratamento",
                titulo: "Quantidade de Atolamentos por Centro",
                orientacao: "h",
                funcaoFormatacao: (v) => this.numberFormatter.formatarCompacto(v),
            }),
            this.ChartBuilder.builderBarChart({
                dados: graficos.qtd_maquina,
                eixo_x: "Nº Máquina",
                eixo_y: "Total de Atolamentos",
                titulo: "Quantidade de Atolamentos por Máquina",
                orientacao: "v",
                funcaoFormatacao: (v) => this.numberFormatter.formatarCompacto(v),
            }),
            this.tableFormatter.formatarColunasDeTempo(tabelas.tempo_centro.data),
            tabelas.tempo_centro.columns,
            
            //Aba Média (Gráficos e Tabela)
            this.ChartBuilder.builderBarChart({
                dados: graficos.media_centro,
                eixo_x: "Objetos Induzidos",
                eixo_y: "Centro de Tratamento",
                titulo: "Média de Objetos Induzidos por Atolamentos por Centro",
                orientacao: "h",
                funcaoFormatacao: (v) => this.numberFormatter.formatarCompacto(v),
            }),
            this.ChartBuilder.builderBarChart({
                dados: graficos.media_maquina,
                eixo_x: "Nº Máquina",
                eixo_y: "Objetos por Atolamento",
                titulo: "Média de Objetos Induzidos por Atolamentos por Máquina",
                orientacao: "v",
                funcaoFormatacao: (v) => this.numberFormatter.formatarCompacto(v),
            }),
            this.tableFormatter.formatarColunasDeTempo(tabelas.tempo_maquina.data),
            tabelas.tempo_maquina.columns
        ];
    }
};
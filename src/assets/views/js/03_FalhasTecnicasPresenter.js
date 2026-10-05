window.FalhasTecnicasPresenter = class FalhasTecnicasPresenter {
    
    constructor(chartBuilder, timeFormatter, numberFormatter, tableFormatter) {
        this.chartBuilder = chartBuilder;
        this.timeFormatter = timeFormatter;
        this.numberFormatter = numberFormatter;
        this.tableFormatter = tableFormatter;
    }

    render(payload) {
        // Se o payload vier vazio, interrompe a atualizaçãode todos os 12 outputs da tela
        if (!payload || Object.keys(payload).length === 0) {
            return Array(12).fill(window.dash_clientside.no_update);
        }

        console.log("Payload recebido do Python:", payload);

        const {kpis, graficos, tabelas} = payload;

        // 1. Processando KPIs (usando os respectivos formatadores)
        const kpiTotal = this.numberFormatter.formatarCompacto(kpis.total);
        const kpiMedia = this.numberFormatter.formatarCompacto(kpis.media);
        const kpiTempo = this.timeFormatter.formatarHHMMSS(kpis.tempo_total);
        const kpiDuracao = this.timeFormatter.formatarHHMMSS(kpis.duracao_media);

        // 2. Processando Gráficos - Aba 1 (Quantidades - usam formatação de números)
        const figCentroQtd = this.chartBuilder.builderBarChart({
            dados: graficos.centro_qtd,
            eixo_x: "Total de Falhas",
            eixo_y: "Centro de Tratamento",
            titulo: "Total de Falhas por Centro",
            orientacao: "h",
            funcaoFormatacao: (v) => this.numberFormatter.formatarCompacto(v)
        });

        const figMaquinaQtd = this.chartBuilder.builderBarChart({
            dados: graficos.maquina_qtd,
            eixo_x: "Nº Máquina",
            eixo_y: "Total de Falhas",
            titulo: "Total de Falhas por Máquina",
            orientacao: "v",
            funcaoFormatacao: (v) => this.numberFormatter.formatarCompacto(v)
        });

        // 3. Processando Gráficos - Aba 2 (Médias de Tempo - usam formatação de Tempo)
        const figCentroMed = this.chartBuilder.builderBarChart({
            dados: graficos.centro_med,
            eixo_x: "Duração Média",
            eixo_y: "Centro de Tratamento",
            titulo: "Duração Média de Falhas por Centro",
            orientacao: "h",
            funcaoFormatacao: (v) => this.timeFormatter.formatarHHMMSS(v)
        });

        const figMaquinaMed = this.chartBuilder.builderBarChart({
            dados: graficos.maquina_med,
            eixo_x: "Nº Máquina",
            eixo_y: "Duração Média",
            titulo: "Duração Média de Falhas por Máquina",
            orientacao: "v",
            funcaoFormatacao: (v) => this.timeFormatter.formatarHHMMSS(v)
        });

        return [
            kpiTotal, 
            kpiMedia, 
            kpiTempo, 
            kpiDuracao, 
            figCentroQtd, 
            figMaquinaQtd, 
            this.tableFormatter.formatarColunasDeTempo(tabelas.centro_qtd.data),
            tabelas.centro_qtd.columns,
            figCentroMed, 
            figMaquinaMed, 
            this.tableFormatter.formatarColunasDeTempo(tabelas.maquina_med.data),
            tabelas.maquina_med.columns
        ];
    }
};
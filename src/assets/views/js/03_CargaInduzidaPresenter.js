window.CargaInduzidaPresenter = class CargaInduzidaPresenter {
    constructor(ChartBuilder, formatter){
        this.ChartBuilder = ChartBuilder;
        this.formatter = formatter;
    }

    render(payload){
        if(!payload || Object.keys(payload).length === 0){
            return Array(7).fill(window.dash_clientside.no_update);
        }

        const {kpis, graficos} = payload;

        return [
            this.formatter.formatarCompacto(kpis.carga),
            this.formatter.formatarCompacto(kpis.media),
            this.formatter.formatarCompacto(kpis.rendimento),

            this.ChartBuilder.builderBarChart({
                dados: graficos.carga_centro, 
                eixo_x: "Centro de Tratamento", 
                eixo_y: "Quantidade Induzida", 
                titulo: "Carga Induzida por Centro",
                funcaoFormatacao: this.formatter.formatarCompacto
            }),
            this.ChartBuilder.builderBarChart({
                dados:graficos.rend_centro, 
                eixo_x:"Centro de Tratamento", 
                eixo_y:"Rendimento Efetivo Médio", 
                titulo:"Rendimento Efetivo por Centro",
                funcaoFormatacao:this.formatter.formatarCompacto
            }),
            this.ChartBuilder.builderBarChart({
                dados:graficos.carga_maquinas, 
                eixo_x:"Nº Máquina", 
                eixo_y:"Quantidade Induzida", 
                titulo:"Carga Induzida por Máquina",
                funcaoFormatacao:this.formatter.formatarCompacto
            }),
            this.ChartBuilder.builderBarChart({
                dados:graficos.rend_maquinas, 
                eixo_x:"Nº Máquina", 
                eixo_y:"Rendimento Efetivo Médio", 
                titulo:"Rendimento Efetivo por Máquina",
                funcaoFormatacao:this.formatter.formatarCompacto
            }),
        ];
    }
};
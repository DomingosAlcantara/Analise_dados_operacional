const chartBuilder = new window.ChartBuilder(window.NumberFormatter);
const presenter = new window.CargaInduzidaPresenter(chartBuilder, window.NumberFormatter);

if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.carga_induzida_resumo = {
    renderizar_tela: function(payload) {
        return presenter.render(payload);
    }
};
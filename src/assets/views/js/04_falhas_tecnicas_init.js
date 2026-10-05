// Instancia o builder (sem travar um formatador especifico nele)
const chartBuilderFalhas = new window.ChartBuilder();
const tableFormatter = new window.TableFormatter(window.TimeFormatter);

const falhasPresenter = new window.FalhasTecnicasPresenter(
    chartBuilderFalhas, 
    window.TimeFormatter, 
    window.NumberFormatter,
    tableFormatter
);

if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.falhas_tecnicas_resumo = {
    renderizar_tela: function(payload) {
        if (!payload || Object.keys(payload).length === 0) {
            return Array(12).fill(window.dash_clientside.no_update);
        }
        return falhasPresenter.render(payload);
    }
};
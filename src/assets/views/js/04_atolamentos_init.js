const chartBuilderAtolamentos = new window.ChartBuilder();
const tableFormatter = new window.TableFormatter(window.TimeFormatter);

const atolamentosPresenter = new window.AtolamentosPresenter(
    chartBuilderAtolamentos,
    window.TimeFormatter,
    window.NumberFormatter,
    tableFormatter
);

if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.atolamentos_resumo = {
    renderizar_tela: function (payload) {
        if (!payload || Object.keys(payload).length === 0) {
            return Array(11).fill(window.dash_clientside.no_update);
        }
        return atolamentosPresenter.render(payload);
    },
};
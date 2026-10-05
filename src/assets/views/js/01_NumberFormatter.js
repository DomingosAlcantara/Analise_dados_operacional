// Expondo a classe globalmente (window) para que os outros arquivos o enxergem
window.NumberFormatter = class NumberFormatter {
    static formatarCompacto(valor) {
        if (!valor) return "0";
        if (typeof valor === 'string') {
            return valor;
        }
        return new Intl.NumberFormat('pt-BR', { 
            notation: "compact", 
            compactDisplay: "short",
            maximumFractionDigits: 1
        }).format(valor);
    }
}
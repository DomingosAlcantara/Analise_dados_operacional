window.TableFormatter = class TableFormatter {

    // Injetamos o timeFormatter para que a tabela saiba como formatar as horas
    constructor(timeFormatter) {
        this.timeFormatter = timeFormatter;
    }

    /**
     * Varre as linhas de uma tabela e formata automaticamente colunas de tempo
     */
    formatarColunasDeTempo(linhas) {
        return (linhas || []).map((linha) => {
            const linhaFormatada = {...linha};
            Object.keys(linhaFormatada).forEach((coluna) => {
                const colLower = coluna.toLowerCase();
                const ehColunaDeTempo = colLower.includes("tempo") || 
                                        colLower.includes("duração") || 
                                        colLower.includes("duracao") ||
                                        colLower.includes("média") ||
                                        colLower.includes("media");

                if (typeof linhaFormatada[coluna] === "number" && ehColunaDeTempo) {
                    // Chama o método estático da classe TimeFormatter que foi injetado
                    linhaFormatada[coluna] = this.timeFormatter.formatarHHMMSS(
                        linhaFormatada[coluna]
                    );
                }
            });
            return linhaFormatada;
        });
    }
}
window.TimeFormatter = class TimeFormatter {
    /**
     * Converte um valor em segundos para o formato "HH:MM:SS".
     * @param {number} totalSegundos.
     * @returns {string} Tempo Formatado.
     */
    static formatarHHMMSS(totalSegundos){
        if (totalSegundos === null || totalSegundos === undefined || isNaN(totalSegundos)) {
            return "00:00:00";
        }

        const total = Math.round(Number(totalSegundos));
        const horas = Math.floor(total / 3600);
        const minutos = Math.floor((total % 3600) / 60);
        const segundos = total % 60;

        const horasFormatadas = horas.toString().padStart(2, "0");
        const minutosFormatados = minutos.toString().padStart(2, "0");
        const segundosFormatados = segundos.toString().padStart(2, "0");

        return `${horasFormatadas}:${minutosFormatados}:${segundosFormatados}`;
    }
}
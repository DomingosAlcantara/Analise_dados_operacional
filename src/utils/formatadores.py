def formatar_tempo_hhmmss(tempo_em_segundos):
    """
    Formata o tempo em segundos para o formato "HH:MM:SS".
    """
    if tempo_em_segundos is None:
        return "---"

    try:
        tempo_em_segundos = float(tempo_em_segundos)
    except (ValueError, TypeError):
        return "---"

    if tempo_em_segundos <= 0:
        return "00:00:00"

    segundos = int(tempo_em_segundos)
    horas, resto = divmod(segundos, 3600)
    minutos, segs = divmod(resto, 60)

    return f"{horas:02d}:{minutos:02d}:{segs:02d}"

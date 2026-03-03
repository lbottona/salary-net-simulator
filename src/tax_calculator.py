def calcola_irpef_lorda(imponibile):
    """
    Calcolo IRPEF lorda 2025
    Scaglioni:
    - 23% fino a 28.000€
    - 35% tra 28.000€ e 50.000€
    - 43% oltre 50.000€
    """
    irpef = 0
    previous_limit = 0

    brackets = [
        (28000, 0.23),
        (50000, 0.35),
        (float("inf"), 0.43),
    ]

    for limit, rate in brackets:
        if imponibile > limit:
            irpef += (limit - previous_limit) * rate
            previous_limit = limit
        else:
            irpef += (imponibile - previous_limit) * rate
            break

    return irpef


def calcola_detrazione_lavoro_dipendente(reddito):
    """
    Detrazione lavoro dipendente 2025 (Art. 13 TUIR)
    """
    if reddito <= 15000:
        return 1955
    elif reddito <= 28000:
        return 1910 + 1190 * ((28000 - reddito) / 13000)
    elif reddito <= 50000:
        return 1910 * ((50000 - reddito) / 22000)
    else:
        return 0


def calcola_netto(ral, mensilita=13):
    # 1️⃣ INPS
    inps = ral * 0.0919

    # 2️⃣ Imponibile fiscale
    imponibile = ral - inps

    # 3️⃣ IRPEF
    irpef_lorda = calcola_irpef_lorda(imponibile)
    detrazione = calcola_detrazione_lavoro_dipendente(imponibile)
    irpef = max(irpef_lorda - detrazione, 0)

    # 4️⃣ Addizionali
    add_regionale = imponibile * 0.0173
    add_comunale = imponibile * 0.008

    totale_tasse = inps + irpef + add_regionale + add_comunale
    netto_annuale = ral - totale_tasse
    netto_mensile = netto_annuale / mensilita

    # 5️⃣ Aliquote
    # Aliquota marginale (basata sull'ultimo scaglione applicato)
    if imponibile <= 28000:
        aliquota_marginale = 0.23
    elif imponibile <= 50000:
        aliquota_marginale = 0.35
    else:
        aliquota_marginale = 0.43

    # Aliquota effettiva (totale tasse su RAL)
    aliquota_effettiva = totale_tasse / ral if ral > 0 else 0

    return {
        "ral": ral,
        "inps": inps,
        "imponibile": imponibile,
        "irpef_lorda": irpef_lorda,
        "detrazione_lavoro_dipendente": detrazione,
        "irpef": irpef,
        "add_regionale": add_regionale,
        "add_comunale": add_comunale,
        "totale_tasse": totale_tasse,
        "netto_annuale": netto_annuale,
        "netto_mensile": netto_mensile,
        "aliquota_marginale": aliquota_marginale,
        "aliquota_effettiva": aliquota_effettiva
    }
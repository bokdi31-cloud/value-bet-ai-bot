def decide_bet(ev, confidence, market_signal, form_strength):

    score = (
        0.4 * ev +
        0.2 * confidence +
        0.2 * market_signal +
        0.2 * form_strength
    )

    if score > 0.25 and ev > 0.04:
        return "BET"
    return "NO_BET"
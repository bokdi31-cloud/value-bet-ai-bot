from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from config import TELEGRAM_TOKEN, BANKROLL
from odds_api import get_odds
from model import predict_probabilities
from value_engine import calc_ev
from ai_decision import decide_bet


def confidence(ev):
    if ev > 0.1:
        return 0.85
    elif ev > 0.06:
        return 0.7
    return 0.55


def market_signal():
    return 0.6  # şimdilik sabit


def form_strength():
    return 0.65  # şimdilik sabit


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = get_odds()
    messages = []

    for match in data[:10]:

        home = match["home_team"]
        away = match["away_team"]

        probs = predict_probabilities(match)

        try:
            o = match["bookmakers"][0]["markets"][0]["outcomes"]

            odds = {
                "home": o[0]["price"],
                "away": o[1]["price"],
                "draw": o[2]["price"] if len(o) > 2 else 0
            }

            for outcome in probs:

                ev = calc_ev(probs[outcome], odds[outcome])

                decision = decide_bet(
                    ev,
                    confidence(ev),
                    market_signal(),
                    form_strength()
                )

                if decision == "BET":

                    stake = BANKROLL * 0.02

                    messages.append(
                        f"🔥 BET APPROVED\n"
                        f"{home} vs {away}\n"
                        f"{outcome.upper()}\n"
                        f"EV: {round(ev,3)}"
                    )

        except:
            continue

    if messages:
        await update.message.reply_text("\n\n".join(messages))
    else:
        await update.message.reply_text("NO BET TODAY")


app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, run))
app.run_polling()
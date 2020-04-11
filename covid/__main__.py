"""Represents executable entrypoint for `covid` telegram bot."""
from COVID19Py import COVID19
from telebot import TeleBot
from telebot.types import Message
from covid import COVID_KEY
from covid.navigation import GramMarkup, Markup, PickButtons

api: COVID19 = COVID19()
bot: TeleBot = TeleBot(COVID_KEY)


@bot.message_handler(commands=("start",))  # type: ignore
def start(message: Message) -> None:
    """Starts `covid telebot` application.

    Args:
        message (Message): input message
    """
    markup: Markup = GramMarkup()
    markup.add_buttons(PickButtons())
    send_message: str = f"<b>Hello {message.from_user.first_name}!</b>\nPlease enter country:"
    bot.send_message(message.chat.id, send_message, parse_mode="html", reply_markup=markup.reply())


def main() -> None:
    """Runs `covid` telegram bot."""
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()

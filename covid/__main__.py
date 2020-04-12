"""Represents executable entrypoint for `covid` telegram bot."""
from telebot.types import Message
from covid.bot import CovidBot
from covid.navigation import GramMarkup, Markup, PickButtons

__bot: CovidBot = CovidBot()


@__bot.message_handler(commands="start")  # type: ignore
def intro(message: Message) -> None:
    """Starts `covid telebot` application.

    Args:
        message (Message): input message
    """
    markup: Markup = GramMarkup()
    markup.add_buttons(PickButtons())
    __bot.send_message(
        message.chat.id,
        text=f"<b>Hello {message.from_user.first_name}!</b>\nPlease enter country:",
        parse_mode="html",
        reply_markup=markup.reply(),
    )


@__bot.message_handler(content_types="text")  # type: ignore
def by_country(message: Message) -> None:
    """Returns covid19 statistics by input country.

    Args:
        message (Message): input message
    """
    message.text = ""


def main() -> None:
    """Runs `covid` telegram bot."""
    __bot.polling(none_stop=True)


if __name__ == "__main__":
    main()

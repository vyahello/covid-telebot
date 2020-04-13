"""Represents executable entrypoint for `covid` telegram bot."""
from punish.style import AbstractStyle
from telebot.types import Message
from covid.bot import CovidBot
from covid.navigation import GramMarkup, Markup, PickButtons
from covid.tracker import CovidTracker, Location

__bot: CovidBot = CovidBot()
bot: CovidBot = __bot


class __Output(AbstractStyle):
    """An output from telegram bot."""

    def __init__(self, message: Message) -> None:
        self._username: str = message.from_user.first_name
        self._message: str = message.text.strip().lower()

    @property
    def message(self) -> str:
        """Returns input message."""
        return self._message

    def as_intro(self) -> str:
        """Returns intro output."""
        return (
            f"<b><i>Hello {self._username}!</i></b>\n"
            f"<i>Please enter country to track covid19 stats:</i>"
        )

    def as_globe(self, location: Location) -> str:
        """Returns globe output.

        Args:
            location (Location): a location item
        """
        globe = location.globe()
        return (
            f"<b><i>Covid19 stats around the {self._message}:</i></b>\n"
            f"<i>Infected: {globe.confirmed()}</i>\n"
            f"<i>Death: {globe.deaths()}</i>\n"
            f"<i>Recovered: {globe.recovered()}</i>\n"
        )

    def as_country(self, location: Location) -> str:
        """Returns country output.

        Args:
            location (Location): a location item
        """
        country = location.by_country(self._message)
        return (
            f"<b><i>Covid19 stats in "
            f"{self._message.title() if len(self._message) > 3 else self._message.upper()}"
            f":</i></b>\n"
            f"<i>Population: {country.population()}</i>\n"
            f"<i>Latest updates: {country.datetime()}</i>\n"
            f"<i>Infected: {country.confirmed()}</i>\n"
            f"<i>Death: {country.deaths()}</i>\n"
            f"<i>Recovered: {country.recovered()}</i>\n"
        )


@__bot.message_handler(commands=("start",))  # type: ignore
def intro(message: Message) -> None:
    """Starts `covid telebot` application.

    Args:
        message (Message): input message
    """
    markup: Markup = GramMarkup()
    markup.add_buttons(PickButtons())
    __bot.send_html_message(
        message.chat.id, text=__Output(message).as_intro(), reply_markup=markup.reply()
    )


@__bot.message_handler(content_types=("text",))  # type: ignore
def by_country(message: Message) -> Message:
    """Returns covid19 statistics by input country.

    Args:
        message (Message): input message
    """
    location: Location = Location(CovidTracker())
    output: __Output = __Output(message)

    if not output.message == "world":
        return __bot.send_html_message(message.chat.id, text=output.as_country(location))
    return __bot.send_html_message(message.chat.id, text=output.as_globe(location))


def main() -> None:
    """Runs `covid` telegram bot."""
    __bot.polling(none_stop=True)


if __name__ == "__main__":
    main()

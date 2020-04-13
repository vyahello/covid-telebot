"""Represents executable entrypoint for `covid` telegram bot."""
from typing import IO, Tuple
from flask import Flask, request
from markdown import markdown
from punish.style import AbstractStyle
from telebot.types import Message, Update
from covid.bot import CovidBot
from covid.navigation import GramMarkup, Markup, PickButtons
from covid.settings import Settings, from_path
from covid.tracker import CovidTracker, Location

__settings: Settings = from_path()
__bot: CovidBot = CovidBot(__settings.bot().token())
__server: Flask = Flask(__name__)


def __as_markdown(content: str) -> str:
    """Returns file content as markdown."""
    with open(content) as readme:  # type: IO[str]
        return markdown(readme.read())


def __readme() -> str:
    """Returns readme documentation as markdown file content."""
    return __as_markdown(content="README.md")


class __Output(AbstractStyle):
    """An output from telegram bot."""

    def __init__(self, message: Message) -> None:
        self._username: str = message.from_user.first_name
        self._message: str = message.text.strip().lower()

    @property
    def message(self) -> str:
        """Returns input __message."""
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


@__bot.message_handler(commands=("start",))
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


@__bot.message_handler(content_types=("text",))
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


@__server.route(f"/{__settings.bot().token()}", methods=("POST",))
def __message() -> Tuple[str, int]:
    """Returns decoded message."""
    __bot.process_new_updates([Update.de_json(request.stream.read().decode("utf-8"))])
    return __readme(), 200


@__server.route("/")
def __web_hook() -> Tuple[str, int]:
    """Sets application web hook for external deployment (e.g `heroku`)."""
    __bot.remove_webhook()
    __bot.set_webhook(__settings.bot().web_hook())
    return __readme(), 200


def main() -> None:
    """Runs `covid` telegram bot."""
    __server.run(
        __settings.server().host(), __settings.server().port(), __settings.server().debug()
    )


if __name__ == "__main__":
    main()

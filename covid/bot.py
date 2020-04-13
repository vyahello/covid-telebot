"""Contains API to manipulate `covid` telegram bot."""
from punish.style import AbstractStyle
from telebot import TeleBot
from telebot.types import Message


class CovidBot(AbstractStyle, TeleBot):
    """Represents `covid` telegram bot."""

    def __init__(
        self, token: str, threaded: bool = True, skip_pending: bool = False, num_threads: int = 10
    ) -> None:
        super().__init__(token, threaded, skip_pending, num_threads)

    def send_html_message(self, chat_id: int, text: str, **kwargs) -> Message:
        """Sends _message to bot in `html` format."""
        return self.send_message(chat_id, text, parse_mode="html", **kwargs)

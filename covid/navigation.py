"""Contains API to manipulate telegram application navigation."""
from abc import abstractmethod
from typing import Any, Sequence
from punish.style import AbstractStyle
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


class Buttons(AbstractStyle):
    """Abstract interface for telegram buttons."""

    @abstractmethod
    def __len__(self) -> int:
        """Returns amount of buttons."""
        pass

    @abstractmethod
    def __getitem__(self, pick: int) -> KeyboardButton:
        """Returns button by it's index.

        Args:
            pick (int): an index
        """
        pass


class Keyboard(AbstractStyle):
    """Abstract interface for telegram keyboard."""

    @abstractmethod
    def buttons(self) -> Buttons:
        """Returns a set of buttons."""
        pass


class Markup(AbstractStyle):
    """Abstract interface for telegram markup form."""

    @abstractmethod
    def reply(self) -> ReplyKeyboardMarkup:
        """Returns reply markup item."""
        pass

    @abstractmethod
    def add_buttons(self, buttons: Buttons) -> None:
        """Adds buttons into markup form.

        Args:
            buttons (Buttons): set of buttons
        """
        pass


class PickButtons(Buttons):
    """Represents button to pick from."""

    def __init__(self) -> None:
        self._buttons: Sequence[KeyboardButton] = (
            KeyboardButton(text="World"),
            KeyboardButton(text="Ukraine"),
            KeyboardButton(text="Spain"),
            KeyboardButton(text="USA"),
        )

    def __len__(self) -> int:
        return len(self._buttons)

    def __getitem__(self, pick: int) -> KeyboardButton:
        return self._buttons[pick]


class GramKeyboard(Keyboard):
    """Represents telegram keyboard."""

    def __init__(self, buttons: Buttons) -> None:
        self._buttons = buttons

    def buttons(self) -> Buttons:
        return self._buttons


class GramMarkup(Markup):
    """Represents telegram markup form."""

    def __init__(self, resize_keyboard: bool = True, row_width: int = 2, **kwargs: Any) -> None:
        self._markup: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard, row_width=row_width, **kwargs
        )

    def reply(self) -> ReplyKeyboardMarkup:
        return self._markup

    def add_buttons(self, buttons: Buttons) -> None:
        self._markup.add(*buttons)

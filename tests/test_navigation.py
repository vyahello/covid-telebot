from telebot.types import ReplyKeyboardMarkup
from covid.navigation import Buttons, Keyboard, Markup
from tests.markers import unit

pytestmark = unit


def test_count_buttons(buttons: Buttons) -> None:
    assert len(buttons) == 6


def test_first_button(buttons: Buttons) -> None:
    assert buttons[0].text == "World"


def test_last_button(buttons: Buttons) -> None:
    assert buttons[-1].text == "China"


def test_keyboard_buttons(keyboard: Keyboard) -> None:
    assert isinstance(keyboard.buttons(), Buttons)


def test_markup_reply(markup: Markup, buttons: Buttons) -> None:
    assert isinstance(markup.reply(), ReplyKeyboardMarkup)


def test_markup_add_buttons(markup: Markup, buttons: Buttons) -> None:
    markup.add_buttons(buttons)
    assert (
        len(tuple(button for row_button in markup.reply().keyboard for button in row_button)) == 6
    )

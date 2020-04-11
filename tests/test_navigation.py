import pytest
from telebot.types import ReplyKeyboardMarkup
from covid.navigation import Buttons, GramKeyboard, GramMarkup, Keyboard, Markup, PickButtons
from tests.markers import unit

pytestmark = unit


@pytest.fixture(scope="module")
def buttons() -> Buttons:
    yield PickButtons()


@pytest.fixture(scope="module")
def keyboard(buttons: Buttons) -> Keyboard:
    yield GramKeyboard(buttons)


@pytest.fixture(scope="module")
def markup() -> Markup:
    yield GramMarkup()


def test_count_buttons(buttons: Buttons) -> None:
    assert len(buttons) == 4


def test_first_button(buttons: Buttons) -> None:
    assert buttons[0].text == "World"


def test_last_button(buttons: Buttons) -> None:
    assert buttons[-1].text == "USA"


def test_keyboard_buttons(keyboard: Keyboard) -> None:
    assert isinstance(keyboard.buttons(), Buttons)


def test_markup_reply(markup: Markup, buttons: Buttons) -> None:
    assert isinstance(markup.reply(), ReplyKeyboardMarkup)


def test_markup_add_buttons(markup: Markup, buttons: Buttons) -> None:
    markup.add_buttons(buttons)
    assert (
        len(tuple(button for row_button in markup.reply().keyboard for button in row_button)) == 4
    )

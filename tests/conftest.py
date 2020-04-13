import pytest
from covid.navigation import Buttons, GramKeyboard, GramMarkup, Keyboard, Markup, PickButtons


@pytest.fixture(scope="module")
def buttons() -> Buttons:
    yield PickButtons()


@pytest.fixture(scope="module")
def keyboard(buttons: Buttons) -> Keyboard:
    yield GramKeyboard(buttons)


@pytest.fixture(scope="module")
def markup() -> Markup:
    yield GramMarkup()

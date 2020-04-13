"""Package contains a set of interfaces to operate `covid` application."""
import os

__author__: str = "Volodymyr Yahello"
__email__: str = "vyahello@gmail.com"
__version__: str = "0.0.0"

COVID_TOKEN: str = os.environ["COVID_KEY"]
WEB_HOOK_URL: str = f"https://corona-telebot.herokuapp.com/{COVID_TOKEN}"
HOST_IP: str = "0.0.0.0"
HOST_PORT: int = int(os.environ.get("PORT", 5000))

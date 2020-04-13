"""Contains API to manipulate settings file."""
import os
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from punish.style import AbstractStyle
from uyaml.loader import Yaml, YamlFromPath, YamlType


class _Server(AbstractStyle):
    """Represents server settings."""

    def __init__(self, content: YamlType) -> None:
        self._content: YamlType = content

    def host(self) -> str:
        """Returns server host."""
        return self._content["host"]

    def port(self) -> int:
        """Returns server port."""
        return int(os.environ.get("PORT", self._content["port"]))

    def debug(self) -> bool:
        """Returns server debug mode."""
        return self._content["debug"]


class _Bot(AbstractStyle):
    """Represents bot settings."""

    def __init__(self, content: YamlType) -> None:
        self._content: YamlType = content

    def token(self) -> str:
        """Returns bot token."""
        return self._content["token"]

    def url(self) -> str:
        """Returns bot url."""
        return self._content["url"]

    def web_hook(self) -> str:
        """Returns bot webhook url."""
        return f"{self.url()}/{self.token()}"


class Settings(AbstractStyle):
    """Represents settings file."""

    def __init__(self, path: str):
        self._yaml: Yaml = YamlFromPath(path)

    def bot(self) -> _Bot:
        """Returns bot settings."""
        return _Bot(self._yaml.section("bot"))

    def server(self) -> _Server:
        """Returns server settings."""
        return _Server(self._yaml.section("server"))


def from_path() -> Settings:
    """Returns telegram bot settings object from passed input `yaml` file."""
    parser: ArgumentParser = ArgumentParser(
        description="Returns telegram bot settings object from passed input `yaml` file",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--setup", "-s", type=str, required=True, help="A settings file (e.g `file.yaml`)"
    )
    return Settings(parser.parse_args().setup)

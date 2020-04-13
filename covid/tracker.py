"""Contains API to manipulate with `covid` stats tracker."""
from abc import abstractmethod
from typing import Any, Dict, List
from COVID19Py import COVID19
from punish.style import AbstractStyle

AnyDict = Dict[Any, Any]
AnyListDict = List[Dict[Any, Any]]


class Tracker(AbstractStyle):
    """Abstract interface for tracker API."""

    @abstractmethod
    def latest(self) -> AnyDict:
        """Returns latest statistics."""
        pass

    @abstractmethod
    def location_by_country(self, code: str) -> AnyListDict:
        """Returns location by given county code e.g `US`."""
        pass


class Target(AbstractStyle):
    """Abstract interface tracker target."""

    @abstractmethod
    def confirmed(self) -> int:
        """Returns amount of confirmed."""
        pass

    @abstractmethod
    def deaths(self) -> int:
        """Returns amount of deaths."""
        pass

    @abstractmethod
    def recovered(self) -> int:
        """Returns amount of recovered."""
        pass


class CovidTracker(Tracker):
    """Represents Covid19 tracker API."""

    __URL: str = "https://coronavirus-tracker-api.herokuapp.com"
    __SOURCE: str = "jhu"

    def __init__(self) -> None:
        self._tracker: COVID19 = COVID19(self.__URL, self.__SOURCE)

    def latest(self) -> AnyDict:
        return self._tracker.getLatest()  # type: ignore

    def location_by_country(self, code: str) -> AnyListDict:
        return self._tracker.getLocationByCountryCode(code)  # type: ignore


class _Country(Target):
    """Represents covid19 statistics for a single country."""

    def __init__(self, country: AnyListDict) -> None:
        self._country = country[0]

    def population(self) -> int:
        """Returns country population."""
        return self._country["country_population"]  # type: ignore

    def datetime(self) -> str:
        """Returns stats datetime."""
        date: str = self._country["last_updated"].split("T")
        return f"{date[0]} {date[1].split('.')[0]}"

    def confirmed(self) -> int:
        return self._country["latest"]["confirmed"]  # type: ignore

    def deaths(self) -> int:
        return self._country["latest"]["deaths"]  # type: ignore

    def recovered(self) -> int:
        return self._country["latest"]["recovered"]  # type: ignore


class _Globe(Target):
    """Represents covid19 statistics around the globe."""

    def __init__(self, globe: Dict[str, int]) -> None:
        self._globe = globe

    def confirmed(self) -> int:
        return self._globe["confirmed"]

    def deaths(self) -> int:
        return self._globe["deaths"]

    def recovered(self) -> int:
        return self._globe["recovered"]


class Location(AbstractStyle):
    """Location target entity."""

    def __init__(self, tracker: Tracker) -> None:
        self._tracker: Tracker = tracker

    def by_country(self, country: str) -> _Country:
        """Returns country target by it's value.

        Raises:
            `ValueError` if given country is not supported.
        """
        if country == "usa":
            return _Country(self._tracker.location_by_country("US"))
        if country == "spain":
            return _Country(self._tracker.location_by_country("ES"))
        if country == "ukraine":
            return _Country(self._tracker.location_by_country("UA"))
        if country == "italy":
            return _Country(self._tracker.location_by_country("IT"))
        if country == "china":
            return _Country(self._tracker.location_by_country("CN"))
        raise ValueError(f"Given '{country}' is not supported!")

    def globe(self) -> _Globe:
        """Returns globe target."""
        return _Globe(self._tracker.latest())

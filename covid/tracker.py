"""Contains API to manipulate with `covid` stats tracker."""
from abc import abstractmethod
from typing import Any, Dict, List
from COVID19Py import COVID19
from punish.style import AbstractStyle


class Tracker(AbstractStyle):
    """Abstract interface for tracker API."""

    @abstractmethod
    def latest(self) -> List[Dict[str, int]]:
        """Returns latest statistics."""
        pass

    @abstractmethod
    def location_by_country(self, code: str) -> List[Dict[Any, Any]]:
        """Returns location by given county code e.g `US`."""
        pass


class CovidTracker(Tracker):
    """Represents Covid19 tracker API."""

    __URL: str = "https://coronavirus-tracker-api.herokuapp.com"
    __SOURCE: str = "jhu"

    def __init__(self) -> None:
        self._tracker: COVID19 = COVID19(self.__URL, self.__SOURCE)

    def latest(self) -> List[Dict[str, int]]:
        return self._tracker.getLatest()  # type: ignore

    def location_by_country(self, code: str) -> List[Dict[Any, Any]]:
        return self._tracker.getLocationByCountryCode(code)  # type: ignore

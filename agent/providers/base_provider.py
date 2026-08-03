from abc import ABC, abstractmethod
from agent.models.venue import Venue
class BaseProvider(ABC):

    def search( self,
    latitude: float,
    longitude: float,
    radius: int = 1000,
    ):
        raise NotImplementedError




    """
    Base class for every venue provider.

    Every provider must inherit from this class
    and implement all abstract methods.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Name of the provider.
        Example:
            OSM
            Geoapify
            Google
        """
        pass

    @abstractmethod
    def search(
        self,
        latitude: float,
        longitude: float,
        radius: int = 1000,
    ) -> list[Venue]:
        """
        Search nearby venues.

        Returns
        -------
        list[Venue]
        """
        pass
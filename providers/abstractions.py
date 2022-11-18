from abc import ABC, abstractmethod

import aiohttp


class RestClient(ABC):
    _session: aiohttp.ClientSession

    @property
    @abstractmethod
    def session(self) -> aiohttp.ClientSession:
        ...


class AuthorizationManager:
    @abstractmethod
    def authorize(self, rest_client: RestClient):
        ...

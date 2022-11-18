import aiohttp

from providers.abstractions import RestClient, AuthorizationManager
from providers.fed_ex.schemas import TrackingRequest

class FedExClient(RestClient):

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    @session.setter
    def session(self, session: aiohttp.ClientSession):
        self._session = session

    async def ensure_authorization(self):
        await self._authorization_manager.authorize(self)

    def __init__(self, base_url: str, authorization_manager: AuthorizationManager):
        self._session = aiohttp.ClientSession(base_url=base_url)
        self._session.headers.update({"Content-Type": "application/json"})
        self._authorization_manager = authorization_manager

    async def get_tracking_details(self, tacking_number: str) -> dict:
        request = TrackingRequest.by_tracking_number_only(tracking_number=tacking_number)
        resp = await self._session.post("/track/v1/trackingnumbers", data=request.json())
        return await resp.json()

    async def __aenter__(self):
        await self.ensure_authorization()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.connector.close()
        await self._session.close()
        print(f"Closing {self.__class__.__name__}")

import os

from providers import abstractions
from providers.abstractions import RestClient
from providers.fed_ex.schemas import AuthRequest, AuthResponse


class FedEXAuthorizationManager(abstractions.AuthorizationManager):
    async def authorize(self, rest_client: RestClient):
        resp = await rest_client.session.post(self._auth_url,
                                              data=self._auth_request_payload.dict(),
                                              headers={"Content-Type": "application/x-www-form-urlencoded"})
        resp.raise_for_status()
        body = AuthResponse(**await resp.json())
        rest_client.session.headers.update({"Authorization": f"{str.title(body.token_type)} {body.access_token}"})

    def __init__(self, client_id: str, client_secret: str, auth_url: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_url = auth_url
        # TODO: implement factory for different grant types
        self._auth_request_payload = AuthRequest(client_id=self._client_id,
                                                 client_secret=self._client_secret,
                                                 grant_type="client_credentials")


fedex_authorization_manager = FedEXAuthorizationManager(client_id=os.getenv("FEDEX_CLIENT_ID"),
                                                        client_secret=os.getenv("FEDEX_CLIENT_SECRET"),
                                                        auth_url="/oauth/token")

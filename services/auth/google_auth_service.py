import httpx

from core.config import app_settings


class GoogleAuthService:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        discovery_url: str,
    ):
        self.httpx_client: httpx.AsyncClient | None = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.discovery_url = discovery_url

    def init_httpx_client(self):
        if self.httpx_client is None:
            self.httpx_client = httpx.AsyncClient()

    async def close_httpx_client(self):
        if self.httpx_client:
            await self.httpx_client.aclose()

    async def _get_config(self):
        self.init_httpx_client()

        if not self.httpx_client:
            raise RuntimeError("Httpx client not initialized")

        response = await self.httpx_client.get(self.discovery_url)
        return response.json()

    async def generate_login_url(self, redirect_uri: str) -> str:
        config = await self._get_config()
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email",
            "prompt": "select_account",
        }
        query_string = "&".join(f"{key}={value}" for key, value in params.items())
        return f"{config["authorization_endpoint"]}?{query_string}"

    async def get_email_from_code(self, code: str, redirect_uri: str) -> str:
        config = await self._get_config()

        if not self.httpx_client:
            raise RuntimeError("Httpx client not initialized")

        response = await self.httpx_client.post(
            config["token_endpoint"],
            data={
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        google_access_token = response.json()["access_token"]

        user = await self.httpx_client.get(
            config["userinfo_endpoint"],
            headers={"Authorization": f"Bearer {google_access_token}"},
        )

        return user.json()["email"]


google_auth_service = GoogleAuthService(
    client_id=app_settings.google_client_id,
    client_secret=app_settings.raw_google_client_secret,
    discovery_url=app_settings.google_discovery_url,
)

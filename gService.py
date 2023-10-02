import os
import json
from cipherio import CBinaryIO
from typing import Any, Callable, Literal, Self, Sequence
from types import TracebackType

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build, Resource


class gCredentials:
    _scopes: Sequence[str]
    _credentials_path: str
    _token_path: str
    _credentials: Credentials
    _credentials_key: bytes | None
    _token_key: bytes | None

    def __init__(
        self,
        scopes: Sequence[str],
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
        password: str | None = None,
    ):
        self._scopes = scopes
        self._credentials_path = credentials_path
        self._token_path = token_path
        if password is not None:
            self._credentials_key = CBinaryIO.createKey(credentials_path, password)
            self._token_key = CBinaryIO.createKey(token_path, password)
        else:
            self._credentials_key = self._token_key = None
        if not self._load():
            raise ValueError("Unable to acquire credentials")

    def _open_file(
        self, file: Literal["credentials", "token"], mode: Literal["r", "w"]
    ):
        path, key = (
            (self._credentials_path, self._credentials_key)
            if file == "credentials"
            else (self._token_path, self._token_key)
        )
        if key is None:
            return open(path, mode + "b")
        else:
            return CBinaryIO.open(path, mode, key=key)

    def _fetch_credentials_v0(self, url_callback: Callable[[str], str]):
        with self._open_file("credentials", "r") as file:
            flow = Flow.from_client_config(
                json.load(file),
                self._scopes,
                redirect_uri="urn:ietf:wg:oauth:2.0:oob",
            )
        url, _ = flow.authorization_url()
        code = url_callback(url)
        flow.fetch_token(code=code)
        return flow.credentials

    def _fetch_credentials(self):
        with self._open_file("credentials", "r") as file:
            flow = InstalledAppFlow.from_client_config(json.load(file), self._scopes)
        self._credentials = flow.run_local_server(port=9000)
        # Save the credentials for the next run
        with self._open_file("token", "w") as file:
            file.write(self._credentials.to_json().encode())

    def _load(self):
        if os.path.exists(self._token_path):
            with self._open_file("token", "r") as file:
                self._credentials = Credentials.from_authorized_user_info(
                    json.load(file), self._scopes
                )
        else:
            self._fetch_credentials()
        return self.update()

    def update(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if self._credentials.valid:
            return True
        if self._credentials.expired and self._credentials.refresh_token:
            try:
                self._credentials.refresh(Request())
            except RefreshError:
                pass
        self._fetch_credentials()
        return self._credentials.valid

    def get(self):
        return self._credentials


class gResource(Resource):
    def execute(self, *args: Any) -> Any:
        ...

    def __call__(self, *args: Any, **kwds: Any) -> Self:
        ...

    def __getattribute__(self, __name: str) -> Self:
        ...


class gData:
    def __getitem__(self, key: str) -> Any:
        ...


class gSubService:
    _resource: gResource

    def __init__(self, resource: gResource):
        self._resource = resource


class gService:
    _service: gResource

    def __init__(self, credentials: gCredentials, serviceName: str, version: str):
        if not credentials.update():
            raise ValueError("Unable to acquire credentials")
        self._service = build(serviceName, version, credentials=credentials.get())

    def __enter__(self):
        self._service.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        self._service.__exit__(exc_type, exc_val, exc_tb)

    def close(self):
        self._service.close()

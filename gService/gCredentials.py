import os
import json
from .cipherio import CBinaryIO
from typing import BinaryIO, Callable, Literal, Self, Sequence

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow, InstalledAppFlow


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
    ) -> None:
        self._scopes = scopes
        self._credentials_path = credentials_path
        self._token_path = token_path
        if password is not None:
            self._credentials_key = CBinaryIO.createKey(credentials_path, password)
            self._token_key = CBinaryIO.createKey(token_path, password)
        else:
            self._credentials_key = self._token_key = None
        self._attemptToLoad()

    def _open_file(
        self, file: Literal["credentials", "token"], mode: Literal["r", "w"]
    ) -> BinaryIO | CBinaryIO:
        path, key = (
            (self._credentials_path, self._credentials_key)
            if file == "credentials"
            else (self._token_path, self._token_key)
        )
        if key is None:
            return open(path, mode + "b")
        else:
            return CBinaryIO.open(path, mode, key=key)

    def _save_credentials_to_file(self) -> None:
        with self._open_file("token", "w") as file:
            file.write(self._credentials.to_json().encode())

    def _update_credentials(self) -> bool:
        if self._credentials.valid:
            return True
        if self._credentials.expired and self._credentials.refresh_token:
            try:
                self._credentials.refresh(Request())
            except RefreshError:
                pass
        return self._credentials.valid

    def _attemptToLoad(self) -> bool:
        if os.path.exists(self._token_path):
            with self._open_file("token", "r") as file:
                self._credentials = Credentials.from_authorized_user_info(
                    json.load(file), self._scopes
                )
            return self._update_credentials()
        return False

    def addCredentials(self, credentails: Credentials) -> bool:
        self._credentials = credentails
        self._save_credentials_to_file()
        return self._update_credentials()

    def fetchCredentialsWithURL(self, url_callback: Callable[[str], str]) -> bool:
        with self._open_file("credentials", "r") as file:
            flow = Flow.from_client_config(
                json.load(file),
                self._scopes,
                redirect_uri="urn:ietf:wg:oauth:2.0:oob",
            )
        url, _ = flow.authorization_url()
        code = url_callback(url)
        flow.fetch_token(code=code)
        return self.addCredentials(flow.credentials)

    def fetchCredentialsWithServer(self) -> bool:
        with self._open_file("credentials", "r") as file:
            flow = InstalledAppFlow.from_client_config(json.load(file), self._scopes)
        credentials = flow.run_local_server()
        return self.addCredentials(credentials)

    def acquireCredentials(self) -> Self:
        if not self._update_credentials() and not self.fetchCredentialsWithServer():
            raise RuntimeError("Unable to fetch credentials")
        return self

    def isValid(self) -> bool:
        return self._credentials.valid

    def get(self) -> Credentials:
        return self._credentials

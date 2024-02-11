from __future__ import annotations
import os
import json
from typing import Any, Callable, cast, Literal, Sequence, Optional

import google.auth
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google.oauth2.credentials import Credentials as OAuth2Credentials
from google_auth_oauthlib.flow import Flow, InstalledAppFlow


class gCredentials:
    _scopes: Sequence[str]

    def __init__(
        self,
        scopes: Sequence[str],
    ) -> None:
        self._scopes = scopes

    def getStoredCredentials(self) -> Credentials | None:
        return None

    def getStoredKey(self) -> str | None:
        return None

    def getScopes(self) -> Sequence[str]:
        return self._scopes

    def default(self) -> tuple[gCredentials, Optional[str]]:
        credentials, project_id = google.auth.default(self._scopes)
        return _gCredentials(self, cast(Any, credentials)), cast(Any, project_id)

    def api_key(self, key: str) -> gCredentials:
        return _gCredentialsApiKey(self, key)

    def oauth2(
        self,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
    ) -> gCredentials:
        return _gCredentialsRefresh(
            self,
            OAuth2Credentials.from_authorized_user_info,
            credentials_path,
            token_path,
        )

    def oauth2_url(
        self,
        url_callback: Callable[[str], str],
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
    ) -> gCredentials:
        return _gCredentialsRefreshUrl(
            self,
            OAuth2Credentials.from_authorized_user_info,
            url_callback,
            credentials_path,
            token_path,
        )

    def service_account(
        self,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
    ) -> gCredentials:
        return _gCredentialsRefresh(
            self,
            ServiceAccountCredentials.from_service_account_file,
            credentials_path,
            token_path,
        )

    def service_account_url(
        self,
        url_callback: Callable[[str], str],
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
    ) -> gCredentials:
        return _gCredentialsRefreshUrl(
            self,
            ServiceAccountCredentials.from_service_account_file,
            url_callback,
            credentials_path,
            token_path,
        )


class _gCredentials(gCredentials):
    _credentials: Credentials

    def __init__(self, c: gCredentials, credentials: Credentials):
        super().__init__(c._scopes)
        self._credentials = credentials

    def getStoredCredentials(self) -> Credentials | None:
        return self._credentials


class _gCredentialsApiKey(gCredentials):
    _key: str

    def __init__(self, c: gCredentials, key: str):
        super().__init__(c._scopes)
        self._key = key

    def getStoredKey(self) -> str | None:
        return self._key


RefreshCredentials = ServiceAccountCredentials | OAuth2Credentials


class _gCredentialsRefresh(gCredentials):
    _credentials_path: str
    _token_path: str
    _stored_credentials: RefreshCredentials | None

    def __init__(
        self,
        c: gCredentials,
        get_credentials: Callable[[Any, Sequence[str]], RefreshCredentials],
        credentials_path: str,
        token_path: str,
    ):
        super().__init__(c._scopes)
        self._credentials_path = credentials_path
        self._token_path = token_path
        self._stored_credentials = self._try_load(get_credentials)

    def _get_file_path(self, file: Literal["credentials", "token"]):
        match file:
            case "credentials":
                return self._credentials_path
            case "token":
                return self._token_path

    def _open_file(
        self, file: Literal["credentials", "token"], mode: Literal["r", "w"]
    ):
        path = self._get_file_path(file)
        return open(path, mode + "b")

    def _save_credentials_to_file(self, credentials: RefreshCredentials) -> None:
        with self._open_file("token", "w") as file:
            file.write(credentials.to_json().encode())

    @staticmethod
    def _update_credentials(credentials: RefreshCredentials) -> bool:
        if credentials.valid:
            return True
        if credentials.expired:
            credentials.refresh(Request())
        return credentials.valid

    def _try_load(
        self, get_credentials: Callable[[Any, Sequence[str]], RefreshCredentials]
    ):
        if os.path.exists(self._token_path):
            with self._open_file("token", "r") as file:
                c = get_credentials(json.load(file), self._scopes)
            if self._update_credentials(c):
                return c
        return None

    def _change_credentials(self, credentails: RefreshCredentials):
        self._save_credentials_to_file(credentails)
        if self._update_credentials(credentails):
            return credentails
        return None

    def _fetch_credentials(self):
        with self._open_file("credentials", "r") as file:
            flow = InstalledAppFlow.from_client_config(json.load(file), self._scopes)
            credentials = flow.run_local_server()
        return self._change_credentials(credentials)

    def getStoredCredentials(self) -> RefreshCredentials | None:
        if self._stored_credentials is not None:
            if not self._update_credentials(self._stored_credentials):
                self._stored_credentials = self._fetch_credentials()
        else:
            self._stored_credentials = self._fetch_credentials()
        return self._stored_credentials


class _gCredentialsRefreshUrl(_gCredentialsRefresh):
    _url_callback: Callable[[str], str]

    def __init__(
        self,
        c: gCredentials,
        get_credentials: Callable[[Any, Sequence[str]], RefreshCredentials],
        url_callback: Callable[[str], str],
        credentials_path: str,
        token_path: str,
    ):
        super().__init__(c, get_credentials, credentials_path, token_path)
        self._url_callback = url_callback

    def _fetch_credentials(self):
        with self._open_file("credentials", "r") as file:
            flow = Flow.from_client_config(
                json.load(file),
                self._scopes,
                redirect_uri="urn:ietf:wg:oauth:2.0:oob",
            )
        url, _ = flow.authorization_url()
        code = self._url_callback(url)
        flow.fetch_token(code=code)
        return self._change_credentials(flow.credentials)

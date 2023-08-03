import requests
from indykite_sdk.model.token import TokenSource, Token
from helpers import data
from indykite_sdk.oauth2 import HttpClient


def test_get_http_client_success(capsys):
    token = None
    client_http = HttpClient()
    assert client_http is not None
    response_http = client_http.get_http_client(token)
    assert isinstance(response_http, HttpClient)
    endpoint = f"{data.get_url()}/knowledge/{data.get_app_space_id}"
    agent_token_bytes = response_http.token_source.token.access_token
    body = {"query": "query ExampleQuery { identityProperties { id }}", "variables": {},
            "operationName": "ExampleQuery"}
    headers = {"Authorization": "Bearer " + agent_token_bytes.decode('utf-8'),
               'Content-Type': 'application/json'}
    response_post = requests.post(endpoint, json=body, headers=headers)
    assert response_post.text is not None


def test_token_valid(capsys):
    token = None
    client_http = HttpClient()
    assert client_http is not None
    response_http = client_http.get_http_client(token)
    assert isinstance(response_http, HttpClient)
    agent_token = Token(response_http.token_source.token.access_token, "Bearer", response_http.token_source.token.expiry)
    assert agent_token.valid
    credentials = client_http.get_credentials()
    token_source = response_http.token_source
    token_source = token_source.static_token_source(response_http.token_source.token, None, credentials)
    assert not token_source.reusable


def test_token_not_valid(capsys):
    token = None
    client_http = HttpClient()
    assert client_http is not None
    response_http = client_http.get_http_client(token)
    assert isinstance(response_http, HttpClient)
    response_http.token_source.token.expiry = 1680000000
    assert response_http.token_source.token.valid
    credentials = client_http.get_credentials()
    response_source = response_http.get_refreshable_token_source(response_http.token_source, credentials)
    assert isinstance(response_source, TokenSource)
    response_error = client_http.get_refreshable_token_source("whoknowswhat", credentials)
    captured = capsys.readouterr()
    assert ("object has no attribute" in captured.err )


def test_http_not_valid(capsys):
    token = None
    client_http = HttpClient()
    assert client_http is not None
    response_http = client_http.get_http_client("whoknowswhat")
    captured = capsys.readouterr()
    assert ("object has no attribute" in captured.err )


def test_get_http_exception(capsys):
    token = None
    client_http = HttpClient()
    assert client_http is not None
    response_http = client_http.get_http_client(token)
    assert isinstance(response_http, HttpClient)
    response_http.token_source = None
    http = response_http.get_http(response_http.token_source)
    captured = capsys.readouterr()
    assert ("TokenSource not found" in captured.err)


def test_no_credentials(capsys):
    token = None
    client_http = HttpClient()
    assert client_http is not None
    response_http = client_http.get_http_client(token)
    assert isinstance(response_http, HttpClient)
    response_source = response_http.get_refreshable_token_source(response_http.token_source, None)
    captured = capsys.readouterr()
    assert ("Credentials not found" in captured.err )


def test_get_http_client_exception(capsys):
    client_http = HttpClient()
    assert client_http is not None
    response_http = client_http.get_http_client("whoknowswhat")
    captured = capsys.readouterr()
    assert ("object has no attribute" in captured.err)


def test_get_token_success(capsys):
    token = None
    client_http = HttpClient()
    response_http = client_http.get_http_client(token)
    access_token = client_http.get_token()
    captured = capsys.readouterr()
    assert access_token is not None


def test_get_token_exception(capsys):
    token = None
    client_http = HttpClient()
    response_http = client_http.get_http_client(token)
    response_http.token_source = None
    access_token = response_http.get_token()
    captured = capsys.readouterr()
    assert ("object has no attribute" in captured.err)


def test_token_success(capsys):
    token = None
    client_http = HttpClient()
    response_http = client_http.get_http_client(token)
    access_token = client_http.get_token()
    captured = capsys.readouterr()
    assert access_token is not None
    token = Token(access_token, "Bearer", 3155760000)
    val = token.valid()
    assert val is not None

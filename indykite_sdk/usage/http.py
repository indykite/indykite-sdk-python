"""
Commandline interface for making an API request with the SDK.
"""
import argparse
import requests
from indykite_sdk.oauth2 import HttpClient
from indykite_sdk.utils import credentials_config
from indykite_sdk import api_helper


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def main():
    # Create parent parser
    parser = argparse.ArgumentParser(description="Identity client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # get_http_client
    get_http_client = subparsers.add_parser("get_http_client")
    get_http_client.add_argument("base_url", help="knowledge endpoint")

    # get_refreshable_token_source
    get_refreshable_token_source = subparsers.add_parser("get_refreshable_token_source")

    args = parser.parse_args()
    command = args.command

    if command == "get_http_client":
        token = None
        # generate an authenticated http client and generate a bearer token from the provided credentials
        client_http = HttpClient()
        response_http = client_http.get_http_client(token)
        client = "identity"
        credentials = credentials_config.lookup_env_credentials_variables(client)
        # call get_refreshable_token_source again to check the token is the same
        response_source = client_http.get_refreshable_token_source(response_http.token_source, credentials)
        print(response_source.token.access_token)
        # call get_http_client again to generate another http client and check if the token is the same
        response_http2 = client_http.get_http_client(response_http.token_source)
        access_token = response_http2.get_token()
        print(response_http2.token_source.token.access_token)
        # make a Knowledge API query
        endpoint = args.base_url
        data = {"query": "query ExampleQuery { identityProperties { id }}", "variables": {},
                "operationName": "ExampleQuery"}
        headers = {"Authorization": "Bearer " + access_token,
                   'Content-Type': 'application/json'}
        response_post = requests.post(endpoint, json=data, headers=headers)
        if response_post.text is not None:
            api_helper.print_response(response_post.text)

    elif command == "get_refreshable_token_source":
        token_source = None
        client_http = HttpClient()
        client = "identity"
        credentials = credentials_config.lookup_env_credentials_variables(client)
        response = client_http.get_refreshable_token_source(token_source, credentials, client)
        access_token_bytes = response.token.access_token
        print(access_token_bytes)


if __name__ == '__main__':  # pragma: no cover
    main()

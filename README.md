# IndyKite Python SDK 🐍

This project serves as a Software Development Kit for developers of Indykite applications.
The Python SDK enables you to easily integrate the IndyKite platform gRPC APIs into your Python application. 
https://console.indykite.id/
https://www.indykite.com/

[![codecov](https://codecov.io/gh/indykite/indykite-sdk-python/branch/master/graph/badge.svg)](https://codecov.io/gh/indykite/indykite-sdk-python)

## Requirements

* Python 3.11

## Installation

    pip install indykite-sdk-python

## Used terminology

| Definition | Description |
| ---------- | ----------- |
| Digital Twin | A digital twin is the digital identity of a physical entity on/in a software/identity system |
| Application Space ID | ID of the application space the digital twin belongs to |
| Application Agent ID | ID of the agent which makes the application available for the different calls |
| Tenant ID | ID of the tenant the digital twin belongs to. The tenant belongs to an application space |
| Private Key and Settings | The secret which required to reach the system. Indykite provides the necessary secrets |
| Property | The digital twin's property (eg.: email, name) |
| JWT | JSON Web Tokens |
| Introspect | A process used to validate the token and to retrieve properties assigned to the token |
| Patch property | Add, change or delete a property of a digital twin |

## Initial settings

1. You need to have an AppAgent credentials json file to be able to use the IndyKite Python SDK. You can get it from the 
   Indykite console: https://console.indykite.id/.

    Example configuration file:

```json
{
    "baseUrl": "",
    "defaultTenantId": "",
    "applicationId": "",
    "appSpaceId": "",
    "appAgentId": "",
    "endpoint": "",
    "privateKeyJWK":
    {
        "alg": "ES256",
        "crv": "P-256",
        "d": "",
        "kid": "",
        "kty": "EC",
        "use": "sig",
        "x": "",
        "y": ""
    },
    "privateKeyPKCS8Base64": "",
    "privateKeyPKCS8": ""
}
```
A token lifetime is 1h by default. You can change this time (from 2 minutes to 24h) by adding a tokenLifetime parameter.

It will have to be human-readable and Golang-like see -> https://pkg.go.dev/time#ParseDuration

Examples: 30m, 1.5h, 2h45m

Example at the end of the json file:
```
{
  ...
  "privateKeyPKCS8": "-----BEGIN PRIVATE KEY-----\nM\n-----END PRIVATE KEY-----",
  "tokenLifetime": "30m"
}
```

Conditionally optional parameters:,
- baseUrl
- defaultTenantId
- endpoint


2. Credentials 
    #### Identity
    You have two choices to set up the necessary credentials. You either pass the json to the `INDYKITE_APPLICATION_CREDENTIALS`
    environment variable or set the `INDYKITE_APPLICATION_CREDENTIALS_FILE` environment variable to the configuration file's path.

   - on Linux and OSX

       ```
        export INDYKITE_APPLICATION_CREDENTIALS='{
          "baseUrl": "",
          "defaultTenantId": "",
          "applicationId": "",
          "appSpaceId": "",
          "appAgentId": "",
          "endpoint": "",
          "privateKeyJWK":
          {
              "alg": "ES256",
              "crv": "P-256",
              "d": "",
              "kid": "",
              "kty": "EC",
              "use": "sig",
              "x": "",
              "y": ""
          },
          "privateKeyPKCS8Base64":"",
          "privateKeyPKCS8": ""
      }'
        ```

     or

      `export INDYKITE_APPLICATION_CREDENTIALS_FILE=/Users/xx/configuration.json`

   - on Windows command line


       ```
        setex INDYKITE_APPLICATION_CREDENTIALS='{
            "baseUrl": "",
            "defaultTenantId": "",
            "applicationId": "",
            "appSpaceId": "",
            "appAgentId": "",
            "endpoint": "",
            "privateKeyJWK":
            {
                "alg": "ES256",
                "crv": "P-256",
                "d": "",
                "kid": "",
                "kty": "EC",
                "use": "sig",
                "x": "",
                "y": ""
            },
            "privateKeyPKCS8Base64":"",
            "privateKeyPKCS8": ""
        }'
        ```

     or

      `setex INDYKITE_APPLICATION_CREDENTIALS_FILE "C:\Users\xx\Documents\configuration.json"`




#### Config
To manage its spaces, among other things, the **DigitalTwin (DT)** who owns the relevant customer creates a **service account**.

A service account is a non person entity which belongs to the **DT** who created it. It is a **DT** with its own credential which acts only through its owner.

A service account is always created under a customer.

The purpose of a service account is for a non person entity to manage the platform configuration: creating AppSpaces, creating applications, creating agent credentials, creating other service accounts, modify user permissions or any action through the **Graph DB**.
The service account is also needed if you want to use Terraform for your configuration.

You have two choices to set up the necessary credentials. You either pass the json to the `INDYKITE_SERVICE_ACCOUNT_CREDENTIALS`
environment variable or set the `INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE` environment variable to the configuration file's path.

   - on Linux and OSX
       ```
        export INDYKITE_SERVICE_ACCOUNT_CREDENTIALS='{
         "serviceAccountId":"",
         "endpoint":"",
         "privateKeyJWK":{
           "alg":"ES256",
           "crv":"P-256",
           "d":"",
           "kid":"",
           "kty":"EC",
           "use":"sig",
           "x":"",
           "y":""
           },
         "privateKeyPKCS8Base64":"",
         "privateKeyPKCS8":"-----BEGIN PRIVATE KEY----------END PRIVATE KEY-----\n"
         }'
        ```

     or

      `export INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE=/Users/xx/configuration.json`

   - on Windows command line


       ```
        setex INDYKITE_SERVICE_ACCOUNT_CREDENTIALS='{
         "serviceAccountId":"",
         "endpoint":"",
         "privateKeyJWK":{
           "alg":"ES256",
           "crv":"P-256",
           "d":"",
           "kid":"",
           "kty":"EC",
           "use":"sig",
           "x":"",
           "y":""
           },
         "privateKeyPKCS8Base64":"",
         "privateKeyPKCS8":"-----BEGIN PRIVATE KEY----------END PRIVATE KEY-----\n"
         }'
        ```

     or

      `setex INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE "C:\Users\xx\Documents\configuration.json"`


3. Initialize a client to establish the connection. This client instance's `self.stub` will be used by the other functions.

*Note:* The client is opening a GRPC channel and the client *must* close the channel, too! If the client doesn't close the channel
after use, it can cause surprises like `_InactiveRpcErrors`.

```python
from indykite_sdk.identity import IdentityClient
import argparse

    # Create parent parser
    parser = argparse.ArgumentParser(description="Identity client API.")
    parser.add_argument("-l", "--local", action="store_true", help="make the request to localhost")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")
    
    # Create 
    args = parser.parse_args()
    local = args.local
    client = IdentityClient(local)
```

4. Close a GRPC channel
You simple call the `close()` function on the channel (The `IdentityClient()` function below represents the def in the previous step)
```python
from indykite_sdk.identity import IdentityClient

def open_and_close_channel():
    client = IdentityClient()
    client.channel.close()
```

### Running tests

To run unit tests, simply execute

    pytest

To display code coverage, enter

    pytest --cov .

### Functions details

https://indykite.github.io/indykite-sdk-python/


### Examples

https://github.com/indykite/indykite-sdk-python/tree/master/indykite_sdk


## SDK Development

Commit message follows
[commit guidelines](./doc/guides/commit-message.md#commit-message-guidelines)

## Roadmap

Checkout our roadmap on our
[issues page](https://github.com/indykite/indykite-sdk-python/issues)

## Contributing

[Contribution guidelines for this project](contributing.md)

## Support, Feedback, Connect with other developers

Feel free to file a bug, submit an issue or give us feedback on our
[issues page](https://github.com/indykite/indykite-sdk-python/issues)

## Vulnerability Reporting

[Responsible Disclosure](responsible_disclosure.md)

## Changelog

[Changelog](CHANGELOG.md)

## Contributers / Acknowledgements

Coming Soon!

## What is IndyKite

IndyKite is a cloud identity platform built to secure and manage human & non-person (IoT) identities and their data. Based on open source standards, the cloud platform gives developers the ability to secure data and embed identity controls into their Web 3.0 applications. Empowering the world’s 23 million developers without the need to involve security and identity specialists.

## License

[This project is licensed under the terms of the Apache 2.0 license.](LICENSE)

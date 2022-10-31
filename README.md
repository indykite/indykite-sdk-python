# JARVIS Python SDK 🐍

This project serves as a Software Development Kit for developers of Indykite applications.

[![codecov](https://codecov.io/gh/indykite/jarvis-sdk-python/branch/master/graph/badge.svg?token=8u4yvyi5PN)](https://codecov.io/gh/indykite/jarvis-sdk-python)

## Requirements

* Python 3.8
* [Buf](https://github.com/bufbuild/buf)

## Installation

* Create virtual env and install dependencies

        pipenv install

* Generate protobufs

        ./gen_proto.sh

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

1. You need to have a configuration json file to be able to use the Jarvis Proto SDK. You can get it from your
   Indykite contact or from Indykite console if you have access to it.

    Example configuration file:

```json
{
  "appSpaceId": "696e6479-6b69-4465-8000-010100000002",
  "baseUrl": "https://jarvis.indykite.com",
  "applicationId": "696e6479-6b69-4465-8000-020100000002",
  "defaultTenantId": "696e6479-6b69-4465-8000-030100000002",
  "appAgentId": "696e6479-6b69-4465-8000-050100000002",
  "endpoint": "jarvis.indykite.com",
  "privateKeyJWK": {
    "kty": "EC",
    "d": "aa",
    "use": "sig",
    "crv": "P-256",
    "kid": "2e5lIxxb6obIwpok",
    "x": "6d83se2Eg",
    "y": "lshzMo",
    "alg": "ES256"
  },
  "privateKeyPKCS8Base64": "LS0tLS==",
  "privateKeyPKCS8": "-----BEGIN PRIVATE KEY-----\nM\n-----END PRIVATE KEY-----"
}
```

Conditionally optional parameters:
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
        "appSpaceId":"00000000-0000-4000-a000-000000000000",
        "appAgentId":"00000000-0000-4000-a000-000000000001",
        "endpoint": "application.indykite.com",
        "privateKeyJWK":{
          "kty":"EC",
          "d": "abcdef",
          "use": "sig",
          "crv": "P-256",
          "kid":"efghij",
          "x":"klmnop",
          "y":"qrstvw",
          "alg":"ES256"
          }
        }'
        ```

     or

      `export INDYKITE_APPLICATION_CREDENTIALS_FILE=/Users/xx/configuration.json`

   - on Windows command line


       ```
        setex INDYKITE_APPLICATION_CREDENTIALS='{
        "appSpaceId":"00000000-0000-4000-a000-000000000000",
        "appAgentId":"00000000-0000-4000-a000-000000000001",
        "endpoint": "application.indykite.com",
        "privateKeyJWK":{
          "kty":"EC",
          "d": "abcdef",
          "use": "sig",
          "crv": "P-256",
          "kid":"efghij",
          "x":"klmnop",
          "y":"qrstvw",
          "alg":"ES256"
          }
        }'
        ```

     or

      `setex INDYKITE_APPLICATION_CREDENTIALS_FILE "C:\Users\xx\Documents\configuration.json"`




#### Config
You have two choices to set up the necessary credentials. You either pass the json to the `INDYKITE_SERVICE_ACCOUNT_CREDENTIALS`
environment variable or set the `INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE` environment variable to the configuration file's path.

   - on Linux and OSX
       ```
        export INDYKITE_SERVICE_ACCOUNT_CREDENTIALS='{
        "serviceAccountId":"gid:AAAAEg5K78iO852lPKlg25Ui6Nm",
        "endpoint":"jarvis.indykite.com",
         "privateKeyJWK":{
            "kty": "EC",
            "d": "Uio125jfi8Oph5hIoj4KLnw6Ha96qhGgh2yUIJki66gYuNjkMg",
            "use": "sig",
            "crv": "P-256",
            "kid": "ph5hIoj4KLnw6HUio125jfi8Oph5hIoj4Khy5Plmy5uk8t7",
            "x": "fr8f5LjhrtjJkyui66gt5i8ff5jflsHtgd3nf",
            "y": "445mfgykk4hisfYyrej4HygTjg46Sqw69gHYh",
            "alg": "ES256"
         }
        }'
        ```

     or

      `export INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE=/Users/xx/configuration.json`

   - on Windows command line


       ```
        setex INDYKITE_SERVICE_ACCOUNT_CREDENTIALS='{
        "serviceAccountId":"gid:AAAAEg5K78iO852lPKlg25Ui6Nm",
        "endpoint":"jarvis.indykite.com",
         "privateKeyJWK":{
            "kty": "EC",
            "d": "Uio125jfi8Oph5hIoj4KLnw6Ha96qhGgh2yUIJki66gYuNjkMg",
            "use": "sig",
            "crv": "P-256",
            "kid": "ph5hIoj4KLnw6HUio125jfi8Oph5hIoj4Khy5Plmy5uk8t7",
            "x": "fr8f5LjhrtjJkyui66gt5i8ff5jflsHtgd3nf",
            "y": "445mfgykk4hisfYyrej4HygTjg46Sqw69gHYh",
            "alg": "ES256"
         }
        }'
        ```

     or

      `setex INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE "C:\Users\xx\Documents\configuration.json"`


3. Initialize a client to establish the connection. This client instance's `self.stub` will be used by the other functions.

*Note:* The client is opening a GRPC channel and the client *must* close the channel, too! If the client doesn't close the channel
after use, it can cause surprises like `_InactiveRpcErrors`.

```python
import certifi
import grpc
import json
import os
import time
import uuid
from authlib.jose import JsonWebKey, jwt
from datetime import datetime, timedelta, timezone

from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2_grpc as pb2_grpc

def __init__(self, credential_json=None, credential_file=None):
    if credential_json is None:
        credentials = os.path.join(os.path.dirname(credential_file), os.path.basename(credential_file))
        with open(credentials, 'r') as file:
            raw_content = file.read()
            credentials = json.loads(raw_content)
    else:
        credentials = json.loads(credential_json)

    # Create JWT token out of the credentials
    jwk = credentials.get('private_key_jwk')
    key = JsonWebKey.import_key(jwk)
    message = {
            'exp': int(time.mktime((datetime.now(timezone.utc) + timedelta(hours=24)).timetuple())),
            'iat': int(time.mktime((datetime.now(timezone.utc)).timetuple())),
            'iss': credentials.get('app_agent_id'),
            'jti': str(uuid.uuid4()),
            'sub': credentials.get('app_agent_id'),
        }

    jwt_token = jwt.encode({
            'alg': 'ES256',
            'cty': 'JWT',
            'kid': jwk['kid']
    }, message, key)

    call_credentials = grpc.access_token_call_credentials(jwt_token.decode("utf-8"))

    certificate_path = certifi.where()
    endpoint = credentials.get("endpoint")

    with open(certificate_path, "rb") as cert_file:
        channel_credentials = grpc.ssl_channel_credentials(cert_file.read())

    composite_credentials = grpc.composite_channel_credentials(channel_credentials,
                                                               call_credentials)

    self.channel = grpc.secure_channel(endpoint, composite_credentials)
    self.stub = pb2_grpc.IdentityManagementAPIStub(channel=self.channel)
```

4. Close a GRPC channel
You simple call the `close()` function on the channel (The `IdentityClient()` function below represents the def in the previous step)
```python
from jarvis_sdk.cmd import IdentityClient

def open_and_close_channel():
    client = IdentityClient()
    client.channel.close()
```

## Running tests

To run unit tests, simply execute

    pytest

To display code coverage, enter

    pytest --cov .

## Functions to call

Most of the calls can be executed in two ways:

1. An admin is able to manipulate a digital twin if he has proper rights to do so ([Admin service](#admin-service))
2. As a self-service, the user is able to manipulate his account (modify/delete) using his active token ([Self-service](#self-serice))

Currently available functions:
- [Introspect token](#introspect-token)
- [Get user infromation](#get-user-information)
- [Add, modify, delete a digital twin's property](#addmodifyremove-user-property-patch-property)
- [Delete a digital twin](#delete-user)
- [Verify email](#verify-email)
- [Send new verification email](#send-new-verification-email-admin-service)
- [Change password](#change-password)
- [Ingest records](#ingest-records)

### Introspect token

“Token introspection” occurs when a resource server sends the token to the authorization server that originally issued the token,
and receives a response from the authorization server with detail on whether the token is active or expired and what attributes are included in the token.
If the token was not valid, then the `response.active` attribute is false and no other information is in the response.


```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2

def introspect_token(self, user_token):
    response = self.stub.TokenIntrospect(
                pb2.TokenIntrospectRequest(token=user_token)
            )

    print (response)
```

### Get user information

It is possible to get an existing user's properties like it's email, mobile, nickname, givenname, familyname ...etc.

#### Admin service

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import model_pb2 as model
from jarvis_sdk.indykite.identity.v1beta1 import attributes_pb2 as attributes

def get_digital_twin(self, digital_twin_id, tenant_id, field_name):
    response = self.stub.GetDigitalTwin(
            pb2.GetDigitalTwinRequest(
                id=pb2.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=digital_twin_id.bytes,
                        tenant_id=tenant_id.bytes
                    )
                ),
                properties=[
                    attributes.PropertyMask(
                        definition=attributes.PropertyDefinition(property=field_name)
                    )
                ]
            )
        )

    print (response)
```

#### Self-service

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import attributes_pb2 as attributes

def get_digital_twin(self, token, field_name):
    response = self.stub.GetDigitalTwin(
                pb2.GetDigitalTwinRequest(
                    id=pb2.DigitalTwinIdentifier(access_token=token),
                    properties=[
                        attributes.PropertyMask(
                            definition=attributes.PropertyDefinition(property=field_name)
                        )
                    ]
                )
        )

    print (response)
```

### Add/Modify/Remove User property (Patch property)

It is possible to add a property to a digital twin, modify an existing property or delete an existing property if it's not
protected. Also, the `PatchDigitalTwin` allows to send multiple operations in one request

#### Admin service

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import model_pb2 as model
from jarvis_sdk.indykite.identity.v1beta1 import attributes_pb2 as attributes
from jarvis_sdk.indykite.objects import struct_pb2 as objects

def patch_property_add(self, digital_twin_id, tenant_id, property_name, value):
    response = self.stub.PatchDigitalTwin(
            pb2.PatchDigitalTwinRequest(
                id=pb2.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=digital_twin_id.bytes,
                        tenant_id=tenant_id.bytes
                    )
                ),
                operations=[
                    attributes.PropertyBatchOperation(
                        add=attributes.Property(
                            definition=attributes.PropertyDefinition(property=property_name),
                            object_value=objects.Value(string_value=value)
                        )
                    )
                ]
            )
        )

    print (response)
```

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import model_pb2 as model
from jarvis_sdk.indykite.identity.v1beta1 import attributes_pb2 as attributes
from jarvis_sdk.indykite.objects import struct_pb2 as objects

def patch_property_replace(self, digital_twin_id, tenant_id, property_id, value):
    response = self.stub.PatchDigitalTwin(
            pb2.PatchDigitalTwinRequest(
                id=pb2.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=digital_twin_id.bytes,
                        tenant_id=tenant_id.bytes
                    )
                ),
                operations=[
                    attributes.PropertyBatchOperation(
                        replace=attributes.Property(
                            id=int(property_id),
                            object_value=objects.Value(string_value=value)
                        )
                    )
                ]
            )
        )

    print (response)
```

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import model_pb2 as model
from jarvis_sdk.indykite.identity.v1beta1 import attributes_pb2 as attributes

def patch_property_remove(self, digital_twin_id, tenant_id, property_id):
    response = self.stub.PatchDigitalTwin(
            pb2.PatchDigitalTwinRequest(
                id=pb2.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=digital_twin_id.bytes,
                        tenant_id=tenant_id.bytes
                    )
                ),
                operations=[
                    attributes.PropertyBatchOperation(
                        remove=attributes.Property(
                            id=int(property_id)
                        )
                    )
                ]
            )
        )

    print (response)
```

#### Self-service

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import model_pb2 as model
from jarvis_sdk.indykite.identity.v1beta1 import attributes_pb2 as attributes
from jarvis_sdk.indykite.objects import struct_pb2 as objects

def patch_property_add_replace_remove(self, token, add_name, add_value, replace_id, replace_value, remove_id):
    response = self.stub.PatchDigitalTwin(
            pb2.PatchDigitalTwinRequest(
                id=pb2.DigitalTwinIdentifier(access_token=token),
                operations=[
                    attributes.PropertyBatchOperation(
                        add=attributes.Property(
                            definition=attributes.PropertyDefinition(property=add_name),
                            object_value=objects.Value(string_value=add_value)
                        )
                    ),
                    attributes.PropertyBatchOperation(
                        replace=attributes.Property(
                            id=int(replace_id),
                            object_value=objects.Value(string_value=replace_value)
                        )
                    ),
                    attributes.PropertyBatchOperation(
                        remove=attributes.Property(
                            id=int(remove_id)
                        )
                    )
                ]
            )
        )

    print (response)

```

### Delete User

It is allowed to send a delete user request which deletes the digital twin and all of it's connected properties from the system.

#### Admin service

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import model_pb2 as model

def del_user(self, digital_twin_id, tenant_id):
    response = self.stub.DeleteDigitalTwin(
            pb2.DeleteDigitalTwinRequest(
                id=pb2.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=digital_twin_id.bytes,
                        tenant_id=tenant_id.bytes
                    )
                )
            )
        )

    print (response)
```

#### Self-service

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2

def del_user(self, token):
    response = self.stub.DeleteDigitalTwin(
                pb2.DeleteDigitalTwinRequest(
                    id=pb2.DigitalTwinIdentifier(access_token=token)
                )
        )
```

### Verify email

When the registration required an email verification to complete the registration, the system sends a verification email to the
registered email address. The email should contain a token which can be sent to the SDK via `VerifyDigitalTwinEmail` function to
set the digital twin's email as verified email.

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2

def verify_email(self, token):
    response = self.stub.VerifyDigitalTwinEmail(
            pb2.VerifyDigitalTwinEmailRequest(token=token)
        )
```

### Send new verification email (admin service)

It is possible that the token in the verification email is already expired when the user tried to verify his email. In this case
it is necessary to send out a new, valid verification email. Calling the `StartDigitalTwinEmailVerification` method the system
sends out another verification email to the registered address with a new token.

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import model_pb2 as model

def new_verification_email(self, digital_twin_id, tenant_id, email):
    response = self.stub.StartDigitalTwinEmailVerification(
            pb2.StartDigitalTwinEmailVerificationRequest(
                digital_twin=model.DigitalTwin(
                    id=digital_twin_id.bytes,
                    tenant_id=tenant_id.bytes
                ),
                email=email
            )
        )
```

### Change password

Where there is a password, there is a high chance to forget it. With the `ChangePassword` function either the admin with the digital twin ID
and tenant ID (Admin service), or the user (self-service) with his active token can change it.

#### Admin service

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import model_pb2 as model

def change_password(self, digital_twin_id, tenant_id, new_password):
    response = self.stub.ChangePassword(
            pb2.ChangePasswordRequest(
                digital_twin=model.DigitalTwin(
                    id=digital_twin_id.bytes,
                    tenant_id=tenant_id.bytes
                ),
                password=new_password
            )
        )

    print (response)
```

#### Self-service

```python
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2

def change_password(self, token, new_password):
    response = self.stub.ChangePassword(
            pb2.ChangePasswordRequest(
                token=token,
                password=new_password,
                ignore_policy=2
            )
        )

    print(response)
```

### Ingest records

```python
def stream_records(self, config_id, records):
    record_iterator = self.generate_records_request(config_id, records)
    response_iterator = self.stub.StreamRecords(record_iterator)

    for response in response_iterator:
      print(response)
```

### Get customer information

It is possible to get an existing customer's information.
If we don't have its id or name, we can get its id through service_account
The service account id is in the config file.
The ServiceAccount class will also return the customer id

#### Read service account

```python
from jarvis_sdk.cmdconfig import helper
from jarvis_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from jarvis_sdk.indykite.config.v1beta1 import model_pb2 as model
from jarvis_sdk.model.service_account import ServiceAccount


def get_service_account(self,service_account_id):
        response = self.stub.ReadServiceAccount(
            pb2.ReadServiceAccountRequest(
                id=str(service_account_id)
            )
        )
        print(response)
```

#### Read customer id with service_account request
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_customer(self, local):
    client_config = ConfigClient(local)
    service_account = client_config.get_service_account()
    print(service_account.customer_id)
    customer = client_config.get_customer_by_id(service_account.customer_id)
    print(customer)
```

#### Read customer name
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_customer(self, local, customer_name):
    client_config = ConfigClient(local)
    customer = client_config.get_customer_by_name(customer_name)
    print(customer)
```

### Get AppSpace information

It is possible to get an existing AppSpace's information from customer, AppSpaceId and AppSpace name.
#### Read appspace with id
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_app_space(self, local, app_space_id):
    client_config = ConfigClient(local)
    app_space = client_config.get_app_space_by_id(app_space_id)
    print(app_space)
```

#### Read appspace with name
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_app_space(self, local, customer_id, app_space_name):
    client_config = ConfigClient(local)
    app_space = client_config.get_app_space_by_name(customer_id, app_space_name)
    print(app_space)
```

#### List appspaces 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_app_spaces(self, local, customer_id, match_list, bookmarks=[]):
    #match_list is a nonempty list of app_spaces names
    client_config = ConfigClient(local)
    list_app_spaces_response = client_config.list_app_spaces(customer_id, match_list, bookmarks)
    print(list_app_spaces_response)
```

### Create, update, delete AppSpace information
delete is not yet implemented in the IK platform

#### Create appspace 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def create_app_space(self, local, customer_id, app_space_name, display_name, description):
    client_config = ConfigClient(local)
    app_space_response = client_config.create_app_space(customer_id, app_space_name, display_name,description, [])
    print(app_space_response)
```

#### Update appspace 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def update_app_space(self, local, app_space_id, etag, display_name, description, bookmarks = []):
    #etag and bookmarks can be retrieved from a get_app_space or with a create_app_space or update_app_space
    client_config = ConfigClient(local)
    app_space_response = client_config.update_app_space(app_space_id, etag, display_name, description, bookmarks)
    print(app_space_response)
```

#### Delete appspace 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def delete_app_space(self, local, app_space_id, etag, bookmarks = []):
    #etag and bookmarks can be retrieved from a get_app_space or with a create_app_space or update_app_space
    client_config = ConfigClient(local)
    delete_app_space_response = client_config.delete_app_space(app_space_id, etag, bookmarks)
    print(delete_app_space_response)
```

### Get Tenant information

It is possible to get an existing Tenant's information from appSpace, TenantId and Tenant name.
A tenant is a grouping of Digital Twins (DT -> digital users) in an appSpace
#### Read tenant with id
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_tenant(self, local, tenant_id):
    client_config = ConfigClient(local)
    tenant = client_config.get_tenant_by_id(tenant_id)
    print(tenant)
```

#### Read tenant with name
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_app_space(self, local, app_space_id, tenant_name):
    client_config = ConfigClient(local)
    tenant = client_config.get_tenant_by_name(app_space_id, tenant_name)
    print(tenant)
```

#### List tenants 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_tenants(self, local, app_space_id, match_list, bookmarks=[]):
    #match_list is a nonempty list of tenants names
    client_config = ConfigClient(local)
    list_tenants_response = client_config.list_tenants(app_space_id, match_list, bookmarks)
    print(list_tenants_response)
```

### Create, update, delete Tenant information
delete is not yet implemented in the IK platform

#### Create tenant 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def create_tenant(self, local, issuer_id, tenant_name, display_name, description):
    client_config = ConfigClient(local)
    tenant_response = client_config.create_tenant(issuer_id, tenant_name, display_name, description, [])
    print(tenant_response)
```

#### Update tenant 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def update_tenant(self, local, tenant_id, etag, display_name, description, bookmarks = []):
    #etag and bookmarks can be retrieved from a get_tenant or with a create_tenant or update_tenant
    client_config = ConfigClient(local)
    tenant_response = client_config.update_tenant(tenant_id, etag, display_name,"description update", [])
    print(tenant_response)
```

#### Delete tenant 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def delete_tenant(self, local, tenant_id, etag, bookmarks = []):
    #etag and bookmarks can be retrieved from a get_tenant or with a create_tenant or update_tenant
    client_config = ConfigClient(local)
    delete_tenant_response = client_config.delete_tenant(tenant_id, etag, bookmarks)
    print(delete_tenant_response)
```

### Get Application information

It is possible to get an existing Application's information from appSpace, Application id and Application name.
An application is created in an appSpace
#### Read application with id
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_application(self, local, application_id):
    client_config = ConfigClient(local)
    application = client_config.get_application_by_id(application_id)
    print(application)
```

#### Read application with name
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_application(self, local, app_space_id, application_name):
    client_config = ConfigClient(local)
    application = client_config.get_application_by_name(app_space_id, application_name)
    print(application)
```

#### List applications 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_applications(self, local, app_space_id, match_list, bookmarks=[]):
    #match_list is a nonempty list of applications names
    client_config = ConfigClient(local)
    list_applications_response = client_config.list_applications(app_space_id, match_list, bookmarks)
    print(list_applications_response)
```

### Create, update, delete Application information
delete is not yet implemented in the IK platform

#### Create application 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def create_application(self, local, app_space_id, application_name, display_name, description):
    client_config = ConfigClient(local)
    application_response = client_config.create_application(app_space_id, application_name, display_name, description, [])
    print(application_response)
```

#### Update application 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def update_application(self, local, application_id, etag, display_name, description, bookmarks = []):
    #etag and bookmarks can be retrieved from a get_application or with a create_application or update_application
    client_config = ConfigClient(local)
    application_response = client_config.update_application(application_id, etag, display_name,description, bookmarks)
    print(application_response)
```

#### Delete application 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def delete_application(self, local, application_id, etag, bookmarks = []):
    #etag and bookmarks can be retrieved from a get_application or with a create_application or update_application
    client_config = ConfigClient(local)
    delete_application_response = client_config.delete_application(application_id, etag, bookmarks)
    print(delete_application_response)
```


### Get ApplicationAgent information

It is possible to get an existing ApplicationAgent's information from Application, ApplicationAgent id and ApplicationAgent name.
An applicationAgent is created for an Application
#### Read applicationAgent with id
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_application_agent(self, local, application_agent_id):
    client_config = ConfigClient(local)
    application_agent = client_config.get_application_agent_by_id(application_agent_id)
    print(application_agent)
```

#### Read applicationAgent with name
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_application_agent(self, local, app_space_id, application_agent_name):
    client_config = ConfigClient(local)
    application_agent = client_config.get_application_agent_by_name(app_space_id, application_agent_name)
    print(application_agent)
```

#### List applicationAgents 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_application_agents(self, local, app_space_id, match_list, bookmarks=[]):
    #match_list is a nonempty list of application agents names
    client_config = ConfigClient(local)
    list_application_agents_response = client_config.list_application_agents(app_space_id, match_list, bookmarks)
    print(list_application_agents_response)
```

### Create, update, delete ApplicationAgent information
delete is not yet implemented in the IK platform

#### Create applicationAgent 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def create_application_agent(self, local, application_id, application_agent_name, display_name, description):
    client_config = ConfigClient(local)
    application_agent_response = client_config.create_application_agent(application_id, application_agent_name, display_name,
                                                                description, [])
    print(application_agent_response)
```

#### Update applicationAgent 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def update_application_agent(self, local, application_agent_id, etag, display_name, description, bookmarks = []):
    #etag and bookmarks can be retrieved from a get_application_agent or with a create_application_agent or update_application_agent
    client_config = ConfigClient(local)
    application_agent_response = client_config.update_application_agent(application_agent_id, etag, display_name, description, bookmarks)
    print(application_agent_response)
```

#### Delete applicationAgent 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def delete_application_agent(self, local, application_agent_id, etag, bookmarks = []):
    #etag and bookmarks can be retrieved from a get_application_agent or with a create_application_agent or update_application_agent
    client_config = ConfigClient(local)
    delete_application_agent_response = client_config.delete_application_agent(application_agent_id, etag, bookmarks)
    print(delete_application_agent_response)
```

### Get ApplicationAgentCredential information

It is possible to get an existing ApplicationAgentCredential's information from ApplicationAgent and ApplicationAgentCredential id.
An applicationAgentCredential is created for an ApplicationAgent
#### Read applicationAgentCredential with id
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def get_application_agent_credential(self, local, application_agent_credential_id):
    client_config = ConfigClient(local)
    application_agent_credential = client_config.get_application_agent_credential(application_agent_credential_id)
    print(application_agent_credential)
```

### Create, delete ApplicationAgentCredential information
delete is not yet implemented in the IK platform

#### Register applicationAgentCredential with jwk
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def create_application_agent_credential(self, local, application_agent_id, display_name, jwk, expire_time_in_seconds, default_tenant_id):
    client_config = ConfigClient(local)
    application_agent_credential_response = client_config.register_application_agent_credential_jwk(application_agent_id,
                                                                                             display_name, jwk,
                                                                                             expire_time_in_seconds,
                                                                                             default_tenant_id, [])
    print(application_agent_credential_response)
```

#### Register applicationAgentCredential with pem
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def create_application_agent_credential(self, local, application_agent_id, display_name, pem, expire_time_in_seconds, default_tenant_id):
    client_config = ConfigClient(local)
    application_agent_credential_response = client_config.register_application_agent_credential_pem(application_agent_id,
                                                                                             display_name, pem,
                                                                                             expire_time_in_seconds,
                                                                                             default_tenant_id, [])
    print(application_agent_credential_response)
```


#### Delete applicationAgentCredential 
```python
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

def delete_application_agent_credential(self, local, application_agent_credential_id, bookmarks = []):
    #bookmarks can be retrieved from a get_application_agent_credential or with a create_application_agent 
    client_config = ConfigClient(local)
    delete_application_agent_credential_response = client_config.delete_application_agent_credential(application_agent_credential_id, bookmarks)
    print(delete_application_agent_credential_response)
```

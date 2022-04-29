# JARVIS Python SDK 🐍

This project serves as a Software Development Kit for developers of Indykite applications.

## Requirements

Python 3.8

## Used terminology

| Definition | Description |
| ---------- | ----------- |
| Digital Twin | A digital twin is the digital identity of a physical entity on/in a software/identity system |
| Application Space ID | ID of the application where the digital twin belongs to |
| Application Agent ID | ID of the agent which makes the application available for the different calls |
| Tenant ID | ID of the tenant where the digital twin belongs to. The tenant is belong to an application space |
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
  "baseUrl": "https://jarvis-dev.indykite.com",
  "applicationId": "696e6479-6b69-4465-8000-020100000002",
  "defaultTenantId": "696e6479-6b69-4465-8000-030100000002",
  "appAgentId": "696e6479-6b69-4465-8000-050100000002",
  "endpoint": "jarvis-dev.indykite.com",
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
   
2. You have two choices to set up the necessary credentials. You either pass the json to the `INDYKITE_APPLICATION_CREDENTIALS`
environment variable or set the `INDYKITE_APPLICATION_CREDENTIALS_FILE` environment variable to the configuration file's path.
   
   - on Linux and OSX
    `export INDYKITE_APPLICATION_CREDENTIALS='{"appSpaceId":"00000000-0000-4000-a000-000000000000","appAgentId":"00000000-0000-4000-a000-000000000001","endpoint": "application.indykite.com","privateKeyJWK":{"kty":"EC","d": "abcdef","use": "sig","crv": "P-256","kid":"efghij","x":"klmnop","y":"qrstvw","alg":"ES256"}}'`
     or
    `export INDYKITE_APPLICATION_CREDENTIALS_FILE=/Users/xx/configuration.json`
   - on Windows command line
    `setex INDYKITE_APPLICATION_CREDENTIALS='{"appSpaceId":"00000000-0000-4000-a000-000000000000","appAgentId":"00000000-0000-4000-a000-000000000001","endpoint": "application.indykite.com","privateKeyJWK":{"kty":"EC","d": "abcdef","use": "sig","crv": "P-256","kid":"efghij","x":"klmnop","y":"qrstvw","alg":"ES256"}}'`
     or
    `setex INDYKITE_APPLICATION_CREDENTIALS_FILE "C:\Users\xx\Documents\configuration.json"`
     
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
            'aud': credentials.get('app_space_id'),
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

Happy hacking!


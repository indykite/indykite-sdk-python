# IndyKite Proto SDK 🐍

This project serves as a Software Development Kit for developers of Indykite applications.
The Python SDK enables you to easily integrate the IndyKite platform gRPC APIs into your Python application. 

## Requirements

* Python 3.11

## Usage / Examples

The SDK methods are separated according the IndyKite platform service they call.

The [api.py](indykite_sdk/api.py) script gives an example for each function.

With the information given in the following credential files and eventually a user token, you can have access to every information you need through different methods to integrate the IK platform in your application.

## Mandatory environment variables

For normal usage `INDYKITE_APPLICATION_CREDENTIALS_FILE` should contain the path to the json configuration file for identity. 
The config file is generated in the [admin console](https://console.indykite.id/) when you create an application -> applicationAgent and applicationAgentCredential. 

`INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE` should contain the path to the json configuration file for config.
The config file is generated in the [admin console](https://console.indykite.id/) when you create a service account.

You should use absolute paths for the files.

# Running the sdk with the api.py script: examples for each function

With the [api.py](indykite_sdk/api.py) script you can simply run the sdk against the system you set up in the configuration 
files

## Connect to the client services

### Connect to Identity Client
Here is an example to open and close a connection to the Identity service with an arguments' parser used in the api.py script.
Each time you want to use an identity method, you need to set up an identity client

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
    ................

    client.channel.close()
```

### Connect to Config Client
Here is an example to open and close a connection to the Config service with an arguments' parser used in the api.py script.
The purpose of a service account is for a non person entity to manage the platform configuration: creating AppSpaces, creating applications, creating agent credentials, creating other service accounts, modify user permissions or any action through the **Graph DB**.
The service account is also needed if you want to use Terraform for your configuration.
Each time you want to use a config method, you need to set up a config client.

```python
from indykite_sdk.config import ConfigClient
import argparse

  # Create parent parser
  parser = argparse.ArgumentParser(description="Config client API.")
  parser.add_argument("-l", "--local", action="store_true", help="make the request to localhost")
  subparsers = parser.add_subparsers(dest="command", help="sub-command help")
  
  # Create 
  args = parser.parse_args()
  local = args.local
  client_config = ConfigClient(local)

 ....................
 
  client_config.channel.close()
```

### Connect to Authorization Client
Here is an example to open and close a connection to the Authorization service with an arguments' parser used in the api.py script.
The authorization service answers authorization requests about whether a subject is authorized to perform an action on a resource.
Each time you want to use an authorization method, you need to set up an authorization client.

```python
from indykite_sdk.authorization import AuthorizationClient
import argparse

  # Create parent parser
  parser = argparse.ArgumentParser(description="Config client API.")
  parser.add_argument("-l", "--local", action="store_true", help="make the request to localhost")
  subparsers = parser.add_subparsers(dest="command", help="sub-command help")
  
  # Create 
  args = parser.parse_args()
  local = args.local
  client_authorization = AuthorizationClient(local)

 ....................
 
  client_authorization.channel.close()
```

### To introspect a user token et get information about the user and the space environment, execute

```shell
python3 api.py introspect USER_TOKEN
```

```shell
positional arguments:
  user_token  JWT bearer token

optional arguments:
  -h, --help  show this help message and exit

```

2. To verify a digital twin email, execute

```shell
python3 api.py verify VERIFICATION_TOKEN
```

```shell
positional arguments:
  verification_token  Token from email to verify

optional arguments:
  -h, --help          show this help message and exit
```

3. Change password using the bearer token

    - The password should be in single quotation marks

```shell
python3 api.py change-password BEARER_TOKEN 'NEW_PASSWORD'
```

```shell
positional arguments:
  user_token    JWT bearer token
  new_password  New password for the user in '' (single quotation mark)

optional arguments:
  -h, --help    show this help message and exit
```

4. Change password using the bearer token and the user's digital twin ID

    - The digital twin ID should be in GID format
    - The password should be in single quotation marks

```shell
python3 api.py change-password-of-user BEARER_TOKEN DIGITAL_TWIN_ID 'NEW_PASSWORD'
```

```shell
positional arguments:
  user_token       JWT bearer token
  digital_twin_id  gid ID of the digital twin for password change
  new_password     New password for the user in '' (single quotation mark)

optional arguments:
  -h, --help       show this help message and exit
```

5. Get digital twin information
    - The digital twin ID should be in GID format
    - The tenant ID should be in GID format

```shell
python3 api.py get-dt DIGITAL_TWIN_ID TENANT_ID PROPERTY_NAMES ...
```

```shell
positional arguments:
  digital_twin_id  gid ID of the digital twin for password change
  tenant_id        gid ID of the tenant
  property_list    Array list of the required properties

optional arguments:
  -h, --help       show this help message and exit
```

example:
```shell
python3 api.py get-dt DT_GID_ID TENANT_GID_ID email mobile
```

6. Get digital twin information by token

```shell
python3 api.py get-dt-by-token BEARER_TOKEN PROPERTY_NAMES
```

```shell
positional arguments:
  user_token     JWT bearer token
  property_list  Array list of the required properties

optional arguments:
  -h, --help     show this help message and exit
```

example:
```shell
python3 api.py get-dt BEARER_TOKEN email mobile
```

7. Add/replace/remove properties by digital twin ID and tenant ID

You can add, replace and remove properties of a digital twin using the digital twin ID and token ID.

```shell
usage: python3 api.py patch-properties [-h] [--add ADD [ADD ...]] [--add_by_ref ADD_BY_REF [ADD_BY_REF ...]] [--replace REPLACE [REPLACE ...]] [--replace_by_ref REPLACE_BY_REF [REPLACE_BY_REF ...]] [--remove REMOVE [REMOVE ...]]
                               digital_twin_id tenant_id

positional arguments:
  digital_twin_id       GID ID of the digital twin for password change
  tenant_id             GID ID of the tenant

optional arguments:
  -h, --help            show this help message and exit
  --add ADD [ADD ...]   Name and value of the property to add (--add email x@x.x)
  --add_by_ref ADD_BY_REF [ADD_BY_REF ...]
                        Name and value of the property where the value is a reference
  --replace REPLACE [REPLACE ...]
                        Property ID and new value (--replace 111 a@a.a)
  --replace_by_ref REPLACE_BY_REF [REPLACE_BY_REF ...]
                        Property ID and value of the property where the value is a reference
  --remove REMOVE [REMOVE ...]
                        Remove the properties with the given ID

```

    - add: Requires a property name (currently the allowed names are: `email`, `mobile`, `nickname`, `givenname`,
            `familyname`, `extid`, `avatar`, `plan`) and the value to add
        example:
```shell
python3 api.py patch-properties DIGITAL_TWIN_ID TENANT_ID --add email xx@xx.xx
```
    - replace: Requires the property's ID and the new value
        example:
```shell
python3 api.py patch-properties DIGITAL_TWIN_ID TENANT_ID --replace 3838323232 xx@xx.xx
```
    - remove: Requires the property's ID to remove
        example:
```shell
python3 api.py patch-properties DIGITAL_TWIN_ID TENANT_ID --remove 3838323232
```

You can combine the subcommands, it will compile in the following order: add, replace, remove


8. Add/replace/remove properties by token

You can add, replace and remove properties of a digital twin using the token as a validation.

```shell
usage: python3 api.py patch-properties-by-token [-h] [--add ADD [ADD ...]] [--add_by_ref ADD_BY_REF [ADD_BY_REF ...]] [--replace REPLACE [REPLACE ...]] [--replace_by_ref REPLACE_BY_REF [REPLACE_BY_REF ...]] [--remove REMOVE [REMOVE ...]]
                                        user_token

positional arguments:
  user_token            JWT bearer token

optional arguments:
  -h, --help            show this help message and exit
  --add ADD [ADD ...]   Name and value of the property to add (--add email x@x.x)
  --add_by_ref ADD_BY_REF [ADD_BY_REF ...]
                        Name and value of the property where the value is a reference
  --replace REPLACE [REPLACE ...]
                        Property ID and new value (--replace 111 a@a.a)
  --replace_by_ref REPLACE_BY_REF [REPLACE_BY_REF ...]
                        Property ID and value of the property where the value is a reference
  --remove REMOVE [REMOVE ...]
                        Remove the properties with the given IDs
```

    - add: Requires a property name (currently the allowed names are: `email`, `mobile`, `nickname`, `givenname`,
            `familyname`, `extid`, `avatar`, `plan`) and the value to add
        example:
```shell
python3 api.py patch-properties-by-token TOKEN --add email xx@xx.xx
```
    - replace: Requires the property's ID and the new value
        example:
```shell
python3 api.py patch-properties-by-token TOKEN --replace 3838323232 xx@xx.xx
```
    - remove: Requires the property's ID to remove
        example:
```shell
python3 api.py patch-properties-by-token TOKEN --remove 3838323232
```

You can combine the subcommands, it will compile in the following order: add, replace, remove

9. Send verification email

Sends out a verification email for the specified digital twin to the given email

    - the digital twin should be in GID form
    - the tenant ID should be in GID form

```shell
usage: api.py start-dt-email-verification [-h] digital_twin tenant_id email

positional arguments:
  digital_twin  GID of the digital twin
  tenant_id     GID of the tenant
  email         email address to validate

optional arguments:
  -h, --help    show this help message and exit
```

10. Delete a user (admin delete)

Sends out a delete request for the specific digital twin

    - the digital twin should bi in GID form
    - the tenant ID should be in GID form

```shell
usage: api.py del-dt [-h] digital_twin_id tenant_id

positional arguments:
  digital_twin_id  GID ID of the digital twin for password change
  tenant_id        GID ID of the tenant

optional arguments:
  -h, --help       show this help message and exit
```

11. Delete the user (self service)

Sends out a delete request with the specified active token (login token).

```shell
usage: api.py del-dt-by-token [-h] user_token

positional arguments:
  user_token  JWT bearer token

optional arguments:
  -h, --help  show this help message and exit
```

12. Enrich token

Sends out a enrich token request with the specified active token (login token).

```shell
usage: api.py enrich-token [-h] user_token --token_claims key=value --session_claims key=value

positional arguments:
  user_token        JWT bearer token

optional arguments:
  --token_claims    token claims to be added
  --session_claims  session claims to be added
  -h, --help        show this help message and exit
```

13. Get the service account information (service account defined in the credential file)

```shell
python3 api.py service_account 
```

14. Get customer information by id

```shell
python3 api.py customer_id 
```

15. Get customer information by name

```shell
python3 api.py customer_name CUSTOMER_NAME
```

```shell
positional arguments:
  customer_name     String
```

16. Get AppSpace information by id

```shell
python3 api.py app_space_id APPSPACE_ID
```

```shell
positional arguments:
  app_space_id     String
```

17. Get AppSpace information by name

```shell
python3 api.py app_space_name APPSPACE_NAME CUSTOMER_ID
```

```shell
positional arguments:
  app_space_name     String
  customer_id        String
```

18. Create a new AppSpace in the customer space

```shell
python3 api.py create_app_space CUSTOMER_ID APPSPACE_NAME DISPLAY_NAME
```

```shell
positional arguments:
  customer_id        String
  app_space_name     String
  display_name       String
```

19. Update a given AppSpace 

```shell
python3 api.py update_app_space APPSPACE_ID ETAG DISPLAY_NAME
```

```shell
positional arguments:
  app_space_id   String
  etag           String
  display_name   String
```

20. List the AppSpaces in the customer matching a defined list

```shell
python3 api.py list_app_spaces CUSTOMER_ID MATCH_LIST 
```

```shell
positional arguments:
  customer_id   String
  match_list    Strings separated by ,
optional arguments:
  bookmarks     List of Strings
```

21. Delete a given AppSpace

```shell
python3 api.py delete_app_space APPSPACE_ID ETAG
```

```shell
positional arguments:
  app_space_id   String
optional arguments:
  etag          String
  bookmarks     List of Strings
```


22. Get Tenant information by id

```shell
python3 api.py tenant_id TENANT_ID
```

```shell
positional arguments:
  tenant_id     String
```

23. Get Tenant information by name

```shell
python3 api.py tenant_name TENANT_NAME APPSPACE_ID
```

```shell
positional arguments:
  tenant_name     String
  app_space_id    String
```

24. Create a new Tenant 

```shell
python3 api.py create_tenant ISSUER_ID TENANT_NAME DISPLAY_NAME 
```

```shell
positional arguments:
  issuer_id        String
  tenant_name     String
  display_name     String
```

25. Update a given Tenant 

```shell
python3 api.py update_tenant TENANT_ID ETAG DISPLAY_NAME
```

```shell
positional arguments:
  tenant_id      String
  etag           String
  display_name   String
```

26. List Tenants in a given AppSpace

```shell
python3 api.py list_tenants APPSPACE_ID MATCH_LIST 
```

```shell
positional arguments:
  app_space_id   String
  match_list     Strings separated by ,
optional arguments:
  bookmarks      List of Strings
```

27. Delete a given Tenant

```shell
python3 api.py delete_tenant TENANT_ID ETAG
```

```shell
positional arguments:
  tenant_id   String
optional arguments:
  etag          String
  bookmarks     List of Strings
```



28. Get Application information by id

```shell
python3 api.py application_id APPLICATION_ID
```

```shell
positional arguments:
  application_id     String
```

29. Get Application information by name

```shell
python3 api.py application_name APPLICATION_NAME APP_SPACE_ID
```

```shell
positional arguments:
  application_name     String
  app_space_id         String
```

30. Create a new Application 

```shell
python3 api.py create_application APP_SPACE_ID APPLICATION_NAME DISPLAY_NAME
```

```shell
positional arguments:
  app_space_id        String
  application_name    String
  display_name        String
```

31. Update a given Application 

```shell
python3 api.py update_application APPLICATION_ID ETAG DISPLAY_NAME
```

```shell
positional arguments:
  application_id   String
  etag           String
  display_name   String
```

32. List Applications in an AppSpace matching a list

```shell
python3 api.py list_applications APP_SPACE_ID MATCH_LIST 
```

```shell
positional arguments:
  app_space_id  String
  match_list    Strings separated by ,
optional arguments:
  bookmarks     List of Strings
```

33. Delete a given Application

```shell
python3 api.py delete_application APPLICATION_ID ETAG
```

```shell
positional arguments:
  application_id   String
optional arguments:
  etag          String
  bookmarks     List of String
```


34. Get ApplicationAgent information by id

```shell
python3 api.py application_agent_id APPLICATION_AGENT_ID
```

```shell
positional arguments:
  application_agent_id     String
```

35. Get ApplicationAgent information by name

```shell
python3 api.py application_agent_name APPLICATION_AGENT_NAME APP_SPACE_ID
```

```shell
positional arguments:
  application_agent_name     String
  app_space_id         String
```

36. Create a new ApplicationAgent 

```shell
python3 api.py create_application_agent APPLICATION_ID APPLICATION_AGENT_NAME DISPLAY_NAME
```

```shell
positional arguments:
  application_id        String
  application_agent_name    String
  display_name        String
```

37. Update a given ApplicationAgent 

```shell
python3 api.py update_application_agent APPLICATION_AGENT_ID ETAG DISPLAY_NAME
```

```shell
positional arguments:
  application_agent_id   String
  etag           String
  display_name   String
```

38. List ApplicationAgents of an AppSpace matching a list

```shell
python3 api.py list_application_agents APP_SPACE_ID MATCH_LIST 
```

```shell
positional arguments:
  app_space_id  String
  match_list    Strings separated by ,
optional arguments:
  bookmarks     List of Strings
```

39. Delete a given ApplicationAgent

```shell
python3 api.py delete_application_agent APPLICATION_AGENT_ID ETAG
```

```shell
positional arguments:
  application_agent_id   String
optional arguments:
  etag          String
  bookmarks     List of String
```

40. Get ApplicationAgentCredential information by id

```shell
python3 api.py application_agent_credential APPLICATION_AGENT_CREDENTIAL_ID
```

```shell
positional arguments:
  application_agent_credential_id     String
```

41. Register new ApplicationAgentCredential with jwk 

```shell
python3 api.py register_application_agent_credential_jwk APPLICATION_AGENT_ID DISPLAY_NAME DEFAULT_TENANT_ID
```

```shell
positional arguments:
 application_agent_id     String
 display_name             String
 jwk                      Bytes
 expire_time_in_seconds   Int
 default_tenant_id        String
 optional arguments:
  bookmarks               List of String 
```

42. Register new ApplicationAgentCredential with pem 

```shell
python3 api.py register_application_agent_credential_pem APPLICATION_AGENT_ID DISPLAY_NAME DEFAULT_TENANT_ID
```

```shell
positional arguments:
 application_agent_id     String
 display_name             String
 pem                      Bytes
 expire_time_in_seconds   Int
 default_tenant_id        String
 optional arguments:
  bookmarks               List of String 
```

43. Delete a given ApplicationAgentCredential

```shell
python3 api.py delete_application_agent_credential APPLICATION_AGENT_CREDENTIAL_ID
```

```shell
positional arguments:
  application_agent_credential_id   String
optional arguments:
  bookmarks     List of String
```

44. Get Service Account information by ID

```shell
python3 api.py service_account_id SERVICE_ACCOUNT_ID
```

```shell
positional arguments:
  service_account_id   String
```

45. Get Service Account information by Name 

```shell
python3 api.py service_account_name CUSTOMER_ID SERVICE_ACCOUNT_NAME
```

```shell
positional arguments:
  customer_id   String
  service_account_name String
```

46. Create a new Service Account

```shell
python3 api.py create_service_account CUSTOMER_ID SERVICE_ACCOUNT_NAME DISPLAY_NAME ROLE
```

```shell
positional arguments:
  customer_id = String
  service_account_name = String
  display_name = String
  role = String
optional arguments:
  bookmarks     List of String
```

47. Update a given Service Account 

```shell
python3 api.py update_service_account SERVICE_ACCOUNT_ID ETAG DISPLAY_NAME
```

```shell
positional arguments:
   service_account_id = String
   etag = String
  display_name = String
optional arguments:
  bookmarks     List of String
```

48. Delete a given Service Account

```shell
python3 api.py delete_service_account SERVICE_ACCOUNT_ID ETAG
```

```shell
positional arguments:
  service_account_id = String
   etag = String
optional arguments:
  bookmarks     List of String
```

49. Get Service Account Credentials

```shell
python3 api.py service_account_credential SERVICE_ACCOUNT_CREDENTIAL_ID
```

```shell
positional arguments:
  service_account_credential_id   String
```

50. Register new Service Account Credentials with JWK 
If no JWK is provided, one will be created automatically (to be used only in dev environments)

```shell
python3 api.py register_service_account_credential_jwk SERVICE_ACCOUNT_ID DISPLAY_NAME
```

```shell
positional arguments:
  service_account_id = String
  display_name = String
optional arguments:
  bookmarks     List of String
```

51. Register new Service Account Credentials with pem
If no pem is provided, one will be created automatically (to be used only in dev environments)

```shell
python3 api.py register_service_account_credential_pem SERVICE_ACCOUNT_ID DISPLAY_NAME
```

```shell
positional arguments:
  service_account_id = String
  display_name = String
optional arguments:
  bookmarks     List of String
```

52.  Delete given Service Account Credentials

```shell
python3 api.py delete_service_account_credential SERVICE_ACCOUNT_CREDENTIAL_ID
```

```shell
positional arguments:
  service_account_credential_id   String
optional arguments:
  bookmarks     List of String
```

53. Create new Email Service Config Node (for example a SendGrid)

```shell
python3 api.py create_email_service_config_node CUSTOMER_ID NAME DISPLAY_NAME DESCRIPTION 
```

```shell
positional arguments:
  location = String
  name = String
  display_name = String
optional arguments:
  description = String
  bookmarks     List of String
```

54. Read any Config Node from its id (email service, authflow, ingest mapping...)

```shell
python3 api.py read_config_node CONFIG_NODE_ID
```

```shell
positional arguments:
  config_node_id   String
optional arguments:
  bookmarks     List of String
```

55. Update a given Email Service Config Node

```shell
python3 api.py update_email_service_config_node CONFIG_NODE_ID ETAG DISPLAY_NAME DESCRIPTION 
```

```shell
positional arguments:
  config_node_id = String
  etag = String
  display_name = String
        
optional arguments:
  description = String
  bookmarks     List of String
```

56. Delete any Config Node from its id and etag

```shell
python3 api.py delete_config_node CONFIG_NODE_ID ETAG
```

```shell
positional arguments:
  config_node_id   String
  etag = String
optional arguments:
  bookmarks     List of String
```

57. Create a new AuthFlow (authentication flow)

```shell
python3 api.py create_auth_flow_config_node APP_SPACE_ID NAME DISPLAY_NAME DESCRIPTION
```

```shell
positional arguments:
  location = String
  name = String
  display_name = String
optional arguments:
  description = String
  bookmarks     List of String
```

58. Update a given AuthFlow 

```shell
python3 api.py update_auth_flow_config_node CONFIG_NODE_ID ETAG DISPLAY_NAME DESCRIPTION
```

```shell
positional arguments:
  config_node_id = String
  etag = String
  display_name = String
        
optional arguments:
  description = String
  bookmarks     List of String
```

59. Create a new OAuth2 Client 

```shell
python3 api.py create_oauth2_client_config_node APP_SPACE_ID NAME DISPLAY_NAME DESCRIPTION
```

```shell
positional arguments:
  location = String
  name = String
  display_name = String
optional arguments:
  description = String
  bookmarks     List of String
```

60. Update a given OAuth2 Client

```shell
python3 api.py update_oauth2_client_config_node CONFIG_NODE_ID ETAG DISPLAY_NAME DESCRIPTION
```

```shell
positional arguments:
  config_node_id = String
  etag = String
  display_name = String
        
optional arguments:
  description = String
  bookmarks     List of String
```

61. Create a new Ingest Mapping (ingestion of application or external data into the IK platform)

```shell
python3 api.py create_ingest_mapping_config_node APP_SPACE_ID NAME DISPLAY_NAME DESCRIPTION
```

```shell
positional arguments:
  location = String
  name = String
  display_name = String
optional arguments:
  description = String
  bookmarks     List of String
```

62. Update a given Ingest Mapping

```shell
python3 api.py update_ingest_mapping_config_node CONFIG_NODE_ID ETAG DISPLAY_NAME DESCRIPTION
```

```shell
positional arguments:
  config_node_id = String
  etag = String
  display_name = String
        
optional arguments:
  description = String
  bookmarks     List of String
```

63. Read a given OAuth2 Provider

```shell
python3 api.py read_oauth2_provider OAUTH2_PROVIDER_ID
```

```shell
positional arguments:
  oauth2_provider_id   String
optional arguments:
  bookmarks     List of String
```

64. Create a new OAuth2 Provider
See documentation [here](https://docs.indykite.com/docs/quick-starts/using-admin-console#oauth-2)

```shell
python3 api.py create_oauth2_provider APP_SPACE_ID NAME DISPLAY_NAME DESCRIPTION
```

```shell
positional arguments:
  app_space_id = String
  name = String
  display_name = String   
optional arguments:
  description = String
  bookmarks     List of String
```

65. Update a given OAuth2 Provider

```shell
python3 api.py update_oauth2_provider OAUTH2_PROVIDER_ID ETAG DISPLAY_NAME DESCRIPTION
```

```shell
positional arguments:
  oauth2_provider_id = String
  etag = String
  display_name = String
optional arguments:
  description = String
  bookmarks     List of String
```

66. Delete a given OAuth2 Provider

```shell
python3 api.py delete_oauth2_provider OAUTH2_PROVIDER_ID ETAG
```

```shell
positional arguments:
  oauth2_provider_id = String
  etag = String
optional arguments:
  bookmarks     List of String
```

67. Read a given OAuth2 Application

```shell
python3 api.py read_oauth2_application OAUTH2_APPLICATION_ID
```

```shell
positional arguments:
  oauth2_application_id   String
optional arguments:
  bookmarks     List of String
```

68. Create a new OAuth2 Application
See documentation [here](https://docs.indykite.com/docs/quick-starts/using-admin-console#application)

```shell
python3 api.py create_oauth2_application OAUTH2_PROVIDER_ID NAME DISPLAY_NAME DESCRIPTION
```

```shell
positional arguments:
  oauth2_provider_id = String
  name = String
  display_name = String
        
optional arguments:
  description = String
  bookmarks     List of String
```

69. Update a given OAuth2 Application

```shell
python3 api.py update_oauth2_application OAUTH2_APPLICATION_ID ETAG DISPLAY_NAME DESCRIPTION
```

```shell
positional arguments:
  oauth2_application_id = String
  etag = String
  display_name = String
optional arguments:
  description = String
  bookmarks     List of String
```

70. Delete a given OAuth2 Application

```shell
python3 api.py delete_oauth2_application OAUTH2_APPLICATION_ID ETAG
```

```shell
positional arguments:
  oauth2_application_id = String
  etag = String
optional arguments:
  bookmarks     List of String
```

71. Import Digital Twins

```shell
python3 api.py import_digital_twins TENANT_ID
```

```shell
positional arguments:
  tenant_id   String
```

72. Import Digital Twins with password hash

```shell
python3 api.py import_digital_twins_hash TENANT_ID
```

```shell
positional arguments:
  tenant_id   String
```

73. Import Digital Twins with hash algorithm

```shell
python3 api.py import_digital_twins_hash256 TENANT_ID
```

```shell
positional arguments:
  tenant_id   String
```

74. Update Imported Digital Twins

```shell
python3 api.py import_digital_twins_update DIGITAL_TWIN_ID TENANT_ID
```

```shell
positional arguments:
 id String
 tenant_id String
```

75. Is Digital Twin identified by id Authorized to perform an Action on a Resource

```shell
python3 api.py is_authorized_dt DIGITAL_TWIN_ID TENANT_ID
```

```shell
positional arguments:
  digital_twin_id String
  tenant_id String
```

76. Is Digital Twin identified by token Authorized to perform an Action on a Resource

```shell
python3 api.py is_authorized_token ACCESS_TOKEN
```

```shell
positional arguments:
  access_token   User Token
```

77. Is Digital Twin identified by property Authorized to perform an Action on a Resource

```shell
python3 api.py is_authorized_property PROPERTY_TYPE PROPERTY_VALUE
```

```shell
positional arguments:
  property_type  String #e.g "email"
  property_value String #e.g test@example.com
```

78. What actions are authorized to be performed on a Resource by a subject identified by id

```shell
python3 api.py what_authorized_dt DIGITAL_TWIN_ID TENANT_ID
```

```shell
positional arguments:
  digital_twin_id String
  tenant_id String
```

79. What actions are authorized to be performed on a Resource by a subject identified by token

```shell
python3 api.py what_authorized_token ACCESS_TOKEN
```

```shell
positional arguments:
  access_token   User Token
```

80.  What actions are authorized to be performed on a Resource by a subject identified by properties

```shell
python3 api.py what_authorized_property PROPERTY_TYPE PROPERTY_VALUE
```

```shell
positional arguments:
  property_type  String #e.g "email"
  property_value String #e.g test@example.com
```

81. Create Consent for OAuth2 application for a given Digital Twin

```shell
python3 api.py create_consent PII_PROCESSOR_ID PII_PRINCIPAL_ID
```

```shell
positional arguments:
  pii_processor_id = String ID of OAuth2 Application
  pii_principal_id = String DigitalTwin Id (gid)

```

82.  List Consents for Digital Twin for OAuth2 application

```shell
python3 api.py list_consents PII_PRINCIPAL_ID
```

```shell
positional arguments:
  pii_principal_id   String
```

83. Revoke Consents for Digital Twin for OAuth2 application

```shell
python3 api.py revoke_consent PII_PRINCIPAL_ID CONSENT_IDS
```

```shell
positional arguments:
  pii_principal_id   String
  consent_ids List of consent ids separated by space
```

84. Check OAuth2 Consent challenge

```shell
python3 api.py check_oauth2_consent_challenge CHALLENGE
```

```shell
positional arguments:
  challenge   String
```

85. Create OAuth2 Consent Verifier with Approval

```shell
python3 api.py create_oauth2_consent_verifier_approval CONSENT_CHALLENGE GRANT_SCOPES GRANTED_AUDIENCE
```

```shell
positional arguments:
  consent_challenge String
  grant_scopes List 
  granted_audiences List
  access_token Dict
  id_token Dict
  userinfo Dict
  remember bool
  remember_for int
```

86. Create OAuth2 Consent Verifier with Denial

```shell
python3 api.py create_oauth2_consent_verifier_denial CONSENT_CHALLENGE
```

```shell
positional arguments:
  consent_challenge String
  error String 
  error_description String
  error_hint String
  status_code int
```

87.  Start forgotten password flow

```shell
python3 api.py start_forgotten_password DIGITAL_TWIN_ID TENANT_ID
```

88.  Create email invitation (invite a user)

```shell
python3 api.py create_email_invitation TENANT_ID EMAIL
```

```shell
positional arguments:
  tenant_id   String
  email   String
```

89. Check invitation state : check if invitation invalid, in future, pending, accepted, expired, cancelled, processing

```shell
python3 api.py check_invitation_state REFERENCE_ID
```

```shell
positional arguments: one of:
  reference_id   id used to create the invitation
  invitation_token  token used in the invitation email
```

90. Resend an invitation

```shell
python3 api.py resend_invitation REFERENCE_ID
```

```shell
positional arguments:
  reference_id   id used to create the invitation
```

91. Cancel an invitation

```shell
python3 api.py cancel_invitation REFERENCE_ID
```

```shell
positional arguments:
  reference_id   id used to create the invitation
```

92. Register a DigitalTwin without credential

```shell
python3 api.py register_digital_twin_without_credential TENANT_ID
```

```shell
positional arguments:
  tenant_id   id of the tenant you want to create the DT into
```

----------------
To see all available options, run

```shell
python3 api.py --help
```

To see the subcommands help page, run

```shell
python3 api.py <sub_command> --help
```

To execute the functions against the local instance, add the `-l` flag to the command:

```shell
python api.py -l introspect USER_TOKEN
```

## Development

To develop this project locally:

* Make sure you have `pipenv and protobuf` installed on your system

* Clone this repository and enter it

      git clone https://github.com/indykite/indykite-sdk-python.git
      cd indykite-sdk-python

* Create a virtual environment and install project dependencies

      pipenv install --dev
      install python 3.11 in your virtual environment

* Install protos
  `./gen_proto.sh`
  
## Testing

In tests, `pytest test_...` 

Happy hacking!


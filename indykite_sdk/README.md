# IndyKite Proto SDK 🐍

This project serves as a Software Development Kit for developers of Indykite applications.

## Requirements

The api.py script runs on python3.8

## Usage

### Mandatory environment variables

For normal usage `INDYKITE_APPLICATION_CREDENTIALS_FILE` should contain the path to the json configuration file for identity. 
The config file is generated in the [admin console](https://console.indykite.id/) when you create an application -> applicationAgent and applicationAgentCredential. 

`INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE` should contain the path to the json configuration file for config.
The config file is generated in the [admin console](https://console.indykite.id/) when you create a service account.

You should use absolute paths for the files.

### Running the sdk with the api.py script

With the [api.py](indykite_sdk/api.py) script you can simply run the sdk against the system you set up in the config
file

1. To introspect a user token, execute

```shell
python3 api.py introspect USER_TOKEN
```

```shell
usage: api.py introspect [-h] user_token

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
usage: api.py verify [-h] verification_token

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
usage: api.py change-password [-h] user_token new_password

positional arguments:
  user_token    JWT bearer token
  new_password  New password for the user in '' (single quotation mark)

optional arguments:
  -h, --help    show this help message and exit
```

4. Change password using the bearer token and the user's digital twin ID

    - The digital twin ID should be in UUID4 format
    - The password should be in single quotation marks

```shell
python3 api.py change-password-of-user BEARER_TOKEN DIGITAL_TWIN_ID 'NEW_PASSWORD'
```

```shell
usage: api.py change-password-of-user [-h] user_token digital_twin_id new_password

positional arguments:
  user_token       JWT bearer token
  digital_twin_id  UUID4 ID of the digital twin for password change
  new_password     New password for the user in '' (single quotation mark)

optional arguments:
  -h, --help       show this help message and exit
```

5. Get digital twin information
    - The digital twin ID should be in UUID4 format
    - The tenant ID should be in UUID4 format

```shell
python3 api.py get-dt DIGITAL_TWIN_ID TENANT_ID property_list PROPERTY_NAMES
```

```shell
usage: api.py get-dt [-h] digital_twin_id tenant_id property_list [property_list ...]

positional arguments:
  digital_twin_id  UUID4 ID of the digital twin for password change
  tenant_id        UUID4 ID of the tenant
  property_list    Array list of the required properties

optional arguments:
  -h, --help       show this help message and exit
```

example:
```shell
python3 api.py get-dt DT_UUID4 TENANT_UUID4 property_list email mobile
```

6. Get digital twin information by token

```shell
python3 api.py get-dt-by-token BEARER_TOKEN property_list PROPERTY_NAMES
```

```shell
usage: api.py get-dt-by-token [-h] user_token property_list [property_list ...]

positional arguments:
  user_token     JWT bearer token
  property_list  Array list of the required properties

optional arguments:
  -h, --help     show this help message and exit
```

7. Add/replace/remove properties by digital twin ID and tenant ID

You can add, replace and remove properties of a digital twin using the digital twin ID and token ID.

```shell
usage: api.py patch-properties [-h] [--add ADD [ADD ...]] [--add_by_ref ADD_BY_REF [ADD_BY_REF ...]] [--replace REPLACE [REPLACE ...]] [--replace_by_ref REPLACE_BY_REF [REPLACE_BY_REF ...]] [--remove REMOVE [REMOVE ...]]
                               digital_twin_id tenant_id

positional arguments:
  digital_twin_id       UUID4 ID of the digital twin for password change
  tenant_id             UUID4 ID of the tenant

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
usage: api.py patch-properties-by-token [-h] [--add ADD [ADD ...]] [--add_by_ref ADD_BY_REF [ADD_BY_REF ...]] [--replace REPLACE [REPLACE ...]] [--replace_by_ref REPLACE_BY_REF [REPLACE_BY_REF ...]] [--remove REMOVE [REMOVE ...]]
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

    - the digital twin should be in UUID4 form
    - the tenant ID should be in UUID4 form

```shell
usage: api.py start-dt-email-verification [-h] digital_twin tenant_id email

positional arguments:
  digital_twin  UUID4 of the digital twin
  tenant_id     UUID4 of the tenant
  email         email address to validate

optional arguments:
  -h, --help    show this help message and exit
```

10. Delete a user (admin delete)

Sends out a delete request for the specific digital twin

    - the digital twin should bi in UUID4 form
    - the tenant ID should be in UUID4 form

```shell
usage: api.py del-dt [-h] digital_twin_id tenant_id

positional arguments:
  digital_twin_id  UUID4 ID of the digital twin for password change
  tenant_id        UUID4 ID of the tenant

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

13. Get service account

```shell
python3 api.py service_account 
```

14. Get customer by id

```shell
python3 api.py customer_id 
```

15. Get customer by name

```shell
python3 api.py customer_name CUSTOMER_NAME
```

```shell
positional arguments:
  customer_name     String
```

16. Get AppSpace by id

```shell
python3 api.py app_space_id APPSPACE_ID
```

```shell
positional arguments:
  app_space_id     String
```

17. Get AppSpace by name

```shell
python3 api.py app_space_name APPSPACE_NAME CUSTOMER_ID
```

```shell
positional arguments:
  app_space_name     String
  customer_id        String
```

18. Create AppSpace 

```shell
python3 api.py create_app_space CUSTOMER_ID APPSPACE_NAME DISPLAY_NAME
```

```shell
positional arguments:
  customer_id        String
  app_space_name     String
  display_name       String
```

19. Update AppSpace 

```shell
python3 api.py update_app_space APPSPACE_ID ETAG DISPLAY_NAME
```

```shell
positional arguments:
  app_space_id   String
  etag           String
  display_name   String
```

20. List AppSpaces 

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

21. Delete AppSpace

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


22. Get Tenant by id

```shell
python3 api.py tenant_id TENANT_ID
```

```shell
positional arguments:
  tenant_id     String
```

23. Get Tenant by name

```shell
python3 api.py tenant_name TENANT_NAME APPSPACE_ID
```

```shell
positional arguments:
  tenant_name     String
  app_space_id    String
```

24. Create Tenant 

```shell
python3 api.py create_tenant ISSUER_ID TENANT_NAME DISPLAY_NAME 
```

```shell
positional arguments:
  issuer_id        String
  tenant_name     String
  display_name     String
```

25. Update Tenant 

```shell
python3 api.py update_tenant TENANT_ID ETAG DISPLAY_NAME
```

```shell
positional arguments:
  tenant_id      String
  etag           String
  display_name   String
```

26. List Tenants 

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

27. Delete Tenant

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



28. Get Application by id

```shell
python3 api.py application_id APPLICATION_ID
```

```shell
positional arguments:
  application_id     String
```

29. Get Application by name

```shell
python3 api.py application_name APPLICATION_NAME APP_SPACE_ID
```

```shell
positional arguments:
  application_name     String
  app_space_id         String
```

30. Create Application 

```shell
python3 api.py create_application APP_SPACE_ID APPLICATION_NAME DISPLAY_NAME
```

```shell
positional arguments:
  app_space_id        String
  application_name    String
  display_name        String
```

31. Update Application 

```shell
python3 api.py update_application APPLICATION_ID ETAG DISPLAY_NAME
```

```shell
positional arguments:
  application_id   String
  etag           String
  display_name   String
```

32. List Applications 

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

33. Delete Application

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


34. Get ApplicationAgent by id

```shell
python3 api.py application_agent_id APPLICATION_AGENT_ID
```

```shell
positional arguments:
  application_agent_id     String
```

35. Get ApplicationAgent by name

```shell
python3 api.py application_agent_name APPLICATION_AGENT_NAME APP_SPACE_ID
```

```shell
positional arguments:
  application_agent_name     String
  app_space_id         String
```

36. Create ApplicationAgent 

```shell
python3 api.py create_application_agent APPLICATION_ID APPLICATION_AGENT_NAME DISPLAY_NAME
```

```shell
positional arguments:
  application_id        String
  application_agent_name    String
  display_name        String
```

37. Update ApplicationAgent 

```shell
python3 api.py update_application_agent APPLICATION_AGENT_ID ETAG DISPLAY_NAME
```

```shell
positional arguments:
  application_agent_id   String
  etag           String
  display_name   String
```

38. List ApplicationAgents 

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

39. Delete ApplicationAgent

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

40. Get ApplicationAgentCredential by id

```shell
python3 api.py application_agent_credential APPLICATION_AGENT_CREDENTIAL_ID
```

```shell
positional arguments:
  application_agent_credential_id     String
```

41. Register ApplicationAgentCredential with jwk 

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

42. Register ApplicationAgentCredential with pem 

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

43. Delete ApplicationAgentCredential

```shell
python3 api.py delete_application_agent_credential APPLICATION_AGENT_CREDENTIAL_ID
```

```shell
positional arguments:
  application_agent_credential_id   String
optional arguments:
  bookmarks     List of String
```

44. To see all available options, run

```shell
python3 api.py --help
```

```shell
usage: api.py [-h] [-l]
              {introspect,verify,change-password,change-password-of-user,get-dt,get-dt-by-token,patch-properties,patch-properties-by-token,start-dt-email-verification}
              ...

Identity client API.

positional arguments:
  {introspect,verify,change-password,change-password-of-user,get-dt,get-dt-by-token,patch-properties,patch-properties-by-token,start-dt-email-verification}
                        sub-command help

optional arguments:
  -h, --help            show this help message and exit
  -l, --local           make the request to localhost
```

45. To see the subcommands help page, run

```shell
python3 api.py <sub_command> --help
```

46. To execute the functions against the local instance, add the `-l` flag to the command:

```shell
python api.py -l introspect USER_TOKEN
```

## Development

To develop this project locally:

* Make sure you have `pipenv` installed on your system

* Clone this repository and enter it

      git clone https://github.com/indykite/indykite-sdk-python.git
      cd indykite-sdk-python

* Create a virtual environment and install project dependencies

      pipenv install --dev

### Generate Python Library

```
python3 -m grpc_tools.protoc \
 --plugin=protoc-gen-grpc=../../ptypes/grpc_php_plugin \
 -I.  -I ../../ptypes/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
 -I ../../ptypes/github.com/googleapis/googleapis/ \
 -I ../../ptypes/github.com/envoyproxy/protoc-gen-validate/ \
 -I ../../ptypes/github.com/grpc-ecosystem/grpc-gateway \
 --python_out=../indykite_sdk \
 validate/validate.proto \
 identity/v1/identity_management_api.proto \
 identity/v1/model.proto \
 identity/v1/attributes.proto \
 identity/v1/authenteq.proto \
 identity/v1/document.proto \
 identity/v1/import.proto \
 objects/struct.proto \
 objects/id.proto

 python3 -m grpc_tools.protoc \
 --plugin=protoc-gen-grpc=../../ptypes/grpc_php_plugin \
 -I.  -I ../../ptypes/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
 -I ../../ptypes/github.com/googleapis/googleapis/ \
 -I ../../ptypes/github.com/envoyproxy/protoc-gen-validate/ \
 -I ../../ptypes/github.com/grpc-ecosystem/grpc-gateway \
 --grpc_python_out=../indykite_sdk \
 identity/v1/identity_management_api.proto
```

## Testing

Use the `python3 -m venv pytest-env` virtual environment and source it with `source pytest-env/bin/activate`

Happy hacking!


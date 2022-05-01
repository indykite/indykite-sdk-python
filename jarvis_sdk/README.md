# JARVIS Proto SDK 🐍

This project serves as a Software Development Kit for developers of Indykite applications.

## Requirements

The api.py script runs on python3.8

## Usage

### Mandatory environment variables

For normal usage `INDYKITE_APPLICATION_CREDENTIALS_FILE` should contain the path to the json configuration file. You can find an example .json
in the [example_config.json](jarvis-proto-sdk/config_example.json) file.

If you run the package against a local system, then it requires an additional ca.pem file. To set the file's path,
please use the `CAPEM` variable point to the `ca.pem` file.

It is highly suggested that you use absolute paths for the files

### Running the sdk with the api.py script

With the [api.py](jarvis-proto-sdk/api.py) script you can simply run the sdk against the system you set up in the config
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

13. To see all available options, run
    
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
   
14. To see the subcommands help page, run
   
```shell
python3 api.py <sub_command> --help 
```
   
15. To execute the functions against the local instance, add the `-l` flag to the command:

```shell
python api.py -l introspect USER_TOKEN
```

## Development

To develop this project locally:

* Make sure you have `pipenv` installed on your system
  
* Clone this repository and enter it
  
      git clone https://github.com/indykite/jarvis-sdk-python-proto.git
      cd jarvis-sdk-python-proto

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
 --python_out=../jarvis_sdk \
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
 --grpc_python_out=../jarvis_sdk \
 identity/v1/identity_management_api.proto
```

## Testing

Use the `python3 -m venv pytest-env` virtual environment and source it with `source pytest-env/bin/activate`

Happy hacking!


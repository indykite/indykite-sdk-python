# IndyKite Proto SDK 🐍

This project serves as a Software Development Kit for developers of Indykite applications.
The Python SDK enables you to easily integrate the IndyKite platform gRPC APIs into your Python application. 

## Requirements

* Python >=3.13
* Organization (customer)created in the hub (see [README](https://github.com/indykite/indykite-sdk-python/blob/master/README.md))
* Service account credentials created in the hub (see [README](https://github.com/indykite/indykite-sdk-python/blob/master/README.md))
* INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE or INDYKITE_SERVICE_ACCOUNT_CREDENTIALS as env variable (see [README](https://github.com/indykite/indykite-sdk-python/blob/master/README.md))

## Usage / Examples

The SDK methods are separated according the IndyKite platform service they call.


With the information given in the following credential files and eventually a user token, you can have access to every information you need through different methods to integrate the IK platform in your application.


The following scripts from the usage folder give an example for each function.
- Configuration service spaces [configuration_spaces.py](usage/configuration_spaces.py)
- Configuration service config nodes [configuration_config_nodes.py](usage/configuration_config_nodes.py)
- Ingest service [ingest.py](usage/ingest.py)
- Knowledge service [knowledge.py](usage/knowledge.py)
- Authorization service [authorization.py](usage/authorization.py)

## Running the sdk with the scripts in the "usage" folder: examples for each function

With the scripts you can simply run the sdk against the system you set up in the configuration 
files

## Connect to the services

### Connect to the Config service

The purpose of a service account is for a non-person entity to manage the platform configuration: creating AppSpaces, creating applications, creating agent credentials, creating other service accounts, modify user permissions or any action through the **Graph DB**.

The service account is also needed if you want to use Terraform for your configuration.

Each time you want to use a config method, you need to set up a config client.

**Example:**

Here is a very simple example to open and close a connection to the Config service with an arguments' parser used in the configuration_spaces.py script.

```python
from indykite_sdk.config import ConfigClient
import argparse

    # Create parent parser
    parser = argparse.ArgumentParser(description="Config client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")
  
    # create command customer_name and argument for the command
    customer_name_parser = subparsers.add_parser("customer_name")
    customer_name_parser.add_argument("customer_name", help="Customer name (not display name)")
  
    # call arguments
    args = parser.parse_args()
  
    # call method
    if command == "customer_name":
        # read_customer_by_name method: to get customer info from customer name
        client_config = ConfigClient()
        customer_name = args.customer_name
        customer = client_config.read_customer_by_name(customer_name)
        client_config.channel.close()
        if customer:
            api_helper.print_response(customer)
        else:
            print("Invalid customer id")
            

```
To call one command in the **usage** directory, check the **command** and the corresponding **arguments** in the list then execute in command line:
```shell
python3 configuration_spaces.py COMMAND arg1 arg2 ...
```    


### Connect to the Authorization service
To be able to connect to the authorization service, you need to have AppAgent credentials generated from the Config service with the service account credentials or in the Hub (https://console.indykite.id/)

Once you have obtained your credentials, you have two choices to set up the necessary credentials. You either pass the json with the credentials to the `INDYKITE_APPLICATION_CREDENTIALS`
environment variable or set the `INDYKITE_APPLICATION_CREDENTIALS_FILE` environment variable to the configuration file's path.

The Authorization service provides functions to send authorization requests and get answers.

Each time you want to use an authorization method, you need to set up an authorization client.

**Example:**

Here is a very simple example to open and close a connection to the Authorization service with an arguments' parser used in the authorization.py script.

```python
from indykite_sdk.authorization import AuthorizationClient
import argparse

    # Create parent parser
    parser = argparse.ArgumentParser(description="Authorization client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
     # is_authorized_identity_node
    is_authorized_identity_node_parser = subparsers.add_parser("is_authorized_identity_node")
    is_authorized_identity_node_parser.add_argument("identity_node_id", help="Identity node gid (node with is_identity equal True)")
  
    # call arguments
    args = parser.parse_args()
    command = args.command
    
    # call method
    if command == "is_authorized_identity_node":
        # is a given subject, identified by its gid, authorized to have a specific action on specific resources
        # replace actions and resources according to your data
        client_authorization = AuthorizationClient()
        identity_node_id = args.identity_node_id
        actions = ["ACTION1", "ACTION2"]
        resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                     IsAuthorizedResource("resource2ID", "TypeName", actions)]
        input_params = {"age": "21"}
        policy_tags = ["Car", "Rental", "Sharing"]
        is_authorized = client_authorization.is_authorized_digital_twin(
            identity_node_id,
            resources,
            input_params,
            policy_tags)

        if is_authorized:
            api_helper.print_response(is_authorized)
        else:
            print("Invalid is_authorized")
        client_authorization.channel.close()
        return is_authorized
    

```
To call one command in the **usage** directory, check the **command** and the corresponding **arguments** in the list then execute in command line:
```shell
python3 authorization.py COMMAND arg1 arg2 ...
```    

### Connect to the Ingest service

To be able to connect to the Ingest service, you need to have AppAgent credentials generated from the Config service with the service account credentials or in the Hub (https://console.indykite.id/)

Once you have obtained your credentials, you have two choices to set up the necessary credentials. You either pass the json with the credentials to the `INDYKITE_APPLICATION_CREDENTIALS`
environment variable or set the `INDYKITE_APPLICATION_CREDENTIALS_FILE` environment variable to the configuration file's path.

The Ingest service provides functions to ingest data into the IndyKite platform.

Each time you want to use an Ingest method, you need to set up an ingest client.

**Example:**

Here is a very simple example to open and close a connection to the Ingest service with an arguments' parser used in the ingest.py script.

```python
from indykite_sdk.ingest import IngestClient
import argparse

    # Create parent parser
    parser = argparse.ArgumentParser(description="Ingest client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
     # ingest
    ingest_record_identity_parser = subparsers.add_parser("ingest_record_identity")
  
    # call arguments
    args = parser.parse_args()
    command = args.command
    
    # call method
    if command == "ingest_record_identity":
        # ingest an identity node record in the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique value which can be random
        record_id = str(uuid.uuid4())
        # unique id in external source
        external_id = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id)
        # type of node
        type = "Person"
        # properties
        ingest_property1 = client_ingest.ingest_property("first_name", "deer")
        ingest_property2 = client_ingest.ingest_property("last_name", "choris")
        ingest_property3 = client_ingest.ingest_property("birthdate", "20 Sep, 1977")
        ingest_property4 = client_ingest.ingest_property("role", "Employee")
        ingest_property5 = client_ingest.ingest_property("email", "deer@yahoo.uk")
        properties = [ingest_property1, ingest_property2, ingest_property3, ingest_property4, ingest_property5]
        # create upsert object with all elements
        upsert = client_ingest.upsert_data_node(
            external_id,
            type,
            ["Person"],
            properties,
            "",
            True)
        # create record with record_id and upsert
        record = client_ingest.record_upsert(record_id, upsert)
        print(record)
        # send the ingestion request and get the response
        ingest_record_identity_node = client_ingest.ingest_record(record)
        if ingest_record_identity_node:
            api_helper.print_response(ingest_record_identity_node)
        else:
            print("Invalid upsert")
        client_ingest.channel.close()
        return ingest_record_identity_node
    

```
To call one command in the **usage** directory, check the **command** and the corresponding **arguments** in the list then execute in command line:
```shell
python3 ingest.py COMMAND arg1 arg2 ...
```    

### Connect to the Knowledge service

To be able to connect to the knowledge service, you need to have AppAgent credentials generated from the Config service with the service account credentials or in the Hub (https://console.indykite.id/)

Once you have obtained your credentials, you have two choices to set up the necessary credentials. You either pass the json with the credentials to the `INDYKITE_APPLICATION_CREDENTIALS`
environment variable or set the `INDYKITE_APPLICATION_CREDENTIALS_FILE` environment variable to the configuration file's path.

The Knowledge service provides functions to read data from the Knowledge API.

Each time you want to use a knowledge method, you need to set up a knowledge client.

**Example:**

Here is a very simple example to open and close a connection to the Knowledge service with an arguments' parser used in the knowledge.py script.

```python
from indykite_sdk.knowledge import KnowledgeClient
import argparse

    # Create parent parser
    parser = argparse.ArgumentParser(description="Knowledge client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # Get Identity node by its gid
    get_identity_by_id_parser = subparsers.add_parser("get_identity_by_id")
    get_identity_by_id_parser.add_argument("id", help="Identity node gid (node with is_identity equal True)")
  
    # call arguments
    args = parser.parse_args()
    command = args.command
    
    # call method
    if command == "get_identity_by_id":
        # send a request to the knowledge API with identity node gid
        # and get the node info
        client_knowledge = KnowledgeClient()
        id = args.id
        response = client_knowledge.get_identity_by_id(id)
        if response:
            api_helper.print_response(response)
        else:
            print("No result")
        client_knowledge.channel.close()
        

```
To call one command in the **usage** directory, check the **command** and the corresponding **arguments** in the list then execute in command line:
```shell
python3 knowledge.py COMMAND arg1 arg2 ...
```    

---------------------------------------------------------------------------------
---------------------------------------------------------------------------------
  
## Testing

In tests, `pytest test_...` 

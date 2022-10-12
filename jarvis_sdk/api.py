"""
Commandline interface for making an API request with the SDK.
"""
import argparse
import base64
import json
from datetime import datetime
from uuid import UUID
from google.protobuf.json_format import MessageToJson

from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier

class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def main():
    # Create parent parser
    parser = argparse.ArgumentParser(description="Identity client API.")
    parser.add_argument("-l", "--local", action="store_true", help="make the request to localhost")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # INTROSPECT
    introspect_parser = subparsers.add_parser("introspect")
    introspect_parser.add_argument("user_token", help="JWT bearer token")

    # VERIFY
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("verification_token", help="Token from email to verify")

    # CHANGE-PASSWORD (self-service)
    password_change = subparsers.add_parser("change-password")
    password_change.add_argument("user_token", help="JWT bearer token")
    password_change.add_argument("new_password", help="New password for the user in '' (single quotation mark)")

    # CHANGE-PASSWORD-OF-USER (admin activity)
    password_change_of_user = subparsers.add_parser("change-password-of-user")
    password_change_of_user.add_argument("digital_twin_id", help="UUID4 ID of the digital twin for password change")
    password_change_of_user.add_argument("tenant_id", help="UUID4 ID of the tenant")
    password_change_of_user.add_argument("new_password", help="New password for the user in '' (single quotation mark)")

    # GET-DT
    get_dt = subparsers.add_parser("get-dt")
    get_dt.add_argument("digital_twin_id", help="UUID4 ID of the digital twin for password change")
    get_dt.add_argument("tenant_id", help="UUID4 ID of the tenant")
    get_dt.add_argument("property_list", nargs="+", help="Array list of the required properties")

    # GET-DT-BY-TOKEN
    get_dt_by_token = subparsers.add_parser("get-dt-by-token")
    get_dt_by_token.add_argument("user_token", help="JWT bearer token")
    get_dt_by_token.add_argument("property_list", nargs="+", help="Array list of the required properties")

    # PATCH-PROPERTIES
    patch_properties = subparsers.add_parser("patch-properties")
    patch_properties.add_argument("digital_twin_id", help="UUID4 ID of the digital twin for password change")
    patch_properties.add_argument("tenant_id", help="UUID4 ID of the tenant")
    patch_properties.add_argument("--add", nargs="+", help="Name and value of the property to add (--add email x@x.x)")
    patch_properties.add_argument("--add_by_ref", nargs="+", help='''
Name and value of the property where the value is a reference
    ''')
    patch_properties.add_argument("--replace", nargs="+", help="Property ID and new value (--replace 111 a@a.a)")
    patch_properties.add_argument("--replace_by_ref", nargs="+", help='''
Property ID and value of the property where the value is a reference
        ''')
    patch_properties.add_argument("--remove", nargs="+", help="Remove the properties with the given ID")

    # PATCH-PROPERTIES-BY-TOKEN
    patch_properties_by_token = subparsers.add_parser("patch-properties-by-token")
    patch_properties_by_token.add_argument("user_token", help="JWT bearer token")
    patch_properties_by_token.add_argument("--add", nargs="+", help='''
Name and value of the property to add (--add email x@x.x)''')
    patch_properties_by_token.add_argument("--add_by_ref", nargs="+", help='''
Name and value of the property where the value is a reference
        ''')
    patch_properties_by_token.add_argument("--replace", nargs="+", help='''
Property ID and new value (--replace 111 a@a.a)''')
    patch_properties_by_token.add_argument("--replace_by_ref", nargs="+", help='''
Property ID and value of the property where the value is a reference
            ''')
    patch_properties_by_token.add_argument("--remove", nargs="+", help="Remove the properties with the given IDs")

    # START-DT-EMAIL-VERIFICATION
    start_dt_email_verification = subparsers.add_parser("start-dt-email-verification")
    start_dt_email_verification.add_argument("digital_twin", help="UUID4 of the digital twin")
    start_dt_email_verification.add_argument("tenant_id", help="UUID4 of the tenant")
    start_dt_email_verification.add_argument("email", help="email address to validate")

    # DELETE-USER (admin activity)
    del_dt = subparsers.add_parser("del-dt")
    del_dt.add_argument("digital_twin_id", help="UUID4 ID of the digital twin for password change")
    del_dt.add_argument("tenant_id", help="UUID4 ID of the tenant")

    # DELETE-USER-BY-TOKEN (self-service)
    del_dt_by_token = subparsers.add_parser("del-dt-by-token")
    del_dt_by_token.add_argument("user_token", help="JWT bearer token")

    # ENRICH-TOKEN
    enrich_token = subparsers.add_parser("enrich-token")
    enrich_token.add_argument("user_token", help="JWT bearer token")
    enrich_token.add_argument("--token_claims", nargs='*',
                              help="Token claims to add (--token_claims key=value)", action=ParseKwargs)
    enrich_token.add_argument("--session_claims", nargs='*',
                              help="Session claims to add (--session_claims key=value)", action=ParseKwargs)

    # customer_id
    customer_id_parser = subparsers.add_parser("customer_id")
    #customer_parser.add_argument("access_token", help="JWT bearer token")

    # customer_name
    customer_name_parser = subparsers.add_parser("customer_name")
    customer_name_parser.add_argument("customer_name", help="Customer name (not display name)")

    # service_account
    service_account_parser = subparsers.add_parser("service_account")

    # app_space_id
    app_space_id_parser = subparsers.add_parser("app_space_id")
    app_space_id_parser.add_argument("app_space_id", help="App Space id (gid)")

    # app_space_name
    app_space_name_parser = subparsers.add_parser("app_space_name")
    app_space_name_parser.add_argument("app_space_name", help="App Space name (not display name)")
    app_space_name_parser.add_argument("customer_id", help="Customer Id (gid)")

    args = parser.parse_args()

    local = args.local
    client = IdentityClient(local)
    client_config = ConfigClient(local)

    command = args.command

    if command == "introspect":
        user_token = args.user_token
        token_info = client.introspect_token(user_token)
        if token_info is not None:
            print_response(token_info)
        else:
            print("Invalid token")

    elif command == "verify":
        verification_token = args.verification_token
        digital_twin_info = client.verify_digital_twin_email(verification_token)
        if digital_twin_info is not None:
            print_response({ "digitalTwin": digital_twin_info })

    elif command == "change-password":
        user_token = args.user_token
        new_password = args.new_password
        password_change = client.change_password(user_token, new_password)
        if password_change is not None:
            print(password_change)

    elif command == "change-password-of-user":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        new_password = args.new_password
        password_change = client.change_password_of_user(digital_twin_id, tenant_id, new_password)
        if password_change is not None:
            print(password_change)

    elif command == "get-dt":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        property_list = args.property_list
        dt = client.get_digital_twin(digital_twin_id, tenant_id, property_list[1:])
        if dt is not None:
            print_response(dt)

    elif command == "get-dt-by-token":
        user_token = args.user_token
        property_list = args.property_list
        dt = client.get_digital_twin_by_token(user_token, property_list[1:])
        if dt is not None:
            print_response(dt)

    elif command == "patch-properties":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        all_args = {
            "add": [],
            "add_by_ref": [],
            "replace": [],
            "replace_by_ref": [],
            "remove": []
        }

        props = args.add
        add_args_to_dict(all_args, "add", props)
        props = args.add_by_ref
        add_args_to_dict(all_args, "add_by_ref", props)
        props = args.replace
        add_args_to_dict(all_args, "replace", props)
        props = args.replace_by_ref
        add_args_to_dict(all_args, "replace_by_ref", props)
        props = args.remove
        add_args_to_dict(all_args, "remove", props)
        properties = client.patch_properties(digital_twin_id, tenant_id, all_args)
        if properties is not None:
            print(properties)

    elif command == "patch-properties-by-token":
        user_token = args.user_token
        all_args = {
            "add": [],
            "add_by_ref": [],
            "replace": [],
            "replace_by_ref": [],
            "remove": []
        }

        props = args.add
        add_args_to_dict(all_args, "add", props)
        props = args.add_by_ref
        add_args_to_dict(all_args, "add_by_ref", props)
        props = args.replace
        add_args_to_dict(all_args, "replace", props)
        props = args.replace_by_ref
        add_args_to_dict(all_args, "replace_by_ref", props)
        props = args.remove
        add_args_to_dict(all_args, "remove", props)
        properties = client.patch_properties_by_token(user_token, all_args)
        if properties is not None:
            print(properties)

    elif command == "start-dt-email-verification":
        digital_twin_id = args.digital_twin
        tenant_id = args.tenant_id
        email = args.email
        resp = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
        if resp is not None:
            print(resp)

    elif command == "del-dt":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        dt = client.del_digital_twin(digital_twin_id, tenant_id)
        if dt is not None:
            print_response({ "digitalTwin": dt })

    elif command == "del-dt-by-token":
        user_token = args.user_token
        dt = client.del_digital_twin_by_token(user_token)
        if dt is not None:
            print_response({ "digitalTwin": dt })

    elif command == "enrich-token":
        user_token = args.user_token
        token_claims = args.token_claims
        session_claims = args.session_claims
        response = client.enrich_token(user_token, token_claims, session_claims)
        if response is not None:
            print("Successfully enriched token")
        else:
            print("Invalid token")

    elif command == "customer_id":

        try:
            service_account = client_config.get_service_account()
        except Exception as exception:
            print(exception)
            return None

        print(service_account.customer_id)
        customer = client_config.get_customer_by_id(service_account.customer_id)
        if customer:
            print_response(customer)
        else:
            print("Invalid customer id")

    elif command == "customer_name":
        customer_name = args.customer_name
        customer = client_config.get_customer_by_name(customer_name)
        if customer:
            print_response(customer)
        else:
            print("Invalid customer id")

    elif command == "service_account":

        service_account = client_config.get_service_account()
        if service_account:
            print_response(service_account)
        else:
            print("Invalid service account")

    elif command == "app_space_id":
        app_space_id = args.app_space_id
        app_space = client_config.get_app_space_by_id(app_space_id)
        if app_space:
            print_response(app_space)
        else:
            print("Invalid app_space id")

    elif command == "app_space_name":
        app_space_name = args.app_space_name
        customer_id = args.customer_id
        app_space = client_config.get_app_space_by_name(customer_id, app_space_name)
        if app_space:
            print_response(app_space)
        else:
            print("Invalid app_space name")


def print_verify_info(digital_twin_info):  # pragma: no cover
    print("Digital twin info")
    print("=================")
    print("Tenant: " + str(UUID(bytes=digital_twin_info.digital_twin.tenant_id)))
    print("Digital twin: " + str(UUID(bytes=digital_twin_info.digital_twin.id)))


def print_token_info(token_info):  # pragma: no cover
    print("Token info")
    print("==========")
    print("Tenant: " + str(UUID(bytes=token_info.tenant_id)))
    print("Customer: " + str(UUID(bytes=token_info.customer_id)))
    print("App space: " + str(UUID(bytes=token_info.app_space_id)))
    print("Application: " + str(UUID(bytes=token_info.application_id)))
    print("Subject: " + str(UUID(bytes=token_info.subject_id)))
    print("Expire time: " + str(datetime.fromtimestamp(token_info.expire_time.seconds)))


def print_response(resp):  # pragma: no cover
    def get_default(x):
        if type(x) is datetime:
            return str(x)
        else:
            return x.__dict__

    if hasattr(resp, "DESCRIPTOR"):
        js = MessageToJson(resp)
        js_dict = json.loads(js)
        prettify(js_dict)
    else:
        js_dict = resp
    pretty_response = json.dumps(js_dict, indent=4, separators=(',', ': '), default=get_default)
    print(pretty_response)


def prettify(js):  # pragma: no cover
    for k, v in js.items():
        if isinstance(v, type(dict())):
            prettify(v)
        elif isinstance(v, type(list())):
            for val in v:
                if isinstance(val, type(str())):
                    val = format_convert(k, val)
                    pass
                elif isinstance(val, type(list())) | isinstance(val, type(float())) | isinstance(val, type(
                    bool())) | isinstance(val, type(None)):
                    pass
                else:
                    prettify(val)
        else:
            if isinstance(v, str):
                js[k] = format_convert(k, v)


def format_convert(k, v):  # pragma: no cover
    try:
        if "id" in k:
            i = int(v)
            return i
    except ValueError:
        pass
    return str(base64_to_uuid(v))


def base64_to_uuid(b):  # pragma: no cover
    try:
        s = b.encode('ascii')
        uid = UUID(bytes=base64.b64decode(s))
    except ValueError:
        return b
    return uid


def add_args_to_dict(all_args, action, values):  # pragma: no cover
    if action == "add" and values is not None:
        for v in values:
            all_args["add"].append(v)
    elif action == "add_by_ref" and values is not None:
        for v in values:
            all_args["add_by_ref"].append(v)
    elif action == "replace" and values is not None:
        for v in values:
            all_args["replace"].append(v)
    elif action == "replace_by_ref" and values is not None:
        for v in values:
            all_args["replace_by_ref"].append(v)
    elif action == "remove" and values is not None:
        for v in values:
            all_args["remove"].append(v)

    return all_args


if __name__ == '__main__':  # pragma: no cover
    main()

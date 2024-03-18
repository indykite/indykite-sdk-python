import base64
from datetime import datetime
import json
from uuid import UUID
from google.protobuf.json_format import MessageToJson


def print_verify_info(digital_twin_info):  # pragma: no cover
    print("Digital twin info")
    print("=================")
    print("Tenant: " + str(UUID(bytes=digital_twin_info.digital_twin.tenant_id)))
    print("Digital twin: " + str(UUID(bytes=digital_twin_info.digital_twin.id)))


def print_credential(credential):  # pragma: no cover
    print("Credential")
    print("==========")
    print("Credential id: " + str(credential.id))
    print("Kid: " + str(credential.kid))
    if hasattr(credential, 'agent_config'):
        print("Agent config: " + str(credential.agent_config))
    elif hasattr(credential, 'service_account_config'):
        print("Service account config: " + str(credential.service_account_config))
    print("Bookmark: " + str(credential.bookmark))
    print("Create time: " + str(credential.create_time))
    print("Expire time: " + str(credential.expire_time))


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

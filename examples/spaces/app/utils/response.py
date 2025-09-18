import base64
import json
from datetime import datetime
from uuid import UUID

from google.protobuf.json_format import MessageToJson


def response_data(code=0, message="ok"):
    data = {"code": code, "message": message}
    return data


def get_response(resp):
    def get_default(x):
        if type(x) is datetime:
            return str(x)
        return x.__dict__

    if hasattr(resp, "DESCRIPTOR"):
        js = MessageToJson(resp)
        js_dict = json.loads(js)
        prettify(js_dict)
    else:
        js_dict = resp
    pretty_response = json.dumps(js_dict, indent=4, separators=(",", ": "), default=get_default)
    return pretty_response


def prettify(js):
    for k, v in js.items():
        if isinstance(v, type(dict())):
            prettify(v)
        elif isinstance(v, type(list())):
            for val in v:
                if isinstance(val, str):
                    val = format_convert(k, val)
                elif isinstance(val, type(list())) | isinstance(val, float) | isinstance(val, bool) | (val is None):
                    pass
                else:
                    prettify(val)
        elif isinstance(v, str):
            js[k] = format_convert(k, v)


def format_convert(k, v):
    try:
        if "id" in k:
            i = int(v)
            return i
    except ValueError:
        pass
    return str(base64_to_uuid(v))


def base64_to_uuid(b):
    try:
        s = b.encode("ascii")
        uid = UUID(bytes=base64.b64decode(s))
    except ValueError:
        return b
    return uid


def get_credentials_response(credentials):
    cred = vars(credentials)
    cred_dict = {}
    for k, v in cred.items():
        cred_dict[k] = str(v)

    return cred_dict

from time import sleep
import string
import random
import requests
from tests.helpers import data


def first_reg_request():
    body = {
            "cc": data.get_code_challenge(),
            "~tenant": "696e6479-6b69-4465-8000-030f00000001",
            "~arg": {
                "flow": "register"
            }
        }
    return send_post(body)


def first_reg_request_with_email():
    body = {
            "cc": data.get_code_challenge(),
            "~tenant": "696e6479-6b69-4465-8000-030F00000002",
            "~arg": {
                "flow": "register"
            }
        }
    return send_post(body)


def second_reg_request(thread_id, email, password):
    body = {
            "~thread": {
                "thid": thread_id
            },
            "@type": "form",
            "@id": "00000000-0000-4040-8000-005400000000",
            "username": email,
            "password": password
        }
    return send_post(body)


def verify_request(thread_id):
    body = {
            "~thread": {
                "thid": thread_id
            },
            "@type": "verifier",
            "cv": data.get_code_verifier()
        }
    return send_post(body)


def first_login():
    body = {
            "cc": data.get_code_challenge(),
            "~tenant": data.get_tenant()
        }
    return send_post(body)


def second_login(thread_id, email, password):
    body = {
            "~thread": {
                "thid": thread_id
            },
            "@type": "form",
            "@id": "00000000-0000-4020-8000-003400000000",
            "username": email,
            "password": password
        }
    return send_post(body)


def send_post(body):
    x = requests.post(data.get_url()+"/auth/"+data.get_application(), json=body)
    return x.json()


def send_get_mailbox(email):
    headers = {'Authorization': 'Bearer ' + data.get_email_token()}
    x = requests.get(data.get_email_url()+"/mailbox/"+email, headers=headers, data={})
    return x.json()


def send_token_verification(token):
    headers = {'Authorization': 'Bearer ' + data.get_verification_bearer()}
    x = requests.post(data.get_url()+"/identity/email/verify/"+token, headers=headers, data={})
    return x.json()


def registration(email, password):
    resp = first_reg_request()
    resp = second_reg_request(resp["~thread"]["thid"], email, password)
    resp = verify_request(resp["~thread"]["thid"])
    return resp["token"], resp["refresh_token"]


def registration_with_email_verification(email, password):
    resp = first_reg_request_with_email()
    resp = second_reg_request(resp["~thread"]["thid"], email, password)
    sleep(2)
    r = send_get_mailbox(email)
    token = r[0]["personalizations"][-1]["dynamic_template_data"]["referenceId"]
    send_token_verification(token)
    resp = verify_request(resp["~thread"]["thid"])
    return resp["token"], resp["refresh_token"]


def registration_until_email_arrives(email, password):
    resp = first_reg_request_with_email()
    resp = second_reg_request(resp["~thread"]["thid"], email, password)
    sleep(2)
    r = send_get_mailbox(email)
    return r[0]["personalizations"][-1]["dynamic_template_data"]["referenceId"]


def login(email, password):
    resp = first_login()
    resp = second_login(resp["~thread"]["thid"], email, password)
    resp = verify_request(resp["~thread"]["thid"])
    return resp["token"], resp["refresh_token"]


def logout(refresh_token):
    body = {
        "refreshToken": refresh_token
    }
    return send_post(body)


def generate_random_gid():
    num = 27
    res = ''.join(random.choices(string.ascii_letters + string.digits + "_", k=num))
    return 'gid:' + res

"""
This file contains examples of Identify API usage.
"""
from datetime import datetime
from uuid import UUID

from jarvis_sdk.cmd import IdentityClient


def introspect_token_example():
    token = "JWT TOKEN"
    client = IdentityClient()
    token_info = client.introspect_token(token)
    if token_info is not None:
        print("Token info")
        print("Tenant: " + str(UUID(bytes=token_info.subject.tenant_id)))
        print("Customer: " + str(UUID(bytes=token_info.customer_id)))
        print("App space: " + str(UUID(bytes=token_info.app_space_id)))
        print("Application: " + str(UUID(bytes=token_info.application_id)))
        print("Subject: " + str(UUID(bytes=token_info.subject.id)))
        print("Expire time: " + str(datetime.fromtimestamp(token_info.expire_time.seconds)))


def verify_digital_twin_email_example():
    token = "VERIFICATION TOKEN FROM TEMPORAL"
    client = IdentityClient()
    digital_twin_info = client.verify_digital_twin_email(token)
    if digital_twin_info is not None:
        print("Digital twin info")
        print("Tenant: " + str(UUID(bytes=digital_twin_info.tenant_id)))
        print("Digital twin: " + str(UUID(bytes=digital_twin_info.digital_twin_id)))

def digital_twin_by_token():
    token = "JWT TOKEN"
    client = IdentityClient()
    response = client.get_digital_twin_by_token(token, ["email"])
    dt = response.digital_twin
    print(response)
    if response is not None:
        print("Digital Twin info")
        print("Digital Twin: " + str(UUID(bytes=dt.digital_twin.id)))
        print("Tenant: " + str(UUID(bytes=dt.digital_twin.tenant_id)))
        print("\nProperties:")
        for property in dt.properties:
            print("Property: " + property.definition.property)
            print("ID: " + property.id)
            if (property.object_value and property.object_value.string_value):
                print("Value: " + property.object_value.string_value)
            print()

import json
import os
import random
import string
import time
from datetime import datetime

import numpy as np

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import model_pb2
from indykite_sdk.indykite.config.v1beta1.model_pb2 import \
    google_dot_protobuf_dot_wrappers__pb2 as wrappers

INDYKITE_SDK_URL = os.getenv("INDYKITE_SDK_URL")
EMAIL_URL = os.getenv("EMAIL_URL")
EMAIL_TOKEN = os.getenv("EMAIL_TOKEN")
APPLICATION = os.getenv("APPLICATION")
IDENTITY_NODE = os.getenv("IDENTITY_NODE")
IDENTITY_NODE_TEST = os.getenv("IDENTITY_NODE_TEST")
IDENTITY_NODE_CONSENT = os.getenv("IDENTITY_NODE_CONSENT")
IDENTITY_NODE_PROPERTY = os.getenv("IDENTITY_NODE_PROPERTY")
CODE_CHALLENGE = os.getenv("CODE_CHALLENGE")
VERIFICATION_BEARER = os.getenv("VERIFICATION_BEARER")
EXPIRED_TOKEN = os.getenv("EXPIRED_TOKEN")
CONFIG_ID = os.getenv("CONFIG_ID")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
WRONG_ACCOUNT_ID = os.getenv("WRONG_ACCOUNT_ID")
SERVICE_ACCOUNT_NAME = os.getenv("SERVICE_ACCOUNT_NAME")
TEST_SERVICE_ACCOUNT = os.getenv("TEST_SERVICE_ACCOUNT")
CUSTOMER_NAME = os.getenv("CUSTOMER_NAME")
APP_SPACE_NAME = os.getenv("APP_SPACE_NAME")
CUSTOMER_ID = os.getenv("CUSTOMER_ID")
CUSTOMER_ID2 = os.getenv("CUSTOMER_ID2")
APP_SPACE_ID = os.getenv("APP_SPACE_ID")
APPLICATION_ID = os.getenv("APPLICATION_ID")
APPLICATION_NAME = os.getenv("APPLICATION_NAME")
APPLICATION_AGENT_ID = os.getenv("APPLICATION_AGENT_ID")
APPLICATION_AGENT_NAME = os.getenv("APPLICATION_AGENT_NAME")
APPLICATION_AGENT_CREDENTIAL_ID = os.getenv("APPLICATION_AGENT_CREDENTIAL_ID")
SERVICE_ACCOUNT_CREDENTIAL_ID = os.getenv("SERVICE_ACCOUNT_CREDENTIAL_ID")
AUTHZ_POLICY_CONFIG_NODE = os.getenv("AUTHZ_POLICY_CONFIG_NODE")
AUTHZ_POLICY_CONFIG_NODE_KQ = os.getenv("AUTHZ_POLICY_CONFIG_NODE_KQ")
CONSENT_CONFIG_NODE = os.getenv("CONSENT_CONFIG_NODE")
CONSENT_ID = os.getenv("CONSENT_ID")
PASSWORD = os.getenv("PASSWORD")
NEW_PASSWORD = os.getenv("NEW_PASSWORD")
BCRYPT = os.getenv("BCRYPT")
SUBMITTER_SECRET = os.getenv("SUBMITTER_SECRET")
MANAGER_SECRET = os.getenv("MANAGER_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
RELYING_PARTIES = os.getenv("RELYING_PARTIES")
ORGANIZATION_EXTERNAL_ID = os.getenv("ORGANIZATION_EXTERNAL_ID")
ASSET_EXTERNAL_ID = os.getenv("ASSET_EXTERNAL_ID")
INDIVIDUAL_EXTERNAL_ID = os.getenv("INDIVIDUAL_EXTERNAL_ID")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")
ASSET_ID = os.getenv("ASSET_ID")
INDIVIDUAL_ID = os.getenv("INDIVIDUAL_ID")


def get_password():
    return PASSWORD


def get_old_password():
    return PASSWORD


def get_new_password():
    return NEW_PASSWORD


def get_new_email():
    email = "automation_" + str(datetime.now().timestamp()) + "@yahoo.com"
    return email


def get_code_challenge():
    return CODE_CHALLENGE


def get_application():
    return APPLICATION


def get_identity_node():
    return INDIVIDUAL_ID


def get_identity_node_external_id():
    return INDIVIDUAL_EXTERNAL_ID


def get_identity_node_test():
    return IDENTITY_NODE_TEST


def get_identity_node_consent():
    return IDENTITY_NODE_CONSENT


def get_identity_node_property():
    return IDENTITY_NODE_PROPERTY


def get_url():
    return INDYKITE_SDK_URL


def get_email_url():
    return EMAIL_URL


def get_email_token():
    return EMAIL_TOKEN


def get_verification_bearer():
    return VERIFICATION_BEARER


def get_expired_token():
    return EXPIRED_TOKEN


def get_config_id():
    return CONFIG_ID


def get_wrong_account_id():
    return WRONG_ACCOUNT_ID


def get_account_id():
    return ACCOUNT_ID


def get_customer_name():
    return CUSTOMER_NAME


def get_customer_id():
    return CUSTOMER_ID


def get_customer_id2():
    return CUSTOMER_ID2


def get_app_space_name():
    return APP_SPACE_NAME


def get_app_space_id():
    return APP_SPACE_ID


def get_application_id():
    return APPLICATION_ID


def get_application_name():
    return APPLICATION_NAME


def get_application_agent_id():
    return APPLICATION_AGENT_ID


def get_application_agent_name():
    return APPLICATION_AGENT_NAME


def get_application_agent_credential_id():
    return APPLICATION_AGENT_CREDENTIAL_ID


def get_service_account_id():
    return TEST_SERVICE_ACCOUNT


def get_service_account_name():
    return SERVICE_ACCOUNT_NAME


def get_service_account_credential_id():
    return SERVICE_ACCOUNT_CREDENTIAL_ID


def get_authz_policy_config_node_id():
    return AUTHZ_POLICY_CONFIG_NODE


def get_authz_policy_config_kq_node_id():
    return AUTHZ_POLICY_CONFIG_NODE_KQ


def get_consent_config_node_id():
    return CONSENT_CONFIG_NODE


def get_consent_id():
    return CONSENT_ID


def get_authz_policy():
    with open(os.path.dirname(__file__) + "/sdk_policy_config.json") as f:
        file_data = f.read()
    policy_dict = json.loads(file_data)
    policy_dict = json.dumps(policy_dict)
    policy_config = ConfigClient().authorization_policy_config(str(policy_dict), "STATUS_ACTIVE", [])
    return policy_config


def get_consent_config():
    text = "".join(random.choices(string.ascii_letters, k=15))
    consent_config = ConfigClient().consent_config(
        purpose=text,
        data_points=[
            '{ "query": "", "returns": [ { "variable": "",' + '"properties": ["name", "email", "location"] } ] }',
        ],
        application_id=get_application_id(),
        validity_period=86400,
        revoke_after_use=False,
        token_status=3,
    )
    return consent_config


def get_token_introspect_config():
    text = "".join(random.choices(string.ascii_letters, k=15))
    text2 = "".join(random.choices(string.ascii_letters, k=15))
    jwt = model_pb2.TokenIntrospectConfig.JWT(issuer="https://example.com", audience="audience-id" + text)
    offline = model_pb2.TokenIntrospectConfig.Offline(
        public_jwks=[
            json.dumps(
                {
                    "kid": "abc",
                    "use": "sig",
                    "alg": "RS256",
                    "n": "--nothing-real-just-random-" + text + "--",
                    "kty": "RSA",
                },
            ).encode("utf-8"),
            json.dumps(
                {
                    "kid": "jkl",
                    "use": "sig",
                    "alg": "RS256",
                    "n": "--nothing-real-just-random-" + text2 + "--",
                    "kty": "RSA",
                },
            ).encode("utf-8"),
        ],
    )
    token_introspect_config = ConfigClient().token_introspect_config(
        token_matcher={"jwt": jwt},
        validation={"offline": offline},
        claims_mapping={"email": "mail", "name": "full_name"},
        ikg_node_type="Person",
        perform_upsert=True,
    )
    return token_introspect_config


def get_external_data_resolver_config(right_now):
    header1 = model_pb2.ExternalDataResolverConfig.Header()
    header1.values.extend(["Authorization", "Bearer token_value"])
    header2 = model_pb2.ExternalDataResolverConfig.Header()
    header2.values.extend(["Content-Type", "application/json"])
    headers = {"AuthHeader": header1, "ContentHeader": header2}
    external_data_resolver_config = ConfigClient().external_data_resolver_config(
        url="https://example.com/source" + right_now,
        method="GET",
        headers=headers,
        request_type=1,
        request_payload=b'{"url": "source", "method": "GET"}',
        response_type=1,
        response_selector=".",
    )
    return external_data_resolver_config


def get_entity_matching_pipeline_config(right_now):
    node_filter = model_pb2.EntityMatchingPipelineConfig.NodeFilter()
    node_filter.source_node_types.extend(["Person"])
    node_filter.target_node_types.extend(["Car"])
    entity_matching_pipeline_config = ConfigClient().entity_matching_pipeline_config(node_filter=node_filter)
    return entity_matching_pipeline_config


def get_entity_matching_pipeline_config_with_url(right_now):
    node_filter = model_pb2.EntityMatchingPipelineConfig.NodeFilter()
    node_filter.source_node_types.extend(["Person"])
    node_filter.target_node_types.extend(["Person"])
    entity_matching_pipeline_config = ConfigClient().entity_matching_pipeline_config(
        node_filter=node_filter,
        similarity_score_cutoff=np.float32(0.9),
        property_mapping_status="STATUS_PENDING",
        entity_matching_status="STATUS_PENDING",
        property_mappings=[],
        rerun_interval="1 day",
        last_run_time=right_now,
        report_url="gs://some-path",
        report_type="csv",
    )
    return entity_matching_pipeline_config


def get_trust_score_profile_config(right_now):
    dimension = model_pb2.TrustScoreDimension(name=4, weight=0.9)
    trust_score_profile_config = ConfigClient().trust_score_profile_config(
        node_classification="Employee", dimensions=[dimension], schedule=4,
    )
    return trust_score_profile_config


def get_knowledge_query_config(right_now):
    knowledge_query_config = ConfigClient().knowledge_query_config(
        query='{"nodes": ["resource.property.value"],'
        ' "relationships": [],'
        '"filter": {"attribute": "resource.property.value", "operator": "=", "value": "$resourceValue"}'
        "}",
        status=1,
        policy_id=get_authz_policy_config_kq_node_id(),
    )
    return knowledge_query_config


def get_knowledge_query_config_upd(right_now):
    knowledge_query_config = ConfigClient().knowledge_query_config(
        query='{"nodes": ["resource.property.value"],'
        ' "relationships": [],'
        '"filter": {"attribute": "resource.property.value", "operator": "=", "value": "$resourceValue"}'
        "}",
        status=2,
        policy_id=get_authz_policy_config_kq_node_id(),
    )
    return knowledge_query_config


def get_event_sink_config(right_now):
    right_now = str(int(time.time()) + 2)
    provider1 = model_pb2.EventSinkConfig.Provider(
        kafka=model_pb2.KafkaSinkConfig(
            brokers=["kafka-01:9092", "kafka-02:9092"],
            topic="events",
            username="my-username",
            password="some-super-secret-password",
            display_name=wrappers.StringValue(value="display_name1"),
        ),
    )
    provider2 = model_pb2.EventSinkConfig.Provider(
        kafka=model_pb2.KafkaSinkConfig(
            brokers=["kafka-01:9092", "kafka-02:9092"],
            topic="events",
            username="my-username",
            password="some-super-secret-password",
            display_name=wrappers.StringValue(value="display_name2"),
        ),
    )
    provider3 = model_pb2.EventSinkConfig.Provider(
        azure_event_grid=model_pb2.AzureEventGridSinkConfig(
            topic_endpoint="https://ik-test.eventgrid.azure.net/api/events",
            access_key="secret-access-key",
            display_name=wrappers.StringValue(value="display_name3"),
        ),
    )
    provider4 = model_pb2.EventSinkConfig.Provider(
        azure_service_bus=model_pb2.AzureServiceBusSinkConfig(
            connection_string="personal-connection-info",
            queue_or_topic_name="your-queue",
            display_name=wrappers.StringValue(value="display_name4"),
        ),
    )
    providers = {"kafka-01": provider1, "kafka-02": provider2, "azure-grid": provider3, "azure-bus": provider4}
    keys_values_filter = {"event_type": "indykite.audit.config.create"}
    pairs = model_pb2.EventSinkConfig.Route.KeyValuePair(key="relationshipcreated", value="access-granted")
    keys_values_filter2 = {"key_value_pairs": [pairs], "event_type": "indykite.audit.capture.*"}
    routes = [
        model_pb2.EventSinkConfig.Route(
            provider_id="kafka-provider-01",
            stop_processing=False,
            keys_values=model_pb2.EventSinkConfig.Route.EventTypeKeysValues(**keys_values_filter),
            display_name=wrappers.StringValue(value="kafka-provider-01"),
            id=wrappers.StringValue(value="gid:kafka-provider-01"),
        ),
        model_pb2.EventSinkConfig.Route(
            provider_id="kafka-provider-02",
            stop_processing=False,
            keys_values=model_pb2.EventSinkConfig.Route.EventTypeKeysValues(**keys_values_filter2),
            display_name=wrappers.StringValue(value="kafka-provider-02"),
            id=wrappers.StringValue(value="gid:kafka-provider-02"),
        ),
        model_pb2.EventSinkConfig.Route(
            provider_id="azure-grid",
            stop_processing=False,
            keys_values=model_pb2.EventSinkConfig.Route.EventTypeKeysValues(**keys_values_filter),
        ),
        model_pb2.EventSinkConfig.Route(
            provider_id="azure-bus",
            stop_processing=False,
            keys_values=model_pb2.EventSinkConfig.Route.EventTypeKeysValues(**keys_values_filter2),
        ),
    ]
    event_sink_config = ConfigClient().event_sink_config(providers=providers, routes=routes)
    return event_sink_config

import sys

from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_config_node import CreateConfigNode
from indykite_sdk.model.update_config_node import UpdateConfigNode
from indykite_sdk.model.config_node import ConfigNode
from indykite_sdk.model.authorization_policy_config_status import Status
from indykite_sdk.indykite.config.v1beta1 import model_pb2
from indykite_sdk.model.token_status import ExternalTokenStatus
from indykite_sdk.model.entity_matching_status import Status as EntityMatchingStatus
from indykite_sdk.model.external_data_resolver_config_content_type import ContentType
import indykite_sdk.utils.logger as logger


def read_config_node(self, config_node_id, version=0):
    """
    read a specific config node
    :param self:
    :param config_node_id: string gid id
    :param version: int
    :return: deserialized ConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadConfigNode(
            pb2.ReadConfigNodeRequest(
                id=str(config_node_id),
                version=version
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return ConfigNode.deserialize(response.config_node)


def delete_config_node(self, config_node_id, etag):
    """
    delete a specific config node
    :param self:
    :param config_node_id: string gid id
    :param etag: etag
    :return: DeleteConfigNodeResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteConfigNode(
            pb2.DeleteConfigNodeRequest(
                id=str(config_node_id),
                etag=wrappers.StringValue(value=etag)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response


def create_authorization_policy_config_node(self,
                                            location,
                                            name,
                                            display_name,
                                            description,
                                            authorization_policy_config):
    """
    create authorization policy
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param authorization_policy_config: AuthorizationPolicyConfig object
    :return: deserialized CreateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        valid = True
        if authorization_policy_config and authorization_policy_config.status:
            valid = self.validate_authorization_policy_status(authorization_policy_config.status)
        if valid:
            response = self.stub.CreateConfigNode(
                pb2.CreateConfigNodeRequest(
                    location=location,
                    name=name,
                    display_name=wrappers.StringValue(value=display_name),
                    description=wrappers.StringValue(value=description),
                    authorization_policy_config=authorization_policy_config
                )
            )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def update_authorization_policy_config_node(self,
                                            config_node_id,
                                            etag,
                                            display_name,
                                            description,
                                            authorization_policy_config):
    """
    update authorization policy
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param authorization_policy_config: AuthorizationPolicyConfig object
    :return: deserialized UpdateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        valid = True
        if authorization_policy_config and authorization_policy_config.status:
            valid = self.validate_authorization_policy_status(authorization_policy_config.status)
        if valid:
            response = self.stub.UpdateConfigNode(
                pb2.UpdateConfigNodeRequest(
                    id=config_node_id,
                    etag=wrappers.StringValue(value=etag),
                    display_name=wrappers.StringValue(value=display_name),
                    description=wrappers.StringValue(value=description),
                    authorization_policy_config= authorization_policy_config
                )
            )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def authorization_policy_config(self, policy, status, tags=[]):
    """
    create AuthorizationPolicyConfig
    :param self:
    :param policy: JSON string format
    :param status: AuthorizationPolicyConfig.Status
    :param tags: list of strings
    :return: AuthorizationPolicyConfig object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        policy_config = model_pb2.AuthorizationPolicyConfig(
            policy=str(policy),
            status=status,
            tags=tags
            )
        return policy_config
    except Exception as exception:
        return logger.logger_error(exception)


def create_consent_config_node(self,
                               location,
                               name,
                               display_name,
                               description,
                               consent_config):
    """
    create consent configuration
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param consent_config: ConsentConfiguration object
    :return: deserialized CreateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                consent_config=consent_config
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def update_consent_config_node(self,
                               config_node_id,
                               etag,
                               display_name,
                               description,
                               consent_config):
    """
    update consent configuration
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param consent_config: ConsentConfiguration object
    :return: deserialized UpdateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateConfigNode(
            pb2.UpdateConfigNodeRequest(
                id=config_node_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                consent_config= consent_config
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def consent_config(self,
                   purpose,
                   data_points,
                   application_id,
                   validity_period,
                   revoke_after_use=False,
                   token_status=3):
    """
    create ConsentConfiguration
    :param self:
    :param purpose: string max_len: 1024
    :param data_points: list
    :param application_id: gid min_len:22, max_len: 254, pattern:"^[A-Za-z0-9-_:]{22,254}$"
    :param validity_period: int minimum value is 1 day and the maximum value is 2 years
    :param revoke_after_use: bool
    :param token_status Enum ExternalTokenStatus
    :return: ConsentConfiguration object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if data_points:
            data_points = self.validate_data_points(data_points)
        token_status = self.validate_token_status(token_status)
        return model_pb2.ConsentConfiguration(
            purpose=purpose,
            data_points=data_points,
            application_id=application_id,
            validity_period=validity_period,
            revoke_after_use=revoke_after_use,
            token_status=token_status
        )
    except Exception as exception:
        return logger.logger_error(exception)


def create_token_introspect_config_node(self,
                                        location,
                                        name,
                                        display_name,
                                        description,
                                        token_introspect_config):
    """
    create token introspect config
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param token_introspect_config: TokenIntrospectConfig object
    :return: deserialized CreateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                token_introspect_config=token_introspect_config
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def update_token_introspect_config_node(self,
                                        config_node_id,
                                        etag,
                                        display_name,
                                        description,
                                        token_introspect_config):
    """
    update token introspect config
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param token_introspect_config: TokenIntrospectConfig object
    :return: deserialized UpdateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateConfigNode(
            pb2.UpdateConfigNodeRequest(
                id=config_node_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                token_introspect_config= token_introspect_config
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def token_introspect_config(self,
                            token_matcher,
                            validation,
                            claims_mapping,
                            ikg_node_type,
                            perform_upsert=False):
    """
    create TokenIntrospectConfig
    :param self:
    :param token_matcher: string max_len: 1024
    :param validation: list
    :param claims_mapping: gid min_len:22, max_len: 254, pattern:"^[A-Za-z0-9-_:]{22,254}$"
    :param ikg_node_type: int minimum value is 1 day and the maximum value is 2 years
    :param perform_upsert: bool
    :return: TokenIntrospectConfig object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        claims_mapping_tmp = {}
        if claims_mapping:
            for k, v in claims_mapping.items():
                claims_mapping_tmp[k] = model_pb2.TokenIntrospectConfig.Claim(selector=v)
        if token_matcher:
            if token_matcher["jwt"]:
                jwt = model_pb2.TokenIntrospectConfig.JWT(
                    issuer=token_matcher["jwt"].issuer,
                    audience=token_matcher["jwt"].audience
                )
            elif token_matcher["opaque"]:
                opaque = model_pb2.TokenIntrospectConfig.Opaque()
            else:
                raise TypeError("token_matcher must be JWT or Opaque")
        if validation:
            if validation["offline"] and token_matcher["jwt"]:
                offline = model_pb2.TokenIntrospectConfig.Offline(
                    public_jwks=[pj for pj in validation["offline"].public_jwks]
                )
                return model_pb2.TokenIntrospectConfig(
                    claims_mapping=claims_mapping_tmp,
                    ikg_node_type=str(ikg_node_type),
                    perform_upsert=perform_upsert,
                    jwt=jwt,
                    offline=offline
                )
            elif validation["online"]:
                online = model_pb2.TokenIntrospectConfig.Online(
                    userinfo_endpoint=validation["online"].userinfo_endpoint,
                    cache_ttl=validation["online"].cache_ttl
                )
                if opaque:
                    return model_pb2.TokenIntrospectConfig(
                        claims_mapping=claims_mapping_tmp,
                        ikg_node_type=str(ikg_node_type),
                        perform_upsert=perform_upsert,
                        opaque=opaque,
                        online=online
                    )
                else:
                    return model_pb2.TokenIntrospectConfig(
                        claims_mapping=claims_mapping_tmp,
                        ikg_node_type=str(ikg_node_type),
                        perform_upsert=perform_upsert,
                        jwt=jwt,
                        online=online
                    )
            else:
                raise TypeError("validation must be Offline + JWT or Online")
    except Exception as exception:
        return logger.logger_error(exception)


def create_external_data_resolver_config_node(self,
                                              location,
                                              name,
                                              display_name,
                                              description,
                                              external_data_resolver_config):
    """
    create external data resolver config node
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param external_data_resolver_config: ExternalDataResolverConfig object
    :return: deserialized CreateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        valid = True
        if external_data_resolver_config and isinstance(external_data_resolver_config, model_pb2.ExternalDataResolverConfig):
            if external_data_resolver_config.method:
                valid = self.validate_external_data_resolver_method(external_data_resolver_config.method)
            if valid and external_data_resolver_config.request_type:
                valid = self.validate_external_data_resolver_content_type(external_data_resolver_config.request_type)
            if valid and external_data_resolver_config.response_type:
                valid = self.validate_external_data_resolver_content_type(external_data_resolver_config.response_type)
        else:
            raise TypeError("ExternalDataResolverConfig must be an object")
            valid = False

        if valid:
            response = self.stub.CreateConfigNode(
                pb2.CreateConfigNodeRequest(
                    location=location,
                    name=name,
                    display_name=wrappers.StringValue(value=display_name),
                    description=wrappers.StringValue(value=description),
                    external_data_resolver_config=external_data_resolver_config
                )
            )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def update_external_data_resolver_config_node(self,
                                              config_node_id,
                                              etag,
                                              display_name,
                                              description,
                                              external_data_resolver_config):
    """
    update external data resolver
    :param self:
    :param config_node_id: string gid id
    :param display_name: string
    :param description: string
    :param external_data_resolver_config: ExternalDataResolverConfig object
    :return: deserialized UpdateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        valid = True
        if external_data_resolver_config and isinstance(external_data_resolver_config, model_pb2.ExternalDataResolverConfig):
            if external_data_resolver_config.method:
                valid = self.validate_external_data_resolver_method(external_data_resolver_config.method)
            if valid and external_data_resolver_config.request_type:
                valid = self.validate_external_data_resolver_content_type(external_data_resolver_config.request_type)
            if valid and external_data_resolver_config.response_type:
                valid = self.validate_external_data_resolver_content_type(external_data_resolver_config.response_type)
        else:
            raise TypeError("ExternalDataResolverConfig must be an object")
            valid = False

        if valid:
            response = self.stub.UpdateConfigNode(
                pb2.UpdateConfigNodeRequest(
                    id=config_node_id,
                    etag=wrappers.StringValue(value=etag),
                    display_name=wrappers.StringValue(value=display_name),
                    description=wrappers.StringValue(value=description),
                    external_data_resolver_config=external_data_resolver_config
                )
            )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def external_data_resolver_config(self,
                                  url,
                                  method,
                                  headers=None,
                                  request_type=None,
                                  request_payload=None,
                                  response_type=None,
                                  response_selector=None):
    """
    create ExternalDataResolverConfig
    :param self:
    :param url: Full URL to endpoint that will be called
    :param method: [GET, POST, PUT, PATCH]
    :param headers: map<string, ExternalDataResolverConfig.Header>
    :param request_type: ExternalDataResolverConfig.ContentType
    :param request_payload: to be sent to the endpoint, in proper format based on request type
    :param response_type: ExternalDataResolverConfig.ContentType
    :param response_selector: Selector to extract data from response
    :return: ExternalDataResolverConfig object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        external_config = model_pb2.ExternalDataResolverConfig(
            url=str(url),
            method=method,
            headers=headers,
            request_type=request_type,
            request_payload=request_payload,
            response_type=response_type,
            response_selector=response_selector
            )
        return external_config
    except Exception as exception:
        return logger.logger_error(exception)


def create_entity_matching_pipeline_config_node(self,
                                              location,
                                              name,
                                              display_name,
                                              description,
                                              entity_matching_pipeline_config):
    """
    create entity matching pipeline config node
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param entity_matching_pipeline_config: EntityMatchingPipelineConfig object
    :return: deserialized CreateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if entity_matching_pipeline_config and not isinstance(
            entity_matching_pipeline_config,
            model_pb2.EntityMatchingPipelineConfig):
            raise TypeError("EntityMatchingPipelineConfig must be an object")

        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                entity_matching_pipeline_config=entity_matching_pipeline_config
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def update_entity_matching_pipeline_config_node(self,
                                              config_node_id,
                                              etag,
                                              display_name,
                                              description,
                                              entity_matching_pipeline_config):
    """
    update entity matching pipeline
    :param self:
    :param config_node_id: string gid id
    :param display_name: string
    :param description: string
    :param entity_matching_pipeline_config: EntityMatchingPipelineConfig object
    :return: deserialized UpdateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if entity_matching_pipeline_config and not isinstance(
            entity_matching_pipeline_config,
            model_pb2.EntityMatchingPipelineConfig):
            raise TypeError("EntityMatchingPipelineConfig must be an object")
        response = self.stub.UpdateConfigNode(
            pb2.UpdateConfigNodeRequest(
                id=config_node_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                entity_matching_pipeline_config=entity_matching_pipeline_config
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def entity_matching_pipeline_config(self,
                                  node_filter=None,
                                  similarity_score_cutoff=None,
                                  property_mapping_status=None,
                                  property_mapping_message=None,
                                  entity_matching_status=None,
                                  entity_matching_message=None,
                                  property_mappings=None,
                                  rerun_interval=None,
                                  last_run_time=None,
                                  report_url=None,
                                  report_type=None):

    """
    create EntityMatchingPipelineConfig
    :param self:
    :param node_filter: EntityMatchingPipelineConfig.NodeFilter object
    :param similarity_score_cutoff: float
    :param property_mapping_status: EntityMatchingPipelineConfig.Status object
    :param property_mapping_message: google.protobuf.StringValue
    :param entity_matching_status: EntityMatchingPipelineConfig.Status
    :param entity_matching_message: google.protobuf.StringValue
    :param property_mappings: array of EntityMatchingPipelineConfig.PropertyMapping
    :param rerun_interval: string
    :param last_run_time: google.protobuf.Timestamp
    :param report_url: google.protobuf.StringValue
    :param report_type: google.protobuf.StringValue
    :return: EntityMatchingPipelineConfig object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        property_mapping_status = self.validate_entity_matching_status(property_mapping_status)
        entity_matching_status = self.validate_entity_matching_status(entity_matching_status)
        external_config = model_pb2.EntityMatchingPipelineConfig(
            node_filter = node_filter,
            similarity_score_cutoff=similarity_score_cutoff,
            property_mapping_status=property_mapping_status,
            property_mapping_message=wrappers.StringValue(value=property_mapping_message),
            entity_matching_status=entity_matching_status,
            entity_matching_message=wrappers.StringValue(value=entity_matching_message),
            property_mappings=property_mappings,
            rerun_interval=rerun_interval,
            last_run_time=last_run_time,
            report_url=wrappers.StringValue(value=report_url),
            report_type=wrappers.StringValue(value=report_type)
            )
        return external_config
    except Exception as exception:
        return logger.logger_error(exception)


def entity_matching_pipeline_config_create(self,node_filter):
    """
    create EntityMatchingPipelineConfig
    :param self:
    :param node_filter: EntityMatchingPipelineConfig.NodeFilter object
    :return: EntityMatchingPipelineConfig object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        external_config = model_pb2.EntityMatchingPipelineConfig(
            node_filter = node_filter,
            )
        return external_config
    except Exception as exception:
        return logger.logger_error(exception)


def entity_matching_pipeline_config_update(self, similarity_score_cutoff):
    """
    create EntityMatchingPipelineConfig
    :param self:
    :param similarity_score_cutoff: float
    :return: EntityMatchingPipelineConfig object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        external_config = model_pb2.EntityMatchingPipelineConfig(
            similarity_score_cutoff = similarity_score_cutoff,
            )
        return external_config
    except Exception as exception:
        return logger.logger_error(exception)


def validate_data_points(self, data_points):
    """
    validate data_points requirement
    :param self:
    :param data_points: array
    :return: reduces to unique list
    """
    try:
        return list(dict.fromkeys(data_points))
    except Exception as exception:
        return logger.logger_error(exception)


def validate_token_status(self, token_status):
    """
    validate token_status requirement
    :param self:
    :param token_status: number
    :return: token_status or error
    """
    try:
        statuses = [s.value for s in ExternalTokenStatus]
        if token_status and token_status not in statuses:
            raise TypeError("token_status must be a member of ExternalTokenStatus")
        return token_status
    except Exception as exception:
        return logger.logger_error(exception)


def validate_authorization_policy_status(self, status):
    """
    validate status
    :param self:
    :param status: string
    :return: True if valid or raises error
    """
    try:
        statuses = [s.value for s in Status]
        if status not in statuses:
            raise TypeError("status must be a member of AuthorizationPolicyConfig.Status")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_external_data_resolver_method(self, method):
    """
    validate method
    :param self:
    :param method: string
    :return: True if valid or raises error
    """
    try:
        methods = ["GET", "POST", "PUT", "PATCH"]
        if method not in methods:
            raise TypeError("method must be in [GET, POST, PUT, PATCH]")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_external_data_resolver_content_type(self, content_type):
    """
    validate content_type
    :param selfcontent_type:
    :param content_type: string
    :return: True if valid or raises error
    """
    try:
        content_types = [c.value for c in ContentType]
        if content_type not in content_types:
            raise TypeError("content_type must be a member of ExternalDataResolverConfig.ContentType")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_entity_matching_status(self, status):
    """
    validate entity matching status requirement
    :param self:
    :param status: number
    :return: status, none  or error
    """
    try:
        if not status:
            return None
        statuses = [s.value for s in EntityMatchingStatus]
        if status and status not in statuses:
            raise TypeError("status must be a member of EntityMatchingPipelineConfig.Status")
        return status
    except Exception as exception:
        return logger.logger_error(exception)


def list_config_node_versions(self, id_config_node):
    """
    list config nodes versions of the specified config node
    :param self:
    :param id_config_node: string gid id
    :return: list of deserialized ConfigNode instances
    """
    sys.excepthook = logger.handle_excepthook
    try:
        list_config_nodes = self.stub.ListConfigNodeVersions(
            pb2.ListConfigNodeVersionsRequest(
                id=id_config_node
            )
        )
        if not list_config_nodes:
            return None
        res = [ConfigNode.deserialize(config_node) for config_node in list_config_nodes.config_nodes]
        return res
    except Exception as exception:
        return logger.logger_error(exception)

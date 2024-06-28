from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_config_node import CreateConfigNode
from indykite_sdk.model.update_config_node import UpdateConfigNode
from indykite_sdk.model.config_node import ConfigNode
from indykite_sdk.model.authorization_policy_config_status import Status
from indykite_sdk.indykite.config.v1beta1 import model_pb2
import sys
import indykite_sdk.utils.logger as logger


def read_config_node(self, config_node_id, bookmarks=[], version=0):
    """
    read a specific config node
    :param self:
    :param config_node_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :param version: int
    :return: deserialized ConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadConfigNode(
            pb2.ReadConfigNodeRequest(
                id=str(config_node_id),
                bookmarks=bookmarks,
                version=version
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return ConfigNode.deserialize(response.config_node)


def delete_config_node(self, config_node_id, etag, bookmarks=[]):
    """
    delete a specific config node
    :param self:
    :param config_node_id: string gid id
    :param etag: etag
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: DeleteConfigNodeResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteConfigNode(
            pb2.DeleteConfigNodeRequest(
                id=str(config_node_id),
                etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
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
                                            authorization_policy_config,
                                            bookmarks=[]):
    """
    create authorization policy
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param authorization_policy_config: AuthorizationPolicyConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
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
                    authorization_policy_config=authorization_policy_config,
                    bookmarks=bookmarks
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
                                            authorization_policy_config,
                                            bookmarks=[]):
    """
    update authorization policy
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param authorization_policy_config: AuthorizationPolicyConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
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
                    authorization_policy_config= authorization_policy_config,
                    bookmarks=bookmarks
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
                               consent_config,
                               bookmarks=[]):
    """
    create consent configuration
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param consent_config: ConsentConfiguration object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
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
                consent_config=consent_config,
                bookmarks=bookmarks
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
                               consent_config,
                               bookmarks=[]):
    """
    update consent configuration
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param consent_config: ConsentConfiguration object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
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
                consent_config= consent_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def consent_config(self, purpose, data_points, application_id, validity_period, revoke_after_use=False):
    """
    create ConsentConfiguration
    :param self:
    :param purpose: string max_len: 1024
    :param data_points: list
    :param application_id: gid min_len:22, max_len: 254, pattern:"^[A-Za-z0-9-_:]{22,254}$"
    :param validity_period: int minimum value is 1 day and the maximum value is 2 years
    :param revoke_after_use: bool
    :return: ConsentConfiguration object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if data_points:
            data_points = self.validate_data_points(data_points)
        return model_pb2.ConsentConfiguration(
            purpose=purpose,
            data_points=data_points,
            application_id=application_id,
            validity_period=validity_period,
            revoke_after_use=revoke_after_use
        )
    except Exception as exception:
        return logger.logger_error(exception)


def create_token_introspect_config_node(self,
                                        location,
                                        name,
                                        display_name,
                                        description,
                                        token_introspect_config,
                                        bookmarks=[]):
    """
    create token introspect config
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param token_introspect_config: TokenIntrospectConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
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
                token_introspect_config=token_introspect_config,
                bookmarks=bookmarks
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
                                        token_introspect_config,
                                        bookmarks=[]):
    """
    update token introspect config
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param token_introspect_config: TokenIntrospectConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
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
                token_introspect_config= token_introspect_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def token_introspect_config(self, token_matcher, validation, claims_mapping, ikg_node_type, perform_upsert=False):
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

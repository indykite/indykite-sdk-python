import json
from indykite_sdk.model.authorization_policy_config_status import Status


class AuthorizationPolicyConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]
        authorization_policy_config = AuthorizationPolicyConfig(
            policy=json.loads(message_config.policy)
        )
        if "status" in fields:
            statuses = [s.value for s in Status]
            if message_config.status and message_config.status not in statuses:
                raise TypeError("status must be a member of AuthorizationPolicyConfig.Status")
            authorization_policy_config.status = message_config.status
        if "tags" in fields:
            authorization_policy_config.tags = [
                str(t)
                for t in message_config.tags
            ]
        return authorization_policy_config

    def __init__(self, policy, status=None, tags=[]):

        self.policy = policy
        self.status = status
        self.tags = tags




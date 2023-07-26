from indykite_sdk.model.username_policy import UsernamePolicy


class ApplicationSpaceConfig:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        app_space_config = ApplicationSpaceConfig()

        if "default_tenant_id" in fields:
            app_space_config.default_tenant_id = str(message.default_tenant_id)

        if "default_auth_flow_id" in fields:
            app_space_config.default_auth_flow_id = str(message.default_auth_flow_id)

        if "default_email_service_id" in fields:
            app_space_config.default_email_service_id = str(message.default_email_service_id)

        if "unique_property_constraints" in fields:
            unique_property_constraints = {}
            for k, v in message.unique_property_constraints.items():
                unique_property_constraints[k] = UniquePropertyConstraint.deserialize(v)
            app_space_config.unique_property_constraints = unique_property_constraints

        if "username_policy" in fields:
            app_space_config.username_policy = UsernamePolicy.deserialize(message.username_policy)
        return app_space_config

    def __init__(self, default_tenant_id=None, default_auth_flow_id=None, default_email_service_id=None):
        self.default_tenant_id = default_tenant_id
        self.default_auth_flow_id = default_auth_flow_id
        self.default_email_service_id = default_email_service_id
        self.unique_property_constraints = None
        self.username_policy = None


class UniquePropertyConstraint:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        unique_property_constraints = UniquePropertyConstraint()
        if "tenant_unique" in fields:
            unique_property_constraints.tenant_unique = bool(message.tenant_unique)
        if "canonicalization" in fields:
            unique_property_constraints.canonicalization = [
                str(t)
                for t in message.canonicalization
            ]
        return unique_property_constraints

    def __init__(self, tenant_unique=False, canonicalization=[]):
        self.tenant_unique = tenant_unique
        self.canonicalization = canonicalization

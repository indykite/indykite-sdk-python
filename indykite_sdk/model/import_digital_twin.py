
class ImportDigitalTwin:
    def __init__(self, tenant_id, kind, state, password):
        self.id = None
        self.tenant_id = tenant_id
        self.kind = kind
        self.state = state
        self.tags = None
        self.password = password
        self.provider_user_info = None
        self.properties = None
        self.metadata = None

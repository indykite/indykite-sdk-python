from indykite_sdk.model.trust_score_profile_dimension_name import Name

class TrustScoreDimension:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]
        names = [n.value for n in Name]
        if message_config.name and message_config.name not in names:
            raise TypeError("name must be a member of TrustScoreDimension.Name")
        if "name" in fields:
            trust_score_dimension = TrustScoreDimension(
                name=message_config.name,
                weight=message_config.weight
            )
            return trust_score_dimension
        raise TypeError("TrustScoreDimension.Name is mandatory")

    def __init__(self,
                 name,
                 weight):

        self.name = name
        self.weight = weight

from indykite_sdk.utils import timestamp_to_date
from indykite_sdk.model.oauth2_application_config import OAuth2ApplicationConfig


class OAuth2Application:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        oauth2_application = OAuth2Application(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag),
            str(message.customer_id),
            str(message.app_space_id),
            str(message.oauth2_provider_id)
        )

        if "create_time" in fields:
            oauth2_application.create_time = timestamp_to_date(message.create_time)

        if "update_time" in fields:
            oauth2_application.update_time = timestamp_to_date(message.update_time)

        if "destroy_time" in fields:
            oauth2_application.destroy_time = timestamp_to_date(message.destroy_time)

        if "delete_time" in fields:
            oauth2_application.delete_time = timestamp_to_date(message.delete_time)

        if "description" in fields:
            oauth2_application.description = str(message.description)

        if "config" in fields:
            oauth2_application.config = OAuth2ApplicationConfig.deserialize(message.config)

        if "created_by" in fields:
            oauth2_application.created_by = str(message.created_by)

        if "updated_by" in fields:
            oauth2_application.updated_by = str(message.updated_by)

        return oauth2_application

    def __init__(self, id, name, display_name, etag, customer_id, app_space_id, oauth2_provider_id):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.etag = etag
        self.customer_id = customer_id
        self.app_space_id = app_space_id
        self.oauth2_provider_id = oauth2_provider_id
        self.create_time = None
        self.update_time = None
        self.destroy_time = None
        self.delete_time = None
        self.description = None
        self.config = None
        self.created_by = None
        self.updated_by = None

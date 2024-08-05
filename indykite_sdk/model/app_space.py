from indykite_sdk.utils import timestamp_to_date
from indykite_sdk.model.ikg_status import AppSpaceIKGStatus


class ApplicationSpace:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        application_space = ApplicationSpace(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag),
            str(message.customer_id)
        )

        if "create_time" in fields:
            application_space.create_time = timestamp_to_date(message.create_time)

        if "update_time" in fields:
            application_space.update_time = timestamp_to_date(message.update_time)

        if "destroy_time" in fields:
            application_space.destroy_time = timestamp_to_date(message.destroy_time)

        if "delete_time" in fields:
            application_space.delete_time = timestamp_to_date(message.delete_time)

        if "description" in fields:
            application_space.description = str(message.description)

        if "created_by" in fields:
            application_space.created_by = str(message.created_by)

        if "updated_by" in fields:
            application_space.updated_by = str(message.updated_by)

        if "ikg_status" in fields:
            statuses = [s.value for s in AppSpaceIKGStatus]
            if message.ikg_status and message.ikg_status not in statuses:
                raise TypeError("status must be a member of AppSpace.AppSpaceIKGStatus")
            application_space.ikg_status = message.ikg_status

        if "region" in fields:
            values = ["europe-west1", "us-east1"]
            if message.region and message.region not in values:
                raise TypeError("region must be europe-west1 or us-east1")
            application_space.region = message.region

        return application_space

    def __init__(self, id, name, display_name, etag, customer_id):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.etag = etag
        self.customer_id = customer_id
        self.create_time = None
        self.update_time = None
        self.destroy_time = None
        self.delete_time = None
        self.description = None
        self.created_by = None
        self.updated_by = None
        self.ikg_status = None
        self.region = None

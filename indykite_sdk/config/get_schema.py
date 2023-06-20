from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.get_schema import GetSchemaHelpers
import sys
import indykite_sdk.utils.logger as logger


def get_schema_helpers(self):
    """
    get knowledge graph schema helpers
    :param self:
    :return: GetSchemaHelpersResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.GetSchemaHelpers(
            pb2.GetSchemaHelpersRequest()
        )
        if not response:
            return None
        return GetSchemaHelpers.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)

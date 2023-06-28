from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.application_agent import ApplicationAgent
from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_application_agent import CreateApplicationAgent
from indykite_sdk.model.update_application_agent import UpdateApplicationAgent
import sys
import indykite_sdk.utils.logger as logger


def read_application_agent_by_id(self, application_agent_id, bookmarks=[]):
    """
    get an ApplAgent object with an id
    :param self:
    :param application_agent_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: ApplicationAgent object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadApplicationAgent(
            pb2.ReadApplicationAgentRequest(
                id=str(application_agent_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return ApplicationAgent.deserialize(response.application_agent)


def read_application_agent_by_name(self, app_space_id, application_agent_name, bookmarks=[]):
    """
    get an ApplAgent object with a name
    :param self:
    :param app_space_id: string gid id
    :param application_agent_name: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: AppAgent object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadApplicationAgent(
            pb2.ReadApplicationAgentRequest(
                name=UniqueNameIdentifier(
                    location=app_space_id,
                    name=application_agent_name
                ),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return ApplicationAgent.deserialize(response.application_agent)


def create_application_agent(self, application_id, name, display_name, description="", bookmarks=[]):
    """
    create an AppAgent
    :param self:
    :param application_id: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateApplicationAgentResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateApplicationAgent(
            pb2.CreateApplicationAgentRequest(
                application_id=application_id,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateApplicationAgent.deserialize(response, application_id, name)


def update_application_agent(self, application_agent_id, etag, display_name, description="", bookmarks=[]):
    """
    update existing AppAgent
    :param self:
    :param application_agent_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateApplicationAgentResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateApplicationAgent(
            pb2.UpdateApplicationAgentRequest(
                id=application_agent_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateApplicationAgent.deserialize(response)


def list_application_agents(self, app_space_id, match=[], bookmarks=[]):
    """
    list App which match exact name in match param
    :param self:
    :param app_space_id: string gid id
    :param match: list of strings
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: ListApplicationAgentResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        streams = self.stub.ListApplicationAgents(
            pb2.ListApplicationAgentsRequest(
                app_space_id=app_space_id,
                match=match,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)
    if not streams:
        return None

    responses = []
    try:
        for response in streams:
            responses.append(response)
    except Exception as exception:
        return logger.logger_error(exception)
    return responses


def delete_application_agent(self, application_agent_id, etag, bookmarks):
    """
    delete an AppAgent
    :param self:
    :param application_agent_id: string gid id
    :param etag: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: DeleteApplicationResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteApplicationAgent(
            pb2.DeleteApplicationAgentRequest(
                id=application_agent_id,
                etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response

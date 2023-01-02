from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.application_agent import ApplicationAgent
from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_application_agent import CreateApplicationAgent
from indykite_sdk.model.update_application_agent import UpdateApplicationAgent


def get_application_agent_by_id(self, application_agent_id):
    try:
        response = self.stub.ReadApplicationAgent(
            pb2.ReadApplicationAgentRequest(
                id=str(application_agent_id)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return ApplicationAgent.deserialize(response.application_agent)


def get_application_agent_by_name(self, app_space_id, application_agent_name):

    try:
        response = self.stub.ReadApplicationAgent(
            pb2.ReadApplicationAgentRequest(
                name=UniqueNameIdentifier(location = app_space_id, name = application_agent_name)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return ApplicationAgent.deserialize(response.application_agent)


def create_application_agent(self, application_id, name, display_name, description="", bookmarks=[]):

    try:
        response = self.stub.CreateApplicationAgent(
            pb2.CreateApplicationAgentRequest(
                application_id=application_id, name=name, display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return CreateApplicationAgent.deserialize(response)


def update_application_agent(self, application_agent_id, etag, display_name, description="", bookmarks=[]):

    try:
        response = self.stub.UpdateApplicationAgent(
            pb2.UpdateApplicationAgentRequest(
                id=application_agent_id,etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return UpdateApplicationAgent.deserialize(response)


def list_application_agents(self, app_space_id, match=[], bookmarks=[]):

    try:
        streams = self.stub.ListApplicationAgents(
            pb2.ListApplicationAgentsRequest(
                app_space_id=app_space_id,match=match,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not streams:
        return None

    responses = []
    try:
        for response in streams:
            responses.append(response)
    except Exception as exception:
        print(exception)
        return None

    return responses


def delete_application_agent(self, application_agent_id, etag, bookmarks):

    try:
        response = self.stub.DeleteApplicationAgent(
            pb2.DeleteApplicationAgentRequest(
                id=application_agent_id, etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response

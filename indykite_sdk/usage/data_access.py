"""
Commandline interface for making an API request with the SDK.
"""
import argparse
from indykite_sdk.tda import DataAccessClient
from indykite_sdk import api_helper


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def main():
    # Create parent parser
    parser = argparse.ArgumentParser(description="DataAccess client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # tda
    grant_consent_by_id_parser = subparsers.add_parser("grant_consent_by_id")
    grant_consent_by_id_parser.add_argument("user_id",
                                            help="Identity node gid (node with is_identity equal True)")
    grant_consent_by_id_parser.add_argument("consent_id",
                                            help="Consent config node gid")

    grant_consent_by_external_id_parser = subparsers.add_parser("grant_consent_by_external_id")
    grant_consent_by_external_id_parser.add_argument(
        "external_id",
        help="Identity node external_id (node with is_identity equal True)")
    grant_consent_by_external_id_parser.add_argument("type",
                                                     help="Identity node type (node with is_identity equal True)")
    grant_consent_by_external_id_parser.add_argument("consent_id",
                                                     help="Consent config node gid")

    grant_consent_by_property_parser = subparsers.add_parser("grant_consent_by_property")
    grant_consent_by_property_parser.add_argument(
        "type",
        help="Identity node property type (node with is_identity equal True)")
    grant_consent_by_property_parser.add_argument(
        "value",
        help="Identity node property value (node with is_identity equal True)")
    grant_consent_by_property_parser.add_argument("consent_id",
                                                  help="Consent config node gid")

    revoke_consent_by_id_parser = subparsers.add_parser("revoke_consent_by_id")
    revoke_consent_by_id_parser.add_argument("user_id",
                                             help="Identity node gid (node with is_identity equal True)")
    revoke_consent_by_id_parser.add_argument("consent_id",
                                             help="Consent config node gid")

    data_access_parser = subparsers.add_parser("data_access")
    data_access_parser.add_argument("consent_id",
                                            help="Consent config node gid")
    data_access_parser.add_argument("application_id",
                                            help="Application gid")
    data_access_parser.add_argument("user_id",
                                            help="Identity node gid (node with is_identity equal True)")

    list_consents_parser = subparsers.add_parser("list_consents")
    list_consents_parser.add_argument("user_id",
                                      help="Identity node gid (node with is_identity equal True)")
    list_consents_parser.add_argument("application_id",
                                            help="Application gid")

    args = parser.parse_args()
    command = args.command

    if command == "grant_consent_by_id":
        """shell
            python3 data_access.py grant_consent_by_id
        """
        # send a request to the DataAccess API with user_id, consent_id, revoke_after_use parameters
        # and get an empty response in case of success
        # send your own values as arguments
        client_tda = DataAccessClient()
        user_id = args.user_id
        consent_id = args.consent_id
        validity_period = 86400
        user = {"user_id": user_id}
        print(user)
        response = client_tda.grant_consent(user, consent_id, validity_period)
        print(response)
        client_tda.channel.close()

    elif command == "grant_consent_by_external_id":
        """shell
            python3 data_access.py grant_consent_by_external_id
        """
        # send a request to the DataAccess API with user_id, consent_id, revoke_after_use parameters
        # and get an empty response in case of success
        # send your own values as arguments
        client_tda = DataAccessClient()
        external_id = args.external_id
        type = args.type
        consent_id = args.consent_id
        validity_period = 86400
        user = {"external_id": {"external_id": external_id, "type": type}}
        print(user)
        response = client_tda.grant_consent(user, consent_id, validity_period)
        print(response)
        client_tda.channel.close()

    elif command == "grant_consent_by_property":
        """shell
            python3 data_access.py grant_consent_by_property
        """
        # send a request to the DataAccess API with user_id, consent_id, revoke_after_use parameters
        # and get an empty response in case of success
        # send your own values as arguments
        client_tda = DataAccessClient()
        type = args.type
        value = args.value
        consent_id = args.consent_id
        validity_period = 86400
        user = {"property": {"type": type, "value": value}}
        print(user)
        response = client_tda.grant_consent(user, consent_id, validity_period)
        print(response)
        client_tda.channel.close()

    elif command == "revoke_consent_by_id":
        """shell
            python3 data_access.py revoke_consent_by_id
        """
        # send a request to the DataAccess API with user_id, consent_id parameters
        # and get an empty response in case of success
        # send your own values as arguments
        client_tda = DataAccessClient()
        user_id = args.user_id
        consent_id = args.consent_id
        user = {"user_id": user_id}
        response = client_tda.revoke_consent(user, consent_id)
        print(response)
        client_tda.channel.close()

    elif command == "data_access":
        """shell
            python3 data_access.py data_access
        """
        # send a request to the DataAccess API with consent_id, application_id, user_id parameters
        # and get list of nodes in case of success
        # send your own values as arguments
        client_tda = DataAccessClient()
        consent_id = args.consent_id
        user_id = args.user_id
        user = {"user_id": user_id}
        application_id = args.application_id
        responses = client_tda.data_access(consent_id, application_id, user)
        api_helper.print_response(responses)
        client_tda.channel.close()

    elif command == "list_consents":
        """shell
            python3 data_access.py list_consents
        """
        # send a request to the DataAccess API with user_id, application_id parameters
        # and get a list of consent objects in case of success
        # send your own values as arguments
        client_tda = DataAccessClient()
        user_id = args.user_id
        user = {"user_id": user_id}
        application_id = args.application_id
        responses = client_tda.list_consents(user, application_id)
        api_helper.print_response(responses)
        client_tda.channel.close()


if __name__ == '__main__':  # pragma: no cover
    main()

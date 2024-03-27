"""
Commandline interface for making an API request with the SDK.
"""
import argparse
from indykite_sdk.trusted_data.access import TrustedDataAccessClient
from indykite_sdk import api_helper


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def main():
    # Create parent parser
    parser = argparse.ArgumentParser(description="TrustedDataAccess client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # tda
    grant_consent_by_id_parser = subparsers.add_parser("grant_consent_by_id")
    grant_consent_by_id_parser.add_argument("user_id",
                                            help="Identity node gid (node with is_identity equal True)")
    grant_consent_by_id_parser.add_argument("consent_id",
                                            help="Consent config node gid")

    revoke_consent_by_id_parser = subparsers.add_parser("revoke_consent_by_id")
    revoke_consent_by_id_parser.add_argument("user_id",
                                             help="Identity node gid (node with is_identity equal True)")
    revoke_consent_by_id_parser.add_argument("consent_id",
                                             help="Consent config node gid")

    access_consented_data_parser = subparsers.add_parser("access_consented_data")
    access_consented_data_parser.add_argument("consent_id",
                                              help="Consent config node gid")
    access_consented_data_parser.add_argument("user_id",
                                              help="Identity node gid (node with is_identity equal True)")

    args = parser.parse_args()
    command = args.command

    if command == "grant_consent_by_id":
        """shell
            python3 trusted_data_access.py grant_consent_by_id
        """
        # send a request to the TrustedDataAccess API with user_id, consent_id, revoke_after_use parameters
        # and get an empty response in case of success
        # send your own values as arguments
        client_tda = TrustedDataAccessClient()
        user_id = args.user_id
        consent_id = args.consent_id
        revoke_after_use = False
        response = client_tda.grant_consent_by_id(user_id, consent_id, revoke_after_use)
        print(response)
        client_tda.channel.close()

    elif command == "revoke_consent_by_id":
        """shell
            python3 trusted_data_access.py revoke_consent_by_id
        """
        # send a request to the TrustedDataAccess API with user_id, consent_id parameters
        # and get an empty response in case of success
        # send your own values as arguments
        client_tda = TrustedDataAccessClient()
        user_id = args.user_id
        consent_id = args.consent_id
        response = client_tda.revoke_consent_by_id(user_id, consent_id)
        print(response)
        client_tda.channel.close()

    elif command == "access_consented_data":
        """shell
            python3 trusted_data_access.py access_consented_data
        """
        # send a request to the TrustedDataAccess API with user_id, consent_id parameters
        # and get an empty response in case of success
        # send your own values as arguments
        client_tda = TrustedDataAccessClient()
        consent_id = args.consent_id
        user_id = args.user_id
        responses = client_tda.revoke_consent_by_id(consent_id, user_id)
        api_helper.print_response(responses)
        client_tda.channel.close()


if __name__ == '__main__':  # pragma: no cover
    main()

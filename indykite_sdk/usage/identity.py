"""
Commandline interface for making an API request with the SDK.
"""
import argparse
import json
import uuid
from datetime import datetime
from indykite_sdk.identity import IdentityClient
from indykite_sdk import api_helper


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def main():
    # Create parent parser
    parser = argparse.ArgumentParser(description="Identity client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # INTROSPECT
    introspect_parser = subparsers.add_parser("introspect")
    introspect_parser.add_argument("user_token", help="JWT bearer token")

    # ENRICH-TOKEN
    enrich_token = subparsers.add_parser("enrich-token")
    enrich_token.add_argument("user_token", help="JWT bearer token")
    enrich_token.add_argument("--token_claims", nargs='*',
                              help="Token claims to add (--token_claims key=value)", action=ParseKwargs)
    enrich_token.add_argument("--session_claims", nargs='*',
                              help="Session claims to add (--session_claims key=value)", action=ParseKwargs)

    # create_consent
    create_consent_parser = subparsers.add_parser("create_consent")
    create_consent_parser.add_argument("pii_processor_id", help="ID of OAuth2 Application")
    create_consent_parser.add_argument("pii_principal_id",
                                       help="Identity node gid (node with is_identity equal True)")

    # list_consents
    list_consents_parser = subparsers.add_parser("list_consents")
    list_consents_parser.add_argument("pii_principal_id",
                                      help="Identity node gid (node with is_identity equal True)")

    # revoke_consent
    revoke_consent_parser = subparsers.add_parser("revoke_consent")
    revoke_consent_parser.add_argument("pii_principal_id",
                                       help="Identity node gid (node with is_identity equal True)")
    revoke_consent_parser.add_argument("consent_ids", nargs='*',
                                       help="List of consent ids separated by space")

    # check_oauth2_consent_challenge
    check_oauth2_consent_challenge_parser = subparsers.add_parser("check_oauth2_consent_challenge")
    check_oauth2_consent_challenge_parser.add_argument("challenge",
                                                       help="Consent challenge extracted from consent URL")

    # create_oauth2_consent_verifier_approval
    create_oauth2_consent_verifier_approval_parser = subparsers.add_parser("create_oauth2_consent_verifier_approval")
    create_oauth2_consent_verifier_approval_parser.add_argument("consent_challenge",
                                                                help="Consent challenge extracted from consent URL")
    create_oauth2_consent_verifier_approval_parser.add_argument("access_token")

    # create_oauth2_consent_verifier_denial
    create_oauth2_consent_verifier_denial_parser = subparsers.add_parser("create_oauth2_consent_verifier_denial")
    create_oauth2_consent_verifier_denial_parser.add_argument("consent_challenge",
                                                              help="Consent challenge extracted from consent URL")

    # create_email_invitation
    create_email_invitation = subparsers.add_parser("create_email_invitation")
    create_email_invitation.add_argument("tenant_id", help="gid ID of the tenant")
    create_email_invitation.add_argument("email", help="invitee's email")

    # create_email_invitation_with_date
    create_email_invitation_with_date = subparsers.add_parser("create_email_invitation_with_date")
    create_email_invitation_with_date.add_argument("tenant_id", help="gid ID of the tenant")
    create_email_invitation_with_date.add_argument("email", help="invitee's email")

    # create_mobile_invitation
    create_mobile_invitation = subparsers.add_parser("create_mobile_invitation")
    create_mobile_invitation.add_argument("tenant_id", help="gid ID of the tenant")
    create_mobile_invitation.add_argument("mobile", help="invitee's mobile")

    # check_invitation_state
    check_invitation_state = subparsers.add_parser("check_invitation_state")
    check_invitation_state.add_argument("reference_id", help="external ID of the invitation reference")

    # resend_invitation
    resend_invitation = subparsers.add_parser("resend_invitation")
    resend_invitation.add_argument("reference_id", help="external ID of the invitation reference")

    # cancel_invitation
    cancel_invitation = subparsers.add_parser("cancel_invitation")
    cancel_invitation.add_argument("reference_id", help="external ID of the invitation reference")

    args = parser.parse_args()
    command = args.command

    if command == "introspect":
        """shell
           python3 identity.py introspect USER_TOKEN
        """
        # token_introspect method: to get info on a user token
        client = IdentityClient()
        user_token = args.user_token
        token_info = client.token_introspect(user_token)
        if token_info is not None:
            api_helper.print_response(token_info)
        else:
            print("Invalid token")
        client.channel.close()

    elif command == "enrich-token":
        # enrich_token method: to allow a session and an access token to be enriched with additional data
        # with user token (access token) and token claims (dict) and session claims (dict) as arguments
        client = IdentityClient()
        user_token = args.user_token
        token_claims = args.token_claims
        session_claims = args.session_claims
        response = client.enrich_token(user_token, token_claims, session_claims)
        if response is not None:
            print("Successfully enriched token")
        else:
            print("Invalid token")
        client.channel.close()

    elif command == "create_consent":
        """shell
           python3 identity.py create_consent OAUTH2_APPLICATION_GID IDENTITY_NODE_GID
        """
        # create_consent method: to create a consent to an application (pii_processor_id ID in GID format)
        # given by an identity node (pii_principal_id ID in GID format)
        client = IdentityClient()
        pii_processor_id = args.pii_processor_id
        pii_principal_id = args.pii_principal_id
        properties = ["icecream"]
        consent_response = client.create_consent(pii_processor_id, pii_principal_id, properties)
        if consent_response:
            api_helper.print_response(consent_response)
        else:
            print("Invalid consent response")
        client.channel.close()
        return consent_response

    elif command == "list_consents":
        # list_consents method: to list the consents given by an identity node (pii_principal_id ID in GID format)
        client = IdentityClient()
        pii_principal_id = args.pii_principal_id
        consent_response = client.list_consents(pii_principal_id)
        if consent_response:
            for c in consent_response:
                api_helper.print_response(c)
        else:
            print("Invalid consent response")
        client.channel.close()
        return consent_response

    elif command == "revoke_consent":
        # revoke_consent method: to revoke list of consents (IDs in GID format)
        # given by an identity node (pii_principal_id ID in GID format)
        client = IdentityClient()
        pii_principal_id = args.pii_principal_id
        consent_ids = args.consent_ids
        consent_response = client.revoke_consent(pii_principal_id, consent_ids)
        if consent_response:
            api_helper.print_response(consent_response)
        else:
            print("Invalid consent response")
        client.channel.close()
        return consent_response

    elif command == "check_oauth2_consent_challenge":
        # check_oauth2_consent_challenge method: read the Consent Challenge from DB
        # with the code challenge as an argument
        client = IdentityClient()
        challenge = args.challenge
        consent_response = client.check_oauth2_consent_challenge(challenge)
        if consent_response:
            api_helper.print_response(consent_response)
        else:
            print("Invalid consent response")
        client.channel.close()
        return consent_response

    elif command == "create_oauth2_consent_verifier_approval":
        # create_oauth2_consent_verifier_approval method: to create a new ConsentApproval verifier
        client = IdentityClient()
        consent_challenge = args.consent_challenge
        grant_scopes = ["openid", "email", "profile"]
        granted_audiences = []
        # custom claims for jwk (map values to enrich token)
        access_token = json.loads(args.access_token)
        consent_response = client.create_oauth2_consent_verifier_approval(
            consent_challenge,
            grant_scopes,
            granted_audiences,
            access_token,
            {},
            {},
            False,
            None
        )
        if consent_response:
            api_helper.print_response(consent_response)
        else:
            print("Invalid consent response")
        client.channel.close()
        return consent_response

    elif command == "create_oauth2_consent_verifier_denial":
        # create_oauth2_consent_verifier_denial method: to create a new DenialResponse verifier
        client = IdentityClient()
        consent_challenge = args.consent_challenge
        error = "access_denied"
        error_description = "Access is denied"
        error_hint = "Your consent challenge may be not valid: check your OAuth2 host and your clientID"
        status_code = 403
        consent_response = client.create_oauth2_consent_verifier_denial(
            consent_challenge, error,
            error_description,
            error_hint,
            status_code
        )
        if consent_response:
            api_helper.print_response(consent_response)
        else:
            print("Invalid consent response")
        client.channel.close()
        return consent_response

    elif command == "create_email_invitation":
        # create_email_invitation method: to create an invitation email
        # with reference id, tenant GID id and recipient email as arguments
        client = IdentityClient()
        reference_id = str(uuid.uuid4())
        # any unique external reference id
        print(reference_id)
        tenant_id = args.tenant_id
        email = args.email
        invitation_response = client.create_email_invitation(
            tenant_id,
            reference_id,
            email,
            invite_at_time=None,
            expire_time=None,
            message_attributes=None
        )
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")
        client.channel.close()

    elif command == "create_email_invitation_with_date":
        # create_email_invitation method: to create an invitation email
        # with reference id, tenant GID id, recipient email, invitation date, expiration and
        # message attributes (attributes passed into message sender)  as arguments
        client = IdentityClient()
        reference_id = str(uuid.uuid4())
        print(reference_id)
        tenant_id = args.tenant_id
        email = args.email
        t = datetime.now().timestamp()
        invite_at_time_in_seconds = int(t) + 3600
        expire_time_in_seconds = invite_at_time_in_seconds + 172800  # now + 2 days example
        message_attributes = {"attr1": "value1"}
        invitation_response = client.create_email_invitation(
            tenant_id,
            reference_id,
            email,
            invite_at_time_in_seconds,
            expire_time_in_seconds,
            message_attributes
        )
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")
        client.channel.close()

    elif command == "check_invitation_state":
        # check_invitation_state method: to return the state of invitation and its data
        client = IdentityClient()
        reference_id = args.reference_id
        # check with either reference_id or invitation_token
        invitation_response = client.check_invitation_state(reference_id, None)
        if invitation_response is not None:
            api_helper.print_response(invitation_response)
        else:
            print("Invalid invitation response")
        client.channel.close()

    elif command == "resend_invitation":
        # resend_invitation method: expects reference ID of invitation to send email again
        client = IdentityClient()
        reference_id = args.reference_id
        invitation_response = client.resend_invitation(reference_id)
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")
        client.channel.close()

    elif command == "cancel_invitation":
        # cancel_invitation method: expects reference ID of invitation to cancel
        client = IdentityClient()
        reference_id = args.reference_id
        invitation_response = client.cancel_invitation(reference_id)
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")
        client.channel.close()


if __name__ == '__main__':  # pragma: no cover
    main()

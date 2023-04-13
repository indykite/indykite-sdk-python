class AudienceItem:
    def __init__(self, user_support_email_address=None, client_id=None, display_name=None, description=None,
                 logo_url=None, homepage_url=None,
                 privacy_policy_url=None, tos_url=None):
        self.user_support_email_address = user_support_email_address
        self.client_id = client_id
        self.display_name = display_name
        self.description = description
        self.logo_url = logo_url
        self.homepage_url = homepage_url
        self.privacy_policy_url = privacy_policy_url
        self.tos_url = tos_url

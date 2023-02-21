from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.forms import ValidationError


def is_gov_uk(email):
    allowed = False
    email = email.lower()
    email_split = email.split(".")
    if len(email_split) > 1:
        if email_split[-2] == "gov" and email_split[-1] == "uk":
            allowed = True
    return allowed


class RestrictEmailAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        print(email)
        email = email.lower()
        email_allowed = False
        email_allowed = is_gov_uk(email)
        print(1)
        print(email_allowed)
        if not email_allowed:
            domain = email.split("@")[-1]
            email_allowed = domain in settings.ALLOWED_DOMAINS
            print(2)
            print(email_allowed)
        if not email_allowed:
            raise ValidationError(
                "This email domain is not yet supported. Please contact the site admin team if you think this is incorrect."
            )
        return email

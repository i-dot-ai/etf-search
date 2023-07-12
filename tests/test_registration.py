from django.core.exceptions import ValidationError
from nose import with_setup

from eva_reg import settings as eva_reg_settings
from eva_reg.evaluation import models, restrict_email

from . import utils
from .utils import _get_latest_email_text

VALID_USER_EMAIL = "test@example.com"
VALID_USER_PASSWORD1 = "elephant99"
VALID_USER_PASSWORD2 = "giraffe47"


def enter_signup_form_data(email, password1, password2, follow=False):
    client = utils.make_testino_client()

    page = client.get("/accounts/signup/")
    form = page.get_form()
    form["email"] = email
    form["password1"] = password1
    form["password2"] = password2

    if follow:
        page = form.submit().follow()
    else:
        page = form.submit()
    return page


def test_invalid_password_too_short():
    page = enter_signup_form_data(VALID_USER_EMAIL, "abc123!", "abc123!")

    assert page.has_text("This password is too short. It must contain at least 8 characters.")
    assert page.has_text("This password is too common.")


def test_invalid_password_all_numeric():
    page = enter_signup_form_data(VALID_USER_EMAIL, "1234567890", "1234567890")

    assert page.has_text("This password is entirely numeric.")


def test_invalid_password_too_common():
    page = enter_signup_form_data(VALID_USER_EMAIL, "asdfghjkl", "asdfghjkl")

    assert page.has_text("This password is too common.")


def test_invalid_password_does_not_match():
    page = enter_signup_form_data(VALID_USER_EMAIL, VALID_USER_PASSWORD1, VALID_USER_PASSWORD2)

    assert page.has_text("You must type the same password each time.")


def test_email_is_valid():
    page = enter_signup_form_data(VALID_USER_EMAIL, VALID_USER_PASSWORD1, VALID_USER_PASSWORD1, True)

    assert page.has_text(f"Successfully signed in as {VALID_USER_EMAIL}.")


def test_email_is_invalid_domain_extension():
    page = enter_signup_form_data("jane.doe@example.org", VALID_USER_PASSWORD1, VALID_USER_PASSWORD1)

    assert page.has_text("Currently you need a Civil Service email address to register.")


def test_email_is_invalid_no_extension():
    page = enter_signup_form_data("jane.doe@example", VALID_USER_PASSWORD1, VALID_USER_PASSWORD1)

    assert page.has_text("Enter a valid email address.")


def test_email_is_invalid_only_domain():
    page = enter_signup_form_data("@example.org", VALID_USER_PASSWORD1, VALID_USER_PASSWORD1)

    assert page.has_text("Enter a valid email address.")


def test_email_is_invalid_no_domain():
    page = enter_signup_form_data("john.doe@", VALID_USER_PASSWORD1, VALID_USER_PASSWORD1)

    assert page.has_text("Enter a valid email address.")


def test_user_already_registered():
    user, _ = models.User.objects.get_or_create(email=VALID_USER_EMAIL)
    user.save()

    page = enter_signup_form_data(VALID_USER_EMAIL, VALID_USER_PASSWORD1, VALID_USER_PASSWORD1)
    signup_email = _get_latest_email_text()
    assert page.has_text("A verification email has been sent to your email address.")
    assert page.has_text("Please click on the link in this email to verify your account and then try to sign in.")
    assert signup_email.__contains__(
        "Someone using this email address has just tried to register for the Evaluation Registry, you can find this at the following link."
    )


@with_setup(
    lambda: setattr(eva_reg_settings, "SEND_VERIFICATION_EMAIL", True),
    lambda: setattr(eva_reg_settings, "SEND_VERIFICATION_EMAIL", False),
)
def test_verify_email():
    client = utils.make_testino_client()

    page = client.get("/accounts/signup/")
    assert page.has_text("Register")
    form = page.get_form()
    form["email"] = "test-verification@example.com"
    form["password1"] = VALID_USER_PASSWORD1
    form["password2"] = VALID_USER_PASSWORD1

    signed_up_page = form.submit()
    assert signed_up_page.has_text("Sign up complete")
    assert signed_up_page.has_text("A verification email has been sent to your email address.")

    verify_url = utils._get_latest_email_url()
    verify_page = client.get(verify_url)
    assert verify_page.has_text("Your account has been successfully verified.")

    login_page = client.get("/accounts/login/")
    form = login_page.get_form()
    form["login"] = "test-verification@example.com"
    form["password"] = VALID_USER_PASSWORD1
    home_page = form.submit().follow()
    assert home_page.has_text("Add evaluation")


def test_password_reset():
    user, _ = models.User.objects.get_or_create(email=VALID_USER_EMAIL)
    user.set_password(VALID_USER_PASSWORD1)
    client = utils.make_testino_client()

    page = client.get("/accounts/password-reset/")
    form = page.get_form()
    form["email"] = VALID_USER_EMAIL
    page = form.submit()
    assert page.has_text("Please check your email for a link to reset your password.")

    url = utils._get_latest_email_url()
    page = client.get(url)
    form = page.get_form()
    form["password1"] = VALID_USER_PASSWORD2
    form["password2"] = VALID_USER_PASSWORD2
    page = form.submit()
    assert page.has_text("Your password has been successfully updated, please login again.")

    page = client.get("/accounts/login/")
    form = page.get_form()
    form["login"] = VALID_USER_EMAIL
    form["password"] = VALID_USER_PASSWORD2
    page = form.submit().follow()
    assert page.has_text("Add evaluation")


def test_incorrect_user_id_and_code_caught():
    client = utils.make_testino_client()
    empty_uuid = "00000000-0000-0000-0000-000000000000"
    page = client.get(f"/accounts/change-password/reset/?code=test&user_id={empty_uuid}")

    assert page.has_text(
        "Something went wrong with this request. Please try entering your email again or login instead."
    )
    assert page.has_text("Enter another email")


def test_correct_email_domains():
    correct_emails = ["test@example.com"]
    for email in correct_emails:
        cleaned_email = restrict_email.clean_email(email)
        assert email == cleaned_email


def test_incorrect_email_domains():
    incorrect_emails = ["test@example.net", "test@example.org"]
    for email in incorrect_emails:
        try:
            cleaned_email = restrict_email.clean_email(email)
            assert not cleaned_email
        except ValidationError as e:
            assert e.message.startswith("Currently you need a Civil Service email address to register.")

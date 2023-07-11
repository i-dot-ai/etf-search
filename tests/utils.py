import functools
import os
import pathlib

import httpx
import testino

import eva_reg.wsgi
from eva_reg import settings
from eva_reg.evaluation import choices
from eva_reg.evaluation.models import Evaluation, User

TEST_SERVER_URL = "http://eva-reg-testserver:8010/"


def with_client(func):
    @functools.wraps(func)
    def _inner(*args, **kwargs):
        with httpx.Client(app=eva_reg.wsgi.application, base_url=TEST_SERVER_URL) as client:
            return func(client, *args, **kwargs)

    return _inner


def with_authenticated_client(func):
    @functools.wraps(func)
    def _inner(*args, **kwargs):
        user, _ = User.objects.get_or_create(email="peter.rabbit@example.com")
        user.set_password("P455W0rd")
        user.verified = True
        user.save()
        with httpx.Client(app=eva_reg.wsgi.application, base_url=TEST_SERVER_URL, follow_redirects=True) as client:
            response = client.get("/accounts/login/")
            csrf = response.cookies["csrftoken"]
            data = {"login": user.email, "password": "P455W0rd"}
            headers = {"X-CSRFToken": csrf}
            client.post("/accounts/login/", data=data, headers=headers)
            return func(client, *args, **kwargs)

    return _inner


def with_authenticated_external_client(func):
    @functools.wraps(func)
    def _inner(*args, **kwargs):
        user, _ = User.objects.get_or_create(email="jemima.puddleduck@example.org")
        user.set_password("P455W0rd")
        user.verified = True
        user.is_external_user = True
        user.save()
        with httpx.Client(app=eva_reg.wsgi.application, base_url=TEST_SERVER_URL, follow_redirects=True) as client:
            response = client.get("/accounts/login/")
            csrf = response.cookies["csrftoken"]
            data = {"login": user.email, "password": "P455W0rd"}
            headers = {"X-CSRFToken": csrf}
            client.post("/accounts/login/", data=data, headers=headers)
            return func(client, *args, **kwargs)

    return _inner


def make_testino_client():
    client = testino.WSGIAgent(eva_reg.wsgi.application, TEST_SERVER_URL)
    return client


def register(client, email, password):
    page = client.get("/accounts/signup/")
    form = page.get_form()
    form["email"] = email
    form["password1"] = password
    form["password2"] = password
    page = form.submit().follow()
    assert page.has_text(f"Successfully signed in as {email}")


def _get_latest_email_text():
    email_dir = pathlib.Path(settings.EMAIL_FILE_PATH)
    latest_email_path = max(email_dir.iterdir(), key=os.path.getmtime)
    content = latest_email_path.read_text()
    return content


def _get_latest_email_url():
    text = _get_latest_email_text()
    lines = text.splitlines()
    url_lines = tuple(word for line in lines for word in line.split() if word.startswith("http://localhost:8010/"))
    assert len(url_lines) == 1
    email_url = url_lines[0].strip()
    whole_url = email_url.strip(",")
    url = f"/{whole_url.split('http://localhost:8010/')[-1]}".replace("?", "?")
    return url


def create_fake_evaluation(title, visibility, users=None):
    evaluation = Evaluation(title=title, visibility=visibility)
    evaluation.save()
    if users:
        for user in users:
            evaluation.users.add(user)
            evaluation.save()
    return evaluation


def create_fake_evaluations():
    # For testing "example.com" is counted as "Civil Service", "example.org" is not
    peter_rabbit, _ = User.objects.update_or_create(email="peter.rabbit2@example.com")
    mrs_tiggywinkle, _ = User.objects.update_or_create(email="mrs.tiggywinkle@example.org")
    users = [peter_rabbit, mrs_tiggywinkle]
    create_fake_evaluation(title="Draft evaluation 1", visibility=choices.EvaluationVisibility.DRAFT.value)
    create_fake_evaluation(title="Draft evaluation 2", visibility=choices.EvaluationVisibility.DRAFT.value, users=users)
    create_fake_evaluation(
        title="Civil Service evaluation 1", visibility=choices.EvaluationVisibility.CIVIL_SERVICE.value
    )
    create_fake_evaluation(
        title="Civil Service evaluation 2", visibility=choices.EvaluationVisibility.CIVIL_SERVICE.value, users=users
    )
    create_fake_evaluation(title="Public evaluation 1", visibility=choices.EvaluationVisibility.PUBLIC.value)
    create_fake_evaluation(
        title="Public evaluation 2", visibility=choices.EvaluationVisibility.PUBLIC.value, users=users
    )


def remove_fake_evaluations():
    fake_evaluation_titles = [
        "Draft evaluation 1",
        "Draft evaluation 2",
        "Civil Service evaluation 1",
        "Civil Service evaluation 2",
        "Public evaluation 1",
        "Public evaluation 2",
    ]
    Evaluation.objects.filter(title__in=fake_evaluation_titles).delete()
    User.objects.filter(email__in=["mrs.tiggywinkle@example.com", "peter.rabbit2@example."]).delete()

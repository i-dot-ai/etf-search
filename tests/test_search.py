from eva_reg.evaluation import interface, models

from . import utils

USER_DATA = {"email": "mr_search_test@example.com", "password": "1-h4t3-p455w0rd-c0mpl3xity-53tt1ng5"}


def test_search():
    client = utils.make_testino_client()
    utils.register(client, **USER_DATA)

    page = client.get("/")
    assert page.status_code == 200, page.status_code
    assert page.has_text("My evaluations")

    user = models.User.objects.get(email=USER_DATA["email"])

    evaluation = interface.facade.evaluation.create(user_id=user.id)
    interface.facade.evaluation.update(
        user_id=user.id, evaluation_id=evaluation["id"], data={"title": "Test evaluation search by title"}
    )
    evaluation = interface.facade.evaluation.get(evaluation_id=evaluation["id"])

    search_page = client.get("/search/")

    search_form = search_page.get_form("""form[action="/search/"]""")

    search_form["search_term"] = evaluation["title"]

    results = search_form.submit()

    assert results.has_text(evaluation["title"])

from eva_reg.evaluation import interface, models

USER_DATA = {"email": "mr_interface_test@example.com", "password": "1-h4t3-p455w0rd-c0mpl3xity-53tt1ng5"}


def test_evaluation_facade():
    user, _ = models.User.objects.get_or_create(email=USER_DATA["email"])
    result = interface.facade.evaluation.create(user_id=user.id)
    expected = [{"email": "mr_interface_test@example.com"}]
    assert result["users"] == expected, result["users"]

    evaluation_id = result["id"]
    result = interface.facade.evaluation.get(evaluation_id=evaluation_id)
    assert result["users"] == expected

    data = {"title": "Flibble", "monetisation_approaches": "Sell, sell, sell"}
    result = interface.facade.evaluation.update(user_id=user.id, evaluation_id=evaluation_id, data=data)
    assert result["title"] == "Flibble"
    assert result["monetisation_approaches"] == "Sell, sell, sell"

    result = interface.facade.evaluation.add_user_to_evaluation(
        evaluation_id=evaluation_id, user_id=user.id, user_to_add_data={"email": "new_user@example.com"}
    )
    assert result["is_new_user"], result
    assert result["evaluation_id"] == evaluation_id, result
    new_user_id = result["user_added_id"]

    result = interface.facade.evaluation.add_user_to_evaluation(
        user_id=user.id, evaluation_id=evaluation_id, user_to_add_data={"email": "mr_interface_test@example.com"}
    )
    assert not result["is_new_user"], result
    assert result["evaluation_id"] == evaluation_id, result

    result = interface.facade.evaluation.remove_user_from_evaluation(
        user_id=user.id, evaluation_id=evaluation_id, user_to_remove_id=new_user_id
    )
    user_emails = [x["email"] for x in result]
    assert "new_user@example.com" not in user_emails, user_emails
    assert "mr_interface_test@example.com" in user_emails, user_emails

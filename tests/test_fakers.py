from eva_reg.evaluation.fakers import add_evals_to_users, add_users


def test_add_users():
    users = add_users(5)
    assert len(list(users)) == 5


def test_add_evaluations_to_user():
    user_gen = add_users(1)
    user = list(user_gen)[0]
    initial_num_evals = user.evaluations.count()
    add_evals_to_users(user, allow_empty=False)
    new_num_evals = user.evaluations.count()
    assert new_num_evals > initial_num_evals

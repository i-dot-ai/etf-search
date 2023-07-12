from eva_reg.evaluation import choices


def test_get_db_values():
    actual_values = choices.get_db_values(choices.EventDateType.choices)
    expected_values = ["INTENDED", "ACTUAL"]
    assert actual_values == expected_values


def test_get_display_name():
    start = choices.get_display_name("EVALUATION_START", choices.EventDateOption.options)
    other = choices.get_display_name("A N other", choices.EventDateOption.options)
    assert start == "Evaluation start", start
    assert not other, other


def test_map_choice_or_other():
    start = choices.map_choice_or_other("EVALUATION_START", choices.EventDateOption.options)
    other = choices.map_choice_or_other("A N other", choices.EventDateOption.options)
    assert start == "Evaluation start", start
    assert other == "A N other", other


def test_turn_list_to_display_values():
    input_list = ["IMPACT", "ECONOMIC", "Specified value"]
    output_list = choices.turn_list_to_display_values(input_list, choices.EvaluationTypeOptions.options)
    expected = ["Impact evaluation", "Economic evaluation", "Specified value"]
    assert output_list == expected, output_list


def test_restrict_choices():
    restricted_values = ["SUPERIORITY", "OTHER"]
    actual = choices.restrict_choices(choices.ImpactFramework.choices, restricted_values)
    expected = (("SUPERIORITY", "Superiority"), ("OTHER", "Other"))
    assert tuple(actual) == expected, actual


def test_restrict_choices_with_other():
    restricted_values = ["SUPERIORITY", "OTHER"]
    actual = choices.restrict_choices(
        choices.ImpactFramework.choices, restricted_values, specified_other="specified text"
    )
    expected = (("SUPERIORITY", "Superiority"), ("OTHER", "Other (specified text)"))
    assert tuple(actual) == expected, actual

from eva_reg.evaluation import pages


def test_get_prev_next_page_name_first():
    page_name = "intro"
    page_options = dict(evaluation_types=["flibble"])
    result = pages.get_prev_next_page_name(page_name, page_options)
    expected = (None, "title")
    assert result == expected, result


def test_get_prev_next_page_name_middle():
    page_name = "ethics"
    page_options = dict(evaluation_types=["flibble"], ethics_option="YES")
    result = pages.get_prev_next_page_name(page_name, page_options)
    expected = ("other-measures", "processes-standards")
    assert result == expected, result


def test_get_prev_next_page_name_middle_impact():
    page_name = "ethics"
    page_options = dict(evaluation_types=["IMPACT"], ethics_option="YES")
    result = pages.get_prev_next_page_name(page_name, page_options)
    expected = ("other-measures", "impact-findings")
    assert result == expected, result


def test_get_prev_next_page_name_penultimate():
    page_name = "visibility"
    page_options = dict(evaluation_types=["flibble"], issue_description_option="YES")
    result = pages.get_prev_next_page_name(page_name, page_options)
    expected = ("links", "end")
    assert result == expected, result


def test_get_prev_next_page_name_last():
    page_name = "end"
    page_options = dict(evaluation_types=["flibble"])
    result = pages.get_prev_next_page_name(page_name, page_options)
    expected = ("visibility", None)
    assert result == expected, result


def test_get_page_name_and_order():
    page_options = dict(evaluation_types=["flibble"], ethics_option="NO")
    page_names_and_order = pages.get_page_name_and_order(page_options)
    assert len(page_names_and_order) == 16, len(page_names_and_order)
    assert "impact-analysis" not in page_names_and_order

    page_options = dict(evaluation_types=["IMPACT"], grants_option="NO")
    page_names_and_order = pages.get_page_name_and_order(page_options)
    assert len(page_names_and_order) == 19, len(page_names_and_order)
    assert "impact-analysis" in page_names_and_order

    page_options = dict(evaluation_types=["PROCESS"], grants_option="YES", ethics_option="YES")
    page_names_and_order = pages.get_page_name_and_order(page_options)
    assert len(page_names_and_order) == 22, len(page_names_and_order)
    assert "process-analysis" in page_names_and_order

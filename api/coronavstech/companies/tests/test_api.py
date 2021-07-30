import json
import pytest
from django.urls import reverse

from api.coronavstech.companies.models import Company

companies_url = reverse("companies-list")
# module decorator 放在这里的话，整个文件里的函数都相当于加了marker: @pytest.mark.django_db
pytestmark = pytest.mark.django_db


# --------------Test Get Companies--------------
def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_exists_should_succeed(client) -> None:
    test_company = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_company.name
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


# --------------Test Post Companies--------------


def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_existing_company_should_fail(client) -> None:
    Company.objects.create(name="google")
    response = client.post(path=companies_url, data={"name": "google"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]
    }


def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(path=companies_url, data={"name": "tests company name"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "tests company name"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_layoffs_should_succeed(client) -> None:
    response = client.post(
        path=companies_url,
        data={"name": "tests company name", "status": "Layoffs"},
    )
    # 如果Layoffs  写成 layoffs
    # raise ValueError(response.content) # ValueError: b'{"status":["\\"layoffs\\" is not a valid choice."]}'
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "tests company name"
    assert response_content.get("status") == "Layoffs"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        path=companies_url,
        data={"name": "tests company name", "status": "WrongStatus"},
    )
    # raise ValueError(response.content) #         raise ValueError(response.content)
    assert response.status_code == 400
    assert "WrongStatus" in str(response.content)
    assert "is not a valid choice" in str(response.content)


@pytest.mark.xfail
def test_should_be_ok_if_fails(client) -> None:
    assert 1 == 2


@pytest.mark.skip
def test_should_be_skipped(client) -> None:
    assert 1 == 2


# --------------Test Exceptions--------------
def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")


def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)


# --------------Test Logs  --------------
import logging

# logging levels:       debug  info  warning  error  critical
# corresponding level:   10     20     30      40      50
logger = logging.getLogger("CORONA_LOGS")


def function_that_logs_something() -> None:
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        # 只log warning level
        logger.warning(f"I am logging {str(e)}")


# 测试 warning level的log
def test_logged_warning_level(caplog) -> None:
    function_that_logs_something()
    assert "I am logging CoronaVirus Exception" in caplog.text


# 测试 info level的log
def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logger.info("I am logging info level")
        assert "I am logging info level" in caplog.text

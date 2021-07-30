import json
import pytest
from unittest import TestCase
from django.test import Client
from django.urls import reverse

from api.coronavstech.companies.models import Company

# 创建测试数据库，schema与开发环境的数据库一样
@pytest.mark.django_db
class BasicCompanyApiTestCase(TestCase):
    # 一开始，自动执行
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    # 在每个test结束的时候执行
    def tearDown(self) -> None:
        pass


class TestGetCompanies(BasicCompanyApiTestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        # urls 里面的basename   -list是pytest规定的用法
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self) -> None:
        test_company = Company.objects.create(name="Amazon")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), test_company.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")
        test_company.delete()


class TestPostCompanies(BasicCompanyApiTestCase):
    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    def test_existing_company_should_fail(self) -> None:
        Company.objects.create(name="google")
        response = self.client.post(path=self.companies_url, data={"name": "google"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["company with this name already exists."]},
        )

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "tests company name"}
        )
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "tests company name")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_should_succeed(self) -> None:
        response = self.client.post(
            path=self.companies_url,
            data={"name": "tests company name", "status": "Layoffs"},
        )
        # 如果Layoffs  写成 layoffs
        # raise ValueError(response.content) # ValueError: b'{"status":["\\"layoffs\\" is not a valid choice."]}'
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "tests company name")
        self.assertEqual(response_content.get("status"), "Layoffs")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(
            path=self.companies_url,
            data={"name": "tests company name", "status": "WrongStatus"},
        )
        # raise ValueError(response.content) #         raise ValueError(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("WrongStatus", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))

    @pytest.mark.xfail
    def test_should_be_ok_if_fails(self) -> None:
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_should_be_skipped(self) -> None:
        self.assertEqual(1, 2)


# tests exception
def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")


def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)


# tests logs
# logging levels:       debug  info  warning  error  critical
# corresponding level:   10     20     30      40      50
import logging

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
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
        self.client = Client();
        self.companies_url = reverse("companies-list")

    # 在每个test结束的时候执行
    def tearDown(self) -> None:
        pass




class TestGetCompanies(BasicCompanyApiTestCase):
    def test_zero_companies_should_return_empty_list(self)->None:
        # urls 里面的basename   -list是pytest规定的用法
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self)->None:
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
    def test_create_company_without_arguments_should_fail(self)->None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    def test_existing_company_should_fail(self)->None:
        Company.objects.create(name="google")
        response = self.client.post(path=self.companies_url, data={"name": "google"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["company with this name already exists."]}
        )

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "test company name"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "test company name")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_should_succeed(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "test company name", "status": "Layoffs"})
        # 如果Layoffs  写成 layoffs
        # raise ValueError(response.content) # ValueError: b'{"status":["\\"layoffs\\" is not a valid choice."]}'
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "test company name")
        self.assertEqual(response_content.get("status"), "Layoffs")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_wrong_status_should_fail(self)-> None:
        response = self.client.post(path=self.companies_url, data={"name": "test company name", "status": "WrongStatus"})
        # raise ValueError(response.content) #         raise ValueError(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("WrongStatus", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))

    @pytest.mark.xfail
    def test_should_be_ok_if_fails(self)->None:
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_should_be_skipped(self)->None:
        self.assertEqual(1, 2)



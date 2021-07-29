import json
import pytest
from unittest import TestCase
from django.test import Client
from django.urls import reverse

from api.coronavstech.companies.models import Company

# 创建测试数据库，schema与开发环境的数据库一样
@pytest.mark.django_db
class TestGetCompanies(TestCase):
    def test_zero_companies_should_return_empty_list(self)->None:
        client = Client();
        # urls 里面的basename   -list是pytest规定的用法
        companies_url = reverse("companies-list")
        response = client.get(companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self)->None:
        client = Client();
        companies_url = reverse("companies-list")
        test_company = Company.objects.create(name="Amazon")
        response = client.get(companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), test_company.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")
        test_company.delete()
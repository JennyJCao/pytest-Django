import pytest
import requests
import json

testing_env_companies_url = "http://127.0.0.1:8000/companies/"


# 要想成功需要数据库是空的
# @pytest.mark.skip_in_ci
# @pytest.mark.skip(reason="This test needs localhost django server running")
def test_zero_companies_django_agnostic() -> None:
    response = requests.get(url=testing_env_companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []

# @pytest.mark.skip_in_ci
# @pytest.mark.skip(reason="This test needs localhost django server running")
def test_create_company_with_layoffs_django_agnostic() -> None:
    response = requests.post(
        url=testing_env_companies_url,
        json={"name": "test company name", "status": "Layoffs"},
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("status") == "Layoffs"
    # 不清空的话，上一个test会失败
    cleanup_company(company_id=response_content["id"])

def cleanup_company(company_id: str) -> None:
    response = requests.delete(url=f"http://127.0.0.1:8000/companies/{company_id}")
    assert response.status_code == 204



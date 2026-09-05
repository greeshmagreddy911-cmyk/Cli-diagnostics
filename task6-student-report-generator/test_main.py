from fastapi.testclient import TestClient

from api import app
from main import calculate_result


client = TestClient(app)


def test_calculate_result_pass():
    student = {
        "name": "Test Student",
        "python": 80,
        "dbms": 70,
        "java": 90,
    }

    result = calculate_result(student)

    assert result["name"] == "Test Student"
    assert result["average"] == 80
    assert result["result"] == "PASS"


def test_calculate_result_fail():
    student = {
        "name": "Fail Student",
        "python": 20,
        "dbms": 30,
        "java": 25,
    }

    result = calculate_result(student)

    assert result["result"] == "FAIL"


def test_root_api():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_report_api():
    response = client.post(
        "/report",
        json={
            "name": "API Student",
            "python": 80,
            "dbms": 75,
            "java": 85,
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == "PASS"

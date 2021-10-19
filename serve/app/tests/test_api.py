import datetime

import pytest
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "input_date,result",
    (("January 5 2016", "2016-01-05"),),
)
def test_predict(input_date, result):
    response = client.post("/", json={"i": input_date})
    assert response.status_code == 200
    r = response.json()
    assert set(r.keys()) == {"input", "model_output", "result", "version"}
    assert r["result"] == result
    assert datetime.datetime.strptime(r["version"][:10], "%Y-%m-%d")

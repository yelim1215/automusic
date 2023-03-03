from fastapi.testclient import TestClient
from fastapi import FastAPI, Header
from main import app
from typing import Optional
from key import secrete_key

import json
import pytest

from httpx import AsyncClient

client = TestClient(app)

def test_auto_music():
    response = client.post(
        "/auto_music",
        headers={"Token": secrete_key["SECRETE-KEY"]},
        json={"control": "00000000"},
    )

    # response = client.get("/auto_music",
    #                       headers={"Token": secrete_key["SECRETE-KEY"]})
    print(response.json())
    assert response.status_code == 200


if __name__ == '__main__':
    test_auto_music()

from fastapi.testclient import TestClient
from fastapi import FastAPI, Header
from main import app
from typing import Optional
from key import secrete_key

import json
import pytest

from httpx import AsyncClient

client = TestClient(app)

# 이제 세가지 API 함수에 대해 테스트하는 함수들을 작성하겠습니다.


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World'}


def test_auto_music():
    response = client.get("/auto_music",
                          headers={"Token": secrete_key["SECRETE-KEY"]})
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}


if __name__ == '__main__':
    test_auto_music()

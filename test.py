from fastapi.testclient import TestClient
from fastapi import FastAPI, Header
from main import app
from typing import Optional
from key import secrete_key

import json
import pytest
import pickle

from httpx import AsyncClient

client = TestClient(app)

def test_auto_music():
    response = client.post(
        "/auto_music",
        headers={"Token": secrete_key["SECRETE-KEY"]},
        json={"control": "0,0,128,127,125,126,60,C-Am-C-F"},
    )
    print(response.json())
    assert response.status_code == 200

def test_read_midi():
    response = client.get("/midi")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "audio/midi"

import pickle
import requests

# MIDI 파일을 다운로드 받아서 로컬에 저장하는 함수
def save_midi_file(response, file_path):
    # HTTP 응답 본문에서 직렬화된 MIDI 데이터를 추출합니다.
    serialized_midi = response.content

    # 추출한 MIDI 데이터를 역직렬화합니다.
    midi_data = pickle.loads(serialized_midi)

    # 역직렬화된 MIDI 데이터를 파일로 저장합니다.
    with open(file_path, "wb") as f:
        f.write(midi_data)

# MIDI 파일 다운로드 테스트 코드
def test_download_midi_file():
    # FastAPI 서버에서 MIDI 파일을 다운로드 받습니다.
    #url = "http://localhost:8000/midi"
    #response = requests.get(url)
    response = client.post(
        "/auto_music",
        headers={"Token": secrete_key["SECRETE-KEY"]},
        json={"control": "0,0,128,127,125,126,60,C-Am-C-F"},
    )
    print(response.content)

    # 다운로드 받은 MIDI 파일을 로컬에 저장합니다.
    #save_midi_file(response, "downloaded_midi_file.mid")
    # 추출한 MIDI 데이터를 역직렬화합니다.
    midi_data = pickle.loads(response.content)

    # 역직렬화된 MIDI 데이터를 파일로 저장합니다.
    with open(file_path, "wb") as f:
        f.write(midi_data)
    # 저장한 MIDI 파일이 존재하는지 확인합니다.
    #assert os.path.isfile("downloaded_midi_file.mid")


if __name__ == '__main__':
    test_download_midi_file()

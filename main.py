from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
import uuid
from key import secrete_key

app = FastAPI()
api_key_header = APIKeyHeader(name="Token")

"""
table name : metagenerator
key : unique 한 key
song : 노래 경로
mood : list 형태로 저장
"""


class test_db:
    def __init__(self):
        pass
# TODO : 요소 각각 json 파일로 내보내기
# TODO : 조합으로 메타 데이터 생성
# TODO : chords 정보 입력
# TODO : 악기 정보 미리 다 선언해두기


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/auto_music")
async def auto_music(token: str = Depends(api_key_header)):
    print(secrete_key["SECRETE-KEY"])
    if token != secrete_key["SECRETE-KEY"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"hello": "world"}

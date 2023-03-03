from commu.preprocessor.utils import constants
from commu.midi_generator.generate_pipeline import MidiGenerationPipeline
from typing import Dict
import argparse
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


def main(model_arg: Dict, input_arg: Dict):
    pipeline = MidiGenerationPipeline(model_arg)

    inference_cfg = pipeline.model_initialize_task.inference_cfg
    model = pipeline.model_initialize_task.execute()

    encoded_meta = pipeline.preprocess_task.execute(input_arg)
    input_data = pipeline.preprocess_task.input_data

    pipeline.inference_task(
        model=model,
        input_data=input_data,
        inference_cfg=inference_cfg
    )
    sequences = pipeline.inference_task.execute(encoded_meta)

    pipeline.postprocess_task(input_data=input_data)
    pipeline.postprocess_task.execute(
        sequences=sequences
    )


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
async def auto_music(control: int, token: str = Depends(api_key_header)):
    # control must be : 00000000 (1/0, length : 8)
    main({'checkpoint_dir': '/home/dani/workspace/checkpoint_best.pt'}, {'output_dir': 'danni', 'bpm': 70, 'audio_key': 'aminor', 'time_signature': '4/4', 'pitch_range': 'mid_high', 'num_measures': 8.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'main_melody', 'rhythm': 'standard',
                                                                         'min_velocity': 60, 'max_velocity': 80, 'chord_progression': 'Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E-Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E', 'num_generate': 3, 'top_k': 32, 'temperature': 0.95})
    if token != secrete_key["SECRETE-KEY"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    uid = uuid.uuid4()

    return {"hello": "world"}

import os
from commu.preprocessor.utils import constants
from commu.midi_generator.generate_pipeline import MidiGenerationPipeline
from inference import inference
from typing import Dict, List
import argparse
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
import uuid
from key import secrete_key
from pydantic import BaseModel
from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.responses import JSONResponse
import shutil
import base64
from inst import InstrumentChange
import pickle

app = FastAPI()
api_key_header = APIKeyHeader(name="Token")

"""
table name : metagenerator
key : unique 한 key
song : 노래 경로
mood : list 형태로 저장
"""


try:

    import mido

except ImportError as error:

    raise ImportError(

        """



`pip install mido`를 수행해서 패키지를 설치하세요.

Package Github: https://github.com/mido/mido

Package Document: https://mido.readthedocs.io/en/latest/

"""

    ) from error


def merge_midi(files: "List[str]") -> mido.MidiFile:

    midis = [mido.MidiFile(path) for path in files]

    if not midis:

        raise ValueError("파일 목록이 비었습니다.")
    # 빈 미디 파일 생성
    mergedMidi = mido.MidiFile()
    mergedMidi.ticks_per_beat = midis[0].ticks_per_beat
    mergedMidi.tracks = sum((midi.tracks for midi in midis), start=[])
    return mergedMidi


def save_midi(path: str, midi: "mido.MidiFile", exist_ok=False) -> None:

    if (not exist_ok) and os.path.exists(path):

        raise FileExistsError(

            f"{path} 은 이미 존재하는 파일입니다. 파일명을 변경하거나, exist_ok 옵션을 True로 설정해 덮어쓰세요."

        )

    midi.save(path)


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


class Item(BaseModel):
    control: str


class responseItem(BaseModel):
    out_list: List[str]
from fastapi import FastAPI, File, UploadFile
import io
import requests

app = FastAPI()

@app.post("/upload_midi/")
async def upload_midi(file: UploadFile = File(...)):
    contents = await file.read()
    files = {"file": ("midi_file.mid", io.BytesIO(contents))}
    response = requests.post("http://<java_spring_backend_url>/save_midi/", files=files)
    return {"status": response.status_code}


@app.get("/midi")
async def send_midi_file():
    # MIDI 파일을 읽어옵니다.
    with open(r'C:/Users/zing1/workspace/automusic/generated/c5799f49-a2cf-4aaa-a4a2-b122018962c4_0.mid', 'rb') as file:
        midi_data = file.read()

    # 직렬화된 데이터로 변환합니다.
    b64_midi_data = base64.b64encode(midi_data).decode('utf-8')

    # Java Spring 백엔드로 응답을 보냅니다.
    return JSONResponse(content={'midi_data': b64_midi_data})

@app.post("/auto_music")#, response_model=responseItem)
async def auto_music(response: Response, token: str = Depends(api_key_header)):
    # control must be : 00000000 (1/0, length : 8)
    #1. 0 긍정 1 부정
    #2. 0 -> 0 : 첫번쨰 경쾌, 1 :차분
    #2. 1 -> 0 : 우울한 음악, 1 : 긴장되는 음악
    #3. 악기 5개
    
    instch = InstrumentChange()
    uid = str(uuid.uuid4())
    opt = 3
    NUM_GEN = 2
    infer = inference()
    seq = infer.main(opt).replace("maj","maj7").replace("maj76","maj7").replace("maj77","maj7")
    if (opt == 1 or opt == 2):
        bpm = 50
        min_v = 40
        max_v = 45
        pitch = "mid_high"
        audio_key = "amajor"
        if(opt == 1):
            audio_key = "aminor"
            pitch = "mid_low"
    else:
        bpm = 70
        min_v = 60
        max_v = 80
        pitch = "mid_high"
        audio_key = "amajor"
        if(opt == 0):
            bpm = 80
            audio_key = "aminor"
            pitch = "mid_low"
    main({'checkpoint_dir': r'C:/Users/zing1/workspace/automusic/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': bpm, 'audio_key': 'aminor', 'time_signature': '3/4', 'pitch_range': pitch, 'num_measures': 16.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'main_melody', 'rhythm': 'standard',
                                                                         'min_velocity': min_v, 'max_velocity': max_v, 'chord_progression':seq, 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    #main({'checkpoint_dir': r'C:/Users/zing1/workspace/automusic/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': bpm, 'audio_key': 'aminor', 'time_signature': '3/4', 'pitch_range': 'mid_low', 'num_measures': 16.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'main_melody', 'rhythm': 'standard',
    #                                                                     'min_velocity': min_v, 'max_velocity': max_v, 'chord_progression':seq, 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    #main({'checkpoint_dir': r'C:/Users/zing1/workspace/automusic/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': bpm, 'audio_key': 'bminor', 'time_signature': '3/4', 'pitch_range': 'mid_low', 'num_measures': 16.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'accompaniment', 'rhythm': 'standard',
    #                                                                     'min_velocity': min_v, 'max_velocity': max_v, 'chord_progression': seq, 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    #main({'checkpoint_dir': r'C:/Users/zing1/workspace/automusic/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': bpm, 'audio_key': 'aminor', 'time_signature': '3/4', 'pitch_range': pitch, 'num_measures': 16.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'pad', 'rhythm': 'standard',
    #                                                                     'min_velocity': min_v, 'max_velocity': max_v, 'chord_progression': seq, 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    #main({'checkpoint_dir': r'C:/Users/zing1/workspace/automusic/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': bpm, 'audio_key': 'aminor', 'time_signature': '3/4', 'pitch_range': pitch, 'num_measures': 16.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'riff', 'rhythm': 'standard',
    #                                                                     'min_velocity': min_v, 'max_velocity': max_v, 'chord_progression': seq, 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    midi_path_list = []
    out_midi_list = []

    uid_directory = os.listdir(uid)
    inst_list = ["Acoustic Grand Piano","Acoustic Grand Piano","Synth Strings 1","Electric Guitar (jazz)","Acoustic Bass"]
    for sub_d in uid_directory:
        sub_d = uid + "/" + sub_d
        sublist = []

        for sub_f in os.listdir(sub_d):
            sublist.append(sub_d + "/" + sub_f)
        midi_path_list.append(sublist)

    for midx in range(NUM_GEN):
        output_list = []
        out_file_name = "generated/"+"{}_{}.mid".format(uid, midx)

        for idx, m in enumerate(midi_path_list):
            instch.change_instrument(m[midx], inst_list[idx])
            output_list.append(m[midx])
        
        save_midi(
            out_file_name,
            merge_midi(output_list),
            exist_ok=True,
        )
        out_midi_list.append(out_file_name)

    if os.path.exists(uid):
        shutil.rmtree(uid)

    if token != secrete_key["SECRETE-KEY"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    with open('C:/Users/zing1/workspace/automusic/generated/0273f555-462a-4366-8ea0-fc2325b4df5f_0.mid', 'rb') as file:
        midi_data = file.read()
    # 직렬화된 데이터로 변환합니다.
    b64_midi_data = base64.b64encode(midi_data).decode('utf-8')

    # Java Spring 백엔드로 응답을 보냅니다.
    return JSONResponse(content={'midi_data': b64_midi_data})
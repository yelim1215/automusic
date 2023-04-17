import os
from commu.preprocessor.utils import constants
from commu.midi_generator.generate_pipeline import MidiGenerationPipeline
from typing import Dict, List
import argparse
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
import uuid
import pickle
from key import secrete_key
from pydantic import BaseModel
from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.responses import FileResponse
import shutil
from inst import InstrumentChange

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

    # 모든 미디 파일 읽기

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

@app.get("/midi")
def get_midi(response: Response):
    # MIDI 파일을 읽어들입니다.
    with open("/root/workspace/automusic/generated/3e0586c2-4bd9-4195-afa4-0ecdd29b5187_1.mid", "rb") as f:
        midi_data = f.read()

    # MIDI 데이터를 직렬화합니다.
    serialized_midi = pickle.dumps(midi_data)

    # HTTP 응답 본문으로 직렬화된 MIDI 데이터를 설정합니다.
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Content-Disposition"] = "attachment; filename=3e0586c2-4bd9-4195-afa4-0ecdd29b5187_1.mid"
    response.content = serialized_midi

    return response

@app.post("/auto_music")#, response_model=responseItem)
async def auto_music(response: Response, token: str = Depends(api_key_header)):
    # control must be : 00000000 (1/0, length : 8)
    ex_inst = ["Acoustic Grand Piano", "Cello", "Lead 8 (bass + lead)", "Synth Drum"]
    
    uid = str(uuid.uuid4())

    NUM_GEN = 2
    # 4/4 3/4 6/8 12/8
    main({'checkpoint_dir': '/root/workspace/automusic/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': 70, 'audio_key': 'aminor', 'time_signature': '4/4', 'pitch_range': 'mid_high', 'num_measures': 8.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'main_melody', 'rhythm': 'standard',
                                                                         'min_velocity': 60, 'max_velocity': 80, 'chord_progression': 'Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E-Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E', 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    #main({'checkpoint_dir': '/root/workspace/automusic/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': 70, 'audio_key': 'bminor', 'time_signature': '4/4', 'pitch_range': 'mid_low', 'num_measures': 8.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'main_melody', 'rhythm': 'standard',
    #                                                                     'min_velocity': 60, 'max_velocity': 80, 'chord_progression': 'Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E-Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E', 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    #main({'checkpoint_dir': '/root/workspace/automusic/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': 70, 'audio_key': 'aminor', 'time_signature': '4/4', 'pitch_range': 'mid_high', 'num_measures': 8.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'pad', 'rhythm': 'standard',
    #                                                                     'min_velocity': 60, 'max_velocity': 80, 'chord_progression': 'Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E-Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E', 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    #main({'checkpoint_dir': '/root/workspace/automusic/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': 70, 'audio_key': 'aminor', 'time_signature': '4/4', 'pitch_range': 'mid_high', 'num_measures': 8.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'riff', 'rhythm': 'standard',
    #                                                                     'min_velocity': 60, 'max_velocity': 80, 'chord_progression': 'Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E-Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E', 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    
           
    midi_path_list = []
    out_midi_list = []

    uid_directory = os.listdir(uid)
    inst_c = InstrumentChange()

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
            inst_c.change_instrument(m[midx], ex_inst[idx])
            output_list.append(m[midx])
        save_midi(
            out_file_name,
            merge_midi(output_list),
            exist_ok=True,
        )
        out_midi_list.append(out_file_name)

    if os.path.exists(uid):
        shutil.rmtree(uid)
    # 미디파일을 연 후 전송 처리

    if token != secrete_key["SECRETE-KEY"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    with open("/root/workspace/automusic/generated/3e0586c2-4bd9-4195-afa4-0ecdd29b5187_1.mid", "rb") as f:
        midi_data = f.read()
    print(midi_data)
    # MIDI 데이터를 직렬화합니다.
    serialized_midi = pickle.dumps(midi_data)

    # HTTP 응답 본문으로 직렬화된 MIDI 데이터를 설정합니다.
    response.headers["Content-Type"] = "audio/midi"
    response.headers["Content-Disposition"] = "attachment; filename=/root/workspace/automusic/generated/3e0586c2-4bd9-4195-afa4-0ecdd29b5187_1.mid"
    response.content = serialized_midi
    print(response.content)
    serialized_midi = response.content

    # 추출한 MIDI 데이터를 역직렬화합니다.
    midi_data = pickle.loads(serialized_midi)
    file_path = "hoon.mid"
    # 역직렬화된 MIDI 데이터를 파일로 저장합니다.
    with open(file_path, "wb") as f:
        f.write(midi_data)
    return response

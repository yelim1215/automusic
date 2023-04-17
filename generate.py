import argparse
from typing import Dict

from commu.midi_generator.generate_pipeline import MidiGenerationPipeline
from commu.preprocessor.utils import constants


def main():
    pipeline = MidiGenerationPipeline(
        {'checkpoint_dir': '/root/workspace/automusic/checkpoint_best.pt'})

    inference_cfg = pipeline.model_initialize_task.inference_cfg
    model = pipeline.model_initialize_task.execute()

    encoded_meta = pipeline.preprocess_task.execute({'output_dir': 'danni', 'bpm': 70, 'audio_key': 'aminor', 'time_signature': '8/8', 'pitch_range': 'mid_high', 'num_measures': 8.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'main_melody', 'rhythm': 'standard',
                                                    'min_velocity': 60, 'max_velocity': 80, 'chord_progression': 'Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E-Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E', 'num_generate': 3, 'top_k': 32, 'temperature': 0.95})
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


if __name__ == "__main__":
    main()

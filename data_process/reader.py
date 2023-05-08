import os

class Reader:
    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.beat_file_paths = []
        self.chord_file_paths = []

        for folder in os.listdir(self.root_folder):
            if os.path.isdir(os.path.join(self.root_folder, folder)):
                beat_file_path = os.path.join(self.root_folder, folder, "beat_audio.txt")
                self.beat_file_paths.append(beat_file_path)
                chord_file_path = os.path.join(self.root_folder, folder, "chord_midi.txt")
                self.chord_file_paths.append(chord_file_path)

    def read_files(self, opt):
        beat_dict = {}
        chord_dict = {}
        if opt == 'chord':
            for file_path in self.chord_file_paths:
                chord = []
                with open(file_path, "r") as f:
                    for line in f:
                        value = line.strip().split()[2]
                        if value != "N":
                            value = value.replace(":", "").replace("min", "m")
                            value = value.split('/')[0]
                            value = value.split('(')[0]
                            chord.append(value.lower())
                chord_dict[int(file_path.split("\\")[-2])] = chord
        elif opt == 'beat':
            for file_path in self.beat_file_paths:
                beat = []
                with open(file_path, "r") as f:
                    for line in f:
                        value = line.strip().split()[0]
                        beat.append(float(value))
                beat_dict[int(file_path.split("\\")[-2])] = beat
        return beat_dict if opt == 'beat' else chord_dict
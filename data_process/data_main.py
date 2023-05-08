from reader import Reader

class DataProcess:
    def __init__(self, root):
        self.reader = Reader(root)

    def get_bpm(self, timestamps):
        gaps = []  # 간격을 저장할 리스트
        for i in range(len(timestamps)-1):
            gap = timestamps[i+1] - timestamps[i]
            gaps.append(gap)

        avg_gap = sum(gaps) / len(gaps)
        return avg_gap

    def run(self):
        beats = self.reader.read_files('beat')
        avg_bpms = [self.get_bpm(beat) for beat in beats.values()]
        chords = self.reader.read_files('chord')
        return avg_bpms, chords


if __name__ == "__main__":
    chordy_0 = []
    chordy_1 = []
    chordy_2 = []
    chordy = []
    main0 = DataProcess(r"C:\Users\zing1\workspace\automusic_model\data_process\dataset\0")
    main1 = DataProcess(r"C:\Users\zing1\workspace\automusic_model\data_process\dataset\1")
    main2 = DataProcess(r"C:\Users\zing1\workspace\automusic_model\data_process\dataset\2")
    main3 = DataProcess(r"C:\Users\zing1\workspace\automusic_model\data_process\dataset\3")
    avg_bpms, chords = main0.run()
    for val in chords.values():
        chordy_1.extend(val)
    print(chordy_1)
    # avg_bpms, chords = main1.run()
    # for val in chords.values():
    #     chordy_1.extend(val)
    
    # avg_bpms, chords = main2.run()
    # for val in chords.values():
    #     chordy_2.extend(val)

    #chordy.extend(chordy_1)
    #chordy.extend(chordy_2)
    #print(set(chordy))
    #print(avg_bpms, chordy)

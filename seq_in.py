from chord_dict import RCHORDS
import random
class SeqIn:
    def __init__(self):
        self.seq = RCHORDS
    def get_seqin0(self):
        seq_in = random.choice(self.seq[0])
        return[l.lower() for l in seq_in]
    def get_seqin1(self):
        seq_in = random.choice(self.seq[1])
        return[l.lower() for l in seq_in]
    def get_seqin2(self):
        seq_in = random.choice(self.seq[2])
        return[l.lower() for l in seq_in]
    def get_seqin3(self):
        seq_in = random.choice(self.seq[3])
        return[l.lower() for l in seq_in]
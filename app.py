import keras
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.utils import np_utils
from chords import get_chords
from seq_in import SeqIn

FLAG = 3
# 랜덤시드 고정시키기
np.random.seed(5)

def seq2dataset(seq, window_size):
    dataset = []
    for i in range(len(seq)-window_size):
        subset = seq[i:(i+window_size+1)]
        dataset.append([code2idx[item] for item in subset])
    return np.array(dataset)  

# 코드 사전 정의
code_list = ['f7', 'g7', 'bmaj', 'daug', 'bbmaj6', 'abdim', 'am7', 'bbsus4', 'f#m6', 'abm7', 'c7', 'dm6', 'fmaj6', 'gaug', 'f#maj', 'f#7', 'ebm', 'bbhdim7', 'fmaj', 'ammaj7', 'ehdim7', 'amaj', 'ebsus4', 'bm7', 'em6', 'em', 'fsus4', 'cmaj6', 'absus4', 'bmaj7', 'abm6', 'dsus4', 'cm7', 'fdim7', 'ebmaj7', 'c#sus4', 'gsus4', 'fsus2', 'abmaj7', 'a7', 'ebaug', 'csus4', 'gm', 'abm', 'bbsus2', 'bsus4', 'dmaj7', 'abhdim7', 'am', 'dsus2', 'cdim', 'c#maj6', 'ab7', 'ebsus2', 'e7', 'amaj6', 'ahdim7', 'dm', 'c#m', 'caug', 'c#7', 'bsus2', 'eb7', 'dhdim7', 'gmaj7', 'ebm6', 'asus4', 'bm', 'dmaj', 'fmaj7', 'em7', 'bbdim', 'bdim', 'f#maj6', 'bbm7', 'absus2', 'bbmmaj7', 'adim', 'edim7', 'bmaj6', 'bbm', 'f#maj7', 'abmaj', 'ddim', 'adim7', 'cmaj7', 'ebhdim7', 'baug', 'f#mmaj7', 'asus2', 'ebm7', 'dmaj6', 'abaug', 'gmaj', 'c#dim', 'f#m7', 'c#hdim7', 'c#sus2', 'b7', 'c#m7', 'gm7', 'abmaj6', 'dm7', 'gmaj6', 'emaj7', 'c#maj', 'c#maj7', 'cm', 'ghdim7', 'amaj7', 'ebmaj6', 'emaj', 'bhdim7', 'bb7', 'f#hdim7', 'edim', 'cmaj', 'gsus2', 'fm7', 'ebdim', 'esus2', 'am6', 'fhdim7', 'bbmaj7', 'f#dim', 'f#sus4', 'eaug', 'fm', 'd7', 'f#sus2', 'cm6', 'esus4', 'f#m', 'ebmaj', 'fdim', 'csus2', 'gdim', 'bbmaj', 'emaj6', 'c#aug']
code2idx = {code: idx for idx, code in enumerate(code_list)}
idx2code = {idx: code for idx, code in enumerate(code_list)}
# 시퀀스 데이터 정의
seqin = SeqIn()
get_seq = get_chords()
if (FLAG == 0):
    seq = get_seq.seq0
    randomseq = seqin.get_seqin0()
elif (FLAG == 1):
    seq = get_seq.seq1
    randomseq = seqin.get_seqin1()
elif (FLAG == 2):
    seq = get_seq.seq2
    randomseq = seqin.get_seqin2()
elif (FLAG == 3):
    seq = get_seq.seq3
    randomseq = seqin.get_seqin3()
    print(randomseq)
# 2. 데이터셋 생성하기

dataset = seq2dataset(seq, window_size = 4)

# 입력(X)과 출력(Y) 변수로 분리하기
x_train = dataset[:,0:4]
y_train = dataset[:,4]

max_idx_value = len(code_list)

# 입력값 정규화 시키기
x_train = x_train / float(max_idx_value)
x_train = np.reshape(x_train, (-1, 4, 1))

# 라벨값에 대한 one-hot 인코딩 수행
y_train = np_utils.to_categorical(y_train)

one_hot_vec_size = y_train.shape[1]

model = tf.keras.models.load_model('trained_model/data{}'.format(FLAG))
model.reset_states()

# 8. 모델 사용하기
pred_count = 60 # 최대 예측 개수 정의

# 곡 전체 예측


seq_in = randomseq.copy()
seq_out = seq_in
print(seq_in)
seq_in = [code2idx[it] / float(max_idx_value) for it in seq_in] # 코드를 인덱스값으로 변환

for i in range(pred_count):
    sample_in = np.array(seq_in)
    sample_in = np.reshape(sample_in, (1, 4, 1)) # 샘플 수, 타입스텝 수, 속성 수
    pred_out = model.predict(sample_in)
    idx = np.argmax(pred_out)
    seq_out.append(idx2code[idx])
    seq_in.append(idx / float(max_idx_value))
    seq_in.pop(0)

model.reset_states()
    
print("full song prediction : ", "-".join(seq_out))
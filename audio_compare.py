import librosa
from dtw import dtw
from numpy.linalg import norm
from scipy import spatial
import numpy as np
from os import listdir

alphabets = ['a', 'aa', 'ae', 'ai', 'e', 'ee', 'o', 'ou', 'u', 'uu']

mfcc_values = {
}

def load_all():
    for alphabet in alphabets:
        reference_files = listdir('/home/nmd/recordings/alphabets/%s' %alphabet)
        for reference_file in reference_files:
            y2, sr2 = librosa.load('/home/nmd/recordings/alphabets/%s/%s' %(alphabet, reference_file))
            mfcc2 = librosa.feature.mfcc(y2, sr2)
            if alphabet not in mfcc_values:
                mfcc_values[alphabet] = []                
            mfcc_values[alphabet].append((mfcc2, reference_file))
    
    print mfcc_values.keys()
    
def my_custom_norm(x, y):
    return spatial.distance.cosine(x, y)

def get_distance(alphabet, audio_file):
    y1, sr1 = librosa.load(audio_file)
    mfcc1 = librosa.feature.mfcc(y1,sr1)
    distance_matrix = {}
    if alphabet not in mfcc_values:
        return {alphabet: '1000000000'}
    for (mfcc2, reference_file) in mfcc_values[str(alphabet)]:
        dist, cost, accumulated_cost, path = dtw(mfcc1.T, mfcc2.T, dist=my_custom_norm)
        distance_matrix[reference_file] = '%.4f' %dist
    return distance_matrix

import random
import typing

NOTE_NUMBER_CONV = {
    'C': 12, 'C#': 13, 'D': 14, 'D#': 15, 'E': 16, 'F': 17, 'F#': 18, 'G': 19, 'G#': 20, 'A': 21, 'B-': 22, 'B': 23,
    12: 'C', 13: 'C#', 14: 'D', 15: 'D#', 16: 'E', 17: 'F', 18: 'F#', 19: 'G', 20: 'G#', 21: 'A', 22: 'B-', 23: 'B'
}
EQUAL_TEMPERAMENT = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'B-', 'B']
NATURAL_SCALE = {'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
                 'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
                 'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
                 'F': ['F', 'G', 'A', 'B-', 'C', 'D', 'E'],
                 'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
                 'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
                 'B': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
                 'c': ['C', 'D', 'D#', 'F', 'G', 'G#', 'B-'],
                 'd': ['D', 'E', 'F', 'G', 'A', 'B-', 'C'],
                 'e': ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],
                 'f': ['F', 'G', 'G#', 'B-', 'C', 'C#', 'D#'],
                 'g': ['G', 'A', 'B-', 'C', 'D', 'D#', 'F'],
                 'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                 'b': ['B', 'C#', 'D', 'E', 'F#', 'G', 'A']}
# minor = major [3,6,7]-1
BASS_SCALE = [35, 36, 41, 43, 45, 47]
HIHAT_SCALE = [42]
SNARE_SCALE = [37, 38, 40, 48, 50]
CLAP_SCALE = [39]
OPEN_HAT_SCALE = [46,49,51,52,55,57, 59,  44, 53,54]

def weight_random_valuable(probability):
    prefix = []
    # print(probability)
    for i in probability:
        prefix.append(i)
        if len(prefix) > 1:
            prefix[-1] += prefix[-2]
    r = random.randint(1, prefix[-1])
    for p in range(len(prefix)):
        if r <= prefix[p]:
            return p
    raise ValueError('probability error')


def index(iter: typing.Iterable, target, function) -> int:
    for i, x in enumerate(iter):
        if function(target, x):
            return i
    return -1

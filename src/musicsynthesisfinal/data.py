import random

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
                 'c': ['C', 'D', 'E-', 'F', 'G', 'A-', 'B-'],
                 'd': ['D', 'E', 'F', 'G', 'A', 'B-', 'C'],
                 'e': ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],
                 'f': ['F', 'G', 'A-', 'B-', 'C', 'D-', 'E-'],
                 'g': ['G', 'A', 'B-', 'C', 'D', 'E-', 'F'],
                 'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                 'b': ['B', 'C#', 'D', 'E', 'F#', 'G', 'A']}
# minor = major [3,6,7]-1
BASS_SCALE = [35, 36, 41, 43, 45, 47]
HIHAT_SCALE = [42, 44, 46, 49, 51, 59]
SNARE_SCALE = [37, 38, 40, 48, 50]


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

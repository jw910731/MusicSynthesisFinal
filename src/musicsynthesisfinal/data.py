import random
NOTE_NUMBER_CONV = {
    'C': 12, 'C#': 13, 'D': 14, 'D#': 15, 'E': 16, 'F': 17, 'F#': 18, 'G': 19, 'G#': 20, 'A': 21, 'B-': 22, 'B': 23,
    12: 'C', 13: 'C#', 14: 'D', 15: 'D#', 16: 'E', 17: 'F', 18: 'F#', 19: 'G', 20: 'G#', 21: 'A', 22: 'B-', 23: 'B'
}
STANDARD_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'B-', 'B']
STANDARD_TONE_NOTES = {'C major': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
                       'D major': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
                       'E major': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
                       'F major': ['F', 'G', 'A', 'B-', 'C', 'D', 'E'],
                       'G major': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
                       'A major': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
                       'B major': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
                       'C minor': ['C', 'D', 'E-', 'F', 'G', 'A-', 'B-'],
                       'D minor': ['D', 'E', 'F', 'G', 'A', 'B-', 'C'],
                       'E minor': ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],
                       'F minor': ['F', 'G', 'A-', 'B-', 'C', 'D-', 'E-'],
                       'G minor': ['G', 'A', 'B-', 'C', 'D', 'E-', 'F'],
                       'A minor': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                       'B minor': ['B', 'C#', 'D', 'E', 'F#', 'G', 'A']}
# minor = major [3,6,7]-1
BASS_SCALE = [35, 36, 41, 43, 45, 47]
HIHAT_SCALE = [42, 44, 46, 49, 51, 59]
SNARE_SCALE = [37, 38, 40, 48, 50]
def weightRandomValuable(probability):
    prefix = []
    # print(probability)
    for i in probability:
        prefix.append(i*100)
        if len(prefix) > 1:
            prefix[-1] += prefix[-2]
    r = random.randint(1,100)
    for p in range(len(prefix)):
        if r <= prefix[p]:
            return p
    raise ValueError('probability error')
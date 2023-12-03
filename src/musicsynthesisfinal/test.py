import math

import classical
import music21
import data

tone = 'C'
b = classical.ClassicalBeat()
c = classical.ClassicalChord(tone)
p1 = music21.stream.Part()
p2 = music21.stream.Part()
p1.append(music21.tempo.MetronomeMark(number=b.get_bpm()))
p2.append(music21.tempo.MetronomeMark(number=b.get_bpm()))
for i in range(4):
    beat = b.generate_beat(8)
    sum_beat = 0
    for bt in beat:
        sum_beat += bt.quarterLength
        p1.append(music21.note.Note(data.NATURAL_SCALE[tone][0], duration=bt))

    ch = music21.stream.Measure()
    for _ in range(math.ceil(sum_beat/4)):
        ch = c.generate_chord()
        ch.quarterLength = 4
        ch = ch.closedPosition(forceOctave=3)
        p2.append(ch)

s = music21.stream.Stream()
s.insert(0, p1)
s.insert(0, p2)
s.show()

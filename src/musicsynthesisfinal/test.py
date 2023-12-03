import math
import random

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

    chords = []
    for _ in range(math.ceil(sum_beat / 4)):
        ch = c.generate_chord()
        ch.quarterLength = 4
        ch = ch.closedPosition(forceOctave=3)
        p2.append(ch)
        chords.append(ch)

    off_tone = 0  # off tone duration in quarter length
    measure_acc = 0  # measure accumulator in quarter length
    for bt in beat:
        current_measure = math.floor(measure_acc) // 4
        note = music21.note.Note(random.choice(data.NATURAL_SCALE[tone]), duration=bt)
        while note.pitch.pitchClass not in (chord.pitchClass for chord in
                                            chords[current_measure].pitches) and off_tone > 2:
            note = music21.note.Note(random.choice(data.NATURAL_SCALE[tone]), duration=bt)
        else:
            off_tone += bt.quarterLength
        p1.append(note)
        measure_acc += bt.quarterLength / 4

s = music21.stream.Stream()
s.insert(0, p1)
s.insert(0, p2)
s.show()

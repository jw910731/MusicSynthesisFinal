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
    for bt in beat:
        p1.append(music21.note.Note(data.STANDARD_TONE_NOTES['C major'][0], duration = bt))
    ch = c.generate_chord_duration(beat)
    for x in ch:
        print(x, x.duration)
    p2.append(ch)
s = music21.stream.Stream()
s.insert(0,p1)
s.insert(0,p2)
s.show()
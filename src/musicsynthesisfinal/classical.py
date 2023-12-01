import beat, chord, melody
import music21


class ClassicalBeat(beat.Beat):
    def generate_beat(self) -> list[music21.duration.Duration]:
        pass


class ClassicalChord(chord.Chord):
    def generate_chord(self) -> music21.chord.Chord:
        pass


class ClassicalMelody(melody.Melody):
    def generate_melody(self) -> music21.stream.Measure:
        pass


class Classical:
    def __init__(self):
        self.melody = ClassicalMelody
        self.chord = ClassicalChord
        self.beat = ClassicalBeat

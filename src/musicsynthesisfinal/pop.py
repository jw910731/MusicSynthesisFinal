import beat, chord, melody
import music21
import random   
class PopBeat(beat.Beat):
    def __init__(self):
        pass
    def __get_random_beat(self):
        pass
    def generate_beat(self, n) -> list[music21.duration.Duration]:
        pass
    def get_bpm(self):
        return self.bpm
    def generate_bass(self):
        pass
    def generate_hihat(self):
        pass
    def generate_snare(self):
        pass

class PopChord(chord.Chord):
    def __init__(self) -> None:
        super().__init__()
        chordProcessor = ['C', 'G/B', 'Am', 'Em/G', 'F', 'C/E', 'Dm', 'G']
    def generate_chord(self) -> music21.chord.Chord:
        pass


class PopMelody(melody.Melody):
    def generate_melody(self) -> music21.stream.Measure:
        pass


class Pop:
    def __init__(self):
        self.melody = PopMelody
        self.chord = PopChord
        self.beat = PopBeat

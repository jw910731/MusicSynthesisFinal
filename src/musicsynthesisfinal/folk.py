import beat, chord, melody
import music21
import random   
class FolkBeat(beat.Beat):
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

class FolkChord(chord.Chord):
    def generate_chord(self) -> music21.chord.Chord:
        pass


class FolkMelody(melody.Melody):
    def generate_melody(self) -> music21.stream.Measure:
        pass


class Folk:
    def __init__(self):
        self.melody = FolkMelody
        self.chord = FolkChord
        self.beat = FolkBeat

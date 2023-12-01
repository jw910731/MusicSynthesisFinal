import beat, chord, melody
import music21
import random   
class HiphopBeat(beat.Beat):
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

class HiphopChord(chord.Chord):
    def generate_chord(self) -> music21.chord.Chord:
        pass


class HiphopMelody(melody.Melody):
    def generate_melody(self) -> music21.stream.Measure:
        pass


class Hiphop:
    def __init__(self):
        self.melody = HiphopMelody
        self.chord = HiphopChord
        self.beat = HiphopBeat

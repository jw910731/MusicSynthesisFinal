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
    AVAILABLE_PROGRESSION = [
        ["I", "V", "vi", "iii", "IV", "I", "IV", "V"],
        ["I", "V", "vi", "VI"],
        ["vi", "VI", "I", "V"],
        ['IV', "V", "iii", "vi"],
        ['IV', "V", "iii", "vi", "ii", "V", "I"],
    ]

    def __init__(self, tone) -> None:
        self.progressions = random.choice(self.AVAILABLE_PROGRESSION)
        self.pivot = 0
        self.tone = tone

    def generate_chord(self) -> music21.chord.Chord:
        chrd = music21.roman.RomanNumeral(self.progressions[self.pivot], self.tone)
        chrd.semiClosedPosition(forceOctave=3, inPlace=True)
        self.pivot = (self.pivot + 1) % len(self.progressions)
        return chrd


class PopMelody(melody.Melody):
    def generate_melody(self) -> music21.stream.Measure:
        pass


class Pop:
    def __init__(self):
        self.melody = PopMelody
        self.chord = PopChord
        self.beat = PopBeat

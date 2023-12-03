import random

import music21

import beat
import chord
import data
import melody


class ClassicalBeat(beat.Beat):
    PROBABILITY = {'Allegro': [0.02, 0.12, 0.45, 0.30, 0.09, 0.02],
                   'Moderato': [0.02, 0.14, 0.34, 0.34, 0.14, 0.02],
                   'Andante': [0.02, 0.10, 0.45, 0.32, 0.09, 0.02]}
    BPMRANGE = {'Allegro': (120, 168),
                'Moderato': (90, 115),
                'Andante': (66, 76)}

    def __init__(self):
        """
        ClassicalBeat class representing a classical beat.

        This class inherits from the Beat class.
        """
        self.speed_type, self.durationProbability = random.choice(list(self.PROBABILITY.items()))
        self.bpm = random.randint(*self.BPMRANGE[self.speed_type])

    def __get_random_beat(self):
        """
        Generates a random beat based on weight.

        Returns:
            float: The duration of the beat in quarter note units.
        """

        r = data.weight_random_valuable(self.durationProbability)
        return 2 ** (r - 3)

    def generate_beat(self, n) -> list[music21.duration.Duration]:
        """
        Generates a list of `Duration` objects representing a classical beat pattern.

        Args:
            n: The total duration of the beat pattern in quarter notes.

        Returns:
            A list of `Duration` objects representing the classical beat pattern.
        """
        now = 0
        ret = []
        while now < n:
            choice_beat = self.__get_random_beat()
            if now + choice_beat > n:
                choice_beat = n - now
            ret.append(music21.duration.Duration(choice_beat))
            now += choice_beat
        return ret

    def get_bpm(self):
        return self.bpm

    def generate_bass(self, instrument: music21.instrument.BassDrum) -> music21.stream.Measure | music21.stream.Part:
        pass

    def generate_hihat(self, instrument: music21.instrument.BassDrum) -> music21.stream.Measure | music21.stream.Part:
        pass

    def generate_snare(self, instrument: music21.instrument.BassDrum) -> music21.stream.Measure | music21.stream.Part:
        pass


class ClassicalChord(chord.Chord):
    def __init__(self, tone):
        self.__Auto__ = {'I': {'IV': 0.5, 'vi': 0.5},
                         'ii': {'IV': 0.5, 'V': 0.5},
                         'iii': {'ii': 0.5, 'IV': 0.5},
                         'IV': {'ii': 0.25, 'iii': 0.25, 'V': 0.25, 'vi': 0.2, 'I': 0.05},
                         'V': {'iii': 0.3, 'vi': 0.5, 'I': 0.2},
                         'vi': {'iii': 0.3, 'IV': 0.3, 'V': 0.4}
                         }
        self.nowChord = 'I'
        self.lastChord = 'ST'
        self.tone = tone

    def generate_chord(self, dur=1) -> music21.chord.Chord:
        roman = music21.roman.RomanNumeral(self.generate_roman(), self.tone)
        pitch = roman.pitches
        minp = 10

        for p in pitch:
            minp = min(minp, p.octave)
        #     print(p.octave, end = ' ')
        # print(minp)
        # print('after')
        for p in pitch:
            p.octave -= min(minp - 1, 3)
        #     print(p.octave, end = ' ')
        # print()
        return music21.chord.Chord(pitch, duration=music21.duration.Duration(dur))

    def __next_chord(self, now_location) -> None:
        val, pro = list(self.__Auto__[now_location].keys()), \
            list(self.__Auto__[now_location].values())
        choose = data.weight_random_valuable(pro)
        while val[choose] == self.lastChord:
            choose = data.weight_random_valuable(pro)
        self.lastChord, self.nowChord = self.nowChord, val[choose]

    def generate_roman(self) -> str:
        ret = self.nowChord
        self.__next_chord(self.nowChord)
        return ret


class ClassicalMelody(melody.Melody):
    def __init__(self) -> None:
        super().__init__()
        pass

    def generate_melody(self) -> music21.stream.Measure:
        # how to pass the chord and beat?

        pass


class Classical:
    def __init__(self):
        self.melody = ClassicalMelody
        self.chord = ClassicalChord
        self.beat = ClassicalBeat

import random

import music21

import beat
import chord
import data
import melody


class ClassicalBeat(beat.Beat):
    PROBABILITY = {'Allegro': [2, 12, 45, 30, 9, 2],
                   'Moderato': [2, 14, 34, 34, 14, 2],
                   'Andante': [2, 10, 45, 32, 9, 2]}
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

    def generate_beat(self, n: int) -> list[music21.duration.Duration]:
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
        self.__Auto__ = {1: {4: 50, 6: 50},
                         2: {4: 50, 5: 50},
                         3: {2: 50, 4: 50},
                         4: {2: 25, 3: 25, 5: 25, 6: 20, 1: 5},
                         5: {3: 30, 6: 50, 1: 20},
                         6: {3: 30, 4: 30, 5: 40}
                         }
        self.__MAJOR_MINOR_CONVERT = [
            ["I", "ii", "iii", "IV", "V", "vi", "viio"],
            # FIXME: Minor tone is quite buggy
            ["I", "iio", "III", "iv", "v", "VI", "VII"]
        ]
        self.nowChord = 1
        self.lastChord = 'ST'
        self.tone = tone

    def generate_chord(self, dur=1) -> music21.chord.Chord:
        roman = self.generate_roman()
        roman = music21.roman.RomanNumeral(self.__MAJOR_MINOR_CONVERT[str.islower(self.tone)][roman], self.tone)
        roman.semiClosedPosition(forceOctave=3, inPlace=True)
        roman.duration = music21.duration.Duration(dur)
        return roman

    def generate_chord_list(self, beat: list[music21.duration.Duration]) -> list[music21.chord.Chord]:
        dur = 0.0
        offset = 0.0
        ret = []
        for bt in [x.quarterLength for x in beat]:
            if dur.is_integer() and dur != 0:
                if dur > 4:
                    ret.append(self.generate_chord(4))
                    ret.append(self.generate_chord(dur - 4))
                else:
                    ret.append(self.generate_chord(dur))
                dur = 0
            offset += bt
            dur += bt
        ret.append(self.generate_chord(dur))
        return ret

    def __next_chord(self, now_location) -> None:
        val, pro = list(self.__Auto__[now_location].keys()), \
            list(self.__Auto__[now_location].values())
        choose = data.weight_random_valuable(pro)
        while val[choose] == self.lastChord:
            choose = data.weight_random_valuable(pro)
        self.lastChord, self.nowChord = self.nowChord, val[choose]

    def generate_roman(self) -> int:
        ret = self.nowChord
        self.__next_chord(self.nowChord)
        return ret


class ClassicalMelody(melody.CommonMelody):
    def __init__(self, beat: list[music21.duration.Duration], chord: list[music21.chord.Chord], tone) -> None:
        super().__init__(beat, chord, tone)
        pass

    # def generate_melody(self) -> music21.stream.Measure:
    #     # how to pass the chord and beat?

    #     pass


class Classical:
    def __init__(self, tone):
        self.chord = ClassicalChord(tone)
        self.beat = ClassicalBeat()
        self.tone = tone

    def generate_music(self):
        part_chord = music21.stream.Part()
        part_chord.insert(0, music21.tempo.MetronomeMark(number=self.beat.get_bpm()))
        part_chord.insert(0, music21.key.Key(self.tone))
        part_melody = music21.stream.Part()
        part_melody.insert(0, music21.tempo.MetronomeMark(number=self.beat.get_bpm()))
        part_melody.insert(0, music21.key.Key(self.tone))
        ret = []
        for i in range(16):
            bt = self.beat.generate_beat(8)
            ch = self.chord.generate_chord_list(bt)
            mel = ClassicalMelody(bt, ch, self.tone)
            for c in ch:
                part_chord.append(c)
            m = mel.generate_melody()
            for x in m:
                part_melody.append(x)
        ret.append(part_melody)
        ret.append(part_chord)
        return ret

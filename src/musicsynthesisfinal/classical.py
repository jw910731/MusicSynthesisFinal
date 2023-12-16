import random

import music21

import beat
import chord
import utils
import melody


class ClassicalBeat(beat.Beat):
    PROBABILITY = {'Allegro': [1, 12, 46, 30, 9, 2],
                   'Moderato': [1, 7, 42, 34, 14, 2],
                   'Andante': [1, 5, 45, 38, 9, 2]}
    BPMRANGE = {'Allegro': (120, 168),
                'Moderato': (90, 115),
                'Andante': (66, 76)}

    def __init__(self, style):
        """
        ClassicalBeat class representing a classical beat.

        This class inherits from the Beat class.
        """
        if style == 'random':
            self.speed_type, self.durationProbability = random.choice(list(self.PROBABILITY.items()))
        else:
            self.speed_type = style
            self.durationProbability = self.PROBABILITY[style]
        self.bpm = random.randint(*self.BPMRANGE[self.speed_type])

    def __get_random_beat(self):
        """
        Generates a random beat based on weight.

        Returns:
            float: The duration of the beat in quarter note units.
        """

        r = utils.weight_random_valuable(self.durationProbability)
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

    def generate_bass(self) -> list[music21.note.Note]:
        pass

    def generate_hihat(self) -> list[music21.note.Note]:
        pass

    def generate_snare(self) -> list[music21.note.Note]:
        pass

    def generate_clap(self) -> list[music21.note.Note]:
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

    def generate_chord(self) -> music21.chord.Chord:
        roman = self.generate_roman()
        roman = music21.roman.RomanNumeral(self.__MAJOR_MINOR_CONVERT[str.islower(self.tone)][roman], self.tone)
        roman.semiClosedPosition(forceOctave=3, inPlace=True)
        return chord.limit_inversion(roman)

    def __next_chord(self, now_location) -> None:
        val, pro = list(self.__Auto__[now_location].keys()), \
            list(self.__Auto__[now_location].values())
        choose = utils.weight_random_valuable(pro)
        while val[choose] == self.lastChord:
            choose = utils.weight_random_valuable(pro)
        self.lastChord, self.nowChord = self.nowChord, val[choose]

    def generate_roman(self) -> int:
        ret = self.nowChord
        self.__next_chord(self.nowChord)
        return ret

    def generate_chord_list(self, beat: list[music21.duration.Duration]) -> list[music21.chord.Chord]:
        dur = 0.0
        offset = 0.0
        ret = []
        for bt in [x.quarterLength for x in beat]:
            if dur.is_integer() and dur != 0:
                if dur > 4:
                    tmp = self.generate_chord()
                    tmp.duration = music21.duration.Duration(4)
                    ret.append(tmp)
                    tmp = self.generate_chord()
                    tmp.duration = music21.duration.Duration(dur-4)
                    ret.append(tmp)
                else:
                    tmp = self.generate_chord()
                    tmp.duration = music21.duration.Duration(dur)
                    ret.append(tmp)
                dur = 0
            offset += bt
            dur += bt
        tmp = self.generate_chord()
        tmp.duration = music21.duration.Duration(dur)
        ret.append(tmp)
        return ret


class ClassicalMelody(melody.CommonMelody):
    def __init__(self, beat: list[music21.duration.Duration], chord: list[music21.chord.Chord], tone) -> None:
        super().__init__(beat, chord, tone)

    # def generate_melody(self) -> music21.stream.Measure:
    #     # how to pass the chord and beat?

    #     pass


class Classical:
    def __init__(self, tone, style='random'):
        self.chord = ClassicalChord(tone)
        self.beat = ClassicalBeat(style=style)
        self.tone = tone

    def generate_music(self):
        part_chord = utils.set_up_part(self.beat.get_bpm(), self.tone)
        part_melody = utils.set_up_part(self.beat.get_bpm(), self.tone)
        ret = []
        for i in range(16):
            bt = self.beat.generate_beat(6)
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

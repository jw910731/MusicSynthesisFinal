import copy
import chord, utils
from hiphoptemplate import *
import random

import music21

import beat
import melody
import pop



class HiphopBeat(beat.Beat):
    def __init__(self):
        self.type = random.choice(["drill", "trap", "Boombap"])
        self.bpm = 0

    def __beat_recursive(self, size: float, part: float) -> list[float]:
        if size <= 0.25:
            return [size]
        if part == 6 and size == 2:
            if random.randint(1, 100) <= 10:
                return [size]
        if size <= 2 and random.random() <= (1 / (1.05 * size)) ** 0.5:
            return [size]
        return self.__beat_recursive(size / 2, part) + self.__beat_recursive(size / 2, part + size / 2)

    def generate_beat(self, n) -> list[music21.duration.Duration]:
        ret = []
        for i in range(0, n, 8):
            ls = self.__beat_recursive(min(n - i, 8), 0)
            for x in ls:
                ret.append(music21.duration.Duration(x))
        return ret

    def get_bpm(self):
        return self.bpm

    def generate_bass(self, instrument: music21.instrument.BassDrum) -> music21.stream.Measure | music21.stream.Part:
        pass

    def generate_hihat(self, instrument: music21.instrument.BassDrum) -> music21.stream.Measure | music21.stream.Part:
        pass

    def generate_snare(self, instrument: music21.instrument.BassDrum) -> music21.stream.Measure | music21.stream.Part:
        pass


class HiphopChord(pop.PopChord):
    def __init__(self, tone):
        super().__init__(tone)


class Hiphop:
    def __init__(self, tone = 'F#'):
        self.chord = HiphopChord(tone)
        self.beat = HiphopBeat()
        self.tone = tone

    def generate_music(self):
        part_chord = music21.stream.Part()
        part_chord.insert(0, music21.tempo.MetronomeMark(number=self.beat.get_bpm()))
        part_chord.insert(0, music21.key.Key(self.tone))
        part_melody = music21.stream.Part()
        part_melody.insert(0, music21.tempo.MetronomeMark(number=self.beat.get_bpm()))
        part_melody.insert(0, music21.key.Key(self.tone))

        for _ in range(4):
            bt = self.beat.generate_beat(8)
            ch = self.chord.generate_chord_list(bt)
            mel = melody.CommonMelody(bt, ch, self.tone)
            m = mel.generate_melody()
            for _ in range(4):
                for c in ch:
                    part_chord.append(copy.deepcopy(c))
                for x in m:
                    part_melody.append(copy.deepcopy(x))

        return part_melody, part_chord




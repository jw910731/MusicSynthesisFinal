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
        self.hiphoptype = random.choice([drill])  # , trap, boombap
        self.bass = random.choice(self.hiphoptype.Bass)
        self.hihat = random.choice(self.hiphoptype.Hihat)
        self.snare = random.choice(self.hiphoptype.Snare)
        self.clap = random.choice(self.hiphoptype.Clap)
        self.bpm = random.randint(*self.hiphoptype.bpmrange)

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

    def generate_bass(self) -> list[music21.note.Note]:
        ret = []
        for i in range(16):
            if self.bass.Template[i]:
                # gen_beat
                du = self.bass.TemplateSplitway[i]
                for p in self.bass.Probability[i]:
                    if random.random() <= p:
                        ret.append(music21.note.Note(self.bass.pitch, quarterLength=du))
                    else:
                        ret.append(music21.note.Rest(quarterLength=du))

            else:
                ret.append(music21.note.Rest(quarterLength=1))
        return ret

    def generate_hihat(self) -> list[music21.note.Note]:
        ret = []
        for i in range(16):
            if self.hihat.Template[i]:
                # gen_beat
                du = self.hihat.TemplateSplitway[i]
                for p in self.hihat.Probability[i]:
                    if random.random() <= p:
                        ret.append(music21.note.Note(self.hihat.pitch, quarterLength=du))
                    else:
                        ret.append(music21.note.Rest(quarterLength=du))

            else:
                ret.append(music21.note.Rest(quarterLength=1))
        return ret

    def generate_snare(self) -> list[music21.note.Note]:
        ret = []
        for i in range(16):
            if self.snare.Template[i]:
                # gen_beat
                du = self.snare.TemplateSplitway[i]
                for p in self.snare.Probability[i]:
                    if random.random() <= p:
                        ret.append(music21.note.Note(self.snare.pitch, quarterLength=du))
                    else:
                        ret.append(music21.note.Rest(quarterLength=du))

            else:
                ret.append(music21.note.Rest(quarterLength=1))
        return ret

    def generate_clap(self) -> list[music21.note.Note]:
        ret = []
        for i in range(16):
            if self.clap.Template[i]:
                # gen_beat
                du = self.clap.TemplateSplitway[i]
                for p in self.clap.Probability[i]:
                    if random.random() <= p:
                        ret.append(music21.note.Note(self.clap.pitch, quarterLength=du))
                    else:
                        ret.append(music21.note.Rest(quarterLength=du))

            else:
                ret.append(music21.note.Rest(quarterLength=1))
        return ret


class HiphopChord(pop.PopChord):
    def __init__(self, tone):
        super().__init__(tone)


class Hiphop:
    def __init__(self, tone='F#'):
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
        instrument = music21.instrument.BassDrum()
        part_bass = music21.stream.Part()
        part_bass.insert(0, music21.tempo.MetronomeMark(number=self.beat.get_bpm()))
        part_bass.insert(0, copy.deepcopy(instrument))
        part_hihat = music21.stream.Part()
        part_hihat.insert(0, music21.tempo.MetronomeMark(number=self.beat.get_bpm()))
        part_hihat.insert(0, copy.deepcopy(instrument))
        part_clap = music21.stream.Part()
        part_clap.insert(0, music21.tempo.MetronomeMark(number=self.beat.get_bpm()))
        part_clap.insert(0, copy.deepcopy(instrument))
        part_snare = music21.stream.Part()
        part_snare.insert(0, music21.tempo.MetronomeMark(number=self.beat.get_bpm()))
        part_snare.insert(0, copy.deepcopy(instrument))
        for x in range(4):
            bt = self.beat.generate_beat(8)
            ch = self.chord.generate_chord_list(bt)
            mel = melody.CommonMelody(bt, ch, self.tone)
            m = mel.generate_melody()
            bass = self.beat.generate_bass()
            snare = self.beat.generate_snare()
            clap = self.beat.generate_clap()
            hihat = self.beat.generate_hihat()
            for y in range(2):
                for a, b in zip([part_chord, part_melody], [ch, m]):
                    for r in b:
                        a.append(copy.deepcopy(r))
                for a, b in zip([part_chord, part_melody, part_bass, part_hihat, part_snare, part_clap],
                                [ch, m, bass, hihat, snare, clap]):
                    for r in b:
                        a.append(copy.deepcopy(r))
        # return part_hihat
        return part_melody, part_chord, part_bass, part_snare, part_clap, part_hihat

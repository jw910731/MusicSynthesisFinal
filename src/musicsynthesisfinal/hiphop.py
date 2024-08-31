import copy
from musicsynthesisfinal import chord, utils, beat, melody, pop
from musicsynthesisfinal.hiphoptemplate import *
import random

import music21


class HiphopBeat(beat.Beat):
    def __init__(self, style):
        if style == 'random':
            self.name, self.hiphoptype = random.choice([ ('boombap',Boombap().boombap), ('drill', Drill().drill),('trap',Trap().trap)])  # , trap, boombap
        else:
            self.name = style
            self.hiphoptype = {'boombap':Boombap().boombap, 'drill': Drill().drill,'trap':Trap().trap}[style]
        self.bass = random.choice(self.hiphoptype.Bass)
        self.hihat = random.choice(self.hiphoptype.Hihat)
        self.snare = random.choice(self.hiphoptype.Snare)
        self.clap = random.choice(self.hiphoptype.Clap)
        self.bpm = random.randint(*self.hiphoptype.bpmrange)
        self.prefixProbability = [0, 0.3, 0.3, 0.4]
        self.postfixProbability = [0.4, 0.3, 0.3, 0]

    def __beat_recursive(self, size: float, part: float) -> list[float]:
        if size <= 0.25:
            return [size]
        if part == 6 and size == 2:
            if random.randint(1, 100) <= 10:
                return [size]
        if size <= 2 and random.random() <= (1 / (2 * size)) ** 0.5:
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

    def get_extention(self, original: list[music21.note.Note], pitch) -> list[music21.note.Note]:
        cnt = 0
        ret = original
        for i in range(len(ret)):
            if isinstance(cnt, int):
                check = 0
                c = 0
                offset = 0
                while (c <= 1):
                    if (ret[i + offset].isNote):
                        check = 1
                    c += ret[i + offset].quarterLength
                    offset += 1
                if check:
                    # postfix
                    if random.random() <= abs(cnt - 0.75) / 10.8:
                        offset2 = 0
                        if (ret[(i + offset + offset2) % len(ret)].quarterLength != 0.25):
                            ret[(i + offset + offset2) % len(ret)].quarterLength = 0.25
                            ret.insert(i + offset + offset2 + 1, music21.note.Rest(quarterLength=0.25))
                            ret.insert(i + offset + offset2 + 1, music21.note.Rest(quarterLength=0.25))
                            ret.insert(i + offset + offset2 + 1, music21.note.Rest(quarterLength=0.25))
                        while ret[(i + offset + offset2) % len(ret)].isRest and offset2 < 4:
                            if (random.random() <= self.postfixProbability[offset2]):
                                ret[(i + offset + offset2) % len(ret)] = music21.note.Note(pitch, quarterLength=ret[
                                    (i + offset + offset2) % len(ret)].quarterLength)
                            offset2 += 1
                    # prefix
                    if random.random() <= abs(cnt - 0.75) / 10.8:
                        offset2 = 0
                        if (ret[(i - offset2 + len(ret)) % len(ret)].quarterLength != 0.25):
                            ret[(i - offset2 + len(ret)) % len(ret)].quarterLength = 0.25
                            ret.insert((i - offset2 - 1 + len(ret)) % len(ret), music21.note.Rest(quarterLength=0.25))
                            ret.insert((i - offset2 - 1 + len(ret)) % len(ret), music21.note.Rest(quarterLength=0.25))
                            ret.insert((i - offset2 - 1 + len(ret)) % len(ret), music21.note.Rest(quarterLength=0.25))
                        while ret[(i - offset2 + len(ret)) % len(ret)].isRest and offset2 < 4:
                            if (random.random() <= self.prefixProbability[offset2]):
                                ret[(i - offset2 + len(ret)) % len(ret)] = music21.note.Note(pitch, quarterLength=ret[
                                    (i - offset2 + len(ret)) % len(ret)].quarterLength)
                            offset2 += 1
            cnt += ret[i].quarterLength
        return ret

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
        return self.get_extention(ret, self.bass.pitch)

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
        return self.get_extention(ret, self.hihat.pitch)

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
        return self.get_extention(ret, self.snare.pitch)

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
        return self.get_extention(ret, self.clap.pitch)


class HiphopChord(pop.PopChord):
    def __init__(self, tone):
        super().__init__(tone)
class HiphopMelody(pop.PopMelody):
    def __init__(self, beat: list[music21.duration.Duration], chord: list[music21.chord.Chord], tone):
        super().__init__(beat, chord, tone)

class Hiphop:
    def __init__(self, tone='F#', style = 'random'):
        self.verse_chord = HiphopChord(tone)
        self.chorus_chord = HiphopChord(tone)
        self.beat = HiphopBeat(style=style)
        self.tone = tone

    def generate_music(self):
        part_chord = utils.set_up_part(self.beat.get_bpm(), self.tone)
        part_melody = utils.set_up_part(self.beat.get_bpm(), self.tone)
        part_bass = utils.set_up_part(self.beat.get_bpm(), self.tone, music21.instrument.BassDrum())
        part_hihat = utils.set_up_part(self.beat.get_bpm(), self.tone, music21.instrument.BassDrum())
        part_clap = utils.set_up_part(self.beat.get_bpm(), self.tone, music21.instrument.BassDrum())
        part_snare = utils.set_up_part(self.beat.get_bpm(), self.tone, music21.instrument.BassDrum())
        verse_beat = []
        verse_chord_list = []
        verse_melody_list = []
        verse_bass = []
        verse_hihat = []
        verse_snare = []
        verse_clap = []
        chorus_beat = []
        chorus_chord_list = []
        chorus_melody_list = []
        chorus_bass = []
        chorus_hihat = []
        chorus_snare = []
        chorus_clap = []
        intro_beat = []
        intro_chord_list = []
        intro_melody_list = []
        intro_bass = []
        intro_hihat = []
        intro_snare = []
        intro_clap = []
        outro_beat = []
        outro_chord_list = []
        outro_melody_list = []
        outro_bass = []
        outro_hihat = []
        outro_snare = []
        outro_clap = []
        bs = self.beat.generate_bass()
        hi = self.beat.generate_hihat()
        sn = self.beat.generate_snare()
        cl = self.beat.generate_clap()
        bt = self.beat.generate_beat(64)
        ch = self.verse_chord.generate_chord_list(bt)
        mel = HiphopMelody(bt, ch, self.tone)
        for b in bt:
            verse_beat.append(b)
        for c in ch:
            verse_chord_list.append(c)
        verse_melody_list = mel.generate_melody()
        for i in range(4):
            for x in bs:
                verse_bass.append(x)
            for x in hi:
                verse_hihat.append(x)
            for x in sn:
                verse_snare.append(x)
            for x in cl:
                verse_clap.append(x)
        if self.beat.name == 'boombap':
            sz = random.choice([4,4,4,4,8])
            verse_melody_list = utils.cut_back(verse_melody_list, sz)
            verse_melody_list.append(music21.note.Rest(quarterLength=sz))
            verse_chord_list = utils.cut_back(verse_chord_list, sz)
            verse_chord_list.append(music21.note.Rest(quarterLength=sz))
        chorus_beat = self.beat.generate_beat(32)
        
        chorus_chord_list = self.chorus_chord.generate_chord_list(chorus_beat)
        chorus_melody_list = HiphopMelody(chorus_beat, chorus_chord_list, self.tone).generate_melody()
        for i in range(2):
            for x in bs:
                chorus_bass.append(copy.deepcopy(x))
            for x in hi:
                chorus_hihat.append(copy.deepcopy(x))
            for x in sn:
                chorus_snare.append(copy.deepcopy(x))
            for x in cl:
                chorus_clap.append(copy.deepcopy(x))
        if self.beat.name == 'boombap':
            intro_chord_list.append(music21.note.Rest(32))
            intro_melody_list.append(music21.note.Rest(32))
            intro_clap.append(music21.note.Rest(32))
            intro_hihat.append(music21.note.Rest(16))
            for i in range(2):
                for x in bs:
                    intro_bass.append(copy.deepcopy(x))
                for x in sn:
                    intro_snare.append(copy.deepcopy(x))
            for x in hi:
                intro_hihat.append(copy.deepcopy(x))
        elif self.beat.name == 'drill':
            intro_chord_list.append(music21.note.Rest(32))
            intro_melody_list.append(music21.note.Rest(32))
            intro_clap.append(music21.note.Rest(32))
            intro_snare.append(music21.note.Rest(32))
            intro_bass.append(music21.note.Rest(16))
            for i in range(2):
                for x in hi:
                    intro_hihat.append(copy.deepcopy(x))
            for x in bs:
                intro_bass.append(copy.deepcopy(x))
        else:
            intro_chord_list.append(music21.note.Rest(32))
            intro_melody_list.append(music21.note.Rest(32))
            intro_clap.append(music21.note.Rest(16))
            intro_snare.append(music21.note.Rest(16))
            for i in range(2):
                for x in hi:
                    intro_hihat.append(copy.deepcopy(x))
                for x in bs:
                    intro_bass.append(copy.deepcopy(x))
            for x in sn:
                intro_snare.append(copy.deepcopy(x))
            for x in cl:
                intro_clap.append(copy.deepcopy(x))
        for x in bs:
            outro_bass.append(copy.deepcopy(x))
        for x in hi:
            outro_hihat.append(copy.deepcopy(x))
        for x in sn:
            outro_snare.append(copy.deepcopy(x))
        for x in cl:
            outro_clap.append(copy.deepcopy(x))
        
        for a, b in zip([part_chord, part_melody, part_bass, part_hihat, part_snare, part_clap],
                                    [intro_chord_list, intro_melody_list, intro_bass, intro_hihat, intro_snare, intro_clap]):
            for r in b:
                a.append(copy.deepcopy(r))
        if self.beat.name != 'trap':
            for _ in range(2):    
                for a, b in zip([part_chord, part_melody, part_bass, part_hihat, part_snare, part_clap],
                                        [chorus_chord_list, chorus_melody_list, chorus_bass, chorus_hihat, chorus_snare, chorus_clap]):
                    for r in b:
                        a.append(copy.deepcopy(r))
        for i in range(2):
            for a, b in zip([part_chord, part_melody, part_bass, part_hihat, part_snare, part_clap],
                                    [verse_chord_list, verse_melody_list, verse_bass, verse_hihat, verse_snare, verse_clap]):
                for r in b:
                    a.append(copy.deepcopy(r))
            for _ in range(2):    
                for a, b in zip([part_chord, part_melody, part_bass, part_hihat, part_snare, part_clap],
                                        [chorus_chord_list, chorus_melody_list, chorus_bass, chorus_hihat, chorus_snare, chorus_clap]):
                    for r in b:
                        a.append(copy.deepcopy(r))
        if self.beat.name == 'drill':
            for _ in range(2):    
                for a, b in zip([part_chord, part_melody, part_bass, part_hihat, part_snare, part_clap],
                                        [chorus_chord_list, chorus_melody_list, chorus_bass, chorus_hihat, chorus_snare, chorus_clap]):
                    for r in b:
                        a.append(copy.deepcopy(r))
        elif self.beat.name == 'boombap':
            for a, b in zip([part_chord, part_melody, part_bass, part_hihat, part_snare, part_clap],
                                    [verse_chord_list, verse_melody_list, verse_bass, verse_hihat, verse_snare, verse_clap]):
                for r in b:
                    a.append(copy.deepcopy(r))
        for a, b in zip([part_chord, part_melody, part_bass, part_hihat, part_snare, part_clap],
                                    [outro_chord_list, outro_melody_list, outro_bass, outro_hihat, outro_snare, outro_clap]):
            for r in b:
                a.append(copy.deepcopy(r))
        # return part_hihat
        # return part_bass, part_snare, part_clap, part_hihat
        return part_melody, part_chord, part_bass, part_snare, part_clap, part_hihat
